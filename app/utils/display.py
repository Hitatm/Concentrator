#coding:UTF-8
from app import app
import time
from time import mktime,strptime,strftime
import sqlite3
from db_operate import DBClass
from gxn_topo_analyzer import topo_statistic
from connect import Connect
from gxn_topo_analyzer import topo_traffic_statistic,topo_traffic_analyzer
from num_of_rounds import countrounds

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

def NetID_all():
    ID_list = list()
    ID_set = DATABASE.my_db_execute("select distinct NodeID from NetMonitor;",None)
    for i in range(len(ID_set)):
        ID_list.append(ID_set[i][0].encode('ascii'))
    return ID_list

def AppID_all():
    ID_list = list()
    ID_set = DATABASE.my_db_execute("select distinct NodeID from ApplicationData;",None)
    for i in range(len(ID_set)):
        ID_list.append(ID_set[i][0].encode('ascii'))
    return ID_list

def singledisplay(time1,time2,dbitem):
    ID_list = NetID_list(time1,time2)
    ID_set = set(ID_list)
    data_dict = dict()
    data = DATABASE.my_db_execute(("select "+ dbitem +",NodeID from NetMonitor where currenttime >= ? and currenttime <= ? order by currenttime asc;"),(time1, time2))
    if len(data)!=0:
        counter=len(data)-1
        while len(ID_set)>0:
            if data[counter][1] in ID_set:
                data_dict[data[counter][1]] = data[counter][0]
                ID_set.remove(data[counter][1])
            counter=counter-1
        data_dict = sorted(data_dict.iteritems(), key=lambda d:d[1], reverse=True)
        ID_list = list()
        data_list = list()
        count=0
        for key, value in data_dict:
            count+=1
            key=key.encode("ascii")
            if count%2!=0:
                key+='      '
            ID_list.append(key)
            data_list.append(value)
    else:
        data_list=[]
    return ID_list,data_list

def energy_display(time1,time2):
    cpu_list = list()
    lpm_list = list()
    tx_list = list()
    rx_list = list()

    ID_list = NetID_list(time1,time2)
    ID_set = set(ID_list)
    energy = DATABASE.my_db_execute("select CPU,LPM,TX,RX,NodeID from NetMonitor where currenttime >= ? and currenttime <= ? order by currenttime asc;",(time1, time2))
    if len(energy)!=0:
        counter=len(energy)-1
        while len(ID_set)>0:
            if energy[counter][4] in ID_set:
                cpu_list.append(round(float(energy[counter][0])/32768,2))
                lpm_list.append(round(float(energy[counter][1])/32768,2))
                tx_list.append(round(float(energy[counter][2])/32768,2))
                rx_list.append(round(float(energy[counter][3])/32768,2))
                ID_set.remove(energy[counter][4])
            counter=counter-1
    return cpu_list,lpm_list,tx_list,rx_list

def flowdisplay(time1,time2):
    topodata_list = DATABASE.my_db_execute("select * from NetMonitor where currenttime >= ? and currenttime <= ?;",(time1, time2))
    topo_traff_dict=topo_traffic_statistic(topodata_list)
    traffic_key_list = list()
    traffic_value_list = list()
    sum_value = 0
    for key ,value in topo_traff_dict.items():
        traffic_key_list.append(key.encode('ascii'))
        sum_value = sum_value+value
        traffic_value_list.append(sum_value)
    lists=topo_traffic_analyzer(topodata_list)
    templist=[lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],lists[7]]
    return lists[0],templist,traffic_key_list,traffic_value_list

def protodisplay(time1,time2):
    num_of_nodes = DATABASE.my_db_execute("select count(distinct NodeID) from NetMonitor;",None)[0][0]
    http_set = selectall(time1,time2,"NetMonitor")
    # 本轮上报个数
    lasttime = DATABASE.my_db_execute("select currenttime from NetMonitor where currenttime >= ? and currenttime <= ? order by currenttime desc LIMIT 1;",(time1, time2))
    if lasttime:
        real_end_time = time.mktime(time.strptime(lasttime[0][0],'%Y-%m-%d %H:%M:%S')) #取选定时间内的最后一个时间，算这个时间与它前十分钟内的数据
        real_start_time = real_end_time - 10 * 60
        rstart_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(real_start_time))
        rend_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(real_end_time))
        post = DATABASE.my_db_execute("select count(distinct NodeID) from NetMonitor where currenttime >= ? and currenttime <= ?;",(rstart_time, rend_time))[0][0]
        thispostrate = round((float(post)/len(http_set[0])), 4) * 100
    else:
        post = "?"
        thispostrate = "?"
    # 根据调度计算所选时间段内轮数
    rounds = countrounds(time1,time2)
    # print rounds
    if rounds:
        allposts = DATABASE.my_db_execute("select count(*) from NetMonitor where currenttime >= ? and currenttime <= ?;",(time1, time2))[0][0]
        postrate = round((float(allposts)/(rounds * num_of_nodes)), 4) * 100
    else:
        postrate = "?"
    return num_of_nodes,postrate,post,thispostrate,http_set[0],http_set[1]

def nodesearch_display(time1,time2,node):
    time_list_1 = list()
    time_list_2 = list()
    voltage_list = list()
    current_list = list()
    nodeid_list = NetID_all()
    nodeid_list.sort()
    cpu ,lpm ,tx ,rx=[0,0,0,0]

    voltage = DATABASE.my_db_execute('select currenttime, volage from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;',(time1, time2, node))
    for i in range(len(voltage)):
        time_list_1.append(voltage[i][0].encode('ascii'))
        voltage_list.append(voltage[i][1])
    current = DATABASE.my_db_execute('select currenttime, electric from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;',(time1, time2, node))
    for i in range(len(current)):
        time_list_2.append(current[i][0].encode('ascii'))
        current_list.append(current[i][1])

    energycost = DATABASE.my_db_execute('select CPU,LPM,TX,RX from NetMonitor where NodeID==? order by ID desc LIMIT 1',(node,))
    cpu= round(float(energycost[0][0])/32768,2)
    lpm= round(float(energycost[0][1])/32768,2)
    tx = round(float(energycost[0][2])/32768,2)
    rx = round(float(energycost[0][3])/32768,2)           

    index_of_pick=nodeid_list.index(node)
    temp=nodeid_list[index_of_pick]
    nodeid_list[index_of_pick]=nodeid_list[0]
    nodeid_list[0]=temp
    nodepick  =  "\""+node+"\""
    return nodeid_list,str(cpu),str(lpm),str(tx),str(rx),voltage_list,time_list_1,time_list_2,current_list


def node_time_display(time1,time2,db,node):
    data = DATABASE.my_db_execute("select currenttime from " + db + " where NodeID==? and currenttime >= ? and currenttime <= ?;",(node, time1, time2))
    count = 0
    timelist = list()
    for time in data:
        time_ms = int(mktime(strptime(time[0],'%Y-%m-%d %H:%M:%S'))*1000)
        count += 1
        timelist.append([time_ms,count])
    dicts = dict()
    dicts["name"] = node.encode('ascii')
    dicts["data"] = timelist
    lists = list()
    lists.append(dicts)
    return lists

def selectall(time1,time2,db):
    data = DATABASE.my_db_execute("select * from " + db + " where currenttime >= ? and currenttime <= ?;",(time1, time2))
    data_dict = topo_statistic(data)
    data_dict = sorted(data_dict.iteritems(), key=lambda d:d[1], reverse=True)
    data_key_list = list()
    data_value_list = list()
    count=0
    for key, value in data_dict:
        count+=1
        if count%2==0:
            data_key_list.append(key.encode('UTF-8'))
        else:
            data_key_list.append(key.encode('UTF-8')+'     ')
        data_value_list.append(value)
    return data_key_list,data_value_list

def topo_display(time1,time2):
    getrootaddr = Connect()
    rootID = getrootaddr.rootaddr()
    lasttime = DATABASE.my_db_execute("select currenttime from NetMonitor where currenttime >= ? and currenttime <= ? order by currenttime desc LIMIT 1;",(time1, time2))
    if lasttime:
        real_end_time = time.mktime(time.strptime(lasttime[0][0],'%Y-%m-%d %H:%M:%S')) #取选定时间内的最后一个时间，算这个时间与它前十分钟内的数据
        real_start_time = real_end_time - 10 * 60
        start_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(real_start_time))
        end_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(real_end_time))
    else:
        return ([],[])
    ID_list = DATABASE.my_db_execute("select distinct NodeID, ParentID from NetMonitor where currenttime >= ? and currenttime <= ?;",(start_time, end_time))
    Parentnode = dict()
    for node in ID_list:
        ID = node[0] # ID
        ParentID = node[1] # parentID
        if ID in Parentnode:
            continue
        else:
            Parentnode[ID] = ParentID
    # 遍历Parentnode的key，绘制散点图；遍历Parentnode的key和value，画箭头

    nodes = list()
    links = list()
    n = dict()
    m = dict()
    if rootID not in Parentnode.keys():
        rootIDjson = {"category":3, "name":"root:"+str(rootID.encode('ascii'))}
        nodes.append(rootIDjson)
        for key ,value in Parentnode.items():
            n = {"category":1, "name":key.encode('ascii')}
            nodes.append(n)
            m = {"source":value.encode('ascii'), "target":key.encode('ascii'), "weight":1}
            links.append(m)
    else:
        for key ,value in Parentnode.items():
            if key==rootID:
                n = {"category":3, "name":key.encode('ascii')}
                nodes.append(n)
                m = {"source":value.encode('ascii'), "target":key.encode('ascii'), "weight":1}
                links.append(m)
            else:
                n = {"category":1, "name":key.encode('ascii')}
                nodes.append(n)
                m = {"source":value.encode('ascii'), "target":key.encode('ascii'), "weight":1}
                links.append(m)
    return nodes,links