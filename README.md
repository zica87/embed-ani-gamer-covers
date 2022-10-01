~~其實我還沒想好這程式要叫什麼名字~~

## 功能
給定 sn 碼或網址，即可：
- 下載動畫瘋的封面／視覺圖。
- 將動畫瘋的封面／視覺圖嵌入為 MP4 檔的封面（縮圖）。
- 輸出[動畫資訊](#動畫資訊格式--內容)。

## 目錄
- [安裝說明](#安裝說明)
  - [執行檔](#執行檔)
  - [直接執行 Python 原始碼](#直接執行-python-原始碼)
- [使用說明](#使用說明)
  - [Windows、Linux、Android](#windowslinuxandroid)
  - [引數說明 & 範例](#引數說明--範例)
  - [互動模式](#互動模式)
- [動畫資訊格式 & 內容](#動畫資訊格式--內容)

# 安裝說明
## 執行檔
- `Windows`、`Linux`：下載執行檔，放到任意資料夾即可。
- `Android`：
  1. 下載安裝[`Termux`](https://f-droid.org/zh_Hant/packages/com.termux/)。輸入時按`Tab`（`Esc`下面那個按鈕）可以自動補全資料夾名／檔名。
  2. 接著要把下載下來的執行檔移到`Termux`的目錄下，例如：`mv /sdcard/Download/embed-ani-gamer-covers-android $HOME`（`mv`是移動檔案的命令）
  3. 最後讓程式可以執行（加上`執行`的許可權）：`chmod +x embed-ani-gamer-covers-android`

## 直接執行 Python 原始碼
**建議[使用執行檔](#執行檔)**，就不用這麼麻煩。

請先安裝下列程式：
- `python 3`（我自己是用 3.10 測試）
- `poetry`（安裝 dependency 用）
- `git`（方便更新，可不裝）

下載檔案：
- `git clone https://github.com/zica87/embed-ani-gamer-covers.git`

- 或是按右上角的 `Code` -> `Download ZIP`，再解壓縮。

安裝 dependency：
- `poetry install`

執行：
- 請使用：`poetry run python3 embed-ani-gamer-covers [引數]`

# 使用說明
## Windows、Linux、Android
- `Windows`：打開程式所在的資料夾，點一下檔案總管上方的路徑欄空白處，輸入 `cmd`，按 `enter`鍵。
  - 或是直接點兩下就可以進入互動模式。不過這樣程式執行完或出錯的話會馬上關掉，如果有 bug 的話不易偵錯，所以不太推薦。

- `Linux`：~~Linux 用戶應該都知道怎麼開終端機，所以略過。~~
- `Android`：照[上面步驟](#執行檔)設置完後，直接打命令即可（程式名前面要加上`./`，如下）。

## 引數說明 & 範例
```
usage: embed-ani-gamer-covers-linux [-h] [-m 檔名] [-v] [-c] [-d 資料夾] [--download-visual [檔名（含路徑）]]
                                    [--download-cover [檔名（含路徑）]] [--metadata [檔名（含路徑）]] [--select [要儲存的欄位]]
                                    [--overwrite | --no-overwrite] [--dont-make-directory]
                                    [--version] sn 碼或網址

使用範例：embed-ani-gamer-covers-linux 16231 -m /home/zica/cover/m.mp4 -c -d /home/zica/cover --download-cover --download-visual
會把Lapis Re：LiGHTs [1]的封面嵌入到/home/zica/cover/m.mp4，並且把封面圖和視覺圖下載到/home/zica/cover。

positional arguments:
  sn 碼或網址               請在以下選項前面先輸入動畫的 sn 碼或網址。

options:
  -h, --help            show this help message and exit
  -m 檔名, --mp4 檔名       要嵌入縮圖的 MP4 檔名。
                        若為資料夾則表示整季的影片都要嵌入封面。
                        目前僅支援檔名與動畫瘋的標題相同的 MP4。
  -v, --embed-visual    嵌入視覺圖。
  -c, --embed-cover     嵌入封面。
                        也指定「嵌入視覺圖」選項的話則會檢查有無封面，
                        有封面的話就嵌入封面，沒有的話就嵌入視覺圖。
  -d 資料夾, --directory 資料夾, --folder 資料夾
                        下載下來的圖片要儲存到的資料夾，僅嵌入不下載的話免填。
                        要下載但不填的話表示與 MP4 檔同資料夾。
  --download-visual [檔名（含路徑）]
                        下載視覺圖。
                        後面接要儲存的檔名（含路徑），
                        不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。
  --download-cover [檔名（含路徑）]
                        下載封面。
                        後面接要儲存的檔名（含路徑），
                        不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。
  --metadata [檔名（含路徑）]  以 TOML 格式儲存動畫資訊。
                        後面接要儲存的檔名（含路徑），
                        不填的話則使用 -d 指定的路徑，也沒有的話則與 MP4 檔同資料夾。
  --select [要儲存的欄位]     在互動模式下選擇要儲存哪些動畫資料。
                        也可以直接在後面加上要儲存哪些欄位，例如：
                        --select "標題 上架時間 台灣代理"
  --overwrite           若已有與要儲存的檔案同名的檔案就覆寫。
  --no-overwrite        若已有與要儲存的檔案同名的檔案就退出程式，不覆寫。
  --dont-make-directory, --dont-make-folder
                        不存在指定資料夾時不建立資料夾，直接退出程式。
  --version             顯示版本號碼。

GitHub repo 網址：https://github.com/zica87/embed-ani-gamer-covers
版本：0.2.0
```
## 互動模式
也可以不帶引數，只輸入`embed-ani-gamer-covers`，例如：
```
zica@zica-VirtualBox:~/shared$ ./embed-ani-gamer-covers-linux
未選擇選項（引數），因此進入互動模式
? 請輸入 sn 碼或網址： 16231
開始尋找此集標題
標題：Lapis Re：LiGHTs [1]
? 請選擇要程式做的事情： 下載封面
? 請輸入下載下來的圖片要儲存到哪個現有的資料夾（或直接指定檔名）：
 /home/zica/cover/
開始尋找封面圖網址
開始尋找視覺圖網址
開始儲存動畫封面
開始下載封面
順利完成！
5 秒鐘後關閉程式
```


# 動畫資訊格式 & 內容
採用簡潔的 TOML 格式，例如：
```toml
"網址" = "https://ani.gamer.com.tw/animeVideo.php?sn=16231"
"此季標題" = "Lapis Re：LiGHTs"
"標題" = "Lapis Re：LiGHTs [1]"
"上架時間" = "2020/07/04 22:30"
"台灣代理" = "木棉花"
"視覺圖網址" = "https://p2.bahamut.com.tw/B/2KU/69/70171e9beae7a766b716bb16901934h5.JPG"
"封面網址" = "https://p2.bahamut.com.tw/B/2KU/61/55c1764efa50f58e7ae6dbbfb9193w15.JPG"
```
