#coding:UTF-8
__author__ = 'dj'


import collections
#数据包大小统计
from gxn_get_sys_config import Config

#http/https协议统计
def topo_statistic(TOPODATA):
    nodes_dict = dict()
    for item in TOPODATA:
        ID= item[1] #ID
        if ID in nodes_dict:
            nodes_dict[ID]+=1
        else:
            nodes_dict[ID]=1
    return nodes_dict

def topo_traffic_analyzer(TOPODICT):
    sysCongfig = Config()
    traffic_dict = collections.OrderedDict()
    # date_set=set()
    # print sysCongfig.ACTIVE_TIME
    for items in TOPODICT:
        traffic_item=items[16].split(' ') #realtimestamp
        date=traffic_item[0].replace('-','/').encode('UTF-8')
        ymd=traffic_item[1][:5]
        # print ymd, 
        traffic = date+' '+ymd
        numberof_10= int(ymd.split(':')[0])*6+(int(ymd.split(':')[1]) +2)/10 # +2 是因为允许有节点早到两分钟(的误差)
        real_minutes= int(ymd.split(':')[0])*60+int(ymd.split(':')[1]) #实际的分钟数
        if numberof_10  in sysCongfig.get_active_time():
            # print sysConfig.ACTIVE_TIME[numberof_10]
            base_time=sysCongfig.get_active_time()[numberof_10]
            tempkey= date+' '+base_time
            base_minutes=int(base_time.split(':')[0])*60+int(base_time.split(':')[1])#基准active的分钟
            real_base_diff= real_minutes-base_minutes
            # print traffic,real_base_diff
            if tempkey in traffic_dict:
                if real_base_diff==-1 :
                    traffic_dict[tempkey][1]+=1
                elif real_base_diff==0:
                    traffic_dict[tempkey][2]+=1
                elif real_base_diff==1:
                    traffic_dict[tempkey][3]+=1
                elif real_base_diff==2:
                    traffic_dict[tempkey][4]+=1
                elif real_base_diff==3:
                    traffic_dict[tempkey][5]+=1
                elif real_base_diff==4:
                    traffic_dict[tempkey][6]+=1
                else:
                    traffic_dict[tempkey][0]+=1
            else:
                traffic_dict[tempkey]=[0,0,0,0,0,0,0]
                if real_base_diff==-1 :
                    traffic_dict[tempkey][1]+=1
                elif real_base_diff==0:
                    traffic_dict[tempkey][2]+=1
                elif real_base_diff==1:
                    traffic_dict[tempkey][3]+=1
                elif real_base_diff==2:
                    traffic_dict[tempkey][4]+=1
                elif real_base_diff==3:
                    traffic_dict[tempkey][5]+=1
                elif real_base_diff==4:
                    traffic_dict[tempkey][6]+=1
                else:
                    traffic_dict[tempkey][0]+=1
    return get_traffic_list(traffic_dict)

def get_traffic_list(traffic_dict):
    resultdict=[]
    templist=[[],[],[],[],[],[],[],[]]
    for key ,value in traffic_dict.items():
        templist[0].append(key)
        templist[1].append(value[0])
        templist[2].append(value[1])
        templist[3].append(value[2])
        templist[4].append(value[3])
        templist[5].append(value[4])
        templist[6].append(value[5])
        templist[7].append(value[6])
    # print templist[1]
    tempdict1 ={
    'name':'others',
    'type':'bar',
    'stack': 'total',
    'itemStyle' : { 'normal': {'label' : {'show': 'true','textStyle':{'align':'center'}, 'position': 'inside'}}},
    'data':templist[1] 
    }
    resultdict.append(templist[0])
    resultdict.append(tempdict1)
    for x in xrange(2,8):
        tempdict2 ={
        'name':str(x-3)+' minute',
        'type':'bar',
        'stack': 'total',
        'itemStyle' : { 'normal': {'label' : {'show': 'true','textStyle':{'align':'center'}, 'position': 'inside'}}},
        'data':templist[x]
        }
        resultdict.append(tempdict2)

    return resultdict



def topo_traffic_statistic(TOPODICT):
    traffic_dict = collections.OrderedDict()
    count=0
    for items in TOPODICT:
        traffic_item=items[16].split(' ') #'realtimestamp'
        traffic = traffic_item[0].replace('-','/')+' '+traffic_item[1]
        # print traffic
        if traffic  in traffic_dict:
            traffic_dict[traffic]+=1
        else:
            traffic_dict[traffic]=count
    # print traffic_dict
    return traffic_dict


def app_traffic_analyzer(TOPODICT):
    sysCongfig = Config()
    traffic_dict = collections.OrderedDict()
    # date_set=set()
    # print sysCongfig.ACTIVE_TIME
    for items in TOPODICT:
        traffic_item=items[2].split(' ') #currenttime
        date=traffic_item[0].replace('-','/').encode('UTF-8')
        ymd=traffic_item[1][:5]
        # print ymd, 
        traffic = date+' '+ymd
        numberof_10= int(ymd.split(':')[0])*6+(int(ymd.split(':')[1]) +2)/10 # +2 是因为允许有节点早到两分钟(的误差)
        real_minutes= int(ymd.split(':')[0])*60+int(ymd.split(':')[1]) #实际的分钟数
        if numberof_10  in sysCongfig.get_active_time():
            # print sysConfig.ACTIVE_TIME[numberof_10]
            base_time=sysCongfig.get_active_time()[numberof_10]
            tempkey= date+' '+base_time
            base_minutes=int(base_time.split(':')[0])*60+int(base_time.split(':')[1])#基准active的分钟
            real_base_diff= real_minutes-base_minutes
            # print traffic,real_base_diff
            if tempkey in traffic_dict:
                if real_base_diff==-1 :
                    traffic_dict[tempkey][1]+=1
                elif real_base_diff==0:
                    traffic_dict[tempkey][2]+=1
                elif real_base_diff==1:
                    traffic_dict[tempkey][3]+=1
                elif real_base_diff==2:
                    traffic_dict[tempkey][4]+=1
                elif real_base_diff==3:
                    traffic_dict[tempkey][5]+=1
                elif real_base_diff==4:
                    traffic_dict[tempkey][6]+=1
                else:
                    traffic_dict[tempkey][0]+=1
            else:
                traffic_dict[tempkey]=[0,0,0,0,0,0,0]
                if real_base_diff==-1 :
                    traffic_dict[tempkey][1]+=1
                elif real_base_diff==0:
                    traffic_dict[tempkey][2]+=1
                elif real_base_diff==1:
                    traffic_dict[tempkey][3]+=1
                elif real_base_diff==2:
                    traffic_dict[tempkey][4]+=1
                elif real_base_diff==3:
                    traffic_dict[tempkey][5]+=1
                elif real_base_diff==4:
                    traffic_dict[tempkey][6]+=1
                else:
                    traffic_dict[tempkey][0]+=1
    return get_traffic_list(traffic_dict)


def app_traffic_statistic(TOPODICT):
    traffic_dict = collections.OrderedDict()
    count=0
    for items in TOPODICT:
        traffic_item=items[2].split(' ') #'currenttime'
        traffic = traffic_item[0].replace('-','/')+' '+traffic_item[1]
        # print traffic
        if traffic  in traffic_dict:
            traffic_dict[traffic]+=1
        else:
            traffic_dict[traffic]=count
    # print traffic_dict
    return traffic_dict
