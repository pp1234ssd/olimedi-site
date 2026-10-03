# 產生 1200x630 社群分享圖（需要 playwright + Chromium；系統需有 Noto Sans CJK TC 字型）
import os, html as _h
HERE=os.path.dirname(os.path.abspath(__file__))
FONT="file://"+os.path.join(HERE,"fonts","plus-jakarta-sans-latin-800-normal.woff2")
LOGO_SVG='<svg viewBox="0 0 120 120" width="{s}" height="{s}"><path d="M88.3 26.3 A44 44 0 1 1 60 16" fill="none" stroke="#2E7D5B" stroke-width="12" stroke-linecap="round"/><path d="M91 25 C 94 13, 103 6, 115 5 C 114 17, 105 25, 91 25 Z" fill="#7BB661"/><rect x="50" y="38" width="20" height="44" rx="6" fill="#F2A541"/><rect x="38" y="50" width="44" height="20" rx="6" fill="#F2A541"/></svg>'
CSS=f"""@font-face{{font-family:PJ;src:url('{FONT}') format('woff2');font-weight:800}}
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;background:#F7F5EE;font-family:'Noto Sans CJK TC','Noto Sans TC',sans-serif;color:#17332B;position:relative}}
.brand{{display:flex;align-items:center;gap:14px;font-family:PJ,'Noto Sans CJK TC';font-weight:800;font-size:40px;letter-spacing:-1px}}
.brand span{{color:#2E7D5B}} .brand small{{font-family:'Noto Sans CJK TC';font-weight:500;font-size:18px;letter-spacing:5px;color:#4A5F57;margin-left:4px}}
.circ{{position:absolute;right:-150px;top:-170px;width:560px;height:560px;border-radius:50%;background:#2E7D5B}}
.leaf{{position:absolute;left:-90px;bottom:-130px;width:320px;height:320px;border-radius:50%;background:#E1EFE6}}
.ol{{position:absolute;right:46px;top:40px}}
"""
OLIVER='<svg viewBox="0 0 640 640" width="{s}" height="{s}"><circle cx="320" cy="320" r="320" fill="#17332B"/><circle cx="320" cy="300" r="175" fill="#FFFFFF"/><path d="M320 133 Q 317 115 327 103" fill="none" stroke="#7BB661" stroke-width="9" stroke-linecap="round"/><path d="M324 119 C 330 83, 360 61, 400 59 C 396 97, 366 119, 324 119 Z" fill="#7BB661"/><ellipse cx="262" cy="276" rx="17" ry="22" fill="#17332B"/><ellipse cx="378" cy="276" rx="17" ry="22" fill="#17332B"/><circle cx="378" cy="276" r="42" fill="none" stroke="#F2A541" stroke-width="10"/><path d="M418 292 Q 446 360 426 430" fill="none" stroke="#F2A541" stroke-width="4"/><ellipse cx="220" cy="328" rx="22" ry="13" fill="#F2A541" opacity="0.6"/><path d="M320 336 C 300 312, 262 312, 246 338 C 262 330, 278 338, 284 348 C 296 356, 314 350, 320 340 Z" fill="#17332B"/><path d="M320 336 C 340 312, 378 312, 394 338 C 378 330, 362 338, 356 348 C 344 356, 326 350, 320 340 Z" fill="#17332B"/><path d="M320 506 L 256 472 L 256 540 Z" fill="#FFFFFF"/><path d="M320 506 L 384 472 L 384 540 Z" fill="#FFFFFF"/><rect x="299" y="487" width="42" height="38" rx="11" fill="#D5DED9"/></svg>'
def _brand(): return f'<div class="brand">{LOGO_SVG.format(s=54)}<div><span>Oli</span>medi<small>奧里醫療資訊</small></div></div>'
def article_html(title, cat):
    t=_h.escape(title)
    # 標題以問號斷行
    if "？" in t:
        a,b=t.split("？",1); t=f"{a}？<br><em>{b}</em>" if b else t
    return f"""<html><head><meta charset="utf-8"><style>{CSS}
.tag{{display:inline-block;background:#FCEBD2;color:#B5701A;font-weight:700;font-size:22px;letter-spacing:3px;padding:6px 18px;border-radius:999px;margin:38px 0 22px}}
h1{{font-weight:900;font-size:74px;line-height:1.25;max-width:960px}} h1 em{{font-style:normal;color:#2E7D5B;font-size:54px;display:inline-block;margin-top:12px}}
.foot{{position:absolute;left:72px;bottom:46px;font-size:22px;color:#4A5F57;font-weight:500;letter-spacing:1px}}
.wrap{{position:absolute;left:72px;top:60px}}
.circ{{width:420px;height:420px;right:-170px;top:-190px}}
</style></head><body><div class="leaf"></div><div class="circ"></div><div class="ol">{OLIVER.format(s=150)}</div>
<div class="wrap">{_brand()}<div class="tag">診所管理專欄・{_h.escape(cat)}</div><h1>{t}</h1></div>
<div class="foot">olimedi.com/blog　｜　把時間還給自己，診所的瑣事交給 Oli。</div></body></html>"""
def default_html():
    return f"""<html><head><meta charset="utf-8"><style>{CSS}
.wrap{{position:absolute;left:72px;top:80px}}
h1{{font-weight:900;font-size:72px;line-height:1.25;margin:44px 0 26px}} h1 em{{font-style:normal;color:#2E7D5B}}
.sub{{font-size:26px;color:#4A5F57;font-weight:500;letter-spacing:1px}}
.ol{{right:90px;top:150px}}
</style></head><body><div class="leaf"></div><div class="circ"></div><div class="ol">{OLIVER.format(s=300)}</div>
<div class="wrap">{_brand()}<h1>把時間<em>還給自己</em>，<br>診所的瑣事交給 Oli。</h1>
<p class="sub">考勤管理系統 · 庫存管理系統　｜　olimedi.com</p></div></body></html>"""
def render(jobs):
    """jobs: list of (html, out_jpg)"""
    if not jobs: return
    from playwright.sync_api import sync_playwright
    from PIL import Image
    import tempfile
    with sync_playwright() as p:
        b=p.chromium.launch(); pg=b.new_page(viewport={"width":1200,"height":630})
        for html,out in jobs:
            with tempfile.NamedTemporaryFile("w",suffix=".html",delete=False) as f: f.write(html); fn=f.name
            pg.goto("file://"+fn); pg.wait_for_timeout(600)
            png=fn+".png"; pg.screenshot(path=png)
            Image.open(png).convert("RGB").save(out,quality=86)
            os.remove(fn); os.remove(png)
        b.close()
