# Line-Bot-Elder
<p align=center>
    <img src="./img/img1.jpg" width = "200">
</p>

<p align=center>
    <a target="_blank" href="#" title="language count"><img src="https://img.shields.io/github/languages/count/lofoz/LineBot?color=red"></a>
    <a target="_blank" href="#" title="top language"><img src="https://img.shields.io/github/languages/top/lofoz/LineBot?color=purple"></a>
</p>
<p align=center>
<img src="./img/436qifls.png" width="200" height="200" title="OR-code">
</p>

## 說明
> 使用FSM(有限狀態機)的概念 實作Line Bot

## 構想
應該很多人都收過家中長輩傳來一種畫質不是很高，總寫著奇怪標語的圖片吧。我自己常常不知道要怎麼回，所以開發出這個Line Bot幫忙大家可以找出回應長輩的圖來增進親子感情。其中還可以藉由維基百科的爬蟲，得知一些老人容易得到的疾病，再來如果想念家中長輩的話，不妨馬上查一下最近的火車班次馬上回家看看吧。

## 架構
* google圖片爬蟲
* 維基百科爬蟲 
* 台鐵資料庫json檔解析(因為新版台鐵網站沒辦法使用爬蟲爬資料)

建立一個可以列出搜尋長輩圖，基本疾病資料，火車時刻表的Line Bot

## 功能
* 客製化搜尋長輩圖
* 查詢維基上疾病的資訊
* 查詢近兩個小時的火車班次
* 可查詢 fsm graph
* 使用Line button回傳訊息

## FSM
![fsm](./img/show-fsm.png)

## Function
**menu**
可以選擇要使用什麼功能
<p align=center>
<img src="./img/img2.jpg" width = "200">
</p>

**elder image**
可用Line Button回覆可以客製化搜尋長輩圖
<p align=center>
<img src="./img/img3.jpg" width = "200">
<img src="./img/img4.jpg" width = "200">
<img src="./img/winter.jpg" width = "200">
<img src="./img/peace.jpg" width = "200">
</p>

**Knowledge**
抓取維基百科上的部分資料
<p align=center>
<img src="./img/img6.jpg" width = "200">
<img src="./img/img7.jpg" width = "200">
<img src="./img/img8.jpg" width = "200">
</p>

**train**
搜尋近三小時內的火車班次
<p align=center>
<img src="./img/img5.jpg" width = "200">
</p>

**fsm**
印出fsm
<p align=center>
<img src="./img/img9.jpg" width = "200">
</p>

## Demo
<p align=center>
<img src="./img/img1.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/img2.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/img3.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/img4.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/winter.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/peace.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/img5.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/img6.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/img7.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/img8.jpg" width="384" height="682.4">
</p>
<p align=center>
<img src="./img/img9.jpg" width="384" height="682.4">
</p>
