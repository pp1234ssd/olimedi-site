# -*- coding: utf-8 -*-
# 開業整合服務頁（services.html）。由 build.py 匯入；需要 page / cta / OLIVER_BAND / LINE / SITE / faq_html / faq_ld。

def build(page, cta, OLIVER_BAND, LINE, SITE, faq_html, faq_ld, AV, preview=True):
    # ---- 六大服務 ----
    # 主服務：開業代辦（含地點評估）
    AGENCY=[("0","開業地點評估（含）","簽約前先到現場看：平面配置能不能符合當地衛生主管機關規範、診間與動線、周邊商圈；建築物評估與相關諮詢可在群組討論，需到場勘查另計車馬費。"),
            ("1","牙醫師／醫師公會送件",""),("2","衛生主管機關開業申請送件",""),("3","衛生局現勘陪同檢查",""),
            ("4","領取開業執照與執業執照",""),("5","醫事機構憑證 IC 卡、醫事人員憑證 IC 卡申請",""),
            ("6","國稅局統一編號配書",""),("7","勞健保投保單位設立與初次人員加保",""),
            ("8","健保醫療網（VPN）申請",""),("9","健保特約診所申請","")]
    SERVICES=[
     ("02","人事制度建置","開業前先把排班、薪資、請假寫清楚，省掉之後的爭議。",
      ["人力配置與排班規劃（含四週變形工時）","勞動契約、工作規則與員工手冊","Oli 考勤管理系統導入與打卡設定","30／60／90 天考核與教育訓練節奏"],"tag-s"),
     ("03","耗材與庫存建置","第一批不要什麼都先買；先把 A 類安全庫存顧好。",
      ["依科別建立耗材分類架構與首批採購清單","安全庫存、ABC 分級與盤點頻率","效期與批號追蹤制度","Oli 庫存管理系統導入與供應商對帳"],"tag-g"),
     ("04","資訊系統規劃","網路、弱電、診所系統與備份，一次規劃好，不要開幕後再拉線。",
      ["診間網路點位、有線為主與雙線備援","診所系統、健保 VPN 與讀卡設備串接","影像、備份與權限規劃","開幕前掛號→看診→收費→申報全流程試跑"],"tag-b"),
     ("05","開業後 90 天追蹤","開幕不是終點，前 90 天把「能看診」變成「能穩定經營」。",
      ["Day 7／30／90 固定回顧會議","營運儀表板：初診、回診、No-show、耗材成本","申報核減追蹤與流程修正","人力、設備與擴充決策建議"],"tag-g"),
    ]
    agency_rows="".join(f'<div class="ag-row{" ag-0" if n=="0" else ""}"><div class="ag-n">{"評估" if n=="0" else n}</div><div><div class="ag-t">{t}</div>{f"<div class=ag-d>{d}</div>" if d else ""}</div></div>' for n,t,d in AGENCY)
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
    FLOW=[("01","加 LINE 跟 Oliver 說","告訴我們科別、開業地點、預計開業時間與目前階段。"),
          ("02","地點評估與訪談","先看地點與平面圖能不能順利變成診所，再一起列出要辦的項目與時程。"),
          ("03","報價與簽約","書面報價單列清楚代辦範圍、不含的規費與付款方式；確認後支付訂金開始。"),
          ("04","送件、領照、特約","公會、衛生局、執照、憑證、統編、勞健保、醫療網到健保特約，每週回報進度。")]
    flow="".join(f'<div class="step"><div class="n">{n}</div><h3>{h}</h3><p>{p}</p></div>' for n,h,p in FLOW)

    FAQ=[("哪些科別可以用這項服務？","西醫、牙醫、中醫、復健、醫美等各類醫療院所都可以。行政流程大致相同，差異在設備、感控與耗材，我們會依科別調整清單。"),
         ("只需要代辦，不需要其他模組可以嗎？","可以。開業代辦可以單獨委託；人事、耗材、資訊系統與 90 天追蹤是加值模組，需要再加。"),
         ("代辦費包含哪些、不包含哪些？","包含地點評估與上面列的 9 項送件、陪同與申請作業。不包含各機關規費（竣工圖申請、公會費用、執照規費等），這些實報實銷；需要額外到場勘查時依趟次計車馬費，會事前告知。"),
         ("我需要準備什麼？","委託書與各項申請的必備文件（我們會給清單）。文件齊全與現場平面配置符合當地衛生主管機關規範，是時程能不能照排的關鍵。"),
         ("已經開業的診所可以嗎？","可以。人事制度、耗材庫存、資訊系統與營運追蹤都適用既有診所；很多診所是在換系統或展第二間店時找我們。"),
         ("你們會幫忙裝潢或找設計師嗎？","不會。建築、裝潢、消防、放射與稅務需由各專業單位負責；我們的角色是把這些單位之間的交界面與時程串起來，並處理行政、人事、耗材與資訊系統。"),
         ("費用怎麼算？","代辦費為固定一筆，依地區與科別報價；加值模組另計。訪談後提供書面報價單，沒有隱藏費用。")]

    body=f'''
<section class="hero simple" style="padding-bottom:40px"><div class="ring-bg"></div><div class="wrap">
<p class="crumb"><a href="index.html">首頁</a> / 開業整合服務</p>
<p class="eyebrow">CLINIC LAUNCH</p>
<h1>診所開業整合服務</h1>
<p class="lead" style="max-width:36em">從開業地點評估、公會送件、衛生局現勘到健保特約，開業必備的許可與執照由我們跑；人事、耗材與資訊系統也能一起建好。開業最容易出錯的，是大家「以為對方會處理」的交界面。</p>
<div class="cta-row">{cta("問 Oliver・預約開業諮詢")}<a class="btn btn-ghost" href="#services">看代辦範圍</a></div>
<div class="trust"><span>各科別醫療院所適用</span><span>含開業地點評估</span><span>規費實報實銷、無隱藏費用</span></div>
</div></section>

<section class="alt" id="services"><div class="wrap">
<p class="eyebrow">CORE SERVICE</p>
<h2>開業代辦：地點評估到健保特約，一條線跑完</h2>
<p class="sub">取得開業必備的許可、執照與合法合規文件。你準備委託書與資料，送件、現勘陪同、領照與申請由我們跑，每週回報進度。</p>
<div class="agency">
<div class="ag-list">{agency_rows}</div>
<div class="ag-side">
<h3>費用怎麼算</h3>
<ul class="check">
<li>代辦費為固定一筆，依地區與科別報價，訪談後出書面報價單</li>
<li>不含規費（例如竣工圖申請、公會異動、執照規費等），實報實銷</li>
<li>確定委託時支付訂金，完成後付尾款</li>
<li>建築物評估與諮詢可線上討論；需另外到場勘查時依趟次計車馬費，事前告知</li>
</ul>
<p class="ag-note">診所需依要求提供委託書與必備文件；若因文件延遲或現場平面配置不符當地衛生主管機關規範而延誤，時程需重新安排。</p>
{cta("問 Oliver・索取代辦報價")}
</div>
</div>
</div></section>

<section><div class="wrap">
<p class="eyebrow">ADD-ON MODULES</p>
<h2>開業之後要跑得順，還有四件事</h2>
<p class="sub">可以跟代辦一起委託，也可以單獨委託；展第二間店、搬遷或換系統的既有診所也適用。</p>
<div class="svc-grid">{cards}</div>
</div></section>

<section class="alt"><div class="wrap">
<p class="eyebrow">TIMELINE</p>
<h2>開業 13 個階段，我們幫你排在同一張時程表上</h2>
<p class="sub">設計、設立申請、設備採購與人員招募常常需要同步推進，不是照順序一件做完再做下一件。</p>
<div class="tl-grid">{timeline}</div>
<p class="note" style="margin-top:24px">時程為一般參考，實際依地區、建物條件與主管機關作業時間而不同。</p>
</div></section>

<section><div class="wrap">
<p class="eyebrow">SCOPE</p>
<h2>我們的角色</h2>
<p class="sub">我們不是裝潢統包，也不取代建築師、會計師或法律顧問；我們把「真正需要的條件」提前說清楚，降低完工後返工與開幕後補件的風險。</p>
<div class="scope">
<div class="scope-col"><h3>Olimedi 可協助</h3><ul class="check">{"".join(f"<li>{x}</li>" for x in CAN)}</ul></div>
<div class="scope-col pro"><h3>需由專業單位／院所確認</h3><ul>{"".join(f"<li>{x}</li>" for x in PRO)}</ul></div>
</div>
</div></section>

<section class="alt"><div class="wrap center">
<p class="eyebrow">HOW IT WORKS</p>
<h2>四步驟開始</h2>
<p class="sub" style="margin-left:auto;margin-right:auto">不用填表單、不用留電話，在 LINE 上跟 Oliver 說一聲就好。</p>
<div class="steps steps-4" style="text-align:left">{flow}</div>
</div></section>

<section><div class="wrap">
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
    svc={"@context":"https://schema.org","@type":"Service","name":"診所開業整合服務","serviceType":"Clinic launch consulting","provider":{"@type":"Organization","name":"Olimedi 奧里醫療資訊"},"areaServed":"TW","url":f"{SITE}/services.html","description":"醫療院所開業代辦：開業地點評估、公會送件、衛生局現勘、開業執照、醫事憑證、統一編號、勞健保、健保醫療網與健保特約申請；另有人事制度、耗材庫存、資訊系統規劃與開業後 90 天追蹤。"}
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"首頁","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"診所開業整合服務","item":f"{SITE}/services.html"}]}
    html=page("services.html","診所開業代辦｜地點評估、公會送件、衛生局現勘到健保特約｜Olimedi 奧里",
              "醫療院所開業代辦：開業地點評估、公會送件、衛生局現勘陪同、開業執照、醫事憑證、統一編號、勞健保、健保醫療網到健保特約申請，一條線跑完；另可加人事制度、耗材庫存、資訊系統規劃與開業後 90 天追蹤。各科別診所適用。",
              body,"services.html",[svc,bc,faq_ld(FAQ)])
    if preview: html=html.replace('<meta name="viewport"','<meta name="robots" content="noindex,nofollow">\n<meta name="viewport"',1)
    open("services.html","w").write(html)
