### 从0开始学python爬虫，看看要多久能学会

>以前只是听过，没真正的写个python代码

开始时间：2017-09-26 14：51
爬取成功时间：2017-9-27 19：12

爬了1个小时，去掉没有数据的连接，才得到2000多条数据，网址348个

### 目标：爬取融360的数据

	https://www.rong360.com/
	
	https://www.rong360.com/anqing/

### 1.安装pyquer库,方便解析html

	pip install pyquery
	pip install PyMySQL

然后在main.py里面引入

	from pyquery import PyQuery as pq


### 	

问题：

Q1:请求https遇到403错误

A1：被百度一些文章坑了，
response = urllib.request.urlopen(req)，而不是response = urllib.request.urlopen(url)




参考文档：

[https://docs.python.org/3/library/urllib.html](https://docs.python.org/3/library/urllib.html)

[http://xiaorui.cc/2014/09/14/%E4%BD%BF%E7%94%A8bloomfilter%E5%AE%9E%E7%8E%B0%E4%BA%BF%E7%BA%A7%E5%88%AB%E7%88%AC%E8%99%ABurl%E9%93%BE%E6%8E%A5%E5%8E%BB%E9%87%8D%E5%AF%B9%E6%AF%94/](http://xiaorui.cc/2014/09/14/%E4%BD%BF%E7%94%A8bloomfilter%E5%AE%9E%E7%8E%B0%E4%BA%BF%E7%BA%A7%E5%88%AB%E7%88%AC%E8%99%ABurl%E9%93%BE%E6%8E%A5%E5%8E%BB%E9%87%8D%E5%AF%B9%E6%AF%94/)
