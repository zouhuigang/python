#!/usr/bin/python3
# -*- coding:utf-8 -*-
import pymysql
import sys
__all__ = ['zdb']
class MySQLModel(object):
	conn = ''
	cursor = ''
	def __init__(self,host='localhost',user='root',passwd='root',db='mysql',charset='utf8'):
		try:
			print(host,user,passwd,db,charset)
#注意用key=value的形式，不然设置charset会报错
			self.conn = pymysql.connect(host=host,user=user,passwd=passwd,db=db,charset='utf8')
		except pymysql.InternalError as error:
			print("Cannot connect to server...",error)
			sys.exit()
		self.cursor = self.conn.cursor()
      
	def query(self,sql):
		#db.commit()
		return self.cursor.execute(sql)
	def insert(self,sql):
		last_id=0
		try:
			self.cursor.execute(sql)
			last_id=self.conn.insert_id()
			self.conn.commit()
		except:
			self.conn.rollback()
		return last_id
  
	def show(self):
		return self.cursor.fetchall()

	#析构函数__del__
	def close(self):
		print("mysql close ...")
		self.cursor.close()
		self.conn.close()
