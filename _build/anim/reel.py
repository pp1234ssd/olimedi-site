#!/usr/bin/env python3
"""IG / FB Reels 知識型短影片產生器（9:16、約 25 秒、動態字卡＋Oliver，無聲，上傳時在 App 內加音樂）。

用法：python3 _build/anim/reel.py _build/anim/specs/reel-xx.json out.mp4
會同時輸出 out_cover.png（封面，取 hook 畫面）。

spec 欄位（全部字串可用 \\n 換行）：
  hook     {"top":"小標", "big":"大標（2 行內，每行 ≤ 8 字）"}            0–3.4s  抓痛點
  calendar {"title":"…", "days":[["10","六","國慶日"],…3 格], "focus":1, "mark":"?", "mark_on":0, "note":"…"}  3.4–8s
  compare  {"q":"…", "a":{"tag","big","sub","stamp"}, "b":{"tag","big","sub","stamp"}}               8–14s
  numbers  {"title":"…", "rows":[["情境","+1,200 元"],…2 列], "note":"…"}                             14–19s
  warn     {"big":"…", "sub":"…"}                                                                     19–21.6s
  end      {"title":"…", "cta":"連結在個人檔案", "keyword":"排班表"}                                     21.6–25s
規則同 README：口語、短句、不用絕對用語；數字只用網站文章有官方來源的。
安全區：重要文字放在 y 260–1560、x 70–940（避開 Reels 上下 UI 與右側按鈕）。
"""
import json, os, sys, subprocess, html, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oliver

FPS = 30
DUR = 25.0
T = dict(hook=(0, 3.4), calendar=(3.4, 8.0), compare=(8.0, 14.0), numbers=(14.0, 19.0), warn=(19.0, 21.6), end=(21.6, DUR))

def esc(s): return html.escape(s).replace("\\n", "<br>").replace("\n", "<br>")

CSS = r"""
:root{--g:#2E7D5B;--gd:#1F5C42;--ink:#17332B;--bg:#F7F5EE;--amber:#F2A541;--red:#D9473B;--mint:#8FC4B5}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--bg);font-family:'Noto Sans CJK TC','Noto Sans TC',sans-serif;color:var(--ink)}
.stage{position:relative;width:1080px;height:1920px;overflow:hidden}
.shake{position:absolute;inset:0}
/* 背景漂浮色塊：整支片持續有動感 */
.blob{position:absolute;border-radius:50%;opacity:.55}
.b1{width:520px;height:520px;background:#E3EFE8;left:-160px;top:180px;animation:drift1 7s ease-in-out infinite}
.b2{width:380px;height:380px;background:#FCEBD2;right:-120px;top:1180px;animation:drift2 6s ease-in-out infinite}
.b3{width:180px;height:180px;background:#DCEBE3;right:120px;top:300px;animation:drift1 5s ease-in-out infinite reverse}
.dots{position:absolute;inset:0;background-image:radial-gradient(#D5DED9 3px,transparent 3px);background-size:60px 60px;opacity:.35;animation:pan 12s linear infinite}
.progress{position:absolute;left:0;top:0;height:12px;background:var(--g);width:0;animation:grow __DUR__s linear 0s forwards}
.brand{position:absolute;left:70px;top:150px;font-size:34px;font-weight:700;color:var(--g);letter-spacing:2px}
.brand b{font-weight:900}
.scene{position:absolute;inset:0;opacity:0}
.wipe{position:absolute;top:-200px;bottom:-200px;width:1500px;left:-2300px;background:var(--g);transform:skewX(-14deg);z-index:50}
.wipe:after{content:"";position:absolute;top:0;bottom:0;right:-120px;width:120px;background:var(--amber)}
/* hook */
.top{position:absolute;left:70px;right:70px;top:300px;font-size:58px;font-weight:700;color:var(--g)}
.big{position:absolute;left:70px;right:70px;top:420px;font-size:118px;line-height:1.18;font-weight:900}
.big span{display:block;opacity:0}
.big em{font-style:normal;color:var(--red)}
.face{position:absolute;left:300px;top:930px;width:480px;height:480px}
.face .head{position:absolute;inset:0;border-radius:50%;background:#FBE3D0}
.face .hair{position:absolute;left:-10px;top:-20px;width:500px;height:240px;border-radius:250px 250px 60px 60px;background:#4A3530}
.face .bun{position:absolute;left:170px;top:-90px;width:140px;height:120px;border-radius:50%;background:#4A3530}
.face .eye{position:absolute;top:230px;width:70px;height:96px;border-radius:50%;background:#2B2B2B}
.face .eye:after{content:"";position:absolute;left:14px;top:14px;width:24px;height:24px;border-radius:50%;background:#fff}
.face .eye.l{left:120px}.face .eye.r{left:290px}
.face .mouth{position:absolute;left:205px;top:360px;width:70px;height:80px;border-radius:50%;background:#B8584E}
.face .ck{position:absolute;top:340px;width:70px;height:36px;border-radius:50%;background:#F7B3A3;opacity:.7}
.face .ck.l{left:60px}.face .ck.r{left:350px}
.sweat{position:absolute;left:420px;top:150px;width:60px;height:86px;background:#7EC3E6;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;opacity:0}
.zap{position:absolute;font-size:120px;font-weight:900;color:var(--amber);opacity:0}
/* calendar */
.h2{position:absolute;left:70px;right:70px;top:300px;font-size:72px;font-weight:900}
.cal{position:absolute;left:70px;top:520px;width:870px;display:flex;gap:30px;perspective:1600px}
.day{flex:1;height:420px;border-radius:36px;background:#fff;box-shadow:0 18px 40px rgba(23,51,43,.12);text-align:center;position:relative;transform-origin:50% 0;opacity:0;overflow:visible}
.day .hd{height:90px;border-radius:36px 36px 0 0;background:var(--mint);color:#fff;font-size:44px;font-weight:900;line-height:90px}
.day .n{font-size:170px;font-weight:900;line-height:1;margin-top:28px}
.day .lb{font-size:42px;font-weight:700;color:var(--g);margin-top:16px;min-height:50px}
.day.focus .hd{background:var(--red)}
.ring{position:absolute;left:-30px;top:60px;width:340px;height:340px;overflow:visible}
.ring path{fill:none;stroke:var(--red);stroke-width:12;stroke-linecap:round;stroke-dasharray:1200;stroke-dashoffset:1200}
.qm{position:absolute;top:-130px;font-size:110px;font-weight:900;color:var(--amber);opacity:0}
.note{position:absolute;left:70px;right:70px;top:1030px;font-size:60px;font-weight:900;text-align:center;opacity:0}
.note mark{background:linear-gradient(transparent 55%,#FCD9A0 55%);color:inherit;padding:0 8px}
.peek{position:absolute;left:640px;top:1200px;width:300px}
/* compare */
.q{position:absolute;left:70px;right:70px;top:290px;font-size:62px;font-weight:900;line-height:1.3}
.card{position:absolute;left:70px;width:870px;height:380px;border-radius:40px;background:#fff;box-shadow:0 18px 40px rgba(23,51,43,.12);padding:40px 50px;opacity:0}
.card.a{top:560px}.card.b{top:990px}
.card .tag{display:inline-block;font-size:40px;font-weight:700;color:#fff;background:var(--mint);padding:8px 26px;border-radius:999px}
.card.b .tag{background:var(--amber)}
.card .cb{font-size:84px;font-weight:900;margin-top:26px;line-height:1.15}
.card .cs{font-size:42px;font-weight:700;color:#4A5F57;margin-top:14px}
.stamp{position:absolute;right:30px;top:-50px;width:170px;height:170px;border-radius:50%;border:11px solid var(--red);color:var(--red);font-size:60px;font-weight:900;display:flex;align-items:center;justify-content:center;transform:rotate(-14deg) scale(3);opacity:0;background:rgba(255,255,255,.85)}
.card.a .stamp{border-color:var(--g);color:var(--g);font-size:50px}
/* numbers */
.tab{position:absolute;left:70px;top:520px;width:870px;border-radius:44px;background:var(--ink);padding:30px;opacity:0}
.tab .scr{background:#fff;border-radius:26px;padding:20px 40px}
.nrow{display:flex;justify-content:space-between;align-items:center;padding:34px 0;border-bottom:4px dashed #E3EAE6;opacity:0}
.nrow:last-child{border-bottom:0}
.nrow .k{font-size:46px;font-weight:700;line-height:1.25}
.nrow .v{font-size:84px;font-weight:900;color:var(--g);display:flex;align-items:flex-end}
.roll{display:inline-block;height:1.1em;overflow:hidden;line-height:1.1em;vertical-align:bottom}
.roll i{display:block;font-style:normal}
.unit{font-size:44px;margin-left:8px;line-height:1.6}
.oli-n{position:absolute;left:650px;top:1150px;width:300px}
.small{position:absolute;left:70px;right:70px;top:1110px;font-size:40px;font-weight:700;color:#4A5F57;opacity:0}
/* warn */
.ban{position:absolute;left:290px;top:420px;width:500px;height:500px;border-radius:50%;border:44px solid var(--red);transform:scale(0);background:#fff}
.ban:before{content:"";position:absolute;left:50%;top:50%;width:520px;height:44px;margin:-22px 0 0 -260px;background:var(--red);transform:rotate(-45deg)}
.ban span{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:150px;font-weight:900;color:var(--ink);-webkit-text-stroke:18px #fff;paint-order:stroke fill;z-index:2}
.wsub{position:absolute;left:70px;right:70px;top:1010px;text-align:center;font-size:66px;font-weight:900;line-height:1.35;opacity:0}
/* end */
.end{position:absolute;inset:0;background:var(--g);color:#fff;opacity:0;z-index:40}
.end .t{position:absolute;left:60px;right:60px;top:790px;text-align:center;font-size:78px;font-weight:900;line-height:1.25;opacity:0}
.end .cta{position:absolute;left:50%;top:1060px;transform:translateX(-50%);white-space:nowrap;font-size:56px;font-weight:900;background:#fff;color:var(--g);padding:24px 54px;border-radius:999px;opacity:0}
.end .line{position:absolute;left:70px;right:70px;top:1230px;text-align:center;font-size:40px;font-weight:700;opacity:0}
.end .oe{position:absolute;left:390px;top:260px;width:300px;opacity:0}
.end .spark{position:absolute;width:26px;height:26px;border-radius:50%;background:var(--amber);opacity:0}
@keyframes grow{to{width:100%}}
@keyframes drift1{0%,100%{transform:translate(0,0)}50%{transform:translate(60px,-40px)}}
@keyframes drift2{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(-50px,30px) scale(1.08)}}
@keyframes pan{to{background-position:60px 120px}}
@keyframes sin{from{opacity:0;transform:translateY(40px)}to{opacity:1;transform:none}}
@keyframes sout{to{opacity:0;transform:translateY(-40px)}}
@keyframes wipe{from{left:-2300px}to{left:1700px}}
@keyframes slam{0%{opacity:0;transform:scale(2.4)}60%{opacity:1;transform:scale(.92)}80%{transform:scale(1.05)}100%{opacity:1;transform:scale(1)}}
@keyframes shake{0%,100%{transform:translate(0,0)}20%{transform:translate(-18px,8px)}40%{transform:translate(16px,-10px)}60%{transform:translate(-10px,6px)}80%{transform:translate(8px,-4px)}}
@keyframes popin{0%{opacity:0;transform:scale(.3)}70%{opacity:1;transform:scale(1.12)}100%{opacity:1;transform:scale(1)}}
@keyframes drop{0%{opacity:0;transform:translateY(-40px)}30%{opacity:1}100%{opacity:0;transform:translateY(120px)}}
@keyframes wob{0%,100%{transform:rotate(0)}25%{transform:rotate(-4deg)}75%{transform:rotate(4deg)}}
@keyframes flip{0%{opacity:0;transform:rotateX(-100deg)}70%{opacity:1;transform:rotateX(12deg)}100%{opacity:1;transform:rotateX(0)}}
@keyframes draw{to{stroke-dashoffset:0}}
@keyframes fadein{to{opacity:1}}
@keyframes bob{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-22px) rotate(-3deg)}}
@keyframes rise{0%{opacity:0;transform:translateY(300px)}70%{opacity:1;transform:translateY(-20px)}100%{opacity:1;transform:translateY(0)}}
@keyframes fromL{0%{opacity:0;transform:translateX(-1100px) rotate(-6deg)}70%{opacity:1;transform:translateX(30px) rotate(1deg)}100%{opacity:1;transform:none}}
@keyframes fromR{0%{opacity:0;transform:translateX(1100px) rotate(6deg)}70%{opacity:1;transform:translateX(-30px) rotate(-1deg)}100%{opacity:1;transform:none}}
@keyframes stamp{0%{opacity:0;transform:rotate(-14deg) scale(3)}60%{opacity:1;transform:rotate(-14deg) scale(.9)}100%{opacity:1;transform:rotate(-14deg) scale(1)}}
@keyframes ban{0%{transform:scale(0) rotate(-90deg)}70%{transform:scale(1.1) rotate(8deg)}100%{transform:scale(1) rotate(0)}}
@keyframes sparkle{0%{opacity:0;transform:scale(0)}40%{opacity:1;transform:scale(1.4)}100%{opacity:0;transform:scale(.4) translateY(-80px)}}
@keyframes pulse{0%,100%{transform:translateX(-50%) scale(1)}50%{transform:translateX(-50%) scale(1.07)}}
"""

def a(name, dur, delay, ease="cubic-bezier(.2,1.2,.4,1)", fill="both", it="1"):
    return f"{name} {dur}s {ease} {delay:.2f}s {it} {fill}"

def scene(key, inner, extra_style=""):
    s, e = T[key]
    out = "" if key == "end" else f", sout .3s ease-in {e-0.3:.2f}s 1 forwards"
    return f'<div class="scene s-{key}" style="animation:sin .35s ease-out {s:.2f}s 1 both{out};{extra_style}">{inner}</div>'

def roller(text, delay):
    out = []
    for i, ch in enumerate(text):
        if ch.isdigit():
            d = int(ch); seq = "0123456789" + "0123456789"[:d + 1]; idx = 10 + d
            col = "".join(f"<i>{c}</i>" for c in seq)
            out.append(f'<span class="roll"><span style="display:block;animation:roll{idx} 1.1s cubic-bezier(.15,.9,.25,1) {delay+i*0.08:.2f}s 1 both">{col}</span></span>')
        else:
            out.append(f"<span>{html.escape(ch)}</span>")
    return "".join(out)

ROLL_CSS = "".join(f"@keyframes roll{k}{{from{{transform:translateY(0)}}to{{transform:translateY(-{k*1.1:.1f}em)}}}}" for k in range(10, 20))

def build_html(sp):
    h, c, cp, nm, w, en = sp["hook"], sp["calendar"], sp["compare"], sp["numbers"], sp["warn"], sp["end"]
    # ---- hook
    lines = [l for l in h["big"].replace("\\n", "\n").split("\n")]
    big = "".join(f'<span style="animation:{a("slam",.5,0.35+i*0.45)}">{html.escape(l).replace("！","<em>！</em>").replace("？","<em>？</em>")}</span>' for i, l in enumerate(lines))
    hook = f'''<div class="top" style="animation:{a("popin",.4,0.1)}">{esc(h["top"])}</div><div class="big">{big}</div>
<div class="face" style="animation:{a("rise",.6,0.5)}, wob .5s ease-in-out 1.4s 3"><div class="bun"></div><div class="head"></div><div class="hair" style="height:200px"></div>
<div class="eye l"></div><div class="eye r"></div><div class="ck l"></div><div class="ck r"></div><div class="mouth" style="animation:{a("popin",.3,1.3)}"></div>
<div class="sweat" style="animation:drop 1s ease-in 1.5s 2 both"></div></div>
<div class="zap" style="left:170px;top:930px;animation:{a("popin",.3,1.35)}">!</div><div class="zap" style="left:830px;top:1000px;animation:{a("popin",.3,1.5)}">?</div>'''
    # ---- calendar
    s = T["calendar"][0]
    days = ""
    for i, (n, wd, lb) in enumerate(c["days"][:3]):
        foc = " focus" if i == c.get("focus", 1) else ""
        ring = f'<svg class="ring" viewBox="0 0 340 340"><path d="M170 18 C 300 20, 330 140, 300 240 C 270 330, 90 340, 40 250 C 0 170, 40 40, 190 30" style="animation:draw .7s ease-out {s+1.6:.2f}s 1 forwards"/></svg>' if foc else ""
        qm = f'<div class="qm" style="left:80px;animation:{a("popin",.35,s+2.4)}, wob .6s ease-in-out {s+2.8:.2f}s 3">{esc(c.get("mark","?"))}</div>' if i == c.get("mark_on", 0) else ""
        days += f'<div class="day{foc}" style="animation:{a("flip",.6,s+0.4+i*0.22)}"><div class="hd">週{esc(wd)}</div><div class="n">{esc(n)}</div><div class="lb">{esc(lb)}</div>{ring}{qm}</div>'
    cal = f'''<div class="h2" style="animation:{a("popin",.4,s+0.15)}">{esc(c["title"])}</div><div class="cal">{days}</div>
<div class="note" style="animation:{a("popin",.4,s+2.0)}"><mark>{esc(c["note"])}</mark></div>
<div class="peek" style="animation:{a("rise",.6,s+2.6)}">{oliver.svg("point",300)}</div>'''
    # ---- compare
    s = T["compare"][0]
    def card(k, d, anim, t0):
        return f'''<div class="card {k}" style="animation:{a(anim,.6,t0)}"><span class="tag">{esc(d["tag"])}</span><div class="cb">{esc(d["big"])}</div><div class="cs">{esc(d["sub"])}</div>
<div class="stamp" style="animation:stamp .4s cubic-bezier(.2,1.2,.4,1) {t0+1.4:.2f}s 1 both">{esc(d.get("stamp",""))}</div></div>'''
    comp = f'''<div class="q" style="animation:{a("popin",.4,s+0.15)}">{esc(cp["q"])}</div>{card("a",cp["a"],"fromL",s+0.6)}{card("b",cp["b"],"fromR",s+2.4)}'''
    # ---- numbers
    s = T["numbers"][0]
    rows = "".join(f'<div class="nrow" style="animation:{a("sin",.4,s+0.9+i*1.0,"ease-out")}"><div class="k">{esc(k)}</div><div class="v">{roller(v.replace(" 元",""),s+1.0+i*1.0)}<span class="unit">元</span></div></div>' for i, (k, v) in enumerate(nm["rows"][:3]))
    nums = f'''<div class="h2" style="animation:{a("popin",.4,s+0.15)}">{esc(nm["title"])}</div><div class="tab" style="animation:{a("rise",.6,s+0.4)}"><div class="scr">{rows}</div></div>
<div class="small" style="animation:fadein .4s ease-out {s+3.0:.2f}s 1 both">{esc(nm.get("note",""))}</div>
<div class="oli-n" style="animation:{a("rise",.6,s+2.6)}"><div style="animation:bob 1.2s ease-in-out {s+3.2:.2f}s infinite">{oliver.svg("thumb",300)}</div></div>'''
    # ---- warn
    s = T["warn"][0]
    warn = f'''<div class="ban" style="animation:ban .6s cubic-bezier(.2,1.2,.4,1) {s+0.2:.2f}s 1 both"><span>{esc(w["big"])}</span></div>
<div class="wsub" style="animation:{a("popin",.4,s+0.9)}">{esc(w["sub"])}</div>'''
    # ---- end
    s = T["end"][0]
    sparks = "".join(f'<div class="spark" style="left:{x}px;top:{y}px;animation:sparkle .9s ease-out {s+0.9+i*0.12:.2f}s 2 both"></div>' for i, (x, y) in enumerate([(300, 330), (760, 300), (250, 560), (820, 540), (520, 220), (900, 420)]))
    end = f'''<div class="end" style="animation:fadein .3s ease-out {s:.2f}s 1 both">{sparks}
<div class="oe" style="animation:{a("rise",.6,s+0.3)}"><div style="animation:bob 1.2s ease-in-out {s+1.0:.2f}s infinite">{oliver.svg("thumb",300)}</div></div>
<div class="t" style="animation:{a("popin",.45,s+0.6)}">{esc(en["title"])}</div>
<div class="cta" style="animation:fadein .3s ease-out {s+1.2:.2f}s 1 both, pulse 1s ease-in-out {s+1.5:.2f}s infinite">{esc(en.get("cta","完整文章連結在個人檔案"))}</div>
<div class="line" style="animation:fadein .4s ease-out {s+1.6:.2f}s 1 both">LINE 搜尋 @336appfx 輸入「{esc(en.get("keyword","Demo"))}」<br>Olimedi 奧里醫療資訊・olimedi.com</div></div>'''
    # 轉場：每個場景交界一道斜向色帶
    wipes = "".join(f'<div class="wipe" style="animation:wipe .55s cubic-bezier(.7,0,.3,1) {T[k][0]-0.28:.2f}s 1 both"></div>' for k in ("calendar", "compare", "numbers", "warn"))
    shakes = ", ".join(f"shake .35s linear {t:.2f}s 1" for t in (0.8, 1.25, T["compare"][0] + 2.0, T["compare"][0] + 3.8, T["warn"][0] + 0.6))
    return f'''<!doctype html><html lang="zh-Hant-TW"><head><meta charset="utf-8"><style>{CSS.replace("__DUR__", str(DUR))}{ROLL_CSS}</style></head><body>
<div class="stage"><div class="shake" style="animation:{shakes}">
<div class="dots"></div><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
<div class="brand"><b>Olimedi</b> 診所管理專欄</div>
{scene("hook", hook)}{scene("calendar", cal)}{scene("compare", comp)}{scene("numbers", nums)}{scene("warn", warn)}
{wipes}{end}</div><div class="progress"></div></div></body></html>'''

def render(spec, out, workdir=None):
    from playwright.sync_api import sync_playwright
    workdir = workdir or os.path.join(os.path.dirname(os.path.abspath(out)), "_frames")
    shutil.rmtree(workdir, ignore_errors=True); os.makedirs(workdir)
    page_path = os.path.join(workdir, "scene.html")
    open(page_path, "w", encoding="utf-8").write(build_html(spec))
    n = int(DUR * FPS)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto("file://" + page_path); pg.wait_for_timeout(800)
        pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
        for i in range(n):
            pg.evaluate("t=>document.getAnimations().forEach(a=>{a.currentTime=t})", i / FPS * 1000)
            pg.screenshot(path=os.path.join(workdir, f"f{i:04d}.png"))
        b.close()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(workdir, "f%04d.png"),
                    "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-movflags", "+faststart", out], check=True)
    shutil.copy(os.path.join(workdir, f"f{int(2.6*FPS):04d}.png"), os.path.splitext(out)[0] + "_cover.png")
    return out

if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[3] == "--frames":   # 只輸出幾張關鍵影格檢查
        sp = json.load(open(sys.argv[1], encoding="utf-8"))
        from playwright.sync_api import sync_playwright
        wd = sys.argv[2]; os.makedirs(wd, exist_ok=True)
        open(os.path.join(wd, "scene.html"), "w", encoding="utf-8").write(build_html(sp))
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
            pg.goto("file://" + os.path.abspath(os.path.join(wd, "scene.html"))); pg.wait_for_timeout(800)
            pg.evaluate("document.getAnimations().forEach(a=>a.pause())")
            for t in [float(x) for x in sys.argv[4].split(",")]:
                pg.evaluate("t=>document.getAnimations().forEach(a=>{a.currentTime=t})", t * 1000)
                pg.screenshot(path=os.path.join(wd, f"t{t:05.2f}.png"))
            b.close()
    else:
        print(render(json.load(open(sys.argv[1], encoding="utf-8")), sys.argv[2]))
