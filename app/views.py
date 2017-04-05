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
from utils.gxn_get_sys_config import Congfig
from utils.gxn_supervisor import getAllProcessInfo,stopProcess,startProcess,startAllProcesses,stopAllProcesses
from utils.jsonconfig import json_config

import os
import collections
import time
import sqlite3
import socket
import json


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
TIME_START = ''
TIME_END   = ''
TOPODATA   = None #login
REALDATA   = None #login
TPDECODE   =TopoDecode()
TOPODATA_DICT =collections.OrderedDict()

serverip = "127.0.1.1"
serverport = 12310
NODE_DICT_NET=dict()
NODE_SET=set()
# SYS_CONFIG = Congfig()
jsconfig = json_config()

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
    if request.method == 'GET':
        # selectime =request.args.get('time')
        return render_template('./upload/upload.html')
        # return render_template('./upload/timestamp.html',time=selectime)
    elif request.method == 'POST':
        selectime =request.form.get('time', '')
        flash(u'检索时间:')
        flash(selectime)
        # return selectime
        # return render_template('./upload/timestamp.html',time=selectime)
        # return render_template('./upload/upload.html')
        # return redirect(url_for('login'))

        # request.args.get
        selectime  =  request.form['field_name']
        global TIME_START,TIME_END
        TIME_START = selectime[0:20]
        TIME_END   = selectime[22:42]
        # comment_message="DateRange: from " + TIME_START+" to "+TIME_END
        if len(selectime)<40:
            flash(u'请选择检索时间!')
        else :
            flash(u'检索时间:'+str(selectime))
        databasepath = os.path.join(app.config['TOPO_FOLDER'],"test.db")
        conn = sqlite3.connect(databasepath)
        c = conn.cursor()
        c.execute("delete from topo;")
        conn.commit()
        conn.close()

        try:
            global TOPODATA,TOPODATA_DICT
            TopoPath=os.path.join(app.config['TOPO_FOLDER'],"topo.txt")
            #DataPath=os.path.join(app.config['DATA_FOLDER'],"data.txt")
            #while True:
            try:   
                TOPODATA=getfile_content(str(TopoPath))
            except Exception, e:
                flash(u'error1:' + unicode(e.message))
            try:
                TOPODATA_DICT=getall_topo(TOPODATA,TPDECODE)
            except Exception, e:
                flash(u'error2:' + unicode(e.message))
            # REALDATA=getfile_content(str(DataPath))
            flash(u',数据读取成功')
            flash('\n'+str(len(TOPODATA)))
                # flash('\n'+str(len(REALDATA)))
                
            return render_template('./upload/upload.html',selectedtime=selectime)
        except Exception, e:
            flash(u'文件提取,错误信息:' + unicode(e.message))
            return render_template('./upload/upload.html')
    else:
        return render_template('./upload/upload.html')

#--------------------------------------------与后台通信----------------------------------------------------
@app.route('/monitor/', methods=['POST', 'GET'])
@app.route('/monitor', methods=['POST', 'GET'])
def monitor():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return render_template('./client/monitor.html')

@app.route('/testconnect/', methods=['POST', 'GET'])
@app.route('/testconnect', methods=['POST', 'GET'])
def testconnect():
    # global serverip, serverport
    # cli=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # cli.connect((serverip,serverport))
    if request.method == 'POST':
        flash(u',信息发送成功')
        data = request.form['emit_data']
        if data:
            print data
    # server_reply=cli.recv(65535)
    # print server_reply
    # cli.close()
    return render_template('./client/monitor.html')

@app.route('/instruction1/', methods=['POST', 'GET'])
@app.route('/instruction1', methods=['POST', 'GET'])
#读表与重启指令下发
def instruction1():
    # insip = jsconfig.get("localhost")
    # insport = jsconfig.get("tcpPort")
    # cli=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # cli.connect((insip,insport))

    if request.method == 'POST':
        ins1 = request.form['readregularly'] # ins = instruction
        if ins1:
            # cli.send(ins+" on all meters")
            print "readregularly on all meters"
        ins2 = request.form["read"]
        if ins2:
            print "read on all meters"
        ins3 = request.form["restart"]
        if ins3:
            print "restart on all meters"

    # server_reply=cli.recv(65535)
    # print server_reply
    # cli.close()
    return render_template('./client/monitor.html')

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
    c.execute("select distinct nodeID from NetMonitor;") # not NetMonitor but another node.db
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
    # print NODE_DICT_NET
    return render_template('./client/monitor.html')

    # insip = jsconfig.get("localhost")
    # insport = jsconfig.get("tcpPort")
    # cli=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # cli.connect((insip,insport))
    # cli.send(ins+" on all meters")
    # server_reply=cli.recv(65535)
    # print server_reply
    # cli.close()



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


@app.route('/instruction3/', methods=['POST', 'GET'])
@app.route('/instruction3', methods=['POST', 'GET'])
#网络参数配置指令下发
def instruction3():
    # # insip = jsconfig.get("localhost")
    # insip = "192.168.0.121"
    # insport = jsconfig.loadjson["tcpPort"]
    # cli=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # cli.connect((insip,insport))
    
    # dicts= {}
    # dicts["pama_data"] = "8205105BF15916"
    # dicts["type"] = "mcast"
    noerror = 1
    data0 = 64*(256**8)
    if request.method == 'POST':
        data1 = request.form['PANID']
        if data1:
            try:
                data1 = int(data1)
            except:
                print ("please input a interger in PANID!")    
            if (data1>=0 and data1<=255):
                data1 = data1*(256**7)
            else:
                noerror = 0
                print "error in data1"
        else:
            data1 = 255*(256**7)
        data2 = request.form['channel']
        if data2:
            try:
                data2 = int(data2)
            except:
                print ("please input a interger in channel!")  
            if (data2>=0 and data2<=255):
                data2 = data2*(256**6)
            else:
                noerror = 0
                print "error in data2"
        else:
            data2 = 255*(256**6)
        data3 = request.form['CCA']
        if data3:
            try:
                data3 = int(data3)
            except:
                print ("please input a interger in CCA!")  
            if (data3>=0 and data3<=255):
                data3 = data3*(256**5)
            else:
                noerror = 0
                print "error in data3"
        else:
            data3 = 255*(256**5)

        data4 = request.form['emitpower']
        if data4:
            try:
                data4 = int(data4)
            except:
                print ("please input a interger in emitpower!")  
            if (data4>=0 and data4<=255):
                data4 = data4*(256**4)
            else:
                noerror = 0
                print "error in data4"
        else:
            data4 = 255*(256**4)
        data5 = request.form['CCAcheckingperiod']
        if data5:
            try:
                data5 = int(data5)
            except:
                print ("please input a interger in CCAcheckingperiod!")  
            if (data5>=0 and data5<=255):
                data5 = data5*(256**3)
            else:
                noerror = 0
                print "error in data5"
        else:
            data5 = 255*(256**3)
        data6 = request.form['inactive']
        if data6:
            try:
                data6 = int(data6)
            except:
                print ("please input a interger in inactive!")  
            if (data6>=0 and data6<=255):
                data6 = data6*(256**2)
            else: 
                noerror = 0
                print "error in data6"
        else:
            data6 = 255*(256**2)
        data7 = request.form['DIO_minlen']
        if data7:
            try:
                data7 = int(data7)
            except:
                print ("please input a interger in DIO_minlen!")  
            if (data7>=0 and data7<=255):
                data7 = data7*(256**1)
            else:
                noerror = 0
                print "error in data7"
        else:
            data7 = 255*(256**1)    
        data8 = request.form['DIO_max']
        if data8:
            try:
                data8 = int(data8)
            except:
                print ("please input a interger in DIO_max!")  
            if (data8>=0 and data8<=255):
                data8 = data8*(256**0)
            else:
                noerror = 0
                print "error in data8"
        else:
            data8 = 255*(256**0)
    if (noerror == 0):
        pass
    else:
        data = hex(data0+data1+data2+data3+data4+data5+data6+data7+data8)
        # cli.send(json.dumps(dicts).encode('utf-8')) hex(180)[2:]
        print data
    # cli.close()
    return render_template('./client/monitor.html')

@app.route('/scheduling/',methods=['POST', 'GET'])
def scheduling():
    l = [2,4,6,8,10]
    # s = ','.join(str(i) for i in l)
    dicts={'lists':l}
    lists= json.dumps(dicts)
    return render_template('./client/scheduling.html',scheduleNow=lists)


@app.route('/update_schedule/',methods=['POST', 'GET'])
def update_schedule():
    if request.method == 'POST':
        data = request.get_json()
        x = data['x']
    print x
    return render_template('./client/scheduling.html')

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
    # global TPDECODE,TOPODATA_DICT
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"topo3.db")
            conn = sqlite3.connect(databasepath)
        except Exception, e:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from topo1;')
        pcaps = c.fetchall()
        conn.close()
        return render_template('./dataanalyzer/basedata.html',pcaps=pcaps)

#详细数据
@app.route('/datashow/', methods=['POST', 'GET'])
def datashow():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        global PDF_NAME
        dataid = request.args.get('id')
        # return dataid
        dataid = int(dataid)
        data = showdata_from_id(TOPODATA_DICT, dataid)
        PDF_NAME = random_name() + '.pdf'
        # TOPODATA[dataid].pdfdump(app.config['PDF_FOLDER'] + PDF_NAME)
        return data

#将数据包保存为pdf
@app.route('/savepdf/', methods=['POST', 'GET'])
def savepdf():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return send_from_directory(app.config['PDF_FOLDER'], PDF_NAME, as_attachment=True)


#协议分析
@app.route('/protoanalyzer/', methods=['POST', 'GET'])
def protoanalyzer():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        #----modified by zzh@2017.1.12
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"test.db")
            conn = sqlite3.connect(databasepath)
        except Exception, e:
            print("no such database in "+databasepath)
        c = conn.cursor()
        c.execute('select * from topo;')
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
    else:
        #----modified by zzh@2017.1.12
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"test.db")
            conn = sqlite3.connect(databasepath)
        except Exception, e:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from topo;')
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


# 其他分析
@app.route('/otheranalyzer/', methods=['POST', 'GET'])
def otheranalyzer():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        topo_traff_dict=topo_traffic_statistic(TOPODATA_DICT)
        traffic_key_list = list()
        traffic_value_list = list()
        for key ,value in topo_traff_dict.items():
            traffic_key_list.append(key)
            traffic_value_list.append(value)
        lists=topo_traffic_analyzer(TOPODATA_DICT)
        templist=[lists[1],lists[2],lists[3],lists[4],lists[5],lists[6],lists[7]]
        templist.append(tempstr)
        return str(templist)


        return render_template('./dataanalyzer/otheranalyzer.html', timeline=lists[0],templist=templist, topo_traffic_key=traffic_key_list,topo_traffic_value=traffic_value_list)

# 拓扑展示
@app.route('/topodisplay/', methods=['POST', 'GET'])
def topodisplay():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        try:
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"test.db")
            conn = sqlite3.connect(databasepath)
        except Exception, e:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select ID, ParentID from topo;')
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
    else:
        return render_template('./exceptions/exception.html')#备注
        dataid = request.args.get('id')
        host_ip = get_host_ip(PCAPS)
        warning_list = exception_warning(PCAPS, host_ip)
        if dataid:
            if warning_list[int(dataid)-1]['data']:
                return warning_list[int(dataid)-1]['data'].replace('\r\n', '<br>')
            else:
                return u'<center><h3>无相关数据包详情</h3></center>'
        else:
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






 
