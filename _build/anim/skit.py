#!/usr/bin/env python3
"""Oliver 情境劇短影片產生器（9:16、無聲、不露臉）。

用法：python3 _build/anim/skit.py spec.json out.mp4
spec.json 範例見 _build/anim/specs/。欄位：
  scene      場景標籤（如「Oli 診所・櫃台」）
  staff_line 診所人員的第一句抱怨（可用 \\n 換行，2 行內）
  prop       人員手上的道具：paper / box / clock / none
  oliver_line Oliver 的回應（2 行內）
  screen     {"type":"grid"} 排班格 | {"type":"list","rows":[["品名","狀態","ok|warn|bad"],...]} | {"type":"check","text":"..."}
             | {"type":"qr-flow", ...} 真實 UI 三步驟示範（櫃台平板 QR 倒數 → 手機點名字 → 按上班打卡成功），
               會把示範卡放大到畫面上半、角色縮小，片長 13 秒 → 19.5 秒。可選欄位：
               who（預設 王小明）、shift（早午班）、session（第一診 08:30–12:30）、time（08:52）、
               names（[[姓名,班別],...] 最多 8 組）、steps（三段說明字，各 ≤ 16 字）、url（QR 內容）
  relief_line 人員鬆一口氣的一句
  caption    畫面下方的一行重點（如「設好人數 → 自動排出草稿 → 微調」）
  end_title  結尾卡大標（可 \\n）
  keyword    LINE 關鍵字（Demo / 排班表 / 盤點表 / 特休表）
  product    結尾小字（如「Oli 考勤管理系統」）
"""
import json, os, sys, subprocess, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oliver

FPS = 24

def esc(s): return html.escape(s).replace("\\n", "<br>").replace("\n", "<br>")

PROPS = {
 "paper": '<div class="paper"><i></i><i></i><i></i><i></i><i></i></div>',
 "box":   '<div class="box"><span>過期</span></div>',
 "clock": '<div class="clock"><b></b><u></u></div>',
 "none":  "",
}

def screen_html(sc):
    t = sc.get("type", "grid")
    if t == "grid":
        cls = ['g','a','s','','g','s','a']
        cells = "".join(f'<b class="{cls[(r+c)%7]}" style="animation-delay:{5.7+(r*7+c)*0.03:.2f}s"></b>' for r in range(7) for c in range(7))
        return f'<div class="screen grid">{cells}</div>'
    if t == "list":
        rows = "".join(f'<div class="row" style="animation-delay:{5.7+i*0.25:.2f}s"><span>{esc(n)}</span><em class="{k}">{esc(s)}</em></div>' for i,(n,s,k) in enumerate(sc["rows"][:5]))
        return f'<div class="screen list">{rows}</div>'
    if t == "check":
        return f'<div class="screen check"><div class="tick"></div><p>{esc(sc.get("text",""))}</p></div>'
    raise SystemExit("unknown screen type")

# ---------- 真實 UI 示範卡（qr-flow） ----------
DEMO_START, DEMO_END = 6.8, 13.6          # 示範卡出現／收起的秒數
DEMO_EXTRA = 6.5                          # 相較 13 秒基本版多出的秒數

def qr_svg(data, size=230):
    """用 qrcode 產真的 QR（掃得到）；沒裝套件就退回示意圖樣。"""
    try:
        import qrcode
        q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0); q.add_data(data); q.make(fit=True)
        m = q.get_matrix()
    except Exception:
        import random; rnd = random.Random(7); n = 29
        m = [[(r < 7 and c < 7) or (r < 7 and c >= n-7) or (r >= n-7 and c < 7) or rnd.random() < .45 for c in range(n)] for r in range(n)]
    n = len(m); cell = size / n
    rects = "".join(f'<rect x="{c*cell:.2f}" y="{r*cell:.2f}" width="{cell+.3:.2f}" height="{cell+.3:.2f}"/>' for r in range(n) for c in range(n) if m[r][c])
    return f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" fill="#17332B" shape-rendering="crispEdges">{rects}</svg>'

def ticker(values, start, step, cls="tk"):
    """依序顯示一串字（倒數、時間秒數）：每個 value 顯示 step 秒。"""
    return "".join(f'<span class="{cls}" style="animation-delay:{start+i*step:.2f}s,{start+(i+1)*step:.2f}s">{esc(str(v))}</span>' for i, v in enumerate(values))

def demo_html(sc):
    who = sc.get("who", "王小明"); shift = sc.get("shift", "早午班"); sess = sc.get("session", "第一診 08:30–12:30")
    tm = sc.get("time", "08:52"); url = sc.get("url", "https://olimedi.com/attendance.html")
    names = sc.get("names") or [["王小明","早午班"],["王小美","午晚班"],["王小華","全天班"],["王小芳","早班"],["王小強","行政・全天"],["王小安","早午班"]]
    steps = sc.get("steps") or ["① 櫃台平板顯示 QR，每 60 秒換一張", "② 手機掃碼，點自己的名字", "③ 按「上班」，打卡完成"]
    s = DEMO_START
    secs = ticker([f"{tm}:{(3+i):02d}" for i in range(7)], s, 1.0)
    countdown = ticker([57-i for i in range(7)], s, 1.0)
    cards = ""
    for i, (n, r) in enumerate(names[:8]):
        cards += f'<div class="nm{" hit" if n == who else ""}" style="animation-delay:{s+2.6+i*0.08:.2f}s"><b>{esc(n)}</b><small>{esc(r)}<br>尚未打卡</small>{"<i class=pk></i>" if n == who else ""}</div>'
    stepbar = "".join(f'<p class="st" style="animation-delay:{s+i*2.4:.2f}s,{s+(i+1)*2.4-.05:.2f}s">{esc(t)}</p>' for i, t in enumerate(steps[:3]))
    return f'''<div class="demo">
<div class="dhead">Oli 考勤管理系統・手機打卡 <em>畫面示意</em></div>
<div class="tab"><div class="tscr">
  <div class="thead"><span><i>Oli</i>掃碼打卡<small>POINT 01</small></span><strong>{secs}</strong></div>
  <div class="qr">{qr_svg(url)}</div>
  <div class="tbar"><b></b></div>
  <p class="t1">用手機相機掃描上方畫面即可打卡</p>
  <p class="t2">這張 QR 將在 <b>{countdown}</b> 秒後更換・75 秒後失效</p>
</div></div>
<div class="phone"><div class="pscr">
  <div class="phead"><span><i>Oli</i>打卡</span><strong>{tm}</strong></div>
  <div class="p1">
    <h4>請點選你的名字</h4><small>共 {len(names)} 位員工</small>
    <div class="search">輸入姓名快速尋找…</div>
    <div class="grid2">{cards}</div>
    <div class="tap tap1"></div>
  </div>
  <div class="p2">
    <small>‹ 換人</small><h4>{esc(who)}</h4><small>{esc(shift)}・現在 {esc(tm)}</small>
    <div class="sess"><b>{esc(sess)}</b><div class="btns"><span class="on">▶ 上班<small>現在打卡</small></span><span>■ 下班<small>尚未打卡</small></div></div>
    <div class="sess dim"><b>第二診 13:30–18:00</b><div class="btns"><span>▶ 上班</span><span>■ 下班</span></div></div>
    <p>按「上班」會以系統時間記錄，不會重複計入。</p>
    <div class="tap tap2"></div>
  </div>
  <div class="p3">
    <div class="tick"></div><h4>上班打卡成功</h4><b>{esc(who)}・{esc(tm)}:08</b><small>{esc(shift)}・{esc(sess)}</small><em>已寫入出勤紀錄</em>
  </div>
</div></div>
<div class="steps">{stepbar}</div>
</div>'''

def is_demo(spec): return (spec.get("screen") or {}).get("type") == "qr-flow"
def duration(spec): return 13.0 + (DEMO_EXTRA if is_demo(spec) else 0)
def cover_time(spec): return float(spec.get("cover_at", 12.9 if is_demo(spec) else 8.5))

def build_html(spec):
    X = DEMO_EXTRA if is_demo(spec) else 0      # 第二段之後所有時間點往後推
    S, E = DEMO_START, DEMO_END
    return f'''<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@500;700;900&display=swap" rel="stylesheet">
<style>
:root{{--g:#2E7D5B;--ink:#17332B;--bg:#F4F7F5;--amber:#F2A541}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1920px;overflow:hidden;background:var(--bg);font-family:"Noto Sans TC",sans-serif;color:var(--ink)}}
.stage{{position:relative;width:1080px;height:1920px}}
.wall{{position:absolute;inset:0;background:linear-gradient(#F4F7F5 0 62%,#E6EEE9 62% 100%)}}
.counter{{position:absolute;left:0;right:0;top:1180px;height:420px;background:#fff;border-top:14px solid #D5DED9}}
.counter:after{{content:"";position:absolute;left:80px;right:80px;top:120px;height:16px;border-radius:8px;background:#E6EEE9}}
.sign{{position:absolute;left:80px;top:240px;padding:18px 36px;border-radius:999px;background:#fff;border:3px solid #D5DED9;font-weight:700;font-size:40px;color:var(--g)}}
.demo-on .sign{{animation:fade .3s linear {S}s forwards, show .3s linear {E+.3:.2f}s forwards}}
.staff{{position:absolute;left:150px;top:720px;width:420px;height:560px;transform-origin:50% 100%;animation:breathe 2.4s ease-in-out infinite}}
.staff .face{{position:absolute;left:100px;top:70px;width:220px;height:210px;border-radius:50%;background:#FBE3D0}}
.staff .hair{{position:absolute;left:90px;top:40px;width:240px;height:130px;border-radius:130px 130px 40px 40px;background:#4A3530}}
.staff .bun{{position:absolute;left:170px;top:10px;width:80px;height:70px;border-radius:50%;background:#4A3530}}
.staff .bun:after{{content:"";position:absolute;left:14px;top:12px;width:24px;height:14px;border-radius:50%;background:#fff;opacity:.15}}
.staff .eye{{position:absolute;top:150px;width:30px;height:40px;border-radius:50%;background:#2B2B2B;animation:blink 3.1s steps(1) infinite}}
.staff .eye:after{{content:"";position:absolute;left:6px;top:7px;width:11px;height:11px;border-radius:50%;background:#fff}}
.staff .eye.l{{left:160px}}.staff .eye.r{{left:232px}}
.staff .cheek{{position:absolute;top:200px;width:40px;height:22px;border-radius:50%;background:#F7B3A3;opacity:.7}}
.staff .cheek.l{{left:128px}}.staff .cheek.r{{left:254px}}
.staff .mouth{{position:absolute;left:198px;top:222px;width:24px;height:10px;border-radius:30px 30px 0 0;background:#C9746A;animation:smile .1s linear {7.2+X:.2f}s forwards}}
.staff .body{{position:absolute;left:90px;top:272px;width:240px;height:290px;border-radius:120px 120px 30px 30px;background:#8FC4B5}}
.staff .collar{{position:absolute;left:176px;top:266px;width:68px;height:34px;background:#fff;clip-path:polygon(0 0,100% 0,50% 100%)}}
.staff .arm{{position:absolute;left:300px;top:340px;width:60px;height:170px;border-radius:40px;background:#8FC4B5;transform-origin:30px 20px;transform:rotate(-20deg);animation:scratch 1.2s ease-in-out .4s 2}}
.staff .arm:after{{content:"";position:absolute;left:8px;bottom:-14px;width:44px;height:44px;border-radius:50%;background:#FBE3D0}}
.paper{{position:absolute;left:330px;top:470px;width:130px;height:160px;background:#fff;border:3px solid #D5DED9;transform:rotate(12deg)}}
.paper i{{display:block;height:8px;margin:18px 14px 0;background:#D5DED9}}
.box{{position:absolute;left:320px;top:480px;width:150px;height:110px;background:#E8DCC8;border:3px solid #C9B99A;border-radius:8px;transform:rotate(8deg);display:flex;align-items:center;justify-content:center}}
.box span{{font-size:30px;font-weight:900;color:#C0392B;border:4px solid #C0392B;padding:2px 10px;transform:rotate(-12deg)}}
.clock{{position:absolute;left:340px;top:470px;width:120px;height:120px;border-radius:50%;background:#fff;border:6px solid #17332B}}
.clock b,.clock u{{position:absolute;left:50%;top:50%;background:#17332B;transform-origin:0 50%}}
.clock b{{width:38px;height:6px;transform:rotate(-60deg)}}.clock u{{width:50px;height:4px;transform:rotate(30deg)}}
.oli{{position:absolute;left:1180px;top:974px;width:220px;transform-origin:50% 100%;animation:slide .9s cubic-bezier(.2,.9,.3,1) 2.6s forwards}}
.oli svg{{position:absolute;left:0;top:0;width:220px;height:auto;opacity:0}}
.oli svg.p-wave{{animation:show .01s linear 2.6s forwards, hide .01s linear 5.1s forwards, bob 1.4s ease-in-out 3.5s 2}}
.oli svg.p-tablet{{animation:show .01s linear 5.11s forwards, hide .01s linear {7.3+X:.2f}s forwards}}
.oli svg.p-thumb{{animation:show .01s linear {7.31+X:.2f}s forwards, bob 1.4s ease-in-out {7.4+X:.2f}s infinite}}
.oli .eyes{{transform-origin:320px 276px;animation:oblink 3.7s steps(1) infinite}}
.oli .mono{{animation:glint 1s ease-out 3.4s forwards}}
.bubble{{position:absolute;white-space:nowrap;padding:28px 40px;background:#fff;border-radius:40px;font-size:52px;font-weight:700;line-height:1.3;box-shadow:0 10px 30px rgba(23,51,43,.12);opacity:0;transform:scale(.6);transform-origin:var(--ox,20%) 100%}}
.bubble:after{{content:"";position:absolute;bottom:-22px;left:var(--tx,60px);border:22px solid transparent;border-top-color:#fff;border-bottom:0}}
.b1{{left:120px;top:470px;--tx:140px;animation:pop .35s cubic-bezier(.2,1.4,.4,1) .6s forwards, fade .3s linear 3.6s forwards}}
.b2{{left:470px;top:720px;--ox:75%;--tx:330px;background:var(--g);color:#fff;animation:pop .35s cubic-bezier(.2,1.4,.4,1) 3.8s forwards, fade .3s linear 6.6s forwards}}
.b2:after{{border-top-color:var(--g)}}
.b3{{left:120px;top:470px;--tx:140px;animation:pop .35s cubic-bezier(.2,1.4,.4,1) {7.4+X:.2f}s forwards, fade .3s linear {9.8+X:.2f}s forwards}}
.tablet{{position:absolute;left:110px;top:1290px;width:480px;height:330px;border-radius:28px;background:#17332B;padding:18px;opacity:0;transform:translateY(60px);animation:rise .5s ease-out 5.2s forwards}}
.screen{{width:100%;height:100%;border-radius:16px;background:#fff;padding:22px}}
.screen.grid{{display:grid;grid-template-columns:repeat(7,1fr);grid-auto-rows:34px;gap:8px}}
.screen.grid b{{display:block;border-radius:8px;background:#E6EEE9;transform:scaleX(0);transform-origin:left;animation:fill .25s ease-out forwards}}
.screen.grid b.g{{background:var(--g)}}.screen.grid b.a{{background:var(--amber)}}.screen.grid b.s{{background:#8FC4B5}}
.screen.list{{display:flex;flex-direction:column;gap:10px}}
.screen.list .row{{display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:700;padding:8px 12px;border-radius:10px;background:#F4F7F5;opacity:0;transform:translateX(-20px);animation:rowin .3s ease-out forwards}}
.screen.list em{{font-style:normal;font-size:20px;padding:4px 12px;border-radius:999px;color:#fff;background:var(--g)}}
.screen.list em.warn{{background:var(--amber)}}.screen.list em.bad{{background:#C0392B}}
.screen.check{{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px}}
.screen.check .tick{{width:90px;height:90px;border-radius:50%;background:var(--g);position:relative;transform:scale(0);animation:pop .4s cubic-bezier(.2,1.4,.4,1) 5.9s forwards}}
.screen.check .tick:after{{content:"";position:absolute;left:28px;top:40px;width:36px;height:18px;border-left:10px solid #fff;border-bottom:10px solid #fff;transform:rotate(-45deg)}}
.screen.check p{{font-size:30px;font-weight:900;opacity:0;animation:fadein .3s linear 6.3s forwards}}
.cap{{position:absolute;left:0;right:0;top:1660px;text-align:center;font-size:52px;font-weight:900;opacity:0;animation:fadein .4s ease-out {7+X:.2f}s forwards;padding:0 60px}}
.brand{{position:absolute;left:0;right:0;bottom:70px;text-align:center;font-size:36px;font-weight:700;color:var(--g);opacity:.9}}
.end{{position:absolute;inset:0;background:var(--g);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;opacity:0;animation:fadein .5s ease-out {10.4+X:.2f}s forwards}}
.end h1{{font-size:88px;font-weight:900;line-height:1.2;text-align:center;padding:0 60px}}
.end p{{font-size:44px;font-weight:700;background:#fff;color:var(--g);padding:20px 44px;border-radius:999px}}
.end small{{font-size:32px;opacity:.85}}
.end .oe{{width:200px;opacity:0;transform:translateY(40px);animation:rise .6s ease-out {10.8+X:.2f}s forwards}}
/* ---- 真實 UI 示範卡（qr-flow）：角色縮小、卡片放大 ---- */
.cast{{position:absolute;inset:0;transform-origin:540px 1290px;animation:shrink .5s ease-out {S}s forwards, grow .5s ease-out {E}s forwards}}
.demo{{position:absolute;left:60px;top:250px;width:960px;height:800px;border-radius:36px;background:#fff;box-shadow:0 24px 60px rgba(23,51,43,.18);opacity:0;transform:translateY(50px);animation:rise .5s ease-out {S}s forwards, fade .4s linear {E}s forwards;overflow:hidden}}
.dhead{{position:absolute;left:36px;top:26px;font-size:26px;font-weight:700;color:var(--g)}}
.dhead em{{font-style:normal;font-size:20px;color:#8A9A93;margin-left:12px;border:2px solid #D5DED9;border-radius:999px;padding:2px 12px}}
.tab{{position:absolute;left:36px;top:80px;width:600px;height:450px;border-radius:26px;background:#17332B;padding:16px}}
.tscr{{position:relative;width:100%;height:100%;border-radius:14px;background:#fff;padding:14px 22px;display:flex;flex-direction:column;align-items:center}}
.thead{{width:100%;display:flex;justify-content:space-between;align-items:center;font-size:20px;font-weight:700}}
.thead i{{font-style:normal;display:inline-block;width:34px;height:34px;line-height:34px;text-align:center;border-radius:8px;background:var(--g);color:#fff;font-size:14px;margin-right:10px;vertical-align:middle}}
.thead small{{display:block;font-size:11px;color:#8A9A93;font-weight:500;margin-left:44px;margin-top:-4px}}
.thead strong{{position:relative;width:150px;height:30px;font-size:26px;font-variant-numeric:tabular-nums;text-align:right}}
.tk{{position:absolute;right:0;top:0;opacity:0;animation:show .01s linear forwards, hide .01s linear forwards}}
.qr{{margin-top:10px;padding:12px;border:3px solid #E6EEE9;border-radius:16px;background:#fff;line-height:0}}
.tbar{{width:260px;height:8px;border-radius:4px;background:#E6EEE9;margin-top:12px;overflow:hidden}}
.tbar b{{display:block;height:100%;width:100%;background:var(--g);transform-origin:left;animation:drain 60s linear {S}s forwards}}
.t1{{margin-top:12px;font-size:20px;font-weight:700}}
.t2{{margin-top:4px;font-size:17px;color:#6B7B74}}
.t2 b{{position:relative;display:inline-block;width:36px;height:22px;color:var(--g);font-size:26px;vertical-align:-3px}}
.t2 .tk{{right:auto;left:0;top:-4px}}
.phone{{position:absolute;left:632px;top:96px;width:300px;height:570px;border-radius:40px;background:#17332B;padding:14px;opacity:0;transform:translateX(220px) rotate(6deg);animation:phin .55s cubic-bezier(.2,.9,.3,1) {S+2.4:.2f}s forwards}}
.pscr{{position:relative;width:100%;height:100%;border-radius:28px;background:#F6F8F7;overflow:hidden;font-size:15px}}
.phead{{height:56px;background:#fff;display:flex;justify-content:space-between;align-items:center;padding:0 16px;font-weight:700;font-size:18px;border-bottom:2px solid #E6EEE9}}
.phead i{{font-style:normal;display:inline-block;width:28px;height:28px;line-height:28px;text-align:center;border-radius:7px;background:var(--g);color:#fff;font-size:12px;margin-right:8px;vertical-align:middle}}
.phead strong{{font-size:22px;font-variant-numeric:tabular-nums}}
.p1,.p2,.p3{{position:absolute;left:0;right:0;top:56px;bottom:0;padding:14px 14px}}
.p1 h4,.p2 h4{{font-size:26px;font-weight:900;line-height:1.2}}
.p1 small,.p2 small{{display:block;font-size:13px;color:#6B7B74;margin-top:2px}}
.search{{margin:10px 0;height:36px;line-height:36px;border:2px solid #D5DED9;border-radius:8px;background:#fff;padding:0 10px;font-size:13px;color:#A0ADA7}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}
.nm{{background:#fff;border:2px solid #E6EEE9;border-radius:10px;padding:8px 10px;opacity:0;transform:translateY(10px);animation:rise .25s ease-out forwards}}
.nm b{{display:block;font-size:17px}}.nm small{{font-size:11px;color:#8A9A93;line-height:1.3;margin-top:2px}}
.nm{{position:relative}}.nm .pk{{position:absolute;inset:-2px;border-radius:10px;border:3px solid var(--g);background:rgba(46,125,91,.12);opacity:0;animation:show .2s ease-out {S+3.75:.2f}s forwards}}
.tap{{position:absolute;width:56px;height:56px;border-radius:50%;background:rgba(46,125,91,.35);border:4px solid var(--g);opacity:0;transform:scale(.3)}}
.tap1{{left:70px;top:176px;animation:tapp .5s ease-out {S+3.6:.2f}s forwards}}
.tap2{{left:70px;top:212px;animation:tapp .5s ease-out {S+5.2:.2f}s forwards}}
.p1{{animation:hide .01s linear {S+4.2:.2f}s forwards}}
.p2{{opacity:0;animation:show .01s linear {S+4.21:.2f}s forwards, hide .01s linear {S+5.8:.2f}s forwards}}
.p2 .sess{{margin-top:10px;background:#fff;border:2px solid #E6EEE9;border-radius:10px;padding:8px 10px}}
.p2 .sess b{{display:block;font-size:14px;margin-bottom:6px}}
.p2 .sess.dim{{opacity:.55}}
.btns{{display:flex;gap:8px}}
.btns span{{flex:1;border:2px solid #D5DED9;border-radius:8px;padding:8px 6px;text-align:center;font-weight:700;font-size:14px;background:#fff;line-height:1.2}}
.btns span.on{{border-color:var(--g);color:var(--g);background:#E9F4EE;animation:pressed .2s ease-out {S+5.35:.2f}s forwards}}
.btns span small{{display:block;font-size:10px;color:#8A9A93;font-weight:500}}
.p2 p{{font-size:11px;color:#8A9A93;margin-top:12px;line-height:1.5}}
.p3{{opacity:0;background:#E9F4EE;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;gap:6px;animation:show .01s linear {S+5.81:.2f}s forwards}}
.p3 .tick{{width:96px;height:96px;border-radius:50%;background:var(--g);position:relative;transform:scale(0);animation:pop .45s cubic-bezier(.2,1.4,.4,1) {S+5.85:.2f}s forwards;margin-bottom:10px}}
.p3 .tick:after{{content:"";position:absolute;left:30px;top:40px;width:38px;height:20px;border-left:11px solid #fff;border-bottom:11px solid #fff;transform:rotate(-45deg)}}
.p3 h4{{font-size:28px;font-weight:900;color:var(--g)}}.p3 b{{font-size:18px}}.p3 small{{font-size:13px;color:#6B7B74}}
.p3 em{{font-style:normal;font-size:12px;color:#fff;background:var(--g);border-radius:999px;padding:3px 12px;margin-top:10px}}
.steps{{position:absolute;left:36px;right:36px;bottom:24px;height:84px;border-radius:20px;background:#F4F7F5}}
.steps .st{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:900;color:var(--ink);opacity:0;animation:show .01s linear forwards, hide .01s linear forwards}}
@keyframes shrink{{to{{transform:translateY(70px) scale(.5)}}}}@keyframes grow{{to{{transform:translateY(0) scale(1)}}}}
@keyframes drain{{to{{transform:scaleX(0)}}}}
@keyframes phin{{to{{opacity:1;transform:translateX(0) rotate(0)}}}}
@keyframes tapp{{0%{{opacity:0;transform:scale(.3)}}30%{{opacity:1;transform:scale(1)}}100%{{opacity:0;transform:scale(1.6)}}}}
@keyframes pick{{to{{border-color:var(--g);background:#E9F4EE}}}}
@keyframes pressed{{to{{background:var(--g);color:#fff}}}}
@keyframes breathe{{0%,100%{{transform:scaleY(1)}}50%{{transform:scaleY(1.015)}}}}
@keyframes blink{{0%,92%,100%{{transform:scaleY(1)}}95%{{transform:scaleY(.1)}}}}
@keyframes scratch{{0%,100%{{transform:rotate(-20deg)}}50%{{transform:rotate(-38deg)}}}}
@keyframes smile{{to{{border-radius:0 0 30px 30px;height:16px;width:40px;left:190px}}}}
@keyframes slide{{to{{left:720px}}}}
@keyframes bob{{0%,100%{{transform:translateY(0) rotate(0)}}50%{{transform:translateY(-16px) rotate(-2deg)}}}}
@keyframes oblink{{0%,90%,100%{{transform:scaleY(1)}}93%{{transform:scaleY(.12)}}}}
@keyframes glint{{0%{{stroke:#F2A541}}30%{{stroke:#fff}}100%{{stroke:#F2A541}}}}
@keyframes show{{to{{opacity:1}}}}@keyframes hide{{to{{opacity:0}}}}
@keyframes pop{{to{{opacity:1;transform:scale(1)}}}}
@keyframes fade{{to{{opacity:0}}}}@keyframes fadein{{to{{opacity:1}}}}
@keyframes rise{{to{{opacity:1;transform:translateY(0)}}}}
@keyframes fill{{to{{transform:scaleX(1)}}}}
@keyframes rowin{{to{{opacity:1;transform:translateX(0)}}}}
</style></head><body><div class="stage{" demo-on" if is_demo(spec) else ""}">
<div class="wall"></div><div class="sign">{esc(spec.get("scene","Oli 診所・櫃台"))}</div><div class="counter"></div>
<div class="{'cast' if is_demo(spec) else 'cast0'}">
<div class="staff"><div class="bun"></div><div class="hair"></div><div class="face"></div><div class="eye l"></div><div class="eye r"></div><div class="cheek l"></div><div class="cheek r"></div><div class="mouth"></div><div class="body"></div><div class="collar"></div><div class="arm"></div>{PROPS.get(spec.get("prop","paper"),"")}</div>
<div class="oli">{oliver.svg("wave",220,"p-wave")}{oliver.svg("tablet",220,"p-tablet")}{oliver.svg("thumb",220,"p-thumb")}</div>
</div>
<div class="bubble b1">{esc(spec["staff_line"])}</div>
<div class="bubble b2">{esc(spec["oliver_line"])}</div>
{demo_html(spec["screen"]) if is_demo(spec) else '<div class="tablet">' + screen_html(spec.get("screen") or dict(type="grid")) + '</div>'}
<div class="bubble b3">{esc(spec["relief_line"])}</div>
<div class="cap">{esc(spec.get("caption",""))}</div>
<div class="brand">{esc(spec.get("product","Oli 考勤管理系統"))}・olimedi.com</div>
<div class="end">{oliver.svg("thumb",200,"oe")}<h1>{esc(spec["end_title"])}</h1><p>LINE 搜尋 @336appfx 輸入「{esc(spec.get("keyword","Demo"))}」</p><small>{esc(spec.get("product","Oli 考勤管理系統"))}・olimedi.com</small></div>
</div></body></html>'''

def render(spec, out, dur=None, workdir=None):
    from playwright.sync_api import sync_playwright
    dur = dur or duration(spec)
    workdir = workdir or os.path.join(os.path.dirname(out) or ".", "_frames")
    os.makedirs(workdir, exist_ok=True)
    for f in os.listdir(workdir): os.remove(os.path.join(workdir, f))
    page_path = os.path.join(workdir, "scene.html")
    open(page_path, "w", encoding="utf-8").write(build_html(spec))
    n = int(dur * FPS)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + os.path.abspath(page_path)); pg.wait_for_timeout(1500)
        pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
        for i in range(n):
            pg.evaluate("t=>document.getAnimations().forEach(a=>{a.currentTime=t})", i / FPS * 1000)
            pg.screenshot(path=os.path.join(workdir, f"f{i:04d}.png"))
        b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(workdir, "f%04d.png"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-movflags", "+faststart", out], check=True)
    # 封面圖（基本版第 8.5 秒；qr-flow 版第 12.9 秒＝打卡成功畫面；spec 可用 cover_at 覆寫）
    import shutil; shutil.copy(os.path.join(workdir, f"f{int(cover_time(spec)*FPS):04d}.png"), os.path.splitext(out)[0] + "_cover.png")
    return out

def frames(spec, outdir, times):
    """只輸出幾個關鍵影格（檢查版面用）：python3 skit.py spec.json 資料夾 --frames 1.5,8,12.9"""
    from playwright.sync_api import sync_playwright
    os.makedirs(outdir, exist_ok=True)
    page_path = os.path.join(outdir, "scene.html"); open(page_path, "w", encoding="utf-8").write(build_html(spec))
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + os.path.abspath(page_path)); pg.wait_for_timeout(1500)
        pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
        for t in times:
            pg.evaluate("t=>document.getAnimations().forEach(a=>{a.currentTime=t})", t * 1000)
            pg.screenshot(path=os.path.join(outdir, f"t{t:05.2f}.png"))
        b.close()
    return outdir

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    if "--frames" in sys.argv:
        print(frames(spec, sys.argv[2], [float(x) for x in sys.argv[sys.argv.index("--frames")+1].split(",")]))
    else:
        print(render(spec, sys.argv[2]))
