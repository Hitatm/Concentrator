# -*- coding: utf-8 -*-
# @Author: Guoxuenan
# @Date:   2016-11-10 17:16:50
# @Last Modified by:   Guoxuenan
# @Last Modified time: 2016-11-10 22:18:23
__author__ ='gxn'

import os 
import linecache
def findline():
	file1=open('/home/wangyu/相关实验/时间同步实验45个节点/sensordata.log','r')
	linecache.clearcache()
	line= len(file1.readlines())
	print linecache.getline('/home/wangyu/相关实验/时间同步实验45个节点/data.log',line/2)
def getdata(startline,endline):
	return
if __name__ == '__main__':
	findline()