#coding:UTF-8
__author__ = 'dj'

from app import app
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask_socketio import SocketIO,emit
from forms import Upload, ProtoFilter,User_and_pwd
from utils.upload_tools import allowed_file, get_filetype, random_name
 
from utils.gxn_topo_handler import getfile_content,getall_topo,showdata_from_id,topo_filter
from utils.gxn_topo_decode  import TopoDecode
from utils.gxn_topo_analyzer import topo_statistic,topo_traffic_statistic,topo_traffic_analyzer
from utils.gxn_get_sys_config import Config
from utils.connect import Connect
from utils.old_data_display import Display, Modify
from utils.gxn_supervisor import getAllProcessInfo,stopProcess,startProcess,startAllProcesses,stopAllProcesses

import os
import collections
import time
from time import strftime,gmtime
import sqlite3
import socket
import json
import math


#导入函数到模板中
app.jinja_env.globals['enumerate'] = enumerate

#全局变量
PCAP_NAME = ''     #上传文件名
# PD = PcapDecode() #解析器
PDF_NAME = ''

# ---------------------------------------------------------------------------
PCAPS = 'yeslogin' #login
HIT_USER ='root'#用户名
HIT_PWD  ='xiaoming'  #默认密码
TOPODATA   = None #login
REALDATA   = None #login
TPDECODE   =TopoDecode()
TOPODATA_DICT =collections.OrderedDict()

NODE_DICT_NET=dict()
NODE_SET=set()
# SYS_CONFIG = Congfig()

#--------------------------------------------------------首页，上传---------------------------------------------
#首页
@app.route('/', methods=['POST', 'GET'])
@app.route('/index/', methods=['POST', 'GET'])
def index():
    if PCAPS == None:
        return redirect(url_for('login'))
    else:
        return render_template('./home/index.html')
        # return render_template('./login/login.html')


#历史数据时间选择
@app.route('/upload/', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if PCAPS==None:
        redirect(url_for('login'))
    else:
        json_dict = dict()
        configfile = Connect()
        json_dict = configfile.all_config_json()
        return render_template('./upload/upload.html',json_dict = json_dict)

@app.route('/upload_modify/', methods=['POST', 'GET'])
@app.route('/upload_modify', methods=['POST', 'GET'])
def upload_modify():
    c = Connect()
    config_dicts = c.all_config_json() # read config.json and put all items in this dict
    if request.method == 'POST':
        val1 = request.form.get("localhost")
        if val1:
            config_dicts["localhost"] = val1
        val2 = request.form.get("id")
        if val2:
            config_dicts["id"] = val2
        val3 = request.form.get("HeartIntSec")
        if val3:
            config_dicts["HeartIntSec"] = val3
        val4 = request.form.get("AckHeartInt")
        if val4:
            config_dicts["AckHeartInt"] = val4
        val5 = request.form.get("MaxAckFail")
        if val5:
            config_dicts["MaxAckFail"] = val5
        val6 = request.form.get("tcpAddr")
        if val6:
            config_dicts["tcpAddr"] = val6
        val7 = request.form.get("tcpPort")
        if val7:
            config_dicts["tcpPort"] = val7
        val8 = request.form.get("tcpRemoteConfigPort")
        if val8:
            config_dicts["tcpRemoteConfigPort"] = val8
        val9 = request.form.get("udpAddr")
        if val9:
            config_dicts["udpAddr"] = val9
        val10 = request.form.get("udpPort")
        if val10:
            config_dicts["udpPort"] = val10
        val11 = request.form.get("rootAddr")
        if val11:
            config_dicts["rootAddr"] = val11
        val12 = request.form.get("rootPort")
        if val12:
            config_dicts["rootPort"] = val12
        val13 = request.form.get("rootRoomId")
        if val13:
            config_dicts["rootRoomId"] = val13
        val14 = request.form.get("rootX")
        if val14:
            config_dicts["rootX"] = val14
        val15 = request.form.get("rootY")
        if val15:
            config_dicts["rootY"] = val15
        val16 = request.form.get("dbIpAddr")
        if val16:
            config_dicts["dbIpAddr"] = val16
        val17 = request.form.get("dbUser")
        if val17:
            config_dicts["dbUser"] = val17
        val18 = request.form.get("dbPassword")
        if val18:
            config_dicts["dbPassword"] = val18
        val19 = request.form.get("dbSchema")
        if val19:
            config_dicts["dbSchema"] = val19
        val20 = request.form.get("tcpWebServerAddr")
        if val20:
            config_dicts["tcpWebServerAddr"] = val20
        val21 = request.form.get("tcpWebServerPort")
        if val21:
            config_dicts["tcpWebServerPort"] = val21
        val22 = request.form.get("remoteAddr")
        if val22:
            config_dicts["remoteAddr"] = val22
        val23 = request.form.get("remotePort")
        if val23:
            config_dicts["remotePort"] = val23
        val24 = request.form.get("netPort")
        if val24:
            config_dicts["netPort"] = val24
        val25 = request.form.get("serverIp")
        if val25:
            config_dicts["serverIp"] = val25
        json_config_dicts = json.dumps(config_dicts)
        currentdir = os.path.dirname(__file__)
        conf_file =  currentdir +'/utils/Config/config.json'  #协议配置文件
        with open(conf_file, 'w') as f:
            f.write(json_config_dicts)
            f.close()

        return "It works"
    else:
        return "Error when writing to the config.json file"

# 部署信息表
@app.route('/deploy_info/', methods=['POST', 'GET'])
@app.route('/deploy_info', methods=['POST', 'GET'])
def deploy_info():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
        conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        c.execute("select ID, NodeID, MeterID, Place from NodePlace;")
        nodeplace = c.fetchall()
        conn.close()

        return render_template('./dataanalyzer/deploy_info.html',nodeplace = nodeplace)

@app.route('/deploy_modify/', methods=['POST', 'GET'])
@app.route('/deploy_modify', methods=['POST', 'GET'])
def deploy_modify():
    databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
    if request.method == 'POST': 
        ID = request.form["ID"]  
        NodeID = request.form["NodeID"].encode('ascii')
        MeterID = request.form["MeterID"].encode('ascii')
        Place = request.form["Place"].encode('ascii')
        # print ID, NodeID, MeterID, Place
        conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        c.execute("select ID, NodeID, MeterID, Place from NodePlace where ID=?;",(ID,))
        old_data = c.fetchall()
        conn.close()
        # print old_data[0]
        flag = 0  #flag==0 未修改 flag==1 修改了
        if (old_data[0][1].encode('ascii') != NodeID):
            flag = 1
        if (old_data[0][2].encode('ascii') != MeterID):
            flag = 1
        if (old_data[0][3].encode('ascii') != Place):
            flag = 1
        # print flag
        if flag==0:
            return "未进行更改"
        elif flag==1:
            conn = sqlite3.connect(databasepath)
            c = conn.cursor()
            c.execute("delete from NodePlace where ID = ?;",(ID,))
            conn.commit()
            c.execute("insert into NodePlace (ID,NodeID,Place,MeterID) VALUES (?,?,?,?);",(ID,str(NodeID),str(Place),str(MeterID)))
            conn.commit()
            conn.close()
            return "更改成功"

@app.route('/deploy_del/', methods=['POST', 'GET'])
@app.route('/deploy_del', methods=['POST', 'GET'])
def deploy_del():
    databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
    del_list = list()
    if request.method == 'POST':
        get_list = request.form.getlist("del_list[]")
    for item in get_list:
        del_list.append(item.encode('ascii'))
    # print del_list
    for item in del_list:
        if item:
            conn = sqlite3.connect(databasepath)
            c = conn.cursor()
            c.execute("delete from NodePlace where ID=? ;",(item,))
            conn.commit()
            conn.close()

    conn = sqlite3.connect(databasepath)
    c = conn.cursor()
    c.execute("select ID, NodeID, MeterID, Place from NodePlace;")
    nodeplace = c.fetchall()
    conn.close()

    return render_template('./dataanalyzer/deploy_info.html',nodeplace = nodeplace)

@app.route('/deploy_add/', methods=['POST', 'GET'])
@app.route('/deploy_add', methods=['POST', 'GET'])
def deploy_add():
    databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
    if request.method == 'POST':
        NodeID = request.form["NodeID"].encode('ascii')
        MeterID = request.form["MeterID"].encode('ascii')
        Place = request.form["Place"].encode('ascii')
        # print NodeID, MeterID, Place
        conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        c.execute("select NodeID from NodePlace where NodeID=?;",(NodeID,))
        node = c.fetchall()
        print node
        conn.close()
        if node:
            return "Error,节点已存在" #节点已存在
        else:
            conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        c.execute("insert into NodePlace (NodeID,Place,MeterID) VALUES (?,?,?);",(str(NodeID),str(Place),str(MeterID)))
        conn.commit()
        conn.close()
     
    conn = sqlite3.connect(databasepath)
    c = conn.cursor()
    c.execute("select ID, NodeID, MeterID, Place from NodePlace;")
    nodeplace = c.fetchall()
    conn.close()
    return "添加成功"
    # return render_template('./dataanalyzer/deploy_info.html',nodeplace = nodeplace)

#节点信息查询
@app.route('/node_search/', methods=['POST', 'GET'])
@app.route('/node_search', methods=['POST', 'GET'])
def node_search():
    nodeid_list = list()
    databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
    conn = sqlite3.connect(databasepath)
    c = conn.cursor()
    c.execute('select distinct NodeID from NodePlace;')
    nodeid = c.fetchall()
    conn.close()
    for i in range(len(nodeid)):
        nodeid_list.append(nodeid[i][0].encode('ascii'))  

    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        nodepick  =  request.form['nodeselect']
        databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
        conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        # c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;',(start_time, end_time, nodepick))
        c.execute('select * from NetMonitor where NodeID == ?;',(nodepick,))
        display = c.fetchall()
        # print display
        conn.close()
        conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        # c.execute('select * from ApplicationData where currenttime >= ? and currenttime <= ? and NodeID == ?;',(start_time, end_time, nodepick))
        c.execute('select * from ApplicationData where NodeID == ?;',(nodepick,))
        appdata = c.fetchall()
        # print appdata
        return render_template('./dataanalyzer/node_search.html',nodelist = nodeid_list,pcaps=display,appdata=appdata)
    else:
        return render_template('./dataanalyzer/node_search.html',nodelist = nodeid_list)


#--------------------------------------------与后台通信----------------------------------------------------
@app.route('/monitor/', methods=['POST', 'GET'])
@app.route('/monitor', methods=['POST', 'GET'])
def monitor():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        display = Display()
        send_data = display.send_display() #旧数据展示
        write_data = display.write_display()
        adjtime_data = display.adjtime_display()
        display_datadict = display.parameters_display()

    return render_template('./client/monitor.html',send_data = send_data, write_data = write_data, adjtime_data = adjtime_data, display_datadict = display_datadict)

@app.route('/instruction_send/', methods=['POST', 'GET'])
@app.route('/instruction_send', methods=['POST', 'GET'])
def instruction_send():
#指令下发
    modify = Modify() #将新配置数据写入配置文件
    sendins = Connect()
    datalist = []
    datalist.append("80")
    dicts = {}
    if request.method == 'POST':
        recvdata = request.form['emit_data']
        if recvdata:
            modify.send_modify(recvdata)
            if (len(recvdata)%2 != 0):
                recvdata = "0"+recvdata
            if (len(recvdata)<32):
                datalength = "0"+hex(len(recvdata)/2)[2:]
            else:
                datalength = hex(len(recvdata))[2:]
        transmit_type = request.form['mySelect']
        nodeip = request.form['nodeIP']

    datalist.append(datalength)
    datalist.append(recvdata)
    data = ''.join(datalist)
    dicts["type"] = transmit_type
    dicts["pama_data"] = data
    if (transmit_type=="mcast"):
        ins = json.dumps(dicts)
    else:
        addrlist = []
        addrlist.append(nodeip)
        dicts["addrList"] = addrlist
        ins = json.dumps(dicts)
    sendins.TCP_send(ins)
    
    return render_template('./client/monitor.html')

@app.route('/instruction_write/', methods=['POST', 'GET'])
@app.route('/instruction_write', methods=['POST', 'GET'])
def instruction_write():
#指令烧写
    modify = Modify() #将新配置数据写入配置文件
    sendins = Connect()
    datalist = []
    datalist.append("82")
    dicts = {}
    if request.method == 'POST':
        recvdata = request.form['write_data']
        if recvdata:
            modify.write_modify(recvdata)
            if (len(recvdata)%2 != 0):
                recvdata = "0"+recvdata
            if (len(recvdata)<32):
                datalength = "0"+hex(len(recvdata)/2)[2:]
            else:
                datalength = hex(len(recvdata))[2:]
        transmit_type = request.form['mySelect2']
        nodeip = request.form['nodeIP2']

    datalist.append(datalength)
    datalist.append(recvdata)
    data = ''.join(datalist)
    dicts["type"] = transmit_type
    dicts["pama_data"] = data
    if (transmit_type=="mcast"):
        ins = json.dumps(dicts)
    else:
        addrlist = []
        addrlist.append(nodeip)
        dicts["addrList"] = addrlist

    sendins.TCP_send(ins)
    return render_template('./client/monitor.html')

@app.route('/instruction_restart/', methods=['POST', 'GET'])
@app.route('/instruction_restart', methods=['POST', 'GET'])
#重启指令下发
def instruction_restart():
    sendins = Connect()
    dicts = {}
    dicts["pama_data"] = "C0"
    if request.method == 'POST':
        transmit_type = request.form['mySelect4']
        nodeip = request.form['nodeIP4']
    dicts["type"] = transmit_type
    if (transmit_type=="mcast"):
        ins = json.dumps(dicts)
    else:
        addrlist = []
        addrlist.append(nodeip)
        dicts["addrList"] = addrlist
        ins = json.dumps(dicts)

    sendins.TCP_send(ins)
    return render_template('./client/monitor.html')

@app.route('/instruction_reset/', methods=['POST', 'GET'])
@app.route('/instruction_reset', methods=['POST', 'GET'])
#恢复出厂设置
def instruction_reset():
    sendins = Connect()
    dicts = {}
    dicts["pama_data"] = "C1"
    if request.method == 'POST':
        transmit_type = request.form['mySelect5']
        nodeip = request.form['nodeIP5']
    dicts["type"] = transmit_type
    if (transmit_type=="mcast"):
        ins = json.dumps(dicts)
    else:
        addrlist = []
        addrlist.append(nodeip)
        dicts["addrList"] = addrlist
        ins = json.dumps(dicts)
    
    sendins.TCP_send(ins)
    return render_template('./client/monitor.html')

@app.route('/instruction_adjtime/', methods=['POST', 'GET'])
@app.route('/instruction_adjtime', methods=['POST', 'GET'])
def instruction_adjtime():
#设定根节点校时周期
    modify = Modify() #将新配置数据写入配置文件
    sendins = Connect()
    dicts = {}
    if request.method == 'POST':
        recvdata = request.form['timeperiod']
        if recvdata:
            modify.adjtime_modify(recvdata)
            dicts["pama_data"] = recvdata   
    dicts["type"] = "pama_corr"
    ins = json.dumps(dicts)
    
    sendins.TCP_send(ins)
    return render_template('./client/monitor.html')

@app.route('/instruction3/', methods=['POST', 'GET'])
@app.route('/instruction3', methods=['POST', 'GET'])
#网络参数配置指令下发
def instruction3():
    modify = Modify() #将新配置数据写入配置文件
    sendins = Connect()
    dicts= {}
    dicts["type"] = "mcast_ack"
    data0 = "40"
    datalist = []
    datalist.append(data0)
    if request.method == 'POST':
        data1 = request.form['PANID']
        if data1:
            modify.PANID_modify(data1)
            data1 = hex(int(data1))[2:]
        else:
            data1 = "ff"
        datalist.append(data1)
        data2 = request.form['channel']
        if data2:
            modify.channel_modify(data2)
            data2 = hex(int(data2))[2:]
        else:
            data2 = "ff"
        datalist.append(data2)
        data3 = request.form['CCA']
        if data3:
            modify.CCA_modify(data3)
            data3 = hex(int(data3))[2:]
        else:
            data3 = "ff"
        datalist.append(data3)
        data4 = request.form['emitpower']
        if data4:
            modify.emitpower_modify(data4)
            data4 = hex(int(data4))[2:]
        else:
            data4 = "ff"
        datalist.append(data4)
        data5 = request.form['CCAcheckingperiod']
        if data5:
            modify.CCAcheckingperiod_modify(data5)
            data5 = hex(int(data5))[2:]
        else:
            data5 = "ff"
        datalist.append(data5)
        data6 = request.form['inactive']
        if data6:
            modify.inactive_modify(data6)
            data6 = hex(int(data6))[2:]
        else:
            data6 = "ff"
        datalist.append(data6)
        data7 = request.form['DIO_minlen']
        if data7:
            modify.DIO_minlen_modify(data7)
            data7 = hex(int(data7))[2:]
        else:
            data7 = "ff"
        datalist.append(data7)
        data8 = request.form['DIO_max']
        if data8:
            modify.DIO_max_modify(data8)
            data8 = hex(int(data8))[2:]
        else:
            data8 = "ff"
        datalist.append(data8)
        # cli.send(json.dumps(dicts).encode('utf-8'))
        data = ''.join(datalist)
        dicts["pama_data"] = data
        ins = json.dumps(dicts)

    sendins.TCP_send(ins)
    return render_template('./client/monitor.html')

@app.route('/getdata/', methods=['POST', 'GET'])
@app.route('/getdata', methods=['POST', 'GET'])
def getdata():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return render_template('./client/getdata.html')

@app.route('/instruction2/', methods=['POST', 'GET'])
@app.route('/instruction2', methods=['POST', 'GET'])
def instruction2():
    global NODE_DICT_NET
    # global NUMBER_NET
    global NODE_SET
    NODE_SET = set()
    # NUMBER_NET=0
    databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
    conn = sqlite3.connect(databasepath)
    c = conn.cursor()
    c.execute("select distinct NodeID from NetMonitor;") # not NetMonitor but from NodePlace
    nodes = list(c.fetchall()) #tuple  -- list
    total = len(nodes)
    previous = 0 #total - len(nodes)
    now = previous
    if request.method == 'GET':   
        for node in nodes:
            NODE_SET.add(str(node[0]))
            c.execute("select nodeID, count(nodeID) from NetMonitor where nodeID like ?", (node))
            temp = c.fetchall()
            NODE_DICT_NET[temp[0][0]] = temp[0][1]
    conn.close()
    # print NODE_DICT_NET
    return render_template('./client/getdata.html')


@app.route('/update_net/', methods=['POST', 'GET'])
@app.route('/update_net', methods=['POST', 'GET'])
#获取网络监测数据
def update_net():
    global NODE_DICT_NET
    # global NUMBER_NET
    databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
    conn = sqlite3.connect(databasepath)
    c = conn.cursor()
    for node ,value in NODE_DICT_NET.items():
        # print node,value
        c.execute("select nodeID, count(nodeID) from NetMonitor where nodeID like ?", (node,))
        temp = c.fetchall()
        # print temp
        if int(temp[0][1])-value>0:
            # NUMBER_NET+= 1
            if(str(temp[0][0])  in NODE_SET):
                NODE_SET.remove(str(temp[0][0]))
    dicts= {}
    dicts["total"] = len(NODE_DICT_NET)
    dicts["now"] = dicts["total"] - len(NODE_SET)
    ins = json.dumps(dicts)
    conn.close()
    # print ins
    return ins

@app.route('/scheduling/',methods=['POST', 'GET'])
def scheduling():
    syn_config = Config()
    l=syn_config.get_active_list()
    dicts={'lists':l}
    lists= json.dumps(dicts)
    return render_template('./client/scheduling.html',scheduleNow=lists)


@app.route('/update_schedule/',methods=['POST', 'GET'])
def update_schedule():
    syn_config = Config()
    sendins = Connect()
    senddicts = {}
    if request.method == 'POST':
        period = request.form.get('period')
        if period:
            syn_config.get_syn_period(period)
            f=open(syn_config.Config_FILE,'r')
            config_dict =json.load(f)
            f.close()
            senddicts["pama_data"] = config_dict
            senddicts["type"] = "pama_syn"
            update_synperiod_ins = json.dumps(senddicts)
            sendins.TCP_send(update_synperiod_ins)
        else:
            data = request.get_json()
            x = data['x']
            syn_config.set_SynBitMap(x)
            # print syn_config.get_active_time()
            f=open(syn_config.Config_FILE,'r')
            config_dict =json.load(f)
            f.close()
            bitmaplist = config_dict["bitmap"]
            config_dict["bitmap"] = str(config_dict["bitmap"])
            subkey = ['minute', 'seqNum', 'level', 'bitmap', 'second', 'hour']
            update_schedule_dict = {key:config_dict[key] for key in subkey}
            senddicts["pama_data"] = update_schedule_dict
            senddicts["type"] = "schedule"
            update_schedule_ins = json.dumps(senddicts)
            config_dict["bitmap"] = bitmaplist
            # print update_schedule_ins
            sendins.TCP_send(update_schedule_ins)  

    l=syn_config.get_active_list()
    dicts={'lists':l}
    lists= json.dumps(dicts)

    return render_template('./client/scheduling.html',scheduleNow=lists)

#上报监测控制
@app.route('/sendmonitor/', methods=['POST', 'GET'])
@app.route('/sendmonitor', methods=['POST', 'GET'])
def sendmonitor():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        display = Display()
        display_data = display.monitor_update_period_display() #旧数据展示
        return render_template('./client/sendmonitor.html', display_data = display_data)

@app.route('/monitor_update_period/', methods=['POST', 'GET'])
@app.route('/monitor_update_period', methods=['POST', 'GET'])
# 修改网络监测数据上报周期
def monitor_update_period():
    modify = Modify() #将新配置数据写入配置文件
    sendins = Connect()
    dicts = {}
    if request.method == 'POST':
        recvdata = request.form['update_period']
        if recvdata:
            modify.monitor_update_period_modify(recvdata)
            if (int(recvdata)<16):
                dicts["pama_data"] = "410" + hex(int(recvdata))[2:]
            else:
                dicts["pama_data"] = "41"+ hex(int(recvdata))[2:]   
    dicts["type"] = "mcast_ack"
    ins = json.dumps(dicts)
    sendins.TCP_send(ins)
    return render_template('./client/sendmonitor.html')

@app.route('/post_monitor_data/', methods=['POST', 'GET'])
@app.route('/post_monitor_data', methods=['POST', 'GET'])
#上报网络监测数据指令
def post_monitor_data():
    sendins = Connect()
    dicts = {}
    if request.method == 'POST':
        dicts["pama_data"] = "00"   
    dicts["type"] = "mcast"
    ins = json.dumps(dicts)
    sendins.TCP_send(ins)
    return render_template('./client/sendmonitor.html')

@app.route('/post_config/', methods=['POST', 'GET'])
@app.route('/post_config', methods=['POST', 'GET'])
#上报网络参数配置指令
def post_config():
    sendins = Connect()
    dicts = {}
    if request.method == 'POST':
        dicts["pama_data"] = "01"   
    dicts["type"] = "mcast"
    ins = json.dumps(dicts)
    sendins.TCP_send(ins)
    return render_template('./client/sendmonitor.html')


#--------------------------------------------认证登陆---------------------------------------------------
@app.route('/login/',methods=['POST', 'GET'])
def login():
    login_msg=User_and_pwd()
    if request.method == 'GET':
        return render_template('./login/login.html')
    elif request.method == 'POST':
        USERNAME = login_msg.username.data
        PASSWRD  = login_msg.password.data
        if USERNAME==HIT_USER and PASSWRD==HIT_PWD:
            global PCAPS 
            PCAPS= 'yes:'
            return render_template('./home/index.html')
        else:
            flash(u"用户名或密码错误!")
            return render_template('./login/login.html')

@app.route('/logout/',methods=['POST', 'GET'])
def logout():
    global PCAPS
    PCAPS = None
    return redirect(url_for('login'))


#-------------------------------------------数据分析----------------------------------------------------
#基本数据
@app.route('/basedata/', methods=['POST', 'GET'])
def basedata():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ?;',(start_time, end_time))
        pcaps = c.fetchall()
        conn.close()
        return render_template('./dataanalyzer/basedata.html',pcaps=pcaps)
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        # c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ?;',(previous_time, current_time))
        c.execute('select * from NetMonitor;')
        pcaps = c.fetchall()
        conn.close()
        return render_template('./dataanalyzer/basedata.html',pcaps=pcaps)
        

# #详细数据
# @app.route('/datashow/', methods=['POST', 'GET'])
# def datashow():
#     if PCAPS == None:
#         flash(u"请完成认证登陆!")
#         return redirect(url_for('login'))
#     else:
#         global PDF_NAME
#         dataid = request.args.get('id')
#         # return dataid
#         dataid = int(dataid)
#         data = showdata_from_id(TOPODATA_DICT, dataid)
#         PDF_NAME = random_name() + '.pdf'
#         # TOPODATA[dataid].pdfdump(app.config['PDF_FOLDER'] + PDF_NAME)
#         return data

# #将数据包保存为pdf
# @app.route('/savepdf/', methods=['POST', 'GET'])
# def savepdf():
#     if PCAPS == None:
#         flash(u"请完成认证登陆!")
#         return redirect(url_for('login'))
#     else:
#         return send_from_directory(app.config['PDF_FOLDER'], PDF_NAME, as_attachment=True)


#协议分析
@app.route('/protoanalyzer/', methods=['POST', 'GET'])
def protoanalyzer():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ?;',(start_time, end_time))
        topodata_list = c.fetchall()
        conn.close()
        http_dict = topo_statistic(topodata_list)
        http_dict = sorted(http_dict.iteritems(), key=lambda d:d[1], reverse=True)
        http_key_list = list()
        http_value_list = list()
        count=0
        for key, value in http_dict:
            count+=1
            if count%2==0:
                http_key_list.append(key.encode('UTF-8'))
            else:
                http_key_list.append(key.encode('UTF-8')+'     ')
            http_value_list.append(value)
        return render_template('./dataanalyzer/protoanalyzer.html',http_key=http_key_list, http_value=http_value_list ,nodecount=len(http_key_list))
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ?;',(previous_time, current_time))
        topodata_list = c.fetchall()
        conn.close()
        http_dict = topo_statistic(topodata_list)
        http_dict = sorted(http_dict.iteritems(), key=lambda d:d[1], reverse=True)
        http_key_list = list()
        http_value_list = list()
        count=0
        for key, value in http_dict:
            count+=1
            if count%2==0:
                http_key_list.append(key.encode('UTF-8'))
            else:
                http_key_list.append(key.encode('UTF-8')+'     ')
            http_value_list.append(value)
        return render_template('./dataanalyzer/protoanalyzer.html',http_key=http_key_list, http_value=http_value_list ,nodecount=len(http_key_list))

#流量分析
@app.route('/flowanalyzer/', methods=['POST', 'GET'])
def flowanalyzer():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ?;',(start_time, end_time))
        topodata_list = c.fetchall()
        conn.close()
        topo_traff_dict=topo_traffic_statistic(topodata_list)
        traffic_key_list = list()
        traffic_value_list = list()
        for key ,value in topo_traff_dict.items():
            traffic_key_list.append(key.encode('UTF-8'))
            traffic_value_list.append(value)
 
        lists=topo_traffic_analyzer(topodata_list)
        templist=[lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],lists[7]]
        # templist.append(tempstr)
        # return str(templist)
        return render_template('./dataanalyzer/trafficanalyzer.html', timeline=lists[0],templist=templist, topo_traffic_key=traffic_key_list,topo_traffic_value=traffic_value_list)
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ?;',(previous_time, current_time))
        topodata_list = c.fetchall()
        conn.close()
        topo_traff_dict=topo_traffic_statistic(topodata_list)
        traffic_key_list = list()
        traffic_value_list = list()
        for key ,value in topo_traff_dict.items():
            traffic_key_list.append(key.encode('UTF-8'))
            traffic_value_list.append(value)
 
        lists=topo_traffic_analyzer(topodata_list)
        templist=[lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],lists[7]]
        # templist.append(tempstr)
        # return str(templist)
        return render_template('./dataanalyzer/trafficanalyzer.html', timeline=lists[0],templist=templist, topo_traffic_key=traffic_key_list,topo_traffic_value=traffic_value_list)

# 应用数据分析
@app.route('/appdataanalyzer/', methods=['POST', 'GET'])
def appdataanalyzer():
    nodeid_list = list()
    try:
        databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
        conn = sqlite3.connect(databasepath)
    except:
        print("no such database in "+ databasepath)
    c = conn.cursor()
    c.execute('select distinct NodeID from NodePlace;')
    appdata = c.fetchall()
    for i in range(len(appdata)):
        nodeid_list.append(appdata[i][0].encode('ascii'))
    conn.close()
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        nodepick  =  request.form['nodeselect']
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select currenttime, Data from ApplicationData where currenttime >= ? and currenttime <= ? and NodeID == ?;',(start_time, end_time, nodepick))
        # c.execute('select currenttime, Data from ApplicationData where NodeID == ?;',(nodepick))
        appdata = c.fetchall()
        conn.close()
        dicts= {}
        time_list = list()
        data_list = list()
        for i in range(len(appdata)):
            time_list.append(appdata[i][0].encode('ascii'))
            data_list.append(appdata[i][1].encode('ascii'))
        time_list = sorted(time_list)
        data_list = sorted(data_list)
        return render_template('./dataanalyzer/appdataanalyzer.html',currenttime=time_list,Datalist=data_list,NodeID=nodepick, nodelist = nodeid_list)
    else:
        return render_template('./dataanalyzer/appdataanalyzer.html',nodelist = nodeid_list, currenttime=[],Datalist=[],NodeID="1")
    


# 拓扑展示
@app.route('/topodisplay/', methods=['POST', 'GET'])
def topodisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ?;',(start_time, end_time))
        ID_list = c.fetchall()
        conn.close()
        # print ID_list
        Parentnode = dict()
        # Childnode = dict()
        for node in ID_list:
            ID = node[0].encode('UTF-8') # ID
            ParentID = node[1].encode('UTF-8') # parentID
            if ID in Parentnode:
                continue
            else:
                Parentnode[ID] = ParentID
        # 遍历Parentnode的key，绘制散点图；遍历Parentnode的key和value，画箭头
        nodes = list()
        links = list()
        n = dict()
        m = dict()
        for key ,value in Parentnode.items():
            n = {'category':2, 'name':key}
            # nodes.append("{category:2, name:"+"'"+key+"'}")
            nodes.append(n)
            # links.append("{source : '"+value+"', target : '"+key+"', weight : 1}")
            m = {'source':value, 'target':key, 'weight':1}
            links.append(m)

        return render_template('./dataanalyzer/topodisplay.html', Parentnode = Parentnode ,nodes = nodes, links = links)
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from NetMonitor where currenttime >= ? and currenttime <= ?;',(previous_time, current_time))
        ID_list = c.fetchall()
        conn.close()
        # print ID_list
        Parentnode = dict()
        # Childnode = dict()
        for node in ID_list:
            ID = node[0].encode('UTF-8') # ID
            ParentID = node[1].encode('UTF-8') # parentID
            if ID in Parentnode:
                continue
            else:
                Parentnode[ID] = ParentID
        # 遍历Parentnode的key，绘制散点图；遍历Parentnode的key和value，画箭头
        nodes = list()
        links = list()
        n = dict()
        m = dict()
        for key ,value in Parentnode.items():
            n = {'category':2, 'name':key}
            # nodes.append("{category:2, name:"+"'"+key+"'}")
            nodes.append(n)
            # links.append("{source : '"+value+"', target : '"+key+"', weight : 1}")
            m = {'source':value, 'target':key, 'weight':1}
            links.append(m)

        return render_template('./dataanalyzer/topodisplay.html', Parentnode = Parentnode ,nodes = nodes, links = links)


#访问地图
@app.route('/sysconfig/', methods=['POST', 'GET'])
def sysconfig():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return redirect('http://192.168.1.152:6175/')
        # return render_template('./systemctrl/index.html')


# ----------------------------------------------系统配置工具---------------------------------------------

#访问地图
@app.route('/terminaltool/', methods=['POST', 'GET'])
def terminaltool():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return redirect('http://192.168.1.152:6175/')
        # return render_template('./systemctrl/index.html')
# ----------------------------------------------数据提取页面---------------------------------------------

#Web数据
@app.route('/webdata/', methods=['POST', 'GET'])
def webdata():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return redirect('https://192.168.1.152:6175/')


#Mail数据
@app.route('/maildata/', methods=['POST', 'GET'])
def maildata():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        dataid = request.args.get('id')
        host_ip = get_host_ip(PCAPS)
        mailata_list = mail_data(PCAPS, host_ip)
        if dataid:
            return mailata_list[int(dataid)-1]['data'].replace('\r\n', '<br>')
        else:
            return render_template('./dataextract/maildata.html', maildata=mailata_list)

#FTP数据
@app.route('/ftpdata/', methods=['POST', 'GET'])
def ftpdata():
    if PCAPS == None:
        flash(u"请先上传要分析得数据包!")
        return redirect(url_for('login'))
    else:
        dataid = request.args.get('id')
        host_ip = get_host_ip(PCAPS)
        ftpdata_list = telnet_ftp_data(PCAPS, host_ip, 21)
        if dataid:
            return ftpdata_list[int(dataid)-1]['data'].replace('\r\n', '<br>')
        else:
            return render_template('./dataextract/ftpdata.html', ftpdata=ftpdata_list)

#Telnet数据
@app.route('/telnetdata/', methods=['POST', 'GET'])
def telnetdata():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        dataid = request.args.get('id')
        host_ip = get_host_ip(PCAPS)
        telnetdata_list = telnet_ftp_data(PCAPS, host_ip, 23)
        if dataid:
            return telnetdata_list[int(dataid)-1]['data'].replace('\r\n', '<br>')
        else:
            return render_template('./dataextract/telnetdata.html', telnetdata=telnetdata_list)

#敏感数据
@app.route('/sendata/', methods=['POST', 'GET'])
def sendata():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        dataid = request.args.get('id')
        host_ip = get_host_ip(PCAPS)
        sendata_list = sen_data(PCAPS, host_ip)
        if dataid:
            return sendata_list[int(dataid)-1]['data'].replace('\r\n', '<br>')
        else:
            return render_template('./dataextract/sendata.html', sendata=sendata_list)

# ----------------------------------------------一异常信息页面---------------------------------------------

#异常数据
@app.route('/exceptinfo/', methods=['POST', 'GET'])
def exceptinfo():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        warning_dict = dict()
        warning_list = list() #取交集和并集要多查询两次数据库
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        # 电流过大
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select ID, electric, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and electric>10;',(start_time, end_time))
        # c.execute('select ID, electric, NodeID, currenttime from NetMonitor where electric>10;')
        data = c.fetchall()
        conn.close()
        for i in range (len(data)):
            warning_dict["seqnum"] = data[i][0]
            warning_dict["warn"] = "current = " + str(data[i][1])
            warning_dict["ip_port"] = data[i][2] #NodeID
            warning_dict["time"] = data[i][3] #currenttime
            warning_list.append(warning_dict)
        # 电压过高
        databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
        conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        c.execute('select ID, volage, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and volage>4;',(start_time, end_time))
        error_data = c.fetchall()
        conn.close()
        for i in range (len(data)):
            warning_dict["seqnum"] = data[i][0]
            warning_dict["warn"] = "voltage = " + str(data[i][1])
            warning_dict["ip_port"] = data[i][2] #NodeID
            warning_dict["time"] = data[i][3] #currenttime
            warning_list.append(warning_dict)

        return render_template('./exceptions/exception.html', warning=warning_list)
    else:
        warning_dict = dict()
        warning_list = list()
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        # 电流过大
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select ID, electric, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and electric>10;',(previous_time, current_time))
        data = c.fetchall()
        conn.close()
        for i in range (len(data)):
            warning_dict["seqnum"] = data[i][0]
            warning_dict["warn"] = "current = " + data[i][1]
            warning_dict["ip_port"] = data[i][2] #NodeID
            warning_dict["time"] = data[i][3] #currenttime
            warning_list.append(warning_dict)
        # 电压过高
        databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
        conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        c.execute('select ID, volage, NodeID, currenttime from NetMonitor where currenttime >= ? and currenttime <= ? and volage>2000;',(previous_time, current_time))
        error_data = c.fetchall()
        conn.close()
        for i in range (len(data)):
            warning_dict["seqnum"] = data[i][0]
            warning_dict["warn"] = "current = " + data[i][1]
            warning_dict["ip_port"] = data[i][2] #NodeID
            warning_dict["time"] = data[i][3] #currenttime
            warning_list.append(warning_dict)

        return render_template('./exceptions/exception.html', warning=warning_list)

 





# ----------------------------------------------进程监管---------------------------------------------
#进程监管
@app.route('/supervisor/', methods=['POST', 'GET'])
def supervisor():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        processInfo = getAllProcessInfo()
        return render_template('./supervisor/supervisor.html',processInfo=processInfo)

@app.route('/supervisor_set_status/', methods=['POST', 'GET'])
def supervisor_set_status():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        deal_process = request.args.get('Processname')
        handle       = deal_process.split('_')[0]
        Processname  = deal_process.split('_')[1]
        if handle=='stop':
            stopProcess(Processname)
        if handle=='start':
            startProcess(Processname)
        if handle=='restart':
            stopProcess(Processname)
            startProcess(Processname)
        processInfo  = getAllProcessInfo()
        return render_template('./supervisor/supervisor.html',processInfo=processInfo)

@app.route('/supervisor_restart_all/', methods=['POST', 'GET'])
def supervisor_restart_all():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        stopAllProcesses()
        startAllProcesses()
        processInfo  = getAllProcessInfo()
        return render_template('./supervisor/supervisor.html',processInfo=processInfo)

@app.route('/supervisor_start_all/', methods=['POST', 'GET'])
def supervisor_start_all():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        startAllProcesses()
        processInfo  = getAllProcessInfo()
        return render_template('./supervisor/supervisor.html',processInfo=processInfo)

@app.route('/supervisor_stop_all/', methods=['POST', 'GET'])
def supervisor_stop_all():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        stopAllProcesses()
        processInfo  = getAllProcessInfo()
        return render_template('./supervisor/supervisor.html',processInfo=processInfo)





# ----------------------------------------------数据包构造页面---------------------------------------------
#协议说明
@app.route('/nettools/', methods=['POST', 'GET'])
def nettools():
    return u'网络工具'

@app.route('/protohelp/', methods=['POST', 'GET'])
def protohelp():
    return u'协议说明'

# ----------------------------------------------错误处理页面---------------------------------------------
@app.errorhandler(404)
def internal_error(error):
    return render_template('./error/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('./error/500.html'), 500

@app.route('/about/', methods=['POST', 'GET'])
def about():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return render_template('./home/about.html')






 
