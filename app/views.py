#coding:UTF-8
__author__ = 'dj'

from app import app
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from forms import Upload, ProtoFilter,User_and_pwd
from utils.upload_tools import allowed_file, get_filetype, random_name
from utils.gxn_topo_handler import getfile_content,getall_topo,showdata_from_id,topo_filter
from utils.gxn_topo_decode  import TopoDecode
from utils.gxn_topo_analyzer import topo_statistic,topo_traffic_statistic,topo_traffic_analyzer
from utils.gxn_get_sys_config import Congfig
from utils.gxn_supervisor import getAllProcessInfo,stopProcess,startProcess,startAllProcesses,stopAllProcesses
import socket
import os
import collections
import time
import sqlite3
#导入函数到模板中
app.jinja_env.globals['enumerate'] = enumerate

#全局变量
PCAP_NAME = ''     #上传文件名
# PD = PcapDecode() #解析器


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


#历史数据时间选择
@app.route('/upload/', methods=['POST', 'GET'])
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if PCAPS==None:
        redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('./upload/upload.html')
    elif request.method == 'POST':
        selectime =request.form.get('time', '')
        flash(u'检索时间:')
        flash(selectime)

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
            try:   
                TOPODATA=getfile_content(str(TopoPath))
            except Exception, e:
                flash(u'error1:' + unicode(e.message))
            try:
                TOPODATA_DICT=getall_topo(TOPODATA,TPDECODE)
            except Exception, e:
                flash(u'error2:' + unicode(e.message))
            flash(u',数据读取成功')
            flash('\n'+str(len(TOPODATA)))
                # flash('\n'+str(len(REALDATA)))
                
            return render_template('./upload/upload.html',selectedtime=selectime)
        except Exception, e:
            flash(u'文件提取,错误信息:' + unicode(e.message))
            return render_template('./upload/upload.html')
    else:
        return render_template('./upload/upload.html')

#--------------------------------------------传文件----------------------------------------------------
@app.route('/client/', methods=['POST', 'GET'])
@app.route('/client', methods=['POST', 'GET'])
def client():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return render_template('./client/client.html')
        

@app.route('/testconnect/', methods=['POST', 'GET'])
@app.route('/testconnect', methods=['POST', 'GET'])
def testconnect():
    cli = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip = socket.gethostbyname(socket.gethostname())
    port = 1111

    cli.connect((ip,port))
    server_reply=cli.recv(65535)

    print server_reply

    cli.close()
    return "aaaaaaaaaa"



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
            databasepath = os.path.join(app.config['TOPO_FOLDER'],"test.db")
            conn = sqlite3.connect(databasepath)
        except Exception, e:
            print("no such database in "+ databasepath)
        c = conn.cursor()
        c.execute('select * from topo;')
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
        dataid = request.args.get('id')
        dataid = int(dataid)
        data = showdata_from_id(TOPODATA_DICT, dataid)
        return data

#协议分析
@app.route('/protoanalyzer/', methods=['POST', 'GET'])
def protoanalyzer():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
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
        # templist.append(tempstr)
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
        Parentnode = dict()
        for node in ID_list:
            ID = node[0].encode('UTF-8') # ID
            ParentID = node[1].encode('UTF-8') # parentID
            if ID in Parentnode:
                continue
            else:
                Parentnode[ID] = ParentID
        nodes = list()
        links = list()
        n = dict()
        m = dict()
        for key ,value in Parentnode.items():
            n = {'category':2, 'name':key}
            nodes.append(n)
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

