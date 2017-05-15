#coding:UTF-8
from app import app
from db_operate import DBClass
import sqlite3

DATABASE = DBClass()
def data_error(time1,time2):
    warning_dict = dict()
    temp_dict = dict()
    warning_list = list()
    idata = DATABASE.my_db_execute('select ID, electric, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and electric>600;',(time1, time2))
    for i in range (len(idata)):
        warning_dict["seqnum"] = idata[i][0]
        warning_dict["warn"] = "current = " + str(idata[i][1]) + "uA"
        warning_dict["ip_port"] = idata[i][2] #NodeID
        warning_dict["time"] = idata[i][3] #currenttime
        warning_list.append(warning_dict)

    vdata = DATABASE.my_db_execute('select ID, volage, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and volage<3;',(time1, time2))       
    for i in range (len(vdata)):
        warning_dict["seqnum"] = vdata[i][0]
        warning_dict["warn"] = "current = " + str(vdata[i][1]) + "V"
        warning_dict["ip_port"] = vdata[i][2] #NodeID
        warning_dict["time"] = vdata[i][3] #currenttime
        warning_list.append(warning_dict)
    return warning_list

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