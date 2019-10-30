# RAITO NOBERU

RAITCO NOBERU可以幫你在各個小說網站尋找輕小說並下載成epub檔案  
目前支援
* wenku8 
* epub輕小說站  

預計支援
* xbook

## usage

### options
```
usage: main.py [-h]
               (--search SEARCH_KEY | --detail SEARCH_DETAIL | --download DOWNLOAD_DATAIL)
               [--cpu PROCESS_COUNT]

optional arguments:
  -h, --help            show this help message and exit
  --search SEARCH_KEY   Search keyword
  --detail SEARCH_DETAIL
                        get the book's detail
  --download DOWNLOAD_DATAIL
                        download book
  --cpu PROCESS_COUNT   set download process count
```

### 搜尋小說
```
$ python main.py --search 無職轉生

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
目前僅支援輕小說文庫(wenku8)，格式為`source : id`，source是來源，目前僅有wenku，id是編號，可以在查詢時候獲得，每個來源的id格式都不一樣。
```
$ python main.py --detail=wenku:1587
[RN-prject][INFO]  第一卷 幼年期
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
[RN-prject][INFO]  第二卷 少年期 家庭教师篇
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
[RN-prject][INFO]  第二十四卷 完结编 web版
[RN-prject][INFO]      第二百六十话 “最后之梦”
[RN-prject][INFO]      第二百六十一话 “３４岁”
[RN-prject][INFO]      间话“阿苏拉王国人物录 ‘卢迪乌斯．格瑞拉特’”
[RN-prject][INFO]      最终话 “死后的世界”
[RN-prject][INFO]      终曲“Prologue Zero”
[RN-prject][INFO]      后记
```

### 下載小說
目前支援wenku8、epub輕小說站，wenku8的會把所有本都下載下來並自動轉檔成epub格式，目前並不提供插圖，epub輕小說站僅會下載指定的本，建議使用epub輕小說站，格式為`source : id`，source是來源，目前僅有wenku，id是編號，可以在查詢時候獲得，每個來源的id格式都不一樣。
```
$ python main.py --download=wenku:2638
```

## License
[MIT](https://choosealicense.com/licenses/mit/)