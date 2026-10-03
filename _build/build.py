# Olimedi 官網產生器：python3 _build/build.py
import os
LOGO = '<svg viewBox="0 0 120 120" width="{s}" height="{s}" aria-hidden="true"><path d="M88.3 26.3 A44 44 0 1 1 60 16" fill="none" stroke="{r}" stroke-width="12" stroke-linecap="round"/><path d="M91 25 C 94 13, 103 6, 115 5 C 114 17, 105 25, 91 25 Z" fill="#7BB661"/><rect x="50" y="38" width="20" height="44" rx="6" fill="#F2A541"/><rect x="38" y="50" width="44" height="20" rx="6" fill="#F2A541"/></svg>'
OLIVER = '<svg viewBox="0 0 640 640" width="{s}" height="{s}" role="img" aria-label="Oliver，Olimedi 的行動管家"><circle cx="320" cy="320" r="320" fill="#17332B"/><circle cx="320" cy="300" r="175" fill="#FFFFFF"/><path d="M320 133 Q 317 115 327 103" fill="none" stroke="#7BB661" stroke-width="9" stroke-linecap="round"/><path d="M324 119 C 330 83, 360 61, 400 59 C 396 97, 366 119, 324 119 Z" fill="#7BB661"/><ellipse cx="262" cy="276" rx="17" ry="22" fill="#17332B"/><ellipse cx="378" cy="276" rx="17" ry="22" fill="#17332B"/><circle cx="378" cy="276" r="42" fill="none" stroke="#F2A541" stroke-width="10"/><path d="M418 292 Q 446 360 426 430" fill="none" stroke="#F2A541" stroke-width="4"/><ellipse cx="220" cy="328" rx="22" ry="13" fill="#F2A541" opacity="0.6"/><path d="M320 336 C 300 312, 262 312, 246 338 C 262 330, 278 338, 284 348 C 296 356, 314 350, 320 340 Z" fill="#17332B"/><path d="M320 336 C 340 312, 378 312, 394 338 C 378 330, 362 338, 356 348 C 344 356, 326 350, 320 340 Z" fill="#17332B"/><path d="M320 506 L 256 472 L 256 540 Z" fill="#FFFFFF"/><path d="M320 506 L 384 472 L 384 540 Z" fill="#FFFFFF"/><rect x="299" y="487" width="42" height="38" rx="11" fill="#D5DED9"/></svg>'

import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LINE="https://line.me/R/ti/p/@336appfx"
SITE="https://olimedi.com"
def logo(s=36,r="#2E7D5B"): return LOGO.format(s=s,r=r)
AV='<img class="av" src="img/oliver.svg" alt="" width="32" height="32">'
def cta(txt="問 Oliver・預約免費展示"): return f'<a class="btn btn-line" href="{LINE}" target="_blank" rel="noopener">{AV}{txt}</a>'
def img(src,alt,w,h,cls="shot",lazy=True):
    return f'<img class="{cls}" src="img/{src}.webp" alt="{alt}" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async">'
SIZES={"att-hero":(1400,951),"att-qr":(1400,682),"att-auto":(1200,801),"att-pay":(1200,801),"att-phones":(1200,819),"mat-dash":(1400,802),"mat-scan":(520,853),"mat-kits":(1200,750),"mat-reorder":(1200,750),"mat-trace":(1200,466),"mat-mobile":(520,1125)}
def I(k,alt,cls="shot",lazy=True): return img(k,alt,*SIZES[k],cls=cls,lazy=lazy)

import re as _re
def _abs(html):
    html=_re.sub(r'(href|src)="(?!https?:|/|#|mailto:)([^"]*)"', r'\1="/\2"', html)
    return html.replace('href="/index.html#','href="/#').replace('href="/index.html"','href="/"')
def page(path,title,desc,body,active,schema,og="/img/og.jpg"):
    return _abs(_page(path,title,desc,body,active,schema,og))
def _page(path,title,desc,body,active,schema,og="/img/og.jpg"):
    url=SITE+"/"+("" if path=="index.html" else path)
    nav="".join(f'<a href="{h}"{" aria-current=\"page\"" if h==active else ""}>{t}</a>' for h,t in [("attendance.html","考勤管理系統"),("materials.html","庫存管理系統"),("blog/","診所管理專欄"),("templates.html","免費範本")])
    ld="\n".join(f'<script type="application/ld+json">{json.dumps(s,ensure_ascii=False)}</script>' for s in schema)
    return f'''<!doctype html>
<html lang="zh-Hant-TW">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Olimedi 奧里醫療資訊">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="zh_TW">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2E7D5B">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
{ld}
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="index.html" aria-label="Olimedi 奧里醫療資訊 首頁">{logo()}<b><span>Oli</span>medi</b><small>奧里醫療資訊</small></a>
<nav class="main">{nav}<a class="btn btn-line" href="{LINE}" target="_blank" rel="noopener">LINE 諮詢</a></nav>
<details class="mnav"><summary aria-label="開啟選單"><span></span><span></span><span></span></summary><div class="mnav-panel">{nav}<a class="btn btn-line" href="{LINE}" target="_blank" rel="noopener">問 Oliver・LINE 諮詢</a></div></details>
</div></header>
<main>
{body}
</main>
<footer><div class="wrap">
<div><a class="brand" href="index.html">{logo(30,"#fff")}<b><span>Oli</span>medi</b></a><p style="margin:12px 0 0">把時間還給自己，診所的瑣事交給 Oli。</p></div>
<nav><a href="attendance.html">Oli 考勤管理系統</a><a href="materials.html">Oli 庫存管理系統</a><a href="blog/">診所管理專欄</a><a href="{LINE}" target="_blank" rel="noopener">LINE：Oliver 行動管家</a><a href="https://www.facebook.com/profile.php?id=61595186213662" target="_blank" rel="noopener">Facebook 粉絲專頁</a><a href="https://www.instagram.com/olimedi2026/" target="_blank" rel="noopener">Instagram</a></nav>
<div style="width:100%;border-top:1px solid rgba(247,245,238,.14);padding-top:20px;line-height:1.9">© 2026 Olimedi 奧里醫療資訊 版權所有　·　<a href="privacy.html">隱私權聲明</a><br>本網站之文字、圖片、系統畫面、Logo 及 Oliver 角色圖像，未經書面授權不得轉載、重製或使用。<br>網站中的系統畫面皆為示範資料，人名、診所、病歷號與廠商名稱均為虛構。系統之薪資、加班、勞健保與特休等計算結果僅供參考，實際仍以相關法令及主管機關公告為準。實際功能以展示及合約內容為準。LINE 為 LY Corporation 之商標。</div>
</div></footer>
<a class="fab" href="{LINE}" target="_blank" rel="noopener" aria-label="加 LINE 問 Oliver"><span class="tip">有問題？問 Oliver 👋</span><span class="pic"><img src="img/oliver.svg" alt="Oliver" width="64" height="64"><span class="dot"></span></span></a>
</body>
</html>
'''

STEPS='''<section class="alt" id="how"><div class="wrap center">
<p class="eyebrow">HOW IT WORKS</p>
<h2>三步驟，看看 Oli 適不適合你的診所</h2>
<p class="sub">不用填表單、不用留電話，在 LINE 上跟 Oliver 說一聲就好。</p>
<div class="steps" style="text-align:left">
<div class="step"><div class="n">01</div><h3>加 LINE 問 Oliver</h3><p>告訴我們診所科別、人數，和現在最困擾的事。</p></div>
<div class="step"><div class="n">02</div><h3>約 20 分鐘線上展示</h3><p>用你的診所情境實際操作給你看，有問題當場問。</p></div>
<div class="step"><div class="n">03</div><h3>專人協助導入</h3><p>資料建檔、人員設定，我們陪你一起上手。</p></div>
</div>
</div></section>'''
def OLIVER_BAND(h="有問題？問 Oliver 就好",p="Oliver 是 Olimedi 的行動管家。想看系統實際操作、想知道適不適合你的診所，加 LINE 跟他說一聲，我們安排免費線上展示。"):
    return f'''<section><div class="wrap"><div class="oliver">
<img class="av-lg" src="img/oliver.svg" alt="Oliver，Olimedi 的行動管家" width="200" height="200" loading="lazy">
<div><span class="bubble">嗨！我是 Oliver 👋</span><h2>{h}</h2><p>{p}</p>{cta("加入 Oliver 好友")}</div>
</div></div></section>'''

ORG={"@context":"https://schema.org","@type":"Organization","name":"Olimedi 奧里醫療資訊","alternateName":["奧里","Olimedi"],"url":SITE+"/","logo":SITE+"/favicon.svg","slogan":"把時間還給自己","sameAs":[LINE,"https://www.facebook.com/profile.php?id=61595186213662","https://www.instagram.com/olimedi2026/"]}
def faq_html(items): return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q,a in items)
def faq_ld(items): return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in items]}

# ================= INDEX
faq=[("Oli 系統適合哪些診所？","專為醫療院所設計，特別適合還在用紙本、Excel 或 LINE 群組處理排班、打卡與耗材的團隊。"),
("需要買設備或安裝軟體嗎？","不用。電腦、平板、手機打開瀏覽器就能用，打卡也不用買打卡鐘。"),
("可以先看看實際畫面嗎？","可以。加入 LINE 官方帳號跟 Oliver 說一聲，我們安排約 20 分鐘的免費線上展示。")]
TEMPLATES=[
 ("排班表","醫療院所早午晚診排班表","早、午、晚診分開排，下拉選單填班；自動算出每人上班天數、總時數、晚診次數，每天每一診人數不足會標紅色，超過工時上限會提醒。",["依年月自動產生日期與星期","每診最少人數檢查","每人工時與晚診次數統計"],"排班考勤"),
 ("盤點表","耗材盤點與安全庫存表","依每日用量與廠商交貨天數算出安全庫存與建議叫貨量，自動做 ABC 分級並建議盤點頻率；另有效期追蹤與盤點差異紀錄。",["安全庫存與叫貨提醒","ABC 分級與盤點頻率","效期追蹤與盤點紀錄"],"庫存管理"),
 ("特休表","特休天數與餘額計算表","輸入到職日與月薪，依勞基法第 38 條自動算出年資、本年度特休天數、年度起訖日、剩餘天數與未休工資試算，年度快結束會提醒排休。",["依年資自動計算特休天數","剩餘天數與未休工資試算","特休天數對照表"],"排班考勤"),
]
def tpl_cards(compact=False):
    out=""
    for kw,name,desc,feats,cat in TEMPLATES:
        fl="" if compact else "<ul class='check' style='margin:0 0 20px'>"+"".join(f"<li style='font-size:15px'>{f}</li>" for f in feats)+"</ul>"
        out+=f'''<div class="post-card" style="cursor:default"><span class="tagline {"tag-g" if cat=="庫存管理" else "tag-s"}" style="align-self:flex-start">免費 Excel 範本</span><h2>{name}</h2><p>{desc}</p>{fl}<a class="btn btn-line" style="font-size:15px;padding:12px 18px" href="{LINE}" target="_blank" rel="noopener">{AV}加 LINE 輸入「{kw}」領取</a></div>'''
    return f'<div class="post-list">{out}</div>'
tbody=f'''<section class="hero" style="padding-bottom:24px"><div class="wrap" style="display:block">
<p class="crumb"><a href="index.html">首頁</a> / 免費範本</p>
<p class="eyebrow">FREE TEMPLATES</p><h1>醫療院所免費 Excel 範本</h1>
<p class="lead">排班、盤點、特休，先用 Excel 把基本功做好。加入 Oliver 的 LINE，輸入關鍵字就會自動傳給你，完全免費。</p>
</div></section>
<section style="padding-top:24px"><div class="wrap">{tpl_cards()}
<div class="note" style="margin-top:32px;font-size:15px">已經是 Oliver 的好友？直接在 LINE 聊天室輸入「排班表」「盤點表」或「特休表」即可。範本為一般管理工具，不構成法律意見；法規相關計算請以主管機關最新公告為準。</div>
</div></section>
{OLIVER_BAND("Excel 管得很累？問 Oliver","範本能幫你把基本功做好；如果想讓排班、打卡、特休、庫存自動算好，加 LINE 跟 Oliver 說一聲，我們安排約 20 分鐘免費線上展示。")}'''
open("templates.html","w").write(page("templates.html","醫療院所免費 Excel 範本｜排班表、盤點表、特休計算表｜Olimedi 奧里","免費下載醫療院所 Excel 範本：早午晚診排班表、耗材盤點與安全庫存表、特休天數與餘額計算表。加入 Olimedi LINE 輸入關鍵字即可領取。",tbody,"templates.html",[]))


home=f'''
<section class="hero"><div class="wrap">
<div>
<p class="eyebrow">診所考勤管理 · 庫存管理系統</p>
<h1>診所瑣事交給 Oli，<br>把時間<em>還給自己</em>。</h1>
<p class="lead">排班、打卡、薪資、耗材、叫貨，<br>專為診所設計，<span style="white-space:nowrap">手機就能用。</span></p>
<div class="cta-row">{cta()}<a class="btn btn-ghost" href="#products">看看產品</a></div>
<p class="cta-note">在 LINE 上直接聊，不用填表單。</p>
</div>
{I("att-hero","Oli 考勤管理系統的電腦總覽畫面與員工手機上的我的班表","hero-img shot bare",False)}
</div></section>

<section class="dark"><div class="wrap">
<p class="eyebrow">聽起來很熟悉？</p>
<h2>診所最花時間的，往往不是看診</h2>
<p class="sub">這些事每個月都在發生，而且都可以不用這麼累。</p>
<div class="pains">
<div class="pain"><p class="q">月底算薪水算到半夜</p><p class="a">打卡、請假、加班分開記，結算要一筆一筆對。</p></div>
<div class="pain"><p class="q">班表改來改去</p><p class="a">早午晚診、輪休、臨時請假，LINE 群組訊息找不到。</p></div>
<div class="pain"><p class="q">要用才發現缺貨</p><p class="a">耗材剩多少只有某個助理知道，叫貨常常來不及。</p></div>
<div class="pain"><p class="q">耗材放到過期</p><p class="a">整盒過期才發現，錢就這樣丟進垃圾桶。</p></div>
</div>
</div></section>

<section id="products"><div class="wrap">
<div class="center"><p class="eyebrow">PRODUCTS</p><h2>Oli 系列，讓診所日常更簡單</h2></div>
<div class="show">
<div class="txt"><span class="tagline tag-s">Oli 考勤管理系統</span><h3>排班、打卡、薪資，<br>一套搞定</h3><p>從早午晚診排班、手機打卡、請假加班，到每月薪資，同一個系統完成。</p>
<ul class="check"><li>設好人力需求，整月班表自動排</li><li>手機掃 QR 打卡，不用買打卡鐘</li><li>加班、請假、勞健保，薪資自動試算</li></ul>
<a class="more" href="attendance.html">看考勤管理系統 →</a></div>
{I("att-qr","櫃台平板顯示打卡 QR，員工用手機掃描打卡","shot bare")}
</div>
<div class="show rev">
<div class="txt"><span class="tagline tag-g">Oli 庫存管理系統</span><h3>診所庫存，<br>一眼看清楚</h3><p>庫存、效期、採購、應付帳款，一套系統管到好。快缺貨、快過期，系統會提醒你。</p>
<ul class="check"><li>手機掃條碼，快速入庫</li><li>依實際用量算出該補多少</li><li>常用耗材設成套組，一鍵領用</li></ul>
<a class="more" href="materials.html">看庫存管理系統 →</a></div>
{I("mat-dash","Oli 庫存管理系統總覽：庫存不足品項與建議補貨數量、效期提醒")}
</div>
</div></section>

<section><div class="wrap"><div class="center"><p class="eyebrow">FREE TEMPLATES</p><h2>先免費拿走這 3 個範本</h2><p class="sub">排班表、盤點表、特休計算表，加 Oliver 的 LINE 輸入關鍵字就會自動傳給你。</p></div>{tpl_cards(compact=True)}</div></section>
{STEPS}
{OLIVER_BAND()}

<section style="padding-top:0"><div class="wrap" style="max-width:820px">
<h2 style="font-size:28px">常見問題</h2>
<div style="margin-top:20px">{faq_html(faq)}</div>
</div></section>
'''
open("index.html","w").write(page("index.html","Olimedi 奧里｜診所考勤管理系統、庫存管理系統｜把時間還給自己",
 "Olimedi 奧里醫療資訊：專為診所設計的 Oli 考勤管理系統與 Oli 庫存管理系統。排班、手機打卡、薪資計算、耗材庫存與效期提醒，手機就能用。加 LINE 預約免費展示。",
 home,"index.html",[ORG,{"@context":"https://schema.org","@type":"WebSite","name":"Olimedi 奧里","url":SITE+"/","inLanguage":"zh-TW"},faq_ld(faq)]))

# ================= product page
def prod(fn,name,title,desc,eyebrow,h1,lead,hero_k,hero_alt,shows,trust,other):
    sh=""
    for i,(tag,h3,p,checks,k,alt,cls) in enumerate(shows):
        media = k if k.startswith("<") else I(k,alt,cls)
        sh+=f'''<div class="show{" rev" if i%2 else ""}">
<div class="txt"><span class="tagline {"tag-s" if fn=="attendance.html" else "tag-g"}">{tag}</span><h3>{h3}</h3><p>{p}</p>{"<ul class='check'>"+"".join(f"<li>{c}</li>" for c in checks)+"</ul>" if checks else ""}</div>
{media}
</div>'''
        if i==1: sh+=f'<div class="center" style="margin:-40px 0 96px">{cta("想看實際操作？問 Oliver")}</div>'
    body=f'''
<section class="hero"><div class="wrap">
<div>
<p class="crumb"><a href="index.html">首頁</a> / Oli {name}</p>
<p class="eyebrow">{eyebrow}</p>
<h1>{h1}</h1>
<p class="lead">{lead}</p>
<div class="cta-row">{cta()}</div>
<div class="trust">{"".join(f"<span>{t}</span>" for t in trust)}</div>
</div>
{I(hero_k,hero_alt,"hero-img shot" + (" bare" if fn=="attendance.html" else ""),False)}
</div></section>
<section class="alt"><div class="wrap">{sh}</div></section>
{STEPS.replace('class="alt" ','')}
{OLIVER_BAND("想看看用在你的診所會怎樣？")}
<section style="padding-top:0"><div class="wrap center"><p>也在找{other[0]}？<a class="more" href="{other[1]}">看 Oli {other[0]} →</a></p></div></section>
'''
    app={"@context":"https://schema.org","@type":"SoftwareApplication","name":"Oli "+name,"applicationCategory":"BusinessApplication","operatingSystem":"Web","description":desc,"url":f"{SITE}/{fn}","image":f"{SITE}/img/{hero_k}.webp","publisher":{"@type":"Organization","name":"Olimedi 奧里醫療資訊"}}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首頁","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Oli "+name,"item":f"{SITE}/{fn}"}]}
    open(fn,"w").write(page(fn,title,desc,body,fn,[app,bc]))

prod("attendance.html","考勤管理系統",
 "Oli考勤管理系統｜診所排班、打卡、請假、薪資一套搞定｜Olimedi 奧里",
 "專為醫療院所設計的考勤管理系統。早午晚診排班、手機 QR 打卡、請假加班、每月薪資，在同一個系統完成。加 LINE 預約免費展示。",
 "OLI 考勤管理系統",
 "排班、打卡、薪資，<br><em>一套搞定</em>",
 "專為診所設計。從早午晚診排班、手機打卡、請假加班，到每月薪資，月底結算不用再對三份表。",
 "att-hero","Oli 考勤管理系統的總覽畫面與員工手機上的我的班表",
 [("智能排班","設好人力需求，<br>整月班表自動排","設定每一診最少需要幾個人，系統依員工可做的崗位、休診日和已核准的請假，自動排出整個月的班表，再微調就好。",["早午晚診分開排","工時規定排班當下就提醒"],"att-auto","智能排班設定畫面","shot"),
  ("手機打卡","手機掃 QR 打卡，<br>拍照轉傳難代打","櫃台平板顯示打卡 QR，每 60 秒換一張。員工用自己的手機掃描、點名字就完成。不用買打卡鐘，也不用裝 App。",["QR 定時更換、單次有效，降低代打卡","可開啟自拍存證"],"att-qr","櫃台平板上的打卡 QR 與員工手機打卡畫面","shot bare"),
  ("薪資計算","每月薪資自動試算，<br>計算過程看得到","加班、請假、勞健保、勞退提繳依診所設定自動試算，點開每個人就看到計算式，確認後再結算。工資清冊、轉帳清冊一鍵匯出。",["加班先核定再計薪","特休、加退保也幫你盯"],"att-pay","每月薪資明細表","shot"),
  ("員工自助","員工用手機<br>看自己的班表與薪資單","員工登入後只看得到自己的資料：本月班表、出勤紀錄、薪資單，薪資單可以線上簽收。主管不用再一個一個回答「我這個月排幾天？」",[],"att-phones","員工手機上的我的班表、我的出勤、我的薪資單","shot bare")],
 ["不用買打卡鐘","不用安裝 App","每間診所獨立資料庫"],("庫存管理","materials.html"))

phones=f'<div class="phones">{I("mat-scan","手機掃碼入庫，自動帶出醫材品名、批號與效期","")}{I("mat-mobile","手機版總覽：庫存不足品項與建議補貨","")}</div>'
prod("materials.html","庫存管理系統",
 "Oli庫存管理系統｜診所耗材庫存、效期、採購管理｜Olimedi 奧里",
 "專為診所設計的庫存管理系統：手機掃條碼入庫、快缺貨快過期自動提醒、依用量算出建議訂購量、植入物批號追溯。加 LINE 預約免費展示。",
 "OLI 庫存管理系統",
 "診所庫存，<br><em>一眼看清楚</em>",
 "庫存、效期、採購、應付帳款，一套系統管到好。手機掃條碼，快速入庫，快缺貨、快過期系統會提醒你。",
 "mat-dash","Oli 庫存管理系統總覽：庫存不足 13 項與建議補貨數量、效期提醒",
 [("掃碼入庫","掃一下條碼，<br>品名自動帶出來","用手機相機掃醫療器材條碼，系統查詢食藥署公開的醫療器材識別（UDI）資料，已登錄的醫材可自動帶出品名、廠商，條碼上的批號、效期也一起讀進來。沒有登錄的品項，第一次手動建立後，下次掃到就直接入庫。",["電腦、平板、手機都能用","不用安裝 App"],phones,"",""),
  ("一鍵領用","常用組合，<br>助理點一下就扣庫存","換藥、注射、洗牙、術前準備……把固定會用到的耗材設成套組，領用時選套組就完成，不用一樣一樣找。",["誰、什麼時候、領了什麼都有紀錄","快到期的批號自動先用"],"mat-kits","領用作業畫面：常用、套組與領取清單","shot"),
  ("採購建議","該補多少，<br>系統幫你算","依近 30 天實際用量、目前庫存和廠商交貨天數，算出每一項的建議補貨量，並依供應商分好，勾一勾就轉成採購單。",["到貨、付款進度一眼看","欠哪家多少錢，月底不用翻帳"],"mat-reorder","採購建議：依供應商分組列出建議訂購量","shot"),
  ("植入物追溯","每一支植入物用在誰身上，<br>查得到","入庫與領用時記下批號、效期、病歷號與醫師。廠商公告召回時，輸入批號就能查出用在哪些病歷上。",[],"mat-trace","植入物來源流向紀錄","shot")],
 ["快缺貨自動提醒","效期先到先用","不用安裝 App"],("考勤管理系統","attendance.html"))

open("404.html","w").write(page("404.html","找不到頁面｜Olimedi 奧里","找不到這個頁面。",f'<section class="center"><div class="wrap"><h1>找不到這個頁面</h1><p class="sub">頁面可能已經移動。</p><div class="cta-row" style="justify-content:center"><a class="btn btn-ghost" href="index.html">回到首頁</a>{cta()}</div></div></section>',"",[]).replace('<link rel="canonical" href="https://olimedi.com/404.html">\n','<meta name="robots" content="noindex">\n'))
print("built")

priv=f'''<section><div class="wrap" style="max-width:820px">
<p class="crumb"><a href="index.html">首頁</a> / 隱私權聲明</p>
<h1 style="font-size:40px">隱私權聲明</h1>
<p class="sub" style="margin-bottom:28px">最後更新：2026 年 10 月 3 日</p>
<h2 style="font-size:22px">一、本網站不直接蒐集個人資料</h2>
<p>本網站為產品介紹網站，未設置會員註冊或表單，不會主動蒐集您的姓名、電話、電子郵件等個人資料，也未使用廣告追蹤或分析 Cookie。</p>
<h2 style="font-size:22px">二、透過 LINE 官方帳號聯繫</h2>
<p>當您點選網站中的 LINE 連結並加入 Olimedi 官方帳號（Oliver），您與我們的對話將透過 LINE 平台傳遞，LINE 平台對資料的處理適用 LY Corporation 的隱私權政策。您在對話中主動提供的資料（例如診所名稱、聯絡人、聯絡方式），我們僅用於回覆詢問、安排產品展示與後續服務聯繫，不會出售或提供給無關之第三人。</p>
<h2 style="font-size:22px">三、第三方服務</h2>
<p>本網站使用 Google Fonts 載入字型，並由 GitHub Pages 提供網站主機服務。瀏覽本網站時，這些服務可能依其政策記錄連線資訊（例如 IP 位址、瀏覽器類型）。</p>
<h2 style="font-size:22px">四、您的權利</h2>
<p>依個人資料保護法，您可以隨時透過 LINE 官方帳號要求查詢、閱覽、更正、停止利用或刪除您提供給我們的個人資料。</p>
<h2 style="font-size:22px">五、聲明修訂</h2>
<p>本聲明如有修訂，將公布於本頁面。</p>
<div class="cta-row" style="margin-top:32px">{cta("透過 LINE 聯絡我們")}</div>
</div></section>'''

open("privacy.html","w").write(page("privacy.html","隱私權聲明｜Olimedi 奧里醫療資訊","Olimedi 奧里醫療資訊網站隱私權聲明。",priv,"",[]))
print("privacy")

# ---- blog ----
# appended-run after build2 definitions (exec'd in same namespace)
os.makedirs("blog",exist_ok=True)
LAW="https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0030001"
POSTS=[]
OG_JOBS=[]
def post(slug,title,desc,cat,intro,body,sources=None,related=(),date="2026-10-03"):
    POSTS.append((slug,title,desc,cat,intro,date))
    src=""
    if sources:
        src='<h2 style="font-size:18px">參考資料</h2><ul class="sources">'+"".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for t,u in sources)+'</ul>'
    rel=""
    if related:
        rel='<div class="related"><p style="margin:0;color:var(--mute);font-size:14px">延伸閱讀</p>'+"".join(f'<a href="/blog/{s}.html">{t} →</a>' for s,t in related)+'</div>'
    html=f'''<article class="article">
<p class="crumb"><a href="/">首頁</a> / <a href="/blog/">診所管理專欄</a> / {cat}</p>
<h1>{title}</h1>
<p class="meta">Olimedi 奧里醫療資訊　·　{int(date[:4])} 年 {int(date[5:7])} 月 {int(date[8:10])} 日</p>
<p class="intro">{intro}</p>
{body}
<div class="post-cta"><img src="/img/oliver.svg" alt="Oliver" width="96" height="96" loading="lazy"><div><h3>想讓這些事自動完成？</h3><p>Oli 系統專為診所設計。加 LINE 問 Oliver，我們安排約 20 分鐘免費線上展示。</p>{cta("問 Oliver・預約免費展示")}</div></div>
<p class="note" style="margin-top:20px">📥 免費下載：<a href="/templates.html">排班表、耗材盤點表、特休計算表 Excel 範本</a></p>
{src}
{rel}
</article>'''
    ld={"@context":"https://schema.org","@type":"BlogPosting","headline":title,"description":desc,"datePublished":date,"dateModified":date,"inLanguage":"zh-TW","mainEntityOfPage":f"{SITE}/blog/{slug}.html","image":f"{SITE}/img/og/{slug}.jpg","author":{"@type":"Organization","name":"Olimedi 奧里醫療資訊"},"publisher":{"@type":"Organization","name":"Olimedi 奧里醫療資訊","logo":{"@type":"ImageObject","url":SITE+"/favicon.svg"}}}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首頁","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"診所管理專欄","item":SITE+"/blog/"},{"@type":"ListItem","position":3,"name":title,"item":f"{SITE}/blog/{slug}.html"}]}
    OG_JOBS.append((slug,title,cat))
    open(f"blog/{slug}.html","w").write(page(f"blog/{slug}.html",f"{title}｜Olimedi 奧里",desc,html,"blog/",[ld,bc],og=f"/img/og/{slug}.jpg"))

import glob,json as _json
_files=sorted(glob.glob("_build/posts/*.html"))
_meta={}
for _f in _files:
    _t=open(_f).read(); _m=_json.loads(_t.split("<!--META",1)[1].split("META-->",1)[0]); _m["body"]=_t.split("META-->",1)[1]; _meta[_m["slug"]]=_m
for _m in _meta.values():
    post(_m["slug"],_m["title"],_m["desc"],_m["cat"],_m["intro"],_m["body"],sources=[tuple(x) for x in _m.get("sources",[])],related=tuple((s,_meta[s]["title"]) for s in _m.get("related",[]) if s in _meta),date=_m.get("date","2026-10-03"))
# blog index
cards="".join(f'<a class="post-card" href="/blog/{s}.html"><span class="tagline {"tag-g" if c=="庫存管理" else "tag-s"}" style="align-self:flex-start">{c}</span><h2>{t}</h2><p>{d}</p><span class="go">閱讀全文 →</span></a>' for s,t,d,c,i,dt in sorted(POSTS,key=lambda p:p[5],reverse=True))
idx=f'''<section class="hero" style="padding-bottom:24px"><div class="wrap" style="display:block">
<p class="crumb"><a href="/">首頁</a> / 診所管理專欄</p>
<p class="eyebrow">BLOG</p><h1>診所管理專欄</h1>
<p class="lead">排班、加班、耗材、叫貨……西醫、牙醫、中醫、復健、醫美等各類醫療院所都適用的日常管理實用整理。</p>
</div></section>
<section style="padding-top:24px"><div class="wrap"><div class="post-list">{cards}</div></div></section>
{OLIVER_BAND("看完還有問題？問 Oliver")}'''
open("blog/index.html","w").write(page("blog/","診所管理專欄｜排班、加班費、耗材管理實用整理｜Olimedi 奧里","Olimedi 診所管理專欄：診所排班、員工加班費計算、耗材與庫存管理等實用文章。",idx,"blog/",[{"@context":"https://schema.org","@type":"Blog","name":"Olimedi 診所管理專欄","url":SITE+"/blog/"}]))

# sitemap
urls=[("",1.0),("attendance.html",0.9),("materials.html",0.9),("blog/",0.8),("templates.html",0.8)]+[(f"blog/{p[0]}.html",0.7) for p in POSTS]+[("privacy.html",0.3)]
open("sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>2026-10-03</lastmod><priority>{p}</priority></url>\n" for u,p in urls)+"</urlset>\n")
print("blog",len(POSTS))

# ---- 社群分享圖（只產生缺少的；要重做就刪掉 img/og/ 裡的檔案）----
import sys as _sys
_sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__))))
import og as _og
_jobs=[(_og.article_html(t,c),f"img/og/{s}.jpg") for s,t,c in OG_JOBS if not os.path.exists(f"img/og/{s}.jpg")]
if not os.path.exists("img/og.jpg"): _jobs.append((_og.default_html(),"img/og.jpg"))
os.makedirs("img/og",exist_ok=True)
_og.render(_jobs); print("og images",len(_jobs))
