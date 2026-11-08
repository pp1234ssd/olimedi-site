# -*- coding: utf-8 -*-
"""Olimedi 診所開業 13 步驟檢核表（Excel）。python3 build_launch_xlsx.py out.xlsx"""
import sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule, CellIsRule
from openpyxl.utils import get_column_letter as L

G="2E7D5B"; INK="17332B"; LEAF="7BB661"; SUN="F2A541"; MINT="E3F1E8"; PEACH="FDEBD3"; CREAM="F7F5EE"; LINE="E6E1D3"; MUTE="5D6F68"; BLUE="0000FF"
F=lambda **k: Font(name="Arial", **k)
thin=Side(style="thin",color=LINE); B=Border(left=thin,right=thin,top=thin,bottom=thin)
fill=lambda c: PatternFill("solid",fgColor=c)
WRAP=Alignment(wrap_text=True,vertical="top"); CEN=Alignment(horizontal="center",vertical="center",wrap_text=True)

def title(ws,t,sub):
    ws["A1"]=t; ws["A1"].font=F(size=15,bold=True,color=G)
    ws["A2"]=sub; ws["A2"].font=F(size=10,color=MUTE)
def hdr(ws,row,cols,widths):
    for i,(c,w) in enumerate(zip(cols,widths),1):
        cell=ws.cell(row=row,column=i,value=c); cell.font=F(bold=True,color="FFFFFF"); cell.fill=fill(G); cell.alignment=CEN; cell.border=B
        ws.column_dimensions[L(i)].width=w
    ws.row_dimensions[row].height=24
def legend(ws,row,text="填寫說明：黃底欄位請自行填寫（負責人、日期、狀態、備註）；其他欄位為公式或固定內容，請勿更動。狀態請用下拉選單選擇。"):
    ws.cell(row=row,column=1,value=text).font=F(size=10,color=MUTE)

STEPS=[
 ("01","開業策略","定位＋預算＋時程",["出資比例、決策權、薪酬／分紅與退場條件白紙黑字（合夥必做）","目標客群與主力療程定位，決定裝潢、設備與人力規模","診間數、人力與未來擴充幅度一起估","總預算拆成：裝潢、設備、器械耗材、資訊、押租、人事、行銷、預備金；保留開業初期週轉金","設定簽約、設計定稿、工程、設備下單、驗收、訓練、試營運、開幕的倒推日期"]),
 ("02","店面與法規可行性","可開業店面＋初勘",["商圈：交通、停車、人流路徑、同業密度、轉診來源","可使用坪數（扣掉樑柱、樓梯、廁所、機房）","土地分區、建物使用類組與用途是否能設立診所（簽約前確認）","水、電、空壓／吸引、網路、排水的設置可行性（最好請設備與工程一起到場）","搬運路徑：電梯、門寬、轉角、樓層","未來擴充的管線與電力預留"]),
 ("03","空間與工程整合","可施工圖＋點位簽認",["平面、立面、系統圖用同一版圖面核對","診療椅／設備實機放樣：操作位置、助理位置、燈臂、顯微鏡干涉","每診間列出水、排水、空壓、吸引、電壓、接地、網路、控制線與完成面高度","消毒區「髒→清洗→包裝→滅菌→儲存」單向動線","大型設備（影像、滅菌、空壓、伺服器）施工前確認安裝條件","工程報價逐項列明；所有追加減以書面確認"]),
 ("04","品牌與對外溝通","品牌資產＋合規素材",["診所名稱符合醫療機構命名規範，同步確認網址、社群帳號與商標","字體、色彩、Logo、文案規則；官網、名片、制服、招牌一致","招牌尺寸、設置與內容限制先確認；院內導視清楚","官網、網域、Google 商家、電話、LINE／預約入口、社群帳號權限由診所持有","對外素材避免療效保證、比較、誇大或不當招攬；指定合規審核人","簡訊、預約提醒、術前術後說明、同意書語氣與版本一致"]),
 ("05","大型設備選購","設備清單＋交期＋驗收",["影像設備：空間、網路、工作站、軟體授權、備份、維護","診療設備：臨床需求、人體工學、管線與維修空間","消毒設備：依每日器械周轉量估算，不只看容量","IT／弱電／診所系統：掛號、病歷、收費、健保、電話、監視、網路、備份視為一套","比價同時比保固、工程師反應時間、零件供應、停機替代方案與教育訓練","採購單寫清楚交期、安裝條件、附件、序號、保固起算與驗收標準"]),
 ("06","人事制度","人力配置＋制度",["櫃台、醫師、諮詢、助理、流動／消毒區分工；指定感控、設備、庫存、資訊負責人","依診間數、醫師班表、四手操作需求與尖峰反推人力","招募加入情境面試：接預約電話、遞器械、面對抱怨","工時、休假、排班、薪資、加班、獎金、請假、保密寫成員工手冊；到職即完成投保","薪酬、試用期目標、30／60／90 天考核與晉升路徑","核心人員提前到職，保留設備教育、SOP 與模擬演練時間"]),
 ("07","教育訓練","能上線的人員",["新進助理、進階助理、櫃台、諮詢師與醫師分別設定必修能力與時限","用診所自己的設備與空間製作操作卡、短影片與流程圖","每台大型設備完成操作、清潔、異常判讀、緊急停止與聯絡方式教育並留簽名紀錄","情境演練：預約、報到、看診、影像、治療、消毒、收費與突發狀況跑一次","30／60／90 天考核留紀錄與下一階段目標","每台設備指定主要負責人與備援"]),
 ("08","器械耗材採購與管理","首批量＋庫存制度",["依區域、科別、站別建立耗材分類架構，再列採購清單","品牌、品名、規格、包裝、供應商與可替代品寫清楚","首批採購量依預計診量與消耗週期估算，建議分兩階段採購","關鍵耗材至少準備第二供應來源","週期盤點、ABC 價值分類、先到期先用（FEFO）出入庫","A 類（缺了不能看診）安全庫存先顧好"]),
 ("09","診所 SOP 與感控","可執行流程文件",["櫃台、臨床、諮詢、消毒室分開診前／診中／診後責任與交接","每日開診／收診點檢：空壓、吸引、治療椅、水路、電腦、網路、滅菌設備","掛號、影像、看診、收費、預約、回診、同意書、轉診與帳務流程文件","器械從污染回收、清洗、包裝、滅菌到儲存批次可追溯，保存滅菌監測紀錄","設備故障與緊急 SOP：第一線排除、拍照、錯誤碼、聯絡設備商；停水停電備案","SOP 標註版本與修訂日，固定每季檢視"]),
 ("10","診所設立申請","證照／代號／帳戶",["加入所在地公會並取得所需證明","向衛生主管機關送件、現勘、取得開業執照與執業執照","國稅局統一編號、稅籍；診所與私人帳戶分離","醫事機構憑證 IC 卡、醫事人員憑證 IC 卡","勞健保投保單位設立、初次人員加保","健保醫療網（VPN）申請與健保特約簽約","畫出申請項目的前後依賴圖，與工程進度同步倒排"]),
 ("11","健保申報／抽審","可申報＋可備查",["建立月申報流程、截止日、負責人與覆核機制","確認電子病歷系統的簽章、修改軌跡、備份與權限","病歷、影像、處置與申報內容一致且完整，指定抽審資料負責人","指定窗口追蹤新特約指標與規範更新","核減與申復流程：追原因、回頭修正病歷與流程","正式開業前用假資料完整跑一次掛號→讀卡→病歷→處置→收費→申報，並測試斷網／設備／資料備援"]),
 ("12","試營運與開幕","低風險上線",["正式開幕前安排 3～7 天低量門診，測掛號、影像、診療、消毒、收費、預約、健保與器械周轉","開幕活動流程與醫療動線分開，感控與隱私不能因熱鬧被犧牲","邀請名單以長期互動者為主：在地社群、轉診醫師、合作夥伴","Google 商家、官網、社群、電話、導航與預約資訊在活動前核對","當日指定問題紀錄人，閉診後立即檢討","開幕文案、照片、優惠或活動內容發布前做醫療廣告與個資／肖像權檢查"]),
 ("13","正式營運與追蹤","營運儀表板",["開幕前最後完整演練；開業後前 3 個月保留短週晨會與固定週檢討","固定追蹤：初診數、回診率、No-show、診次、療程結構、醫師／診間產能、耗材與客訴","Day 7 抓 bug、Day 30 看流程、Day 90 看效率與財務、Day 180 決定擴充","設備保養週期、故障、到場時間、零件與教育紀錄留存","客訴與安全事件：紀錄、原因分析、處理、回覆與預防措施形成閉環","增加醫師、助理、診次、設備前，先看利用率、等待時間、空間與現金流"]),
]
PHASES={"01":"T-6～8 個月","02":"T-6～8 個月","03":"T-6～8 個月","04":"T-4～6 個月","05":"T-4～6 個月","06":"T-2～3 個月","07":"T-2～3 個月","08":"T-2～3 個月","09":"T-2～3 個月","10":"T-4～6 個月","11":"T-14 天～開幕","12":"T-14 天～開幕","13":"開幕後"}
AGENCY=[("0","開業地點評估（含）"),("1","公會送件"),("2","衛生主管機關開業申請送件"),("3","衛生局現勘陪同檢查"),("4","領取開業執照與執業執照"),("5","醫事機構憑證 IC 卡、醫事人員憑證 IC 卡申請"),("6","國稅局統一編號配書"),("7","勞健保投保單位設立與初次人員加保"),("8","健保醫療網（VPN）申請"),("9","健保特約診所申請")]
COUNTDOWN=[("D-14","工程完成面總驗收；缺失清單定責任人與完成日"),("D-12","水／電／氣／吸引／網路點位實測；機房試運轉"),("D-10","大型設備進場安裝；序號與附件點收"),("D-9","影像／電腦／診所系統／網路／備份串接測試"),("D-8","器械耗材首批到貨、分類、效期與安全庫存建立"),("D-7","大型設備操作與日常保養教育；負責人指定"),("D-6","消毒室與感控全流程實作；滅菌追溯紀錄測試"),("D-5","掛號→影像→看診→收費→預約→申報全流程演練"),("D-4","緊急情境演練：停電、停水、設備故障、病人突發狀況"),("D-3","試營運：低量真實病人；記錄所有問題"),("D-2","修正試營運問題；官網／地圖／電話／預約資訊核對"),("D-1","水電氣設備總點檢、清潔、耗材補滿、隔日人力確認"),("D-Day","晨會 10 分鐘；指定問題紀錄人，當日閉診後立即檢討"),("D+1","整理開幕第一天問題，48 小時內完成高風險修正")]

def build(out):
    wb=Workbook()
    # ---- 說明
    ws=wb.active; ws.title="使用說明"
    title(ws,"Olimedi 奧里醫療資訊｜診所開業 13 步驟檢核表","適用各科別醫療院所（西醫、牙醫、中醫、復健、醫美）。先排順序、再指定負責人與期限，每週固定更新一次。")
    rows=["怎麼使用",
    "1. 到「總覽」分頁：每個階段填負責人、預計完成日，依進度選狀態；完成度與成熟度分數會自動算。",
    "2. 到「檢核明細」分頁：13 個階段共 76 個檢核項目，逐項勾選狀態、填負責人與備註。",
    "3. 到「開業代辦」分頁：若委託 Olimedi 代辦，這裡追蹤地點評估與 9 項送件／申請的進度。",
    "4. 到「開幕倒數」分頁：開幕前 14 天每天該做的事，填正式開幕日後日期自動帶出。",
    "",
    "三個原則",
    "・13 個步驟是管理框架，不是只能串行：設計、設立申請、設備採購與人員招募常需同步推進。",
    "・每一步都要有「負責人＋期限」，不把進度留在群組訊息裡。",
    "・正式開幕前一定安排試營運，先用低量病人測流程，再正式放大。",
    "",
    "免責提醒",
    "本檢核表為診所開業流程與管理工具，不構成法律、稅務、建築、消防、放射、健保或醫療專業意見；各項申請文件、審查方式及法規可能更新，實際辦理請以主管機關最新公告為準。",
    "",
    "想把排班、打卡、特休、庫存也一起建好？加 LINE 搜尋 @336appfx，輸入「Demo」預約免費展示；輸入「排班表」「盤點表」「特休表」可領其他範本。olimedi.com"]
    for i,t in enumerate(rows,4):
        c=ws.cell(row=i,column=1,value=t); c.font=F(size=13,bold=True) if t in("怎麼使用","三個原則","免責提醒") else F(size=11); c.alignment=Alignment(wrap_text=True,vertical="top")
    ws.column_dimensions["A"].width=110
    # ---- 總覽
    ws=wb.create_sheet("總覽")
    title(ws,"13 STEPS｜總覽與進度追蹤","黃底欄位請填寫。完成度依「檢核明細」勾選自動計算；成熟度請依 0～3 分自評。")
    hdr(ws,4,["STEP","階段","關鍵產出","建議時程","負責人","預計完成日","狀態","檢核完成度","成熟度自評 (0-3)","備註"],[7,22,22,16,12,14,12,14,16,30])
    dvS=DataValidation(type="list",formula1='"未開始,進行中,已完成"',allow_blank=True); ws.add_data_validation(dvS)
    dvM=DataValidation(type="list",formula1='"0,1,2,3"',allow_blank=True); ws.add_data_validation(dvM)
    for i,(n,name,outp,items) in enumerate(STEPS):
        r=5+i
        vals=[n,name,outp,PHASES[n],"","", "未開始" if i else "進行中", None, 1 if i==0 else "", "合夥條款待律師確認" if i==0 else ""]
        for c,v in enumerate(vals,1):
            cell=ws.cell(row=r,column=c,value=v); cell.font=F(size=10); cell.border=B; cell.alignment=Alignment(vertical="center",wrap_text=True,horizontal="center" if c in(1,4,6,7,8,9) else "left")
            if c in(5,6,7,9,10): cell.fill=fill("FFF9DB"); cell.font=F(size=10,color=BLUE)
        ws.cell(row=r,column=8,value=f'=IFERROR(COUNTIFS(檢核明細!$A:$A,A{r},檢核明細!$E:$E,"已完成")/COUNTIF(檢核明細!$A:$A,A{r}),0)').number_format="0%"
        ws.cell(row=r,column=6).number_format="yyyy/mm/dd"
        dvS.add(ws.cell(row=r,column=7)); dvM.add(ws.cell(row=r,column=9))
        ws.row_dimensions[r].height=30
    last=5+len(STEPS)-1
    r=last+2
    ws.cell(row=r,column=2,value="整體檢核完成度").font=F(bold=True); ws.cell(row=r,column=8,value=f'=IFERROR(COUNTIF(檢核明細!$E:$E,"已完成")/COUNTA(檢核明細!$C$5:$C$200),0)').number_format="0%"; ws.cell(row=r,column=8).font=F(bold=True)
    ws.cell(row=r+1,column=2,value="成熟度總分 / 39").font=F(bold=True); ws.cell(row=r+1,column=9,value=f"=SUM(I5:I{last})").font=F(bold=True)
    ws.cell(row=r+2,column=2,value="成熟度 %").font=F(bold=True); ws.cell(row=r+2,column=9,value=f"=I{r+1}/39").number_format="0%"; ws.cell(row=r+2,column=9).font=F(bold=True)
    ws.cell(row=r+3,column=2,value="目前階段判讀").font=F(bold=True)
    ws.cell(row=r+3,column=9,value=f'=IF(I{r+2}<=0.25,"概念期：定位、資金、店面與時程仍在形成；先避免大額不可逆決策",IF(I{r+2}<=0.5,"規劃期：店面與設計開始確定；優先完成設備放樣與機電介面",IF(I{r+2}<=0.75,"施工期：工程與採購同步；把封板前點位複核、交期與進場條件盯緊",IF(I{r+2}<=0.9,"上線準備期：安裝、教育、系統串接、耗材與 SOP 進入壓力測試","開幕就緒：進入試營運與問題閉環，準備正式放大營運"))))').font=F(size=10)
    ws.merge_cells(start_row=r+3,start_column=9,end_row=r+3,end_column=10); ws.cell(row=r+3,column=9).alignment=WRAP; ws.row_dimensions[r+3].height=40
    legend(ws,r+5)
    for row in range(5,last+1):
        ws.conditional_formatting.add(f"G{row}",CellIsRule(operator="equal",formula=['"已完成"'],fill=fill(MINT)))
        ws.conditional_formatting.add(f"G{row}",CellIsRule(operator="equal",formula=['"進行中"'],fill=fill(PEACH)))
    ws.freeze_panes="C5"
    # ---- 檢核明細
    ws=wb.create_sheet("檢核明細")
    title(ws,"13 STEPS｜檢核明細","每一項選狀態、填負責人與備註。狀態為「已完成」時會回寫到「總覽」的完成度。")
    hdr(ws,4,["STEP","階段","檢核項目","負責人","狀態","期限","備註"],[7,18,70,12,12,14,30])
    dv=DataValidation(type="list",formula1='"未開始,進行中,已完成,不適用"',allow_blank=True); ws.add_data_validation(dv)
    r=5
    for n,name,outp,items in STEPS:
        for j,it in enumerate(items):
            vals=[n,name,it,"","未開始","",""]
            if n=="01" and j==0: vals=[n,name,it,"王院長","已完成","","合夥契約 10/20 簽妥（範例）"]
            for c,v in enumerate(vals,1):
                cell=ws.cell(row=r,column=c,value=v); cell.font=F(size=10); cell.border=B; cell.alignment=Alignment(vertical="center",wrap_text=True,horizontal="center" if c in(1,5,6) else "left")
                if c in(4,5,6,7): cell.fill=fill("FFF9DB"); cell.font=F(size=10,color=BLUE)
            ws.cell(row=r,column=6).number_format="yyyy/mm/dd"; dv.add(ws.cell(row=r,column=5)); r+=1
    ws.conditional_formatting.add(f"E5:E{r}",CellIsRule(operator="equal",formula=['"已完成"'],fill=fill(MINT)))
    ws.conditional_formatting.add(f"E5:E{r}",CellIsRule(operator="equal",formula=['"進行中"'],fill=fill(PEACH)))
    legend(ws,r+1); ws.freeze_panes="D5"; ws.auto_filter.ref=f"A4:G{r-1}"
    # ---- 開業代辦
    ws=wb.create_sheet("開業代辦")
    title(ws,"開業代辦進度｜地點評估到健保特約","委託 Olimedi 代辦時使用。診所端需準備委託書與各項必備文件（清單由代辦窗口提供）。")
    hdr(ws,4,["項次","代辦項目","診所需提供","送件日","完成日","狀態","備註"],[7,40,34,14,14,12,30])
    need={"0":"平面圖、地址、科別與預計診間數","1":"醫師證書、身分證、照片、入會申請書","2":"平面圖、執照影本、負責醫師資料","3":"現場配合開放、設備到位","4":"衛生局通知領照文件","5":"機構／人員申請表、證件","6":"開業執照、負責人證件、印章","7":"統編、員工名冊、到職資料","8":"統編、機構代號、網路環境","9":"開業執照、統編、健保專用帳戶"}
    dv=DataValidation(type="list",formula1='"未開始,準備文件,已送件,審查中,已完成"',allow_blank=True); ws.add_data_validation(dv)
    for i,(n,t) in enumerate(AGENCY):
        r=5+i; vals=["評估" if n=="0" else n,t,need[n],"","", "已完成" if n=="0" else "未開始",""]
        for c,v in enumerate(vals,1):
            cell=ws.cell(row=r,column=c,value=v); cell.font=F(size=10); cell.border=B; cell.alignment=Alignment(vertical="center",wrap_text=True,horizontal="center" if c in(1,4,5,6) else "left")
            if c in(4,5,6,7): cell.fill=fill("FFF9DB"); cell.font=F(size=10,color=BLUE)
        for c in(4,5): ws.cell(row=r,column=c).number_format="yyyy/mm/dd"
        dv.add(ws.cell(row=r,column=6)); ws.row_dimensions[r].height=30
    last=5+len(AGENCY)-1
    ws.cell(row=last+2,column=2,value="已完成項目").font=F(bold=True); ws.cell(row=last+2,column=6,value=f'=COUNTIF(F5:F{last},"已完成")&" / "&COUNTA(B5:B{last})').font=F(bold=True)
    ws.cell(row=last+4,column=1,value="費用說明：代辦費為固定一筆、依地區與科別報價；不含各機關規費（實報實銷）；確定委託支付訂金、完成付尾款；需到場勘查依趟次計車馬費並事前告知。若文件延遲或現場平面配置不符當地衛生主管機關規範，時程需重新安排。").font=F(size=10,color=MUTE)
    ws.merge_cells(start_row=last+4,start_column=1,end_row=last+4,end_column=7); ws.cell(row=last+4,column=1).alignment=WRAP; ws.row_dimensions[last+4].height=44
    ws.conditional_formatting.add(f"F5:F{last}",CellIsRule(operator="equal",formula=['"已完成"'],fill=fill(MINT)))
    legend(ws,last+6)
    # ---- 開幕倒數
    ws=wb.create_sheet("開幕倒數")
    title(ws,"開業前 14 天倒數表","填入正式開幕日（黃底），各日日期自動帶出；完成後選「完成」。")
    ws["A4"]="正式開幕日"; ws["A4"].font=F(bold=True); ws["B4"]="2027/3/1";
    from datetime import date
    ws["B4"]=date(2027,3,1); ws["B4"].number_format="yyyy/mm/dd"; ws["B4"].fill=fill("FFF9DB"); ws["B4"].font=F(color=BLUE,bold=True)
    ws["D4"]="（範例日期，請改成你的開幕日）"; ws["D4"].font=F(size=10,color=MUTE)
    hdr(ws,6,["時間","日期","關鍵任務","負責人","完成","備註"],[9,13,64,12,10,30])
    dv=DataValidation(type="list",formula1='"完成,未完成"',allow_blank=True); ws.add_data_validation(dv)
    for i,(d,t) in enumerate(COUNTDOWN):
        r=7+i; off=0 if d=="D-Day" else (1 if d=="D+1" else -int(d[2:]))
        vals=[d,f"=$B$4+({off})",t,"","未完成",""]
        for c,v in enumerate(vals,1):
            cell=ws.cell(row=r,column=c,value=v); cell.font=F(size=10); cell.border=B; cell.alignment=Alignment(vertical="center",wrap_text=True,horizontal="center" if c in(1,2,5) else "left")
            if c in(4,5,6): cell.fill=fill("FFF9DB"); cell.font=F(size=10,color=BLUE)
        ws.cell(row=r,column=2).number_format="yyyy/mm/dd"; dv.add(ws.cell(row=r,column=5))
    last=7+len(COUNTDOWN)-1
    ws.cell(row=last+2,column=3,value="已完成").font=F(bold=True); ws.cell(row=last+2,column=5,value=f'=COUNTIF(E7:E{last},"完成")&" / "&COUNTA(A7:A{last})').font=F(bold=True)
    ws.conditional_formatting.add(f"E7:E{last}",CellIsRule(operator="equal",formula=['"完成"'],fill=fill(MINT)))
    legend(ws,last+4)
    for w in wb.worksheets: w.sheet_view.showGridLines=False
    wb.save(out)
if __name__=="__main__": build(sys.argv[1])
