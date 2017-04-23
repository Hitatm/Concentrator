#coding:UTF-8

import os
from app import app
import sqlite3

class connectDB:
	def __init__(self):
		self.DB_FILE = os.path.join(app.config['DB_FOLDER'],"topo3.db")

	def all_NetMonitor_withtime(self,time1,time2):
		conn = sqlite3.connect(self.DB_FILE)
		c = conn.cursor()
		c.execute("select * from NetMonitor where currenttime >= ? and currenttime <= ?;",(time1,time2))
		datalist = c.fetchall()
		conn.close()
		return datalist

	def NetMonitor_withtime_and_NodeID(self,time1,time2,NodeID):
		conn = sqlite3.connect(self.DB_FILE)
		c = conn.cursor()

		c.execute("select * from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;",(time1,time2,NodeID))
		datalist = c.fetchall()
		conn.close()
		return datalist

	def NetMonitor_ID_withtime(self,time1,time2):
		conn = sqlite3.connect(self.DB_FILE)
		c = conn.cursor()
		c.execute("select NodeID, ParentID from NetMonitor where currenttime >= ? and currenttime <= ?;",(time1,time2))
		datalist = c.fetchall()
		conn.close()
		return datalist

	def NetMonitor_voltage_error(self,time1,time2):
		conn = sqlite3.connect(self.DB_FILE)
		c = conn.cursor()
		c.execute('select ID, volage, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and volage<3;',(start_time, end_time))
		datalist = c.fetchall()
		conn.close()
		return datalist

	def NetMonitor_current_error(self,time1,time2):
		conn = sqlite3.connect(self.DB_FILE)
		c = conn.cursor()
		c.execute('select ID, electric, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and electric>25;',(start_time, end_time))
		datalist = c.fetchall()
		conn.close()
		return datalist