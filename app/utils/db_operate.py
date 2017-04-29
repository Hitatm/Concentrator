#coding:UTF-8

import os
from app import app
import sqlite3
import time

class DBClass:
	def __init__(self):
		self.DB_FILE = os.path.join(app.config['DB_FOLDER'],"topo3.db")
	def my_db_execute(self,str_exe,parameter):
		conn = sqlite3.connect(self.DB_FILE)
		c = conn.cursor()
		if parameter!=None:
			# print parameter
			c.execute(str_exe,parameter)
		else:
			c.execute(str_exe)
		datalist = c.fetchall()
		conn.close()
		return datalist
	def db_del_or_insert(self,str_exe,parameter):
		conn = sqlite3.connect(self.DB_FILE)
		c = conn.cursor()
		if parameter!=None:
			# print parameter
			c.execute(str_exe,parameter)
		else:
			c.execute(str_exe)
		conn.commit()
		datalist = c.fetchall()
		conn.close()
		return 
		# return datalist


# test=DBClass()

# t = time.time()
# current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
# previous_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 1000*60*60))
# print current_time,previous_time
# NodeID='222'
# print test.my_db_execute("select * from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;"
# 	,(previous_time,current_time,NodeID))
# print test.my_db_execute("select * from NetMonitor;",None)

