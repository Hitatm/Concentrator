#coding:UTF-8
from app import app
from db_operate import DBClass
import sqlite3
import time
from time import strftime

DATABASE = DBClass()
# def data_error(time1,time2):
#     warning_list = list()
#     idata = DATABASE.my_db_execute('select ID, electric, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and electric>600;',(time1, time2))
#     for i in idata:
#         warning_dict = dict()
#         warning_dict["seqnum"] = i[0]
#         warning_dict["warn"] = "current = " + str(i[1]) + "uA"
#         warning_dict["ip_port"] = i[2] #NodeID
#         warning_dict["time"] = i[3] #currenttime
#         warning_list.append(warning_dict)

#     vdata = DATABASE.my_db_execute('select ID, volage, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and volage<3;',(time1, time2))       
#     for v in vdata:
#         warning_dict = dict()
#         warning_dict["seqnum"] = v[0]
#         warning_dict["warn"] = "voltage = " + str(v[1]) + "V"
#         warning_dict["ip_port"] = v[2] #NodeID
#         warning_dict["time"] = v[3] #currenttime
#         warning_list.append(warning_dict)
#         # print warning_dict
#         print warning_list
#     return warning_list

def data_error_new(time1,time2):
    warning_list_v = list()
    warning_list_i = list()    
    vnodeset = set()
    inodeset = set()
    # {
    #     "name": "阿里巴巴上市", 
    #     "evolution": [
    #         {
    #             "time": "2014-05-01", 
    #             "value": 14, 
    #             "detail": {
    #                 "link": "http://www.baidu.com", 
    #                 "text": "百度指数", 
    #                 "img": '../asset/ico/favicon.png'
    #             }
    #         }
    #     ]
    # }
    idata = DATABASE.my_db_execute('select ID, electric, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and electric>600;',(time1, time2))
    if idata:
        nodedict = dict()
        for i in idata:
            warning_dict_temp = dict()
            # warning_dict_i = dict()
            if i[2] in nodedict:
                evolution_dict_temp = dict()
                warning_detail = dict()
                evolution_dict_temp["time"] = str(i[3]).encode('ascii')
                evolution_dict_temp["value"] = 50
                warning_detail["text"] = i[2].encode('ascii')+":Current="+str(i[1])+"uA"
                evolution_dict_temp["detail"] = warning_detail
                evolution_list = nodedict[i[2]]["evolution"]
                evolution_list.append(evolution_dict_temp)
                warning_dict_temp["name"] = i[2].encode('ascii')
                warning_dict_temp["evolution"] = evolution_list
            else:
                inodeset.add(i[2])
                evolution_dict_temp = dict()
                warning_detail = dict()
                evolution_list = list()
                evolution_dict_temp["time"] = str(i[3]).encode('ascii')
                evolution_dict_temp["value"] = 50
                warning_detail["text"] = i[2].encode('ascii')+":Current="+str(i[1])+"uA"
                evolution_dict_temp["detail"] = warning_detail
                evolution_list.append(evolution_dict_temp)
                warning_dict_temp["name"] = i[2].encode('ascii') #NodeID
                warning_dict_temp["evolution"] = evolution_list
                nodedict[i[2]]=warning_dict_temp
        warning_list_i.append(warning_dict_temp)
    else:
        warning_dict_i = dict()
        warning_dict_temp = dict()
        warning_detail = dict()
        warning_dict_temp["value"] = 30
        warning_dict_temp["time"] = time2.encode('ascii')
        warning_detail["text"] = "No Current Error"
        warning_dict_temp["detail"] = warning_detail
        warning_dict_i["name"] = "None"
        warning_dict_i["evolution"] = [warning_dict_temp]
        warning_list_i.append(warning_dict_i)
    # print warning_list_i
    
    vdata = DATABASE.my_db_execute('select ID, volage, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and volage<3;',(time1, time2))
    if vdata:
        nodedict = dict()
        for v in vdata:            
            warning_dict_temp = dict()
            # warning_dict_i = dict()
            if v[2] in nodedict:
                evolution_dict_temp = dict()
                warning_detail = dict()
                evolution_dict_temp["time"] = str(v[3]).encode('ascii')
                evolution_dict_temp["value"] = 50
                warning_detail["text"] = v[2].encode('ascii')+":Current="+str(v[1])+"uA"
                evolution_dict_temp["detail"] = warning_detail
                evolution_list = nodedict[v[2]]["evolution"]
                evolution_list.append(evolution_dict_temp)
                warning_dict_temp["name"] = v[2].encode('ascii')
                warning_dict_temp["evolution"] = evolution_list
            else:
                vnodeset.add(i[2])
                evolution_dict_temp = dict()
                warning_detail = dict()
                evolution_list = list()
                evolution_dict_temp["time"] = str(v[3]).encode('ascii')
                evolution_dict_temp["value"] = 50
                warning_detail["text"] = v[2].encode('ascii')+":Current="+str(v[1])+"uA"
                evolution_dict_temp["detail"] = warning_detail
                evolution_list.append(evolution_dict_temp)
                warning_dict_temp["name"] = v[2].encode('ascii') #NodeID
                warning_dict_temp["evolution"] = evolution_list
                nodedict[v[2]]=warning_dict_temp
        warning_list_v.append(warning_dict_temp)
    else:
        warning_dict_v = dict()
        warning_dict_temp = dict()
        warning_detail = dict()
        warning_dict_temp["value"] = 30
        warning_dict_temp["time"] = time1.encode('ascii')
        warning_detail["text"] = "No Voltage Error"
        warning_dict_temp["detail"] = warning_detail
        warning_dict_v["name"] = "None"
        warning_dict_v["evolution"] = [warning_dict_temp]
        warning_list_v.append(warning_dict_v)
    # print warning_list_v
    nodeinfo = DATABASE.my_db_execute('select * from NodePlace;',None)
    lists = list() # nodeplace info
    for info in nodeinfo:
        if info[1] in (inodeset | vnodeset):
            lists.append([info[1],info[2],info[3]])

    return warning_list_v,warning_list_i,lists

def syn_error(time1,time2):
    warning_list = list()
    idata = DATABASE.my_db_execute('select NodeID, currenttime, syntime from NetMonitor where currenttime >= ? and currenttime <= ? and (syntime>10 or syntime<-10) ;',(time1, time2))
    for data in idata:
        warning_dict = dict()
        warning_dict["NodeID"] = data[0]
        warning_dict["warn"] = "syntime = " + str(data[2]) + "s"
        warning_dict["time"] = data[1] #currenttime
        warning_list.append(warning_dict)
    return warning_list