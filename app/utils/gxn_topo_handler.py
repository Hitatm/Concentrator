# -*- coding: utf-8 -*-
# @Author: Guoxuenan
# @Date:   2016-11-10 17:16:50
# @Last Modified by:   Guoxuenan
# @Last Modified time: 2016-11-14 22:39:08
__author__ ='gxn'

import os 
import linecache
import collections
from gxn_topo_decode import TopoDecode
# TPDECODE =TopoDecode()

def getfile_content(path):
	result=None
	filetemp=open(path,'r')
	if not filetemp:
		raise Exception(u"没有找到数据或者拓扑数据！"+path)
		return None
	result=filetemp.readlines()
	if result==None:
		raise Exception(u"数据读取出错　try again"+path)
		return None
	filetemp.close()
	return result

def findline():
	file1=open('/home/wangyu/相关实验/时间同步实验45个节点/data.log','r')
	# linecache.clearcache()
	items=file1.readlines();
	line= len(items)
	print line
	# print linecache.getline('/home/wangyu/myspace/Concentrator/datalog/topo.txt',100)
	# linecache.clearcache()

def getdata(startline,endline):
	return

def getall_topo(TOPODATA,TPDECODE):
	items = collections.OrderedDict()
	count = 0
	for p in TOPODATA:
	    count += 1
	    item = TPDECODE.topo_decode(p)
	    # print item
	    # break
	    items[count] = item
	    # break
	return items

# if __name__ == '__main__':
	# data__=getfile_content('/home/wangyu/myspace/Concentrator/datalog/topo.txt')
	# print getall_topo(data__,TPDECODE)[3]





















	
	# for x in data__:
		# index0= x.find('[')
		# index1= x.find(']')
		# print x
		# print str(x[0:index0-1].split()[0]+'#'+x[0:index0-1].split()[1])+' '+x[index0+1:index1]+' '+x[index1+10:]
		
# 1476361828169 aaaa:0:0:0:12:7400:1:e8 -125 -65 0 21 32 27 1 15 0 0 0 22 32 35 0 0 47 -13 -115 -36 0 0 0 0 89 -28 0 0 0 26 51 -77 14 51 16 98 0 17 4 0 0 0 4 1 15 32 19 17 2
