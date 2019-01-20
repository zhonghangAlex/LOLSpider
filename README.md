# LOLSpider
本项目基于scrapy，对租号玩网站的英雄联盟相关出租账号信息进行爬取，并且存取入库，使用随机User-Agent和随机高匿IP（Based on scrapy, this project crawls the rental account information related to heroic alliance of rental number playing website, and accesses and stores it in the library, using random User-Agent and random high-anonymity IP.）

## 相关库、框架、功能  
* scrapy（爬虫框架）  
* scrapyd（服务端部署）  
* fake_useragent（随机请求头）  
* crawl_xici（西刺高匿代理）  
* twisted（异步存储数据库）  
* pymysql（mysql链接）  

## 说明  
* 项目入口文件是main.py，直接运行该文件则可以启动爬虫项目  
* 请先pip安装scrapy，fake_useragent,pymysql保证程序可以正常运行  
* 项目通过使用fake_useragent,制造了随机请求头  
* 数据库文件存放在db_file中，请先将数据还原，并且如果要使用动态IP，需要找到crawl_xici.py文件，调用crawl_ips()方法，将最新的高匿IP写入到数据库中   
* 动态IP请求功能默认关闭，如果希望开启，可以在settings.py文件中，将DOWNLOADER_MIDDLEWARES的注释部分LOLSpider.middlewares.RandomProxyMiddleware取消注释  

## 爬取网站
[爬取网站主页面](https://www.zuhaowan.com/zuhao-17) 

## 数据库存储效果
![数据库效果图](https://github.com/zhonghangAlex/LOLSpider/blob/master/db_pic1.png)  
![数据库效果图](https://github.com/zhonghangAlex/LOLSpider/blob/master/db_pic2.png)
