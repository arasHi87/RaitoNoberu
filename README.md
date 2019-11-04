# RAITO NOBERU

RAITO NOBERU可以幫你在各個小說網站尋找輕小說並下載成epub檔案  
目前支援
* wenku8 
* epub輕小說站  

預計支援
* ~~xbook~~

## Installation
you can clone it and install by your self
```
git clone https://github.com/arasHi87/RaitoNoberu
cd raitonoberu

# if you only have python3 use this
python setup.py install

# if you have 2 and 3 use this
python3 setup.py install
```
or you can install by use pip
```
# if you only have python3 use this
pip install lightdo

# if you have 2 and 3 use this
pip3 install lightdo
```

## usage

### options
```
usage: lightdo [-h] [--search SEARCH_KEY] [--detail SEARCH_ID]
               [--download DOWNLOAD_ID] [--cpu PROCESS_COUNT]
               [--wenku WENKU_SEACHER] [--redata WENKU_REDATA] [--renew]
               [--clean] [--wenku_account WENKU_ACCOUNT]
               [--wenku_password WENKU_PASSWORD] [--anonymous]
               [--path SAVE_PATH] [--number DOWNLOAD_NUMBER] [-w] [-e]

optional arguments:
  -h, --help            show this help message and exit
  --search SEARCH_KEY   Search keyword
  --detail SEARCH_ID    get the book's detail
  --download DOWNLOAD_ID
                        download book
  --cpu PROCESS_COUNT   set download process count
  --wenku WENKU_SEACHER
                        set wenku searcher to online/local
  --redata WENKU_REDATA
                        reget all wenku local data, please enter the latest
                        you want renew
  --renew               renew wenku local data
  --clean               clean your wenku account
  --wenku_account WENKU_ACCOUNT, -wa WENKU_ACCOUNT
                        set your wenku account
  --wenku_password WENKU_PASSWORD, -wp WENKU_PASSWORD
                        set your wenku password
  --anonymous, -am      this will not store your account
  --path SAVE_PATH      set download path
  --number DOWNLOAD_NUMBER
                        set number you want to download, default is download
                        all
  -w                    set type to wenku
  -e                    set type to epubsite
```
### 登入wenku8
你需要先登入帳號才能進行線上搜索，或是你可以在搜索同時使用`--anonymous`，這將不會保存你的帳密，但每次都需要重新輸入。
```
lightdo -wa your_account -wp your_password
```

### 搜尋小說
可以在後面加上`--wenku=local`，使用本地資料庫搜索，預設為線上搜索，但在wenku8裡如果搜尋結果超過兩頁，獲得下一頁需要等待五秒。
```
$ lightdo --search 無職轉生 -wa=account -wp=pasword --anonymous # this will not save your account

[RN-prject][INFO]  ======= wenku =======
[RN-prject][INFO]  use cookie login wenku
[RN-prject][INFO]  1587 : 无职转生～到了异世界就拿出真本事～(无职转生~在异世界认真地活下去~)
[RN-prject][INFO]  ===== epub site =====
[RN-prject][INFO]  2016/06/03_16 : 無職轉生 03 〜到了異世界就拿出真本事〜
[RN-prject][INFO]  2015/12/02_16 : 無職轉生 02
[RN-prject][INFO]  2014/08/01_82 : 無職轉生 01 ~在異世界認真地活下去~
[RN-prject][INFO]  2018/07/12_21 : 無職轉生 ～到了異世界就拿出真本事～ 12
[RN-prject][INFO]  2018/03/11_17 : 無職轉生 ～到了異世界就拿出真本事～ 11
[RN-prject][INFO]     2018/01/10 : 無職轉生～到了異世界就拿出真本事～ 10
[RN-prject][INFO]     2017/10/09 : 無職轉生～到了異世界就拿出真本事～ 09
[RN-prject][INFO]     2017/10/08 : 無職轉生～到了異世界就拿出真本事～ 08
[RN-prject][INFO]     2017/08/07 : 無職轉生～到了異世界就拿出真本事～ 07
[RN-prject][INFO]  2017/03/06_28 : 無職轉生～到了異世界就拿出真本事～ 06
[RN-prject][INFO]     2016/06/05 : 無職轉生 05 〜在異世界認真地活下去〜
[RN-prject][INFO]  2016/06/04_16 : 無職轉生 04 〜到了異世界就拿出真本事〜
```

### 獲得小說詳細資料 (章節)
目前僅支援輕小說文庫(wenku8)，`--detail`後面接你要的id，然後在後面接你要的選擇器，目前提供`-w`、`-e`，`-w`是指`wenku`，`-e`是`epub site`。
```
$ lightdo --detail 1587 -w
[RN-prject][INFO]  1- 第一卷 幼年期
[RN-prject][INFO]      序章
[RN-prject][INFO]      第一话「难道是：异世界」
[RN-prject][INFO]      第二话「心生反感的女仆」
[RN-prject][INFO]      第三话「魔术教科书」
[RN-prject][INFO]      第四话「师傅」
[RN-prject][INFO]      第五话「剑术与魔术」
[RN-prject][INFO]      第六话「尊敬的理由」
[RN-prject][INFO]      第七话「朋友」
[RN-prject][INFO]      第八话「迟钝」
[RN-prject][INFO]      第九话「紧急家族会议」
[RN-prject][INFO]      第十话「遭遇瓶颈」
[RN-prject][INFO]      第十一话「离别」
[RN-prject][INFO]      外传 格雷拉特家的母亲
[RN-prject][INFO]      插图
[RN-prject][INFO]      特典〈人生的绿洲〉
[RN-prject][INFO]  2- 第二卷 少年期 家庭教师篇
[RN-prject][INFO]      序章
[RN-prject][INFO]      第一话「大小姐的暴力」
[RN-prject][INFO]      第二话「自导自演」
[RN-prject][INFO]      闲话「后日谈与伯雷亚斯式问候」
[RN-prject][INFO]      第三话「凶暴性质尚未衰退」
[RN-prject][INFO]      第四话「职员会议与星期日」
[RN-prject][INFO]      第五话「大小姐十岁」
[RN-prject][INFO]      第六话「学习语言」
[RN-prject][INFO]      第七话「诺言」
[RN-prject][INFO]      第八话「转折点」
[RN-prject][INFO]      终章
[RN-prject][INFO]      外传「森之女神」
[RN-prject][INFO]      插图
[RN-prject][INFO]      特典〈腹肌的力量〉
                  .
                  .
                  .
                  .
                  .
                  .
[RN-prject][INFO]  24 - 第二十四卷 完结编 web版
[RN-prject][INFO]      第二百六十话 “最后之梦”
[RN-prject][INFO]      第二百六十一话 “３４岁”
[RN-prject][INFO]      间话“阿苏拉王国人物录 ‘卢迪乌斯．格瑞拉特’”
[RN-prject][INFO]      最终话 “死后的世界”
[RN-prject][INFO]      终曲“Prologue Zero”
[RN-prject][INFO]      后记
```

### 下載小說
目前支援wenku8、epub輕小說站，wenku8的會把所有本都下載下來並自動轉檔成epub格式，目前並不提供插圖，epub輕小說站僅會下載指定的本，建議使用epub輕小說站，`--detail`後面接你要的id，然後在後面接你要的選擇器，目前提供`-w`、`-e`，`-w`是指`wenku`，`-e`是`epub site`，目前僅有wenku，id是編號，可以在查詢時候獲得，每個來源的id格式都不一樣，也可以使用`--path`設定下載路徑，如果沒有的話預設下載在當前目錄，也可以單獨下載一本，只需要在後面加上`--number nth`，`nth`是在查詢detail前面會輸出的編號。
```
$ lightdo --download 2638 -w
$ lightdo --download 2638 -w --path=fuck/this/world
$ lightdo --download 1587 -w --number 87
```

### 更新wenku8本地資料
更新本地的wenku8資料，會從上次最新的下一本開始尋找直到找不到為止
```
lightdo --renew
```

### 重新獲得wenku8的資料
可以設定一個範圍，建議從2700開始
```
lightdo --redata 2700
```

### 清除wenku8帳號
```
lightdo --clean
```

## License
[MIT](https://choosealicense.com/licenses/mit/)