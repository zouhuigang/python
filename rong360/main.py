#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = 'zouhuigang'
import os
import urllib.request
from pyquery import PyQuery as pq
from mysqlModel import MySQLModel as mdb
from threading import Thread
from queue import Queue
from time import ctime,sleep
#from collections import deque

qUrl = Queue() #待抓取的网页
TNUM =1 #线程数

def CrawUrl(chaper_url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}  
	req = urllib.request.Request(url=chaper_url, headers=headers)  
	response = urllib.request.urlopen(req)
	data =response.read().decode('UTF-8')
	return data


#过滤空格
def filterStr(text):
	return ''.join(text.split())

def InToDb(db,city_cn,url):
	data=CrawUrl(url)
	jq = pq(data)
	city=city_cn
	product_name=jq(".face-info h1").text()
	product_id=jq("#productId").val()
	_list=jq(".import-info span.item span.spec")
	farr={}
	for k,v in enumerate(_list):
		 farr["feature%d" % (k+1)]="'"+filterStr(jq(v).text())+"'"
		 #print('%d-%s\n' % (k+1,f1))
	keys=','.join(list(farr.keys()))
	values=','.join(list(farr.values()))
	_sql="INSERT INTO `produce` (`product_name`, `product_id`,`city`,%s) VALUES ('%s', %s,'%s',%s);" \
			% (keys,filterStr(product_name),product_id,city,values)
	last_id=db.insert(_sql)
	#print(_sql,last_id)
	return

def CrawCityInfo():
	data=CrawUrl("https://www.rong360.com/cityNavi.html")
	jq = pq(data)
	_list=jq("#TabWordList .city-list-item .city_list a")
	_sql="INSERT INTO `city` (`city_cn`, `city_en`,`url`) VALUES "
	for k,v in enumerate(_list):
		city_cn=jq(v).text()
		city_en=jq(v).attr("domain")
		url='https://www.rong360.com/%s/' % (city_en)
		if k==0 :
			_sql+="('%s','%s','%s')" %  (city_cn,city_en,url)
		else:
			_sql+=",('%s','%s','%s')" %  (city_cn,city_en,url)
		#print(city_cn,city_en,url)
	print(_sql)
		
	last_id=db.insert(_sql)
	return last_id

def getUrlList(db):
	num=db.query("select * from city")
	rs=db.show()
	return rs

#爬取某一个城市下的某个type的所有标签,并存入数据库
def getOneCityListData(db,city_cn,list_url):
	data=CrawUrl(list_url)#"https://www.rong360.com/guangzhou/s_tp9m5t12f4"
	#解析html
	jq = pq(data)
	_list=jq('.a-product_list li.item')
	#_list=jq('.other-result-list div.result-item')
	#取出url
	ListArr = []
	for k,v in enumerate(_list):
		#print('%d-%s\n' % (k+1,jq(v).text()))
		#print('%d-%s\n' % (k+1,jq(v).find('a.ui-btn').attr('href')))
		url='https:%s' % (jq(v).find('a.ui-btn').attr('href'))
		#print(url)
		InToDb(db,city_cn,url)
		#ListArr.append(jq(v).text())
	return
def gorun(db):
	while True:
		arr = qUrl.get() #默认队列为空时，线程暂停
		print(arr[1],arr[2])
		getOneCityListData(db,arr[1],arr[2])	
		sleep(1)
		qUrl.task_done()
	


db = mdb(host='139.196.48.36',user='root',passwd='yy2017622',db='rongdb',charset='utf8')


#初始化参数
types=['s_tp9m5t12f4','s_tp9m5t12f2']#上班族和个体户
pn_max=3 #最多三页

#getOneCityListData(db,"中卫","https://www.rong360.com/aba/s_tp9m5t12f4?&pn=1")
#db.close()
#os._exit(0)

#第一次请爬取城市信息及url地址
#data=CrawCityInfo()
#db.close()
#os._exit(0)
rs=getUrlList(db)
for k1,v1 in  enumerate(rs):
	for i in range(pn_max):
		city_cn=v1[1]
		url=v1[3]+types[0]+"?&pn="+str(i+1)
		info=[k1,city_cn,url]
		qUrl.put(info)

		url=v1[3]+types[1]+"?&pn="+str(i+1)
		info1=[k1,city_cn,url]
		qUrl.put(info1)


#开多线程处理数据
#开启线程  
threads = []  
for i in range(TNUM):  
    t = Thread(target=gorun,args=(db,))#线程的执行函数为getOneCityListData2  
    threads.append(t)  
for item in threads:  
    item.setDaemon(True)  
    item.start()  

#等待队列结束
qUrl.join()

db.close()
os._exit(0)



db.close()
os._exit(0)
#print(data)
#print(response.getheaders())
print("Hello, World!");

