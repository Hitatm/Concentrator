# -*- coding: utf-8 -*-
# @Author: Guoxuenan
# @Date:   2016-11-10 17:16:50
# @Last Modified by:   Guoxuenan
# @Last Modified time: 2016-12-22 15:22:40
__author__ ='gxn'

import os 
import linecache
import collections
from gxn_topo_decode import TopoDecode
from gxn_get_sys_config import Congfig

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

def getall_topo(TOPODATA,TPDECODE):
    items = collections.OrderedDict()
    count = 0
    for p in TOPODATA:
        count += 1
        item = TPDECODE.topo_decode(p)
        # print item
        items[count] = item
    return items

def get_filter_item(TOPODATA, TPDECODE, key, value):
    items = collections.OrderedDict()
    count = 0
    for p in TOPODATA:
        item = TPDECODE.topo_decode(p)
        if value in item[key].lower():
        	count += 1
        	items[count] = item
    return items


#过滤器
def topo_filter(filter_type, value, TOPODATA, TPDECODE):
    if filter_type == u'all':
        items = getall_topo(TOPODATA, TPDECODE)
    elif filter_type == u'ID':
        if value:
            value = str(value).strip().lower()
            items = get_filter_item(TOPODATA, TPDECODE, filter_type, value)
        else:
            items = getall_topo(TOPODATA, TPDECODE)
    elif filter_type == u'synparentID':
        if value:
            value = str(value).strip().lower()
            items = get_filter_item(TOPODATA, TPDECODE, filter_type, value)
        else:
            items = getall_topo(TOPODATA, TPDECODE)
    elif filter_type == u'synlevel':
        if value:
            value = str(value).strip().lower()
            items = get_filter_item(TOPODATA, TPDECODE, filter_type, value)
        else:
            items = getall_topo(TOPODATA, TPDECODE)
    else:
        items = getall_topo(TOPODATA, TPDECODE)
    return items


def showdata_from_id(DATA_DICT, dataid):
    Dict = DATA_DICT[dataid]
    html = '''
            <div class="accordion-group">
                <div class="accordion-heading">
                    <b><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion" href="#collapse{id}">
                        {proto}
                    </a></b><br>
                    </div>
                    <div id="collapse{id}" class="accordion-body collapse" style="height: 0px; ">
                    <div class="accordion-inner">
                        {values}
                    </div>
                </div>
            </div>
    '''
    all_html = ''
    id = 0
    for proto, value in Dict.items():
        id += 1
        html_proto = proto
        html_values = value
        all_html += html.format(proto=html_proto, values=html_values, id=str(id))
    return all_html

def topo_statistic(TOPODICT):
    nodes_dict = dict()
    for count, item in TOPODICT.items():
    	ID= item['ID']
    	if ID in nodes_dict:
    		nodes_dict[ID]+=1
    	else:
    		nodes_dict[ID]=1
    return nodes_dict



def topo_traffic_statistic(TOPODICT):
    traffic_dict = collections.OrderedDict()
    count=0
    for count ,items in TOPODICT.items():
        traffic_item=items['realtimestamp'].split('_')
        traffic = traffic_item[0].replace('-','/')+' '+traffic_item[1]
        # print traffic
        # print count
        # print TOPODICT[count]
        if traffic  in traffic_dict:
            traffic_dict[traffic]+=1
        else:
            traffic_dict[traffic]=count
    # print traffic_dict
    return traffic_dict

# if __name__ == '__main__':
# 	TPDECODE =TopoDecode()
# # 	sysConfig=Congfig()
# # 	# print sysConfig.
# 	data__=getfile_content('/home/wangyu/myspace/Concentrator/datalog/topo.txt')
# 	print getall_topo(data__,TPDECODE)
# 	# data= topo_filter('ID','',data__ ,TPDECODE)
# 	data= getall_topo(data__,TPDECODE)
# 	# print data
# 	traffic_dict= topo_traffic_statistic(data)
	# print traffic_dict
	# get_traffic_list(traffic_dict)
	# print topo_statistic(data)
	# for i,item in data.items():
		# print i,item
		# print "**********************************"
	# for key ,value in topo_traffic_statistic(data).items():
		# print key ,value



 # templist=[
 #        {
 #            'name':'直接访问',
 #            'type':'bar',
 #            'stack': '总量',
 #            'itemStyle' : { 'normal': {'label' : {'show': 'true', 'position': 'insideTop'}}},
 #            'data':[120, 132, 101, 134, 90, 230, 210]
 #        }
 #        ]

















	
	# for x in data__:
		# index0= x.find('[')
		# index1= x.find(']')
		# print x
		# print str(x[0:index0-1].split()[0]+'#'+x[0:index0-1].split()[1])+' '+x[index0+1:index1]+' '+x[index1+10:]
		
# 1476361828169 aaaa:0:0:0:12:7400:1:e8 -125 -65 0 21 32 27 1 15 0 0 0 22 32 35 0 0 47 -13 -115 -36 0 0 0 0 89 -28 0 0 0 26 51 -77 14 51 16 98 0 17 4 0 0 0 4 1 15 32 19 17 2
