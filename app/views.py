#coding:UTF-8
__author__ = 'dj'

from app import app
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from forms import Upload, ProtoFilter,User_and_pwd
from utils.upload_tools import allowed_file, get_filetype, random_name
 
from utils.gxn_topo_handler import getfile_content,getall_topo,showdata_from_id,topo_filter
from utils.gxn_topo_decode  import TopoDecode
from utils.gxn_get_sys_config import Config
from utils.connect import Connect
from utils.db_operate import DBClass
from utils.display import multipledisplay,singledisplay,NetID_list,NetID_all,AppID_all,selectall,node_time_display,topo_display,energy_display,flowdisplay,protodisplay,nodesearch_display
from utils.error import data_error_new,syn_error

from utils.old_data_display import Display, Modify
from utils.gxn_supervisor import getAllProcessInfo,stopProcess,startProcess,startAllProcesses,stopAllProcesses

import os
import collections
import time,datetime
from time import strftime
# import sqlite3
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
DATABASE   =DBClass()

# TOPODATA_DICT =collections.OrderedDict()
# TPDECODE   =TopoDecode()

NODE_DICT_NET=dict()
NODE_SET=set()
 

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
        json_dict = configfile.display_config()
        return render_template('./upload/upload.html',json_dict = json_dict)

@app.route('/upload_modify/', methods=['POST', 'GET'])
@app.route('/upload_modify', methods=['POST', 'GET'])
def upload_modify():
    c = Connect()
    config_dicts = c.all_config_json() # read config.json and put all items in this dict
    if request.method == 'POST':
        val1 = request.form.get("id")
        if val1:
            config_dicts["id"] = val1
        val2 = request.form.get("HeartIntSec")
        if val2:
            config_dicts["HeartIntSec"] = val2
        val3 = request.form.get("AckHeartInt")
        if val3:
            config_dicts["AckHeartInt"] = val3
        val4 = request.form.get("rootAddr")
        if val4:
            config_dicts["rootAddr"] = val4
        val5 = request.form.get("ftpuser")
        if val5:
            config_dicts["ftpuser"] = val5
        val6 = request.form.get("ftphost")
        if val6:
            config_dicts["ftphost"] = val6
        val7 = request.form.get("ftpPwd")
        if val7:
            config_dicts["ftpPwd"] = val7
        val8 = request.form.get("ftpPort")
        if val8:
            config_dicts["ftpPort"] = val8
        val9 = request.form.get("serverIp")
        if val9:
            config_dicts["serverIp"] = val9
        json_config_dicts = json.dumps(config_dicts,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True)
        # print json_config_dicts
        # conf_file = os.path.join(app.config['CONFIG_FOLDER'],"config.json")
        # with open(conf_file, 'w') as f:
        #     f.write(json_config_dicts)
        #     f.close()
        c.update_config(json_config_dicts)
        return "It works"
    else:
        return "Error when writing to the config.json file"

# rtmetric展示
@app.route('/rtmetricdisplay/', methods=['POST', 'GET'])
@app.route('/rtmetricdisplay', methods=['POST', 'GET'])
def rtmetricdisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        time1=time.time()
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        rtxdata_list = multipledisplay(start_time,end_time,"rtimetric")
        
        return render_template('./dataanalyzer/rtmetricdisplay.html',rtxdata_list=rtxdata_list[0],time=rtxdata_list[1])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        rtxdata_list = multipledisplay(previous_time,current_time,"rtimetric")
        
        return render_template('./dataanalyzer/rtmetricdisplay.html',rtxdata_list=rtxdata_list[0],time=rtxdata_list[1])
            
#电流随时间变化
@app.route('/currentdisplay/', methods=['POST', 'GET'])
@app.route('/currentdisplay', methods=['POST', 'GET'])
def currentdisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        currentdata_list = multipledisplay(start_time,end_time,"electric")
        return render_template('./dataanalyzer/currentdisplay.html',currentdata_list=currentdata_list[0],time=currentdata_list[1])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        currentdata_list = multipledisplay(previous_time,current_time,"electric")
        return render_template('./dataanalyzer/currentdisplay.html',currentdata_list=currentdata_list[0],time=currentdata_list[1])

#时间同步展示
@app.route('/syntime/', methods=['POST', 'GET'])
@app.route('/syntime', methods=['POST', 'GET'])
def syntime():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        syntimedata_list = multipledisplay(start_time,end_time,"syntime")
        return render_template('./dataanalyzer/syntime.html',syntimedata_list=syntimedata_list[0],time=syntimedata_list[1])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        syntimedata_list = multipledisplay(previous_time,current_time,"syntime")
        return render_template('./dataanalyzer/syntime.html',syntimedata_list=syntimedata_list[0],time=syntimedata_list[1])


# 节点能耗展示
@app.route('/energydisplay/', methods=['POST', 'GET'])
@app.route('/energydisplay', methods=['POST', 'GET'])
def energydisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        ID_list = NetID_list(start_time,end_time)
        data = energy_display(start_time,end_time)
        return render_template('./dataanalyzer/energydisplay.html', nodecount=len(ID_list), ID_list=ID_list, cpu_list=data[0], lpm_list=data[1], tx_list=data[2], rx_list=data[3],time=data[4])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        ID_list = NetID_list(previous_time,current_time)
        data = energy_display(previous_time,current_time)
        return render_template('./dataanalyzer/energydisplay.html', nodecount=len(ID_list), ID_list=ID_list, cpu_list=data[0], lpm_list=data[1], tx_list=data[2], rx_list=data[3],time=data[4])

# 采样电压展示
@app.route('/voltagedisplay/', methods=['POST', 'GET'])
@app.route('/voltagedisplay', methods=['POST', 'GET'])
def voltagedisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        voltagedata_list = multipledisplay(start_time,end_time,"volage")
        return render_template('./dataanalyzer/voltagedisplay.html',voltagedata_list=voltagedata_list[0],time=voltagedata_list[1])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        voltagedata_list = multipledisplay(previous_time,current_time,"volage")
        return render_template('./dataanalyzer/voltagedisplay.html',voltagedata_list=voltagedata_list[0],time=voltagedata_list[1])

#重启情况展示
@app.route('/restartdisplay/', methods=['POST', 'GET'])
@app.route('/restartdisplay', methods=['POST', 'GET'])
def restartdisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        dataset = singledisplay(start_time,end_time,"reboot")
        return render_template('./dataanalyzer/restartdisplay.html', nodecount = len(dataset[0]), ID_list = dataset[0], reboot_list = dataset[1],time=dataset[2])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        dataset = singledisplay(previous_time,current_time,"reboot")
        return render_template('./dataanalyzer/restartdisplay.html', nodecount = len(dataset[0]), ID_list = dataset[0], reboot_list = dataset[1],time=dataset[2])

#节点邻居数展示
@app.route('/nbdisplay/', methods=['POST', 'GET'])
@app.route('/nbdisplay', methods=['POST', 'GET'])
def nbdisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        data_list = multipledisplay(start_time,end_time,"numneighbors")
        return render_template('./dataanalyzer/nbdisplay.html',data_list=data_list[0],time=data_list[1])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        data_list = multipledisplay(previous_time,current_time,"numneighbors")
        return render_template('./dataanalyzer/nbdisplay.html',data_list=data_list[0],time=data_list[1])
#信标间隔展示
@app.route('/beacondisplay/', methods=['POST', 'GET'])
@app.route('/beacondisplay', methods=['POST', 'GET'])
def beacondisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        data_list = multipledisplay(start_time,end_time,"beacon")
        return render_template('./dataanalyzer/beacondisplay.html',data_list=data_list[0],time=data_list[1])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        data_list = multipledisplay(previous_time,current_time,"beacon")
        return render_template('./dataanalyzer/beacondisplay.html',data_list=data_list[0],time=data_list[1])

# 部署信息表
@app.route('/deploy_info/', methods=['POST', 'GET'])
@app.route('/deploy_info', methods=['POST', 'GET'])
def deploy_info():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        nodeplace = DATABASE.my_db_execute("select ID, NodeID, MeterID, Place from NodePlace;",None)
        return render_template('./dataanalyzer/deploy_info.html',nodeplace = nodeplace)

@app.route('/deploy_modify/', methods=['POST', 'GET'])
@app.route('/deploy_modify', methods=['POST', 'GET'])
def deploy_modify():
    flag = 0  #flag==0 未修改 flag==1 修改了 flag==2 NodeID长度过长 flag==3 NodeID长度为3 flag==4 NodeID长度为2 flag==5 NodeID长度为1 flag==1 NodeID长度为4
    if request.method == 'POST':
        ID = request.form["ID"]
        old_data = DATABASE.my_db_execute("select ID, NodeID, MeterID, Place from NodePlace where ID=?;",(ID,))
        # conn.close()          
        NodeID = str(request.form["NodeID"])
        MeterID = str(request.form["MeterID"])
        Place = request.form["Place"]
        if len(NodeID) == 4:
            # print old_data[0]
            if (str(old_data[0][1]) != NodeID):
                flag = 1
            elif (str(old_data[0][2]) != MeterID):
                flag = 1
            elif (old_data[0][3] != Place):
                flag = 1
            else:
                flag = 0
        elif len(NodeID) > 4:
            flag = 2
        elif len(NodeID) == 3:
            flag = 3
        elif len(NodeID) == 2:
            flag = 4
        elif len(NodeID) == 1:
            flag = 5
        # print ID, NodeID, MeterID, Place
        if flag==0:
            return "未进行更改"
        elif flag==2:
            return "节点ID长度过长，请重新输入！(4位)"
        elif flag==3:
            node=DATABASE.my_db_execute("select NodeID from NodePlace where NodeID=?;",("0"+str(NodeID),))
            if node:
                return "Error,节点已存在" #节点已存在
            else:
                DATABASE.db_del_or_insert("delete from NodePlace where ID = ?;",(ID,))
                DATABASE.db_del_or_insert("insert into NodePlace (ID,NodeID,Place,MeterID) VALUES (?,?,?,?);",(ID,str("0"+str(NodeID)),Place,str(MeterID)))
            return "更改成功"
        elif flag==4:
            node=DATABASE.my_db_execute("select NodeID from NodePlace where NodeID=?;",("00"+str(NodeID),))
            if node:
                return "Error,节点已存在" #节点已存在
            else:
                DATABASE.db_del_or_insert("delete from NodePlace where ID = ?;",(ID,))
                DATABASE.db_del_or_insert("insert into NodePlace (ID,NodeID,Place,MeterID) VALUES (?,?,?,?);",(ID,str("00"+str(NodeID)),Place,str(MeterID)))
            return "更改成功"
        elif flag==5:
            node=DATABASE.my_db_execute("select NodeID from NodePlace where NodeID=?;",("000"+str(NodeID),))
            if node:
                return "Error,节点已存在" #节点已存在
            else:
                DATABASE.db_del_or_insert("delete from NodePlace where ID = ?;",(ID,))
                DATABASE.db_del_or_insert("insert into NodePlace (ID,NodeID,Place,MeterID) VALUES (?,?,?,?);",(ID,str("000"+str(NodeID)),Place,str(MeterID)))
            return "更改成功"
        elif flag==1:
            node=DATABASE.my_db_execute("select NodeID from NodePlace where NodeID=?;",(NodeID,))
            if node:
                return "Error,节点已存在" #节点已存在
            else:
                DATABASE.db_del_or_insert("delete from NodePlace where ID = ?;",(ID,))
                DATABASE.db_del_or_insert("insert into NodePlace (ID,NodeID,Place,MeterID) VALUES (?,?,?,?);",(ID,NodeID,Place,str(MeterID)))
            return "更改成功"
        else:
            DATABASE.db_del_or_insert("delete from NodePlace where ID = ?;",(ID,))
            DATABASE.db_del_or_insert("insert into NodePlace (ID,NodeID,Place,MeterID) VALUES (?,?,?,?);",(ID,str(NodeID),Place,str(MeterID)))
            return "更改成功"

@app.route('/deploy_del/', methods=['POST', 'GET'])
@app.route('/deploy_del', methods=['POST', 'GET'])
def deploy_del():
    del_list = list()
    if request.method == 'POST':
        get_list = request.form.getlist("del_list[]")
    for item in get_list:
        del_list.append(item.encode('ascii'))
    # print del_list
    for item in del_list:
        if item:
            DATABASE.db_del_or_insert("delete from NodePlace where ID=? ;",(item,))

    nodeplace = DATABASE.my_db_execute("select ID, NodeID, MeterID, Place from NodePlace;",None)


    return render_template('./dataanalyzer/deploy_info.html',nodeplace = nodeplace)

@app.route('/deploy_add/', methods=['POST', 'GET'])
@app.route('/deploy_add', methods=['POST', 'GET'])
def deploy_add():
    databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
    if request.method == 'POST':
        NodeID = str(request.form["NodeID"])
        MeterID = str(request.form["MeterID"])
        Place = request.form["Place"]
        # print NodeID, MeterID, Place
        if len(NodeID) == 4:
            node=DATABASE.my_db_execute("select NodeID from NodePlace where NodeID=?;",(NodeID,))
            if node:
                return "Error,节点已存在" #节点已存在
            else:
                DATABASE.db_del_or_insert("insert into NodePlace (NodeID,Place,MeterID) VALUES (?,?,?);",(str(NodeID),Place,str(MeterID)))
        elif len(NodeID) > 4:
            return "节点ID长度过长，请重新输入！(4位)"
        elif len(NodeID) == 3:
            node=DATABASE.my_db_execute("select NodeID from NodePlace where NodeID=?;",("0"+str(NodeID),))
            if node:
                return "Error,节点已存在" #节点已存在
            else:
                DATABASE.db_del_or_insert("insert into NodePlace (NodeID,Place,MeterID) VALUES (?,?,?);",("0"+str(NodeID),Place,str(MeterID)))
        elif len(NodeID) == 2:
            node=DATABASE.my_db_execute("select NodeID from NodePlace where NodeID=?;",("00"+str(NodeID),))
            if node:
                return "Error,节点已存在" #节点已存在
            else:
                DATABASE.db_del_or_insert("insert into NodePlace (NodeID,Place,MeterID) VALUES (?,?,?);",("00"+str(NodeID),Place,str(MeterID)))
        elif len(NodeID) == 1:
            node=DATABASE.my_db_execute("select NodeID from NodePlace where NodeID=?;",("000"+str(NodeID),))
            if node:
                return "Error,节点已存在" #节点已存在
            else:
                DATABASE.db_del_or_insert("insert into NodePlace (NodeID,Place,MeterID) VALUES (?,?,?);",("000"+str(NodeID),Place,str(MeterID)))
     
    nodeplace = DATABASE.my_db_execute("select ID, NodeID, MeterID, Place from NodePlace;",None)
    return "添加成功"

#节点信息查询
@app.route('/node_search/', methods=['POST', 'GET'])
@app.route('/node_search', methods=['POST', 'GET'])
def node_search():
    nodeid_list = NetID_all()
    nodeid_list.sort()
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        nodepick  =  request.form['nodeselect']
        data = nodesearch_display(start_time,end_time,nodepick)

        return render_template('./dataanalyzer/node_search.html',
            nodeid=nodepick,nodelist = data[0],cpu=data[1],lpm=data[2],tx=data[3],rx=data[4],
            voltage_list=data[5],time_list_1=data[6],time_list_2=data[7],current_list=data[8],time_list_3=data[9],rtx_list=data[10],deploy=data[11],time=data[12])
    else:
        nodepick    =  nodeid_list[0]
        end_time    = strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        start_time  = strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 6*60*60))
        data = nodesearch_display(start_time,end_time,nodepick)

        return render_template('./dataanalyzer/node_search.html',
            nodeid=str(nodepick),nodelist = data[0],cpu=data[1],lpm=data[2],tx=data[3],rx=data[4],
            voltage_list=data[5],time_list_1=data[6],time_list_2=data[7],current_list=data[8],time_list_3=data[9],rtx_list=data[10],deploy=data[11],time=data[12])

#节点部署信息查询
@app.route('/deploysearch/', methods=['POST', 'GET'])
@app.route('/deploysearch', methods=['POST', 'GET'])
def deploysearch():
    nodeid_list = list()
    nodeid = DATABASE.my_db_execute('select distinct NodeID from NodePlace;',None)
    for i in range(len(nodeid)):
        nodeid_list.append(nodeid[i][0].encode('ascii'))
    nodeid_list.sort()

    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        nodepick  =  request.form['nodeselect']
        # print nodepick
        deploy_info = DATABASE.my_db_execute('select NodeID, MeterID, Place from NodePlace where NodeID == ?;',(nodepick,))
        deploy = list()
        deploy.append(deploy_info[0][0].encode('ascii'))
        deploy.append(deploy_info[0][1].encode('ascii'))
        deploy.append(deploy_info[0][2].encode('ascii'))

        index_of_pick=nodeid_list.index(nodepick)
        temp=nodeid_list[index_of_pick]
        nodeid_list[index_of_pick]=nodeid_list[0]
        nodeid_list[0]=temp
        nodepick  =  "\""+nodepick+"\""

        return render_template('./dataanalyzer/deploysearch.html',
            nodeid=nodepick,nodelist = nodeid_list,deploy=deploy)
    else:

        return render_template('./dataanalyzer/deploysearch.html',
            nodeid="",nodelist = nodeid_list,deploy=[])

@app.route('/network_data/', methods=['POST', 'GET'])
@app.route('/network_data', methods=['POST', 'GET'])
def network_data():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        select = request.form['filter_type']
        nid = request.form['value']
        if select == "all":
            pcaps = DATABASE.my_db_execute("select * from NetMonitor where currenttime >= ? and currenttime <= ?;",(start_time, end_time))
            timedisplay = ("\""+start_time + ' - ' + end_time+u"\",查询所有节点")
        elif select == "ID":
            pcaps = DATABASE.my_db_execute("select * from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;",(start_time, end_time, nid))
            timedisplay = ("\""+start_time + ' - ' + end_time+u"\",节点ID为:\""+nid+"\"")
        elif select == "parentID":
            pcaps = DATABASE.my_db_execute("select * from NetMonitor where currenttime >= ? and currenttime <= ? and ParentID == ?;",(start_time, end_time, nid))
            timedisplay = ("\""+start_time + ' - ' + end_time+u"\",父节点ID为:\""+nid+"\"")
        else:
            pcaps = DATABASE.my_db_execute("select * from NetMonitor where currenttime >= ? and currenttime <= ?;",(start_time, end_time))
            timedisplay = ("\""+start_time + ' - ' + end_time+u"\",查询所有节点")
        return render_template('./dataanalyzer/network_data.html',pcaps=pcaps,length=len(pcaps),time=timedisplay)
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        timedisplay = ("\""+previous_time + ' - ' + current_time+u"\",未选取节点")

        pcaps = DATABASE.my_db_execute("select * from NetMonitor where currenttime >= ? and currenttime <= ?;",(previous_time, current_time))
        return render_template('./dataanalyzer/network_data.html',pcaps=pcaps,length=len(pcaps),time=timedisplay)

@app.route('/app_data/', methods=['POST', 'GET'])
@app.route('/app_data', methods=['POST', 'GET'])
def app_data():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        select = request.form['filter_type']
        nid = request.form['value']
        if select == "all":
            pcaps = DATABASE.my_db_execute("select * from ApplicationData where currenttime >= ? and currenttime <= ?;",(start_time, end_time))
            timedisplay = ("\""+start_time + ' - ' + end_time+u"\",查询所有节点")
        elif select == "ID":
            pcaps = DATABASE.my_db_execute("select * from ApplicationData where currenttime >= ? and currenttime <= ? and NodeID == ?;",(start_time, end_time, nid))
            timedisplay = ("\""+start_time + ' - ' + end_time+u"\",节点ID为:\""+nid+"\"")
        else:
            pcaps = DATABASE.my_db_execute("select * from ApplicationData where currenttime >= ? and currenttime <= ?;",(start_time, end_time)) 
            timedisplay = ("\""+start_time + ' - ' + end_time+u"\",查询所有节点")
        lendict = dict()
        for pcap in pcaps:
            lendict[int(pcap[0])] = len(str(pcap[3]))
        return render_template('./dataanalyzer/app_data.html',appdata=pcaps,lendict = lendict,length=len(pcaps),time=timedisplay)
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        timedisplay = ("\""+previous_time + ' - ' + current_time+u"\",未选取节点")

        pcaps = DATABASE.my_db_execute("select * from ApplicationData where currenttime >= ? and currenttime <= ?;",(previous_time, current_time))
        lendict = dict()
        for pcap in pcaps:
            lendict[int(pcap[0])] = len(str(pcap[3]))
        return render_template('./dataanalyzer/app_data.html',appdata=pcaps,lendict = lendict,length=len(pcaps),time=timedisplay)


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
        # print display_datadict

    return render_template('./client/monitor.html',send_data = send_data, write_data = write_data, adjtime_data = adjtime_data, display_datadict = display_datadict)

@app.route('/instruction_send/', methods=['POST', 'GET'])
@app.route('/instruction_send', methods=['POST', 'GET'])
def instruction_send():
#指令下发
    modify = Modify() #将新配置数据写入配置文件
    sendins = Connect()
    datalist = []
    dicts = {}
    datalist.append("80")
    datalength = ""
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
        else:
            display = Display()
            recvdata = display.send_display() #旧数据

        transmit_type = request.form['mySelect']
        nodeip = request.form['nodeIP']
    if datalength:
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
    # print ins
    
    return render_template('./client/monitor.html',display_datadict=None)

@app.route('/instruction_write/', methods=['POST', 'GET'])
@app.route('/instruction_write', methods=['POST', 'GET'])
def instruction_write():
#指令烧写
    modify = Modify() #将新配置数据写入配置文件
    sendins = Connect()
    datalist = []
    datalist.append("82")
    datalength = ""
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
        else:
            display = Display()
            recvdata = display.write_display() #旧数据
        transmit_type = request.form['mySelect2']
        nodeip = request.form['nodeIP2']
    if datalength:
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
    return render_template('./client/monitor.html',display_datadict=None)
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
    # print ins
    sendins.TCP_send(ins)
    return render_template('./client/monitor.html',display_datadict=None)

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
    # print ins
    return render_template('./client/monitor.html',display_datadict=None)

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
        else:
            display = Display()
            recvdata = display.adjtime_display() #旧数据
    dicts["pama_data"] = recvdata
    dicts["type"] = "pama_corr"
    ins = json.dumps(dicts)
    
    sendins.TCP_send(ins)
    return render_template('./client/monitor.html',display_datadict=None)

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
    # print "adsadsfasdf"
    sendins.TCP_send(ins)
    # return 
    return render_template('./client/monitor.html',display_datadict=None)



@app.route('/update_net/', methods=['POST', 'GET'])
@app.route('/update_net', methods=['POST', 'GET'])
#获取网络监测数据
def update_net():
    global NODE_DICT_NET
    dicts= {}
    for node ,value in NODE_DICT_NET.items():
        # print node,value
        temp = DATABASE.my_db_execute("select nodeID, count(nodeID) from NetMonitor where nodeID == ?", (node,))
        # print temp
        if int(temp[0][1])-value>0:
            # NUMBER_NET+= 1
            if(str(temp[0][0])  in NODE_SET):
                NODE_SET.remove(str(temp[0][0]))
    if len(NODE_DICT_NET):
        dicts["total"] = len(NODE_DICT_NET)
        dicts["now"] = dicts["total"] - len(NODE_SET)
    else:
        dicts["total"] = 1
        dicts["now"] = 0
    ins = json.dumps(dicts)
    # print ins
    return ins

@app.route('/scheduling/',methods=['POST', 'GET'])
def scheduling():
    syn_config = Config()
    l=syn_config.get_active_list()
    dicts={'lists':l}
    lists= json.dumps(dicts,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True)
    return render_template('./client/scheduling.html',scheduleNow=lists)

@app.route('/setall_schedule/',methods=['POST', 'GET'])
@app.route('/setall_schedule',methods=['POST', 'GET'])
def setall_schedule():
    if request.method == 'POST':
        syn_config = Config()
        syn_config.bitmap_checkall()
    return "1"

@app.route('/cancelall_schedule/',methods=['POST', 'GET'])
@app.route('/cancelall_schedule',methods=['POST', 'GET'])
def cancelall_schedule():
    if request.method == 'POST':
        syn_config = Config()
        syn_config.bitmap_cancelall()
    return "2"
@app.route('/recommend_schedule1/',methods=['POST', 'GET'])
@app.route('/recommend_schedule1',methods=['POST', 'GET'])
def recommend_schedule1():
    if request.method == 'POST':
        syn_config = Config()
        syn_config.recommend_schedule1()
    return "2"

@app.route('/recommend_schedule2/',methods=['POST', 'GET'])
@app.route('/recommend_schedule2',methods=['POST', 'GET'])
def recommend_schedule2():
    if request.method == 'POST':
        syn_config = Config()
        syn_config.recommend_schedule2()
    return "2"

@app.route('/recommend_schedule3/',methods=['POST', 'GET'])
@app.route('/recommend_schedule3',methods=['POST', 'GET'])
def recommend_schedule3():
    if request.method == 'POST':
        syn_config = Config()
        syn_config.recommend_schedule3()
    return "2"


    
@app.route('/update_schedule/',methods=['POST', 'GET'])
def update_schedule():
    syn_config = Config()
    sendins = Connect()
    senddicts = {}

    if request.method == 'POST':
        data = request.get_json()
        bitmap_array = data['x']
        if not bitmap_array:
            bitmap_array = [0]*18
        syn_config.set_SynBitMap(bitmap_array)
        config_dict =syn_config.get_New_Synconfig()
        period = data['p']
        config_dict["bitmap"]=syn_config.format_To_SendBitMap(config_dict["bitmap"])
        if period:
            syn_config.get_syn_period(period)
            # config_dict["bitmap"]=syn_config.format_To_SendBitMap(config_dict["bitmap"])
            senddicts["pama_data"] = config_dict
            senddicts["type"] = "pama_syn"
            update_synperiod_ins = json.dumps(senddicts)
            sendins.TCP_send(update_synperiod_ins)
            # print update_synperiod_ins
        else:
            bitmaplist = config_dict["bitmap"]
            subkey = ['minute', 'seqNum', 'level', 'bitmap', 'second', 'hour']
            update_schedule_dict = {key:config_dict[key] for key in subkey}
            senddicts["pama_data"] = update_schedule_dict
            senddicts["type"] = "schedule"
            update_schedule_ins = json.dumps(senddicts)
            config_dict["bitmap"] = bitmaplist
            sendins.TCP_send(update_schedule_ins)  
            # print update_schedule_ins
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
        else:
            display = Display()
            recvdata = display.monitor_update_period_display()
        if (int(recvdata)<16):
            dicts["pama_data"] = "410" + hex(int(recvdata))[2:]
        else:
            dicts["pama_data"] = "41"+ hex(int(recvdata))[2:]
    dicts["type"] = "mcast_ack"
    ins = json.dumps(dicts)
    sendins.TCP_send(ins)
    # print ins
    return render_template('./client/sendmonitor.html')

@app.route('/post_monitor_data/', methods=['POST', 'GET'])
@app.route('/post_monitor_data', methods=['POST', 'GET'])
#上报网络监测数据指令
def post_monitor_data():
    global NODE_DICT_NET
    # global NUMBER_NET
    global NODE_SET
    NODE_SET = set()
    # NUMBER_NET=0
    nodes = list(DATABASE.my_db_execute("select distinct NodeID from NodePlace;",None))
    # nodes = list(c.fetchall()) #tuple  -- list
    total = len(nodes)
    previous = 0 #total - len(nodes)
    now = previous

    sendins = Connect()
    dicts = {}

    if request.method == 'GET':   
        for node in nodes:
            NODE_SET.add(str(node[0]))
            temp = DATABASE.my_db_execute("select nodeID, count(nodeID) from NetMonitor where nodeID == ?", (node))
            NODE_DICT_NET[temp[0][0]] = temp[0][1]
        dicts["pama_data"] = "00"   
        dicts["type"] = "mcast"
        ins = json.dumps(dicts)
        sendins.TCP_send(ins)
        # print ins
   
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
        data = protodisplay(start_time,end_time)
        return render_template('./dataanalyzer/protoanalyzer.html',num_of_nodes=data[0],postrate=data[1] ,post=data[2], thispostrate=data[3] , http_key=data[4], http_value=data[5] ,nodecount=len(data[4]),time=data[6])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        data = protodisplay(previous_time,current_time)
        return render_template('./dataanalyzer/protoanalyzer.html',num_of_nodes=data[0],postrate=data[1] ,post=data[2], thispostrate=data[3] , http_key=data[4], http_value=data[5] ,nodecount=len(data[4]),time=data[6])

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
        data = flowdisplay(start_time,end_time)
        return render_template('./dataanalyzer/trafficanalyzer.html', timeline=data[0],templist=data[1], topo_traffic_key=data[2],topo_traffic_value=data[3],time=data[4])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        data = flowdisplay(previous_time,current_time)
        return render_template('./dataanalyzer/trafficanalyzer.html', timeline=data[0],templist=data[1], topo_traffic_key=data[2],topo_traffic_value=data[3],time=data[4])

        #上报数量分析
@app.route('/count_appdata/', methods=['POST', 'GET'])
def count_appdata():
    databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        dataset = selectall(start_time,end_time,"ApplicationData")
        return render_template('./dataanalyzer/count_appdata.html',nodelist=dataset[0], countlist=dataset[1],time=dataset[2])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))   
        dataset = selectall(previous_time,current_time,"ApplicationData")
        return render_template('./dataanalyzer/count_appdata.html',nodelist=dataset[0], countlist=dataset[1],time=dataset[2])

# 应用数据分析
@app.route('/appdataanalyzer/', methods=['POST', 'GET'])
def appdataanalyzer():
    nodeid_list = AppID_all()
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        nodepick  =  request.form['nodeselect']
        timelist = node_time_display(start_time,end_time,"ApplicationData",nodepick)
        return render_template('./dataanalyzer/appdataanalyzer.html',timelist=timelist[0], nodelist = nodeid_list,time=timelist[1],node=nodepick)
    else:
        node = DATABASE.my_db_execute('select distinct NodeID from ApplicationData limit 1;',None)
        nodeid = (node[0][0].encode('ascii'))
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))   
        timelist = node_time_display(previous_time,current_time,"ApplicationData",nodeid)
        return render_template('./dataanalyzer/appdataanalyzer.html',timelist=timelist[0], nodelist = nodeid_list,time=timelist[1],node=nodeid)

#网络数据个数随时间变化曲线
@app.route('/netcountdisplay/', methods=['POST', 'GET'])
def netcountdisplay():
    nodeid_list = list()
    appdata = DATABASE.my_db_execute('select distinct NodeID from NetMonitor;',None)
    for i in range(len(appdata)):
        nodeid_list.append(appdata[i][0].encode('ascii'))
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        nodepick  =  request.form['nodeselect']
        timelist = node_time_display(start_time,end_time,"NetMonitor",nodepick)
        return render_template('./dataanalyzer/netcountdisplay.html',timelist=timelist[0], nodelist = nodeid_list,time=timelist[1],node=nodepick)
    else:
        node = DATABASE.my_db_execute('select distinct NodeID from NetMonitor limit 1;',None)
        nodeid = (node[0][0].encode('ascii'))
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))   
        timelist = node_time_display(previous_time,current_time,"NetMonitor",nodeid)
        return render_template('./dataanalyzer/netcountdisplay.html',timelist=timelist[0], nodelist = nodeid_list,time=timelist[1],node=nodeid)

#同步时差随时间变化
@app.route('/syntimediffdisplay/', methods=['POST', 'GET'])
@app.route('/syntimediffdisplay', methods=['POST', 'GET'])
def syntimediffdisplay():
    syntime_list = list()
    time_list = list()
    nodeid_list = NetID_all()
    nodeid_list.sort()

    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        nodepick  =  request.form['nodeselect']

        syntime = DATABASE.my_db_execute('select currenttime, syntime from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;',(start_time, end_time, nodepick))
        for i in range(len(syntime)):
            time_list.append(syntime[i][0].encode('ascii'))
            syntime_list.append(syntime[i][1])
        timedisplay = ("\""+start_time + ' - ' + end_time+"\"").encode('ascii')
        return render_template('./dataanalyzer/syntimediffdisplay.html',
            nodeid=nodepick,nodelist = nodeid_list,time_list=time_list,syntime_list=syntime_list,time=timedisplay)
    else:
        nodepick    =  nodeid_list[0]
        end_time    = strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        start_time  = strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - 6*60*60))

        syntime = DATABASE.my_db_execute('select currenttime, syntime from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;',(start_time, end_time, nodepick))
        for i in range(len(syntime)):
            time_list.append(syntime[i][0].encode('ascii'))
            syntime_list.append(syntime[i][1])
        timedisplay = ("\""+start_time + ' - ' + end_time+"\"").encode('ascii')
        # print nodepick,nodeid_list,cpu,lpm,tx,rx,voltage_list,time_list
        return render_template('./dataanalyzer/syntimediffdisplay.html',
            nodeid=nodepick,nodelist = nodeid_list,time_list=time_list,syntime_list=syntime_list,time=timedisplay)


# 拓扑展示
@app.route('/topodisplay/', methods=['POST', 'GET'])
def topodisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        echarts_start_time = selectime.encode("utf-8")[0:19]
        echarts_end_time = selectime.encode("utf-8")[22:41]
        topodata = topo_display(echarts_start_time,echarts_end_time)

        return render_template('./dataanalyzer/topodisplay.html',nodes = topodata[0], links = topodata[1],time=topodata[2])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        topodata = topo_display(previous_time,current_time)
        # lasttime = DATABASE.my_db_execute("select currenttime from NetMonitor where currenttime >= ? and currenttime <= ? order by currenttime desc LIMIT 1;",(previous_time, current_time))
        # if lasttime:
        #     real_end_time = time.mktime(time.strptime(lasttime[0][0],'%Y-%m-%d %H:%M:%S')) #取选定时间内的最后一个时间，算这个时间与它前十分钟内的数据
        #     real_start_time = real_end_time - 10 * 60
        #     start_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(real_start_time))
        #     end_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(real_end_time))
        #     ID_list = DATABASE.my_db_execute("select NodeID, ParentID from NetMonitor where currenttime >= ? and currenttime <= ?;",(start_time, end_time))
            
        #     for node in ID_list:
        #         ID = node[0] # ID
        #         ParentID = node[1] # parentID
        #         if ID in Parentnode:
        #             continue
        #         else:
        #             Parentnode[ID] = ParentID
        # # 遍历Parentnode的key，绘制散点图；遍历Parentnode的key和value，画箭头
        # nodes = list()
        # links = list()
        # n = dict()
        # m = dict()
        # if lasttime:
        #     if rootID not in Parentnode.keys():
        #         rootIDjson = {"category":3, "name":"root:"+str(rootID.encode('ascii'))}
        #         nodes.append(rootIDjson)
        #         for key ,value in Parentnode.items():
        #             n = {"category":1, "name":key.encode('ascii')}
        #             nodes.append(n)
        #             m = {"source":value.encode('ascii'), "target":key.encode('ascii'), "weight":1}
        #             links.append(m)
        # else:
        #     for key ,value in Parentnode.items():
        #         if key==rootID:
        #             n = {"category":3, "name":key.encode('ascii')}
        #             nodes.append(n)
        #             m = {"source":value.encode('ascii'), "target":key.encode('ascii'), "weight":1}
        #             links.append(m)
        #         else:
        #             n = {"category":1, "name":key.encode('ascii')}
        #             nodes.append(n)
        #             m = {"source":value.encode('ascii'), "target":key.encode('ascii'), "weight":1}
        #             links.append(m)

        return render_template('./dataanalyzer/topodisplay.html',nodes = topodata[0], links = topodata[1],time=topodata[2])



# ----------------------------------------------系统配置工具---------------------------------------------

@app.route('/terminaltool/', methods=['POST', 'GET'])
def terminaltool():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        config=Connect()
        url="http://"+config.all_config_json()["serverIp"]+":6175"
        # print url
        return redirect(url)
        # return render_template('./systemctrl/index.html')

# ----------------------------------------------一异常信息页面---------------------------------------------

#异常数据
@app.route('/exceptinfo/', methods=['POST', 'GET'])
def exceptinfo():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        data = data_error_new(start_time,end_time)
        return render_template('./exceptions/exception.html', vwarning=data[0],iwarning=data[1],lists=data[2],time=data[3])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        # 电流过大
        data = data_error_new(previous_time,current_time)
        return render_template('./exceptions/exception.html', vwarning=data[0],iwarning=data[1],lists=data[2],time=data[3])

#时间同步节点异常列表
@app.route('/synerror/', methods=['POST', 'GET'])
def synerror():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        # 时间同步节点异常
        warning_list = syn_error(start_time,end_time)
        return render_template('./exceptions/synerror.html', warning=warning_list[0],lists=warning_list[1],time=warning_list[2])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        warning_list = syn_error(previous_time,current_time)
        return render_template('./exceptions/synerror.html', warning=warning_list,lists=warning_list[1],time=warning_list[2])




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






@app.route('/test/', methods=['POST', 'GET'])
def test():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    elif request.method == 'POST':
        selectime  =  request.form['field_name']
        start_time = selectime.encode("utf-8")[0:19]
        end_time = selectime.encode("utf-8")[22:41]
        data = data_error_new(start_time,end_time)
        # print data
        return render_template('./upload/timestamp.html', vwarning=data[0],iwarning=data[1])
    else:
        t = time.time()
        current_time = strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
        previous_time = strftime('%Y-%m-%d %H:%M:%S', time.localtime(t - 6*60*60))
        data = data_error_new(previous_time,current_time)
        return render_template('./upload/timestamp.html', vwarning=data[0],iwarning=data[1])
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






 
