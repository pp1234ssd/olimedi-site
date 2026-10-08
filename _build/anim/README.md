# Oliver 情境劇短影片（IG Reels / FB Reels / Threads）

- `oliver.py`：Oliver 全身 Q 版向量零件與姿勢（wave / tablet / thumb / stand / point）。`python3 _build/anim/oliver.py` 會輸出 `img/oliver/*.svg`。
- `skit.py`：固定分鏡模板（13 秒、9:16、無聲、不露臉）：人員抱怨 → Oliver 出場回應 → 平板畫面解決 → 人員鬆口氣 → 結尾卡。
- `specs/*.json`：每支影片只要寫一個 JSON（欄位見 skit.py 開頭）。
- 產生：`python3 _build/anim/skit.py _build/anim/specs/04-schedule.json out.mp4`，同時產生 `out_cover.png` 封面。
- 需要：`pip install playwright`（Chromium）與 ffmpeg。

規則：台詞口語、2 行內、每行 ≤ 12 字；不用絕對用語（保證／一定／完全／防止）；法規數字只寫網站文章有官方來源的；診所一律「Oli 診所」；畫面是示意，不說「所有」。

## Reels 知識短片（reel.py，IG 固定用這個）
- `reel.py`：約 25 秒、30fps、9:16，六段固定分鏡（hook／calendar／compare／numbers／warn／end），每段有彈跳、甩入、蓋章、數字滾動、斜向轉場與畫面震動；附靜音音軌，上傳時在 IG App 內選音樂。
- 產生：`python3 _build/anim/reel.py _build/anim/specs/reel-01-national-holiday.json out.mp4`（同時輸出 `out_cover.png`）。
- 檢查關鍵影格：`python3 _build/anim/reel.py spec.json 輸出資料夾 --frames 1.5,6,12,17,20,23`。
- 文字放安全區（y 260–1560），hook 大標每行 ≤ 8 字、卡片大字 ≤ 8 字。
