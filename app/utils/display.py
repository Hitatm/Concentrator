#coding:UTF-8
from app import app
import time
import sqlite3
from db_operate import DBClass

DATABASE = DBClass()

def multipledisplay(time1,time2,dbitems):
    # dbitems = "NodeID,rtimetric,currenttime"
    data_list = list() #形如[ [Date.UTC(1970,  9, 27), 0],[Date.UTC(1970, 10, 10), 0.6 ],...]

    dlist=  list()
    Data_set = DATABASE.my_db_execute(("select NodeID,"+ dbitems +",currenttime from NetMonitor where currenttime >= ? and currenttime <= ?;"),(time1, time2))    
    for x in Data_set:
        dicts=dict()
        time_ms = int(time.mktime(time.strptime(x[2],'%Y-%m-%d %H:%M:%S'))*1000)
        dicts["name"] = x[0].encode('ascii')
        dicts["data"] = [int(time_ms),int(x[1])]
        dlist.append(dicts)     
        # {'data': [1493568035000L, 835], 'name': u'0101'}

    dicttemp=dict()
    for x in dlist:
        if x["name"] in dicttemp:
            dicttemp[x["name"]].append(x["data"])
        else:
            dicttemp[x["name"]]=[x["data"]]

    for key,value in dicttemp.items():
        dicts = dict()
        dicts["name"] = key
        dicts["data"] = value
        # print dicts
        data_list.append(dicts)
    return data_list

def NetID_list(time1,time2):
    ID_list = list()
    ID_set = DATABASE.my_db_execute("select distinct NodeID from NetMonitor where currenttime >= ? and currenttime <= ?;",(time1, time2))
    for i in range(len(ID_set)):
        ID_list.append(ID_set[i][0].encode('ascii'))
    return ID_list

def singledisplay(time1,time2,dbitem):
    ID_list = NetID_list(time1,time2)
    data_dict = dict()
    for ID in ID_list:
        data = DATABASE.my_db_execute(("select "+ dbitem +" from NetMonitor where NodeID == ? and currenttime >= ? and currenttime <= ? order by currenttime desc LIMIT 1;"),(ID, time1, time2))
        if data:
            data_dict[ID] = data[0][0]
    data_dict = sorted(data_dict.iteritems(), key=lambda d:d[1], reverse=True)
    ID_list = list()
    data_list = list()
    count=0
    for key, value in data_dict:
        count+=1
        if count%2==0:
            ID_list.append(key)
        else:
            ID_list.append(key+'     ')
        data_list.append(value)
    return ID_list,data_list
    # data = DATABASE.my_db_execute(("select "+ dbitem +" from NetMonitor where currenttime >= ? and currenttime <= ? order by currenttime desc LIMIT 1;"),(ID, time1, time2))
    # if data:
    #     data_dict[ID] = data[0][0]
    # data_dict = sorted(data_dict.iteritems(), key=lambda d:d[1], reverse=True)
    # ID_list = list()
    # data_list = list()
    # count=0
    # for key, value in data_dict:
    #     count+=1
    #     if count%2==0:
    #         ID_list.append(key)
    #     else:
    #         ID_list.append(key+'     ')
    #     data_list.append(value)
    # return ID_list,data_list
    # http_dict = topo_statistic(topodata_list)
