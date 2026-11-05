# -*- coding: utf-8 -*-
# 開業整合服務頁（services.html）。由 build.py 匯入；需要 page / cta / OLIVER_BAND / LINE / SITE / faq_html / faq_ld。

def build(page, cta, OLIVER_BAND, LINE, SITE, faq_html, faq_ld, AV, preview=True):
    # ---- 六大服務 ----
    SERVICES=[
     ("01","開業行政代辦","從公會入會到健保特約簽約，一條線跑完。",
      ["公會入會、衛生局現勘與執照申請","統一編號、健保專用帳戶、勞健保投保單位","健保醫療網、VPN 與醫事人員卡","健保特約簽約與開業前備查"],"tag-b"),
     ("02","開業前評估","簽約前先看清楚：這個空間能不能順利變成診所。",
      ["商圈、交通與同業密度初勘","建物使用執照與用途、分區初步檢核","診間數、動線與水電氣網點位可行性","裝潢前把「以為對方會處理」的交界面列出來"],"tag-b"),
     ("03","人事制度建置","開業前先把排班、薪資、請假寫清楚，省掉之後的爭議。",
      ["人力配置與排班規劃（含四週變形工時）","勞動契約、工作規則與員工手冊","Oli 考勤管理系統導入與打卡設定","30／60／90 天考核與教育訓練節奏"],"tag-s"),
     ("04","耗材與庫存建置","第一批不要什麼都先買；先把 A 類安全庫存顧好。",
      ["依科別建立耗材分類架構與首批採購清單","安全庫存、ABC 分級與盤點頻率","效期與批號追蹤制度","Oli 庫存管理系統導入與供應商對帳"],"tag-g"),
     ("05","資訊系統規劃","網路、弱電、診所系統與備份，一次規劃好，不要開幕後再拉線。",
      ["診間網路點位、有線為主與雙線備援","診所系統、健保 VPN 與讀卡設備串接","影像、備份與權限規劃","開幕前掛號→看診→收費→申報全流程試跑"],"tag-b"),
     ("06","開業後 90 天追蹤","開幕不是終點，前 90 天把「能看診」變成「能穩定經營」。",
      ["Day 7／30／90 固定回顧會議","營運儀表板：初診、回診、No-show、耗材成本","申報核減追蹤與流程修正","人力、設備與擴充決策建議"],"tag-g"),
    ]
    cards="".join(f'''<div class="svc"><div class="svc-n">{n}</div><span class="tagline {tag}">服務 {n}</span><h3>{h}</h3><p>{p}</p><ul class="check">{"".join(f"<li>{x}</li>" for x in items)}</ul></div>''' for n,h,p,items,tag in SERVICES)

    # ---- 13 步驟時程 ----
    PHASES=[("T-6～8 個月","定位／店面／設計",["開業策略與預算","店面與法規可行性","空間與工程整合"]),
            ("T-4～6 個月","施工／設備／設立",["品牌與對外溝通","大型設備選購","診所設立申請"]),
            ("T-2～3 個月","裝機／招募／訓練",["人事制度","教育訓練","器械耗材採購與管理","診所 SOP 與感控"]),
            ("T-14 天～開幕","驗收／試營運／開診",["健保申報模擬","試營運與開幕","正式營運與追蹤"])]
    timeline="".join(f'''<div class="tl"><div class="tl-when">{w}</div><div class="tl-what">{t}</div><ul>{"".join(f"<li>{x}</li>" for x in xs)}</ul></div>''' for w,t,xs in PHASES)

    # ---- 可協助 / 需專業單位 ----
    CAN=["開業行政流程與文件準備、送件與追蹤","人事、考勤、薪資制度與系統導入","耗材分類、首批採購與庫存制度","診所網路、資訊系統與健保連線規劃","開業時程管理與跨單位交界面確認","開業後營運數字追蹤"]
    PRO=["建築、室內裝修、消防與結構簽證","放射防護與相關法定申請","稅務、會計與合夥契約","勞動契約最終法律審閱","醫療廣告內容的法規審核","臨床醫療流程與院內醫療決策"]

    # ---- 服務流程 ----
    FLOW=[("01","加 LINE 跟 Oliver 說","告訴我們科別、預計開業時間與目前階段（概念／規劃／施工／試營運）。"),
          ("02","線上或現場訪談","約 40 分鐘，一起看平面圖、時程與現在卡住的事，列出需要處理的項目。"),
          ("03","提案與報價","依你需要的模組出一份清單：哪些我們做、哪些要找專業單位、各自的期限與負責人。"),
          ("04","執行與追蹤","每週固定更新進度，不把事情留在群組訊息裡；開幕後 90 天繼續追蹤。")]
    flow="".join(f'<div class="step"><div class="n">{n}</div><h3>{h}</h3><p>{p}</p></div>' for n,h,p in FLOW)

    FAQ=[("哪些科別可以用這項服務？","西醫、牙醫、中醫、復健、醫美等各類醫療院所都可以。行政流程大致相同，差異在設備、感控與耗材，我們會依科別調整清單。"),
         ("只需要其中一項可以嗎？","可以。六個模組可以單獨委託，例如只做行政代辦，或只做人事與考勤系統建置。"),
         ("已經開業的診所可以嗎？","可以。人事制度、耗材庫存、資訊系統與營運追蹤都適用既有診所；很多診所是在換系統或展第二間店時找我們。"),
         ("你們會幫忙裝潢或找設計師嗎？","不會。建築、裝潢、消防、放射與稅務需由各專業單位負責；我們的角色是把這些單位之間的交界面與時程串起來，並處理行政、人事、耗材與資訊系統。"),
         ("費用怎麼算？","依委託的模組與診所規模報價，訪談後提供書面清單與報價，沒有隱藏費用。")]

    body=f'''
<section class="hero" style="padding-bottom:40px"><div class="wrap" style="display:block;max-width:860px">
<p class="crumb"><a href="index.html">首頁</a> / 開業整合服務</p>
<p class="eyebrow">CLINIC LAUNCH</p>
<h1>診所開業整合服務</h1>
<p class="lead" style="max-width:36em">把行政、人事、耗材、資訊系統與開業時程接起來。開業最容易出錯的不是哪一家廠商，而是大家「以為對方會處理」的交界面；我們把它先顧好。</p>
<div class="cta-row">{cta("問 Oliver・預約開業諮詢")}<a class="btn btn-ghost" href="#services">看六項服務</a></div>
<div class="trust"><span>各科別醫療院所適用</span><span>模組可單獨委託</span><span>開業後 90 天追蹤</span></div>
</div></section>

<section class="alt" id="services"><div class="wrap">
<p class="eyebrow">SERVICES</p>
<h2>六個模組，依你的階段組合</h2>
<p class="sub">第一次開業、展第二間店、搬遷或換系統，都可以只挑需要的部分。</p>
<div class="svc-grid">{cards}</div>
</div></section>

<section><div class="wrap">
<p class="eyebrow">TIMELINE</p>
<h2>開業 13 個階段，我們幫你排在同一張時程表上</h2>
<p class="sub">設計、設立申請、設備採購與人員招募常常需要同步推進，不是照順序一件做完再做下一件。</p>
<div class="tl-grid">{timeline}</div>
<p class="note" style="margin-top:24px">時程為一般參考，實際依地區、建物條件與主管機關作業時間而不同。</p>
</div></section>

<section class="alt"><div class="wrap">
<p class="eyebrow">SCOPE</p>
<h2>我們的角色</h2>
<p class="sub">我們不是裝潢統包，也不取代建築師、會計師或法律顧問；我們把「真正需要的條件」提前說清楚，降低完工後返工與開幕後補件的風險。</p>
<div class="scope">
<div class="scope-col"><h3>Olimedi 可協助</h3><ul class="check">{"".join(f"<li>{x}</li>" for x in CAN)}</ul></div>
<div class="scope-col pro"><h3>需由專業單位／院所確認</h3><ul>{"".join(f"<li>{x}</li>" for x in PRO)}</ul></div>
</div>
</div></section>

<section><div class="wrap center">
<p class="eyebrow">HOW IT WORKS</p>
<h2>四步驟開始</h2>
<p class="sub" style="margin-left:auto;margin-right:auto">不用填表單、不用留電話，在 LINE 上跟 Oliver 說一聲就好。</p>
<div class="steps steps-4" style="text-align:left">{flow}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="lead-magnet">
<div>
<p class="eyebrow">FREE CHECKLIST</p>
<h2 style="font-size:clamp(24px,3vw,32px)">先領一份「診所開業 13 步驟檢核表」</h2>
<p>每個階段要確認的事、負責人與期限欄位，開業前 14 天倒數表也在裡面。加 LINE 輸入「開業」就會自動傳給你，完全免費。</p>
<a class="btn btn-line" href="{LINE}" target="_blank" rel="noopener">{AV}加 LINE 輸入「開業」領取</a>
</div>
<div class="lm-art"><div class="lm-sheet"><b></b><b></b><b></b><b></b><b></b><b></b></div></div>
</div>
</div></section>

<section><div class="wrap" style="max-width:860px">
<p class="eyebrow">FAQ</p>
<h2>常見問題</h2>
<div style="margin-top:20px">{faq_html(FAQ)}</div>
<p class="note" style="margin-top:28px">本頁服務內容為開業流程與管理協助，不構成法律、稅務、建築、消防、放射、健保或醫療專業意見；各項申請文件與審查方式以主管機關最新公告為準。</p>
</div></section>

{OLIVER_BAND("準備開業？先跟 Oliver 聊聊","告訴 Oliver 你的科別、預計開業時間與目前階段，我們安排約 40 分鐘的免費開業諮詢，一起看看哪些事該先做。")}
'''
    svc={"@context":"https://schema.org","@type":"Service","name":"診所開業整合服務","serviceType":"Clinic launch consulting","provider":{"@type":"Organization","name":"Olimedi 奧里醫療資訊"},"areaServed":"TW","url":f"{SITE}/services.html","description":"醫療院所開業行政代辦、開業前評估、人事制度、耗材庫存、資訊系統規劃與開業後 90 天追蹤。"}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首頁","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"診所開業整合服務","item":f"{SITE}/services.html"}]}
    html=page("services.html","診所開業整合服務｜行政代辦、人事制度、耗材庫存、資訊系統規劃｜Olimedi 奧里",
              "醫療院所開業整合服務：從公會入會到健保特約的行政代辦、開業前評估、人事與考勤制度、耗材庫存建置、資訊系統規劃與開業後 90 天追蹤。各科別診所適用，模組可單獨委託。",
              body,"services.html",[svc,bc,faq_ld(FAQ)])
    if preview: html=html.replace('<meta name="viewport"','<meta name="robots" content="noindex,nofollow">\n<meta name="viewport"',1)
    open("services.html","w").write(html)
