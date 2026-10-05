#!/usr/bin/env python3
"""Oliver 情境劇短影片產生器（9:16、無聲、不露臉）。

用法：python3 _build/anim/skit.py spec.json out.mp4
spec.json 範例見 _build/anim/specs/。欄位：
  scene      場景標籤（如「Oli 診所・櫃台」）
  staff_line 診所人員的第一句抱怨（可用 \\n 換行，2 行內）
  prop       人員手上的道具：paper / box / clock / none
  oliver_line Oliver 的回應（2 行內）
  screen     {"type":"grid"} 排班格 | {"type":"list","rows":[["品名","狀態","ok|warn|bad"],...]} | {"type":"check","text":"..."}
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

def build_html(spec):
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
.staff{{position:absolute;left:150px;top:720px;width:420px;height:560px;transform-origin:50% 100%;animation:breathe 2.4s ease-in-out infinite}}
.staff .face{{position:absolute;left:110px;top:60px;width:200px;height:220px;border-radius:50%;background:#FBE3D0}}
.staff .hair{{position:absolute;left:96px;top:30px;width:228px;height:130px;border-radius:120px 120px 30px 30px;background:#3B2A26}}
.staff .eye{{position:absolute;top:150px;width:22px;height:30px;border-radius:50%;background:#2B2B2B;animation:blink 3.1s steps(1) infinite}}
.staff .eye.l{{left:166px}}.staff .eye.r{{left:234px}}
.staff .mouth{{position:absolute;left:196px;top:214px;width:28px;height:10px;border-radius:30px 30px 0 0;background:#C9746A;animation:smile .1s linear 7.2s forwards}}
.staff .body{{position:absolute;left:80px;top:270px;width:260px;height:300px;border-radius:120px 120px 20px 20px;background:#8FC4B5}}
.staff .collar{{position:absolute;left:170px;top:262px;width:80px;height:40px;background:#fff;clip-path:polygon(0 0,100% 0,50% 100%)}}
.staff .arm{{position:absolute;left:300px;top:330px;width:70px;height:220px;border-radius:40px;background:#8FC4B5;transform-origin:35px 20px;transform:rotate(-20deg);animation:scratch 1.2s ease-in-out .4s 2}}
.paper{{position:absolute;left:330px;top:470px;width:130px;height:160px;background:#fff;border:3px solid #D5DED9;transform:rotate(12deg)}}
.paper i{{display:block;height:8px;margin:18px 14px 0;background:#D5DED9}}
.box{{position:absolute;left:320px;top:480px;width:150px;height:110px;background:#E8DCC8;border:3px solid #C9B99A;border-radius:8px;transform:rotate(8deg);display:flex;align-items:center;justify-content:center}}
.box span{{font-size:30px;font-weight:900;color:#C0392B;border:4px solid #C0392B;padding:2px 10px;transform:rotate(-12deg)}}
.clock{{position:absolute;left:340px;top:470px;width:120px;height:120px;border-radius:50%;background:#fff;border:6px solid #17332B}}
.clock b,.clock u{{position:absolute;left:50%;top:50%;background:#17332B;transform-origin:0 50%}}
.clock b{{width:38px;height:6px;transform:rotate(-60deg)}}.clock u{{width:50px;height:4px;transform:rotate(30deg)}}
.oli{{position:absolute;left:1180px;top:820px;width:420px;transform-origin:50% 100%;animation:slide .9s cubic-bezier(.2,.9,.3,1) 2.6s forwards}}
.oli svg{{position:absolute;left:0;top:0;width:420px;height:auto;opacity:0}}
.oli svg.p-wave{{animation:show .01s linear 2.6s forwards, hide .01s linear 5.1s forwards, bob 1.4s ease-in-out 3.5s 2}}
.oli svg.p-tablet{{animation:show .01s linear 5.11s forwards, hide .01s linear 7.3s forwards}}
.oli svg.p-thumb{{animation:show .01s linear 7.31s forwards, bob 1.4s ease-in-out 7.4s infinite}}
.oli .eyes{{transform-origin:320px 276px;animation:oblink 3.7s steps(1) infinite}}
.oli .mono{{animation:glint 1s ease-out 3.4s forwards}}
.bubble{{position:absolute;padding:28px 40px;background:#fff;border-radius:40px;font-size:52px;font-weight:700;line-height:1.3;box-shadow:0 10px 30px rgba(23,51,43,.12);opacity:0;transform:scale(.6);transform-origin:var(--ox,20%) 100%}}
.bubble:after{{content:"";position:absolute;bottom:-22px;left:var(--tx,60px);border:22px solid transparent;border-top-color:#fff;border-bottom:0}}
.b1{{left:120px;top:470px;--tx:140px;animation:pop .35s cubic-bezier(.2,1.4,.4,1) .6s forwards, fade .3s linear 3.6s forwards}}
.b2{{left:470px;top:520px;--ox:90%;--tx:520px;background:var(--g);color:#fff;animation:pop .35s cubic-bezier(.2,1.4,.4,1) 3.8s forwards, fade .3s linear 6.6s forwards}}
.b2:after{{border-top-color:var(--g)}}
.b3{{left:120px;top:470px;--tx:140px;animation:pop .35s cubic-bezier(.2,1.4,.4,1) 7.4s forwards, fade .3s linear 9.8s forwards}}
.tablet{{position:absolute;left:300px;top:1270px;width:480px;height:330px;border-radius:28px;background:#17332B;padding:18px;opacity:0;transform:translateY(60px);animation:rise .5s ease-out 5.2s forwards}}
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
.cap{{position:absolute;left:0;right:0;top:1660px;text-align:center;font-size:52px;font-weight:900;opacity:0;animation:fadein .4s ease-out 7s forwards;padding:0 60px}}
.brand{{position:absolute;left:0;right:0;bottom:70px;text-align:center;font-size:36px;font-weight:700;color:var(--g);opacity:.9}}
.end{{position:absolute;inset:0;background:var(--g);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:30px;opacity:0;animation:fadein .5s ease-out 10.4s forwards}}
.end h1{{font-size:88px;font-weight:900;line-height:1.2;text-align:center;padding:0 60px}}
.end p{{font-size:44px;font-weight:700;background:#fff;color:var(--g);padding:20px 44px;border-radius:999px}}
.end small{{font-size:32px;opacity:.85}}
.end .oe{{width:300px;opacity:0;transform:translateY(40px);animation:rise .6s ease-out 10.8s forwards}}
@keyframes breathe{{0%,100%{{transform:scaleY(1)}}50%{{transform:scaleY(1.015)}}}}
@keyframes blink{{0%,92%,100%{{transform:scaleY(1)}}95%{{transform:scaleY(.1)}}}}
@keyframes scratch{{0%,100%{{transform:rotate(-20deg)}}50%{{transform:rotate(-38deg)}}}}
@keyframes smile{{to{{border-radius:0 0 30px 30px;height:16px;width:44px;left:188px}}}}
@keyframes slide{{to{{left:600px}}}}
@keyframes bob{{0%,100%{{transform:translateY(0) rotate(0)}}50%{{transform:translateY(-16px) rotate(-2deg)}}}}
@keyframes oblink{{0%,90%,100%{{transform:scaleY(1)}}93%{{transform:scaleY(.12)}}}}
@keyframes glint{{0%{{stroke:#F2A541}}30%{{stroke:#fff}}100%{{stroke:#F2A541}}}}
@keyframes show{{to{{opacity:1}}}}@keyframes hide{{to{{opacity:0}}}}
@keyframes pop{{to{{opacity:1;transform:scale(1)}}}}
@keyframes fade{{to{{opacity:0}}}}@keyframes fadein{{to{{opacity:1}}}}
@keyframes rise{{to{{opacity:1;transform:translateY(0)}}}}
@keyframes fill{{to{{transform:scaleX(1)}}}}
@keyframes rowin{{to{{opacity:1;transform:translateX(0)}}}}
</style></head><body><div class="stage">
<div class="wall"></div><div class="sign">{esc(spec.get("scene","Oli 診所・櫃台"))}</div><div class="counter"></div>
<div class="staff"><div class="hair"></div><div class="face"></div><div class="eye l"></div><div class="eye r"></div><div class="mouth"></div><div class="body"></div><div class="collar"></div><div class="arm"></div>{PROPS.get(spec.get("prop","paper"),"")}</div>
<div class="bubble b1">{esc(spec["staff_line"])}</div>
<div class="oli">{oliver.svg("wave",420,"p-wave")}{oliver.svg("tablet",420,"p-tablet")}{oliver.svg("thumb",420,"p-thumb")}</div>
<div class="bubble b2">{esc(spec["oliver_line"])}</div>
<div class="tablet">{screen_html(spec.get("screen") or dict(type="grid"))}</div>
<div class="bubble b3">{esc(spec["relief_line"])}</div>
<div class="cap">{esc(spec.get("caption",""))}</div>
<div class="brand">{esc(spec.get("product","Oli 考勤管理系統"))}・olimedi.com</div>
<div class="end">{oliver.svg("thumb",300,"oe")}<h1>{esc(spec["end_title"])}</h1><p>LINE 搜尋 @336appfx 輸入「{esc(spec.get("keyword","Demo"))}」</p><small>{esc(spec.get("product","Oli 考勤管理系統"))}・olimedi.com</small></div>
</div></body></html>'''

def render(spec, out, dur=13.0, workdir=None):
    from playwright.sync_api import sync_playwright
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
    # 封面圖（第 8.5 秒）
    import shutil; shutil.copy(os.path.join(workdir, f"f{int(8.5*FPS):04d}.png"), os.path.splitext(out)[0] + "_cover.png")
    return out

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    print(render(spec, sys.argv[2]))
