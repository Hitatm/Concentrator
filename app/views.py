#coding:UTF-8
__author__ = 'dj'

from app import app
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from flask_socketio import SocketIO
from forms import Upload, ProtoFilter,User_and_pwd
from utils.upload_tools import allowed_file, get_filetype, random_name
# from utils.pcap_decode import PcapDecode
# from utils.pcap_filter import get_all_pcap, proto_filter
# from utils.proto_analyzer import common_proto_statistic, pcap_len_statistic, dns_statistic, most_proto_statistic
# from utils.flow_analyzer import time_flow, data_flow, get_host_ip, data_in_out_ip, proto_flow, most_flow_statistic
# from utils.ipmap_tools import getmyip, get_ipmap, get_geo
# from utils.data_extract import web_data, telnet_ftp_data, mail_data, sen_data
# from utils.except_info import exception_warning
# from utils.file_extract import web_file, ftp_file, mail_file, all_files
#---------------------------------------
from utils.gxn_topo_handler import getfile_content,getall_topo,showdata_from_id,topo_filter
from utils.gxn_topo_decode  import TopoDecode
from utils.gxn_topo_analyzer import topo_statistic,topo_traffic_statistic,topo_traffic_analyzer
from utils.gxn_get_sys_config import Congfig
from utils.gxn_supervisor import getAllProcessInfo,stopProcess,startProcess,startAllProcesses,stopAllProcesses

import os
import collections
import time
import sqlite3
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

#--------------------------------------------传文件----------------------------------------------------
# @app.route('/client/', methods=['POST', 'GET'])
# @app.route('/client', methods=['POST', 'GET'])
# def client():
#     if PCAPS==None:
#         redirect(url_for('login'))
#     if request.method == 'POST':
#         try:
#             clientpath = os.path.join(app.config['CLIENT_FOLDER'],"client.py")
#             os.system("python " + clientpath)
#         except Exception, e:
#             flash(u'发送文件,错误信息:' + unicode(e.message))
#             return render_template('./client/client.html')
#         flash(u'文件传输成功')
#         return render_template('./client/client.html')
#     else:
#         return render_template('./client/client.html')
socketio = SocketIO(app, async_mode="gevent")
@app.route('/client/', methods=['POST', 'GET'])
@app.route('/client', methods=['POST', 'GET'])

def client():
    if PCAPS == None:
        flash(u"请完成认证登陆!")
        return redirect(url_for('login'))
    else:
        return render_template('./client/client.html', async_mode=socketio.async_mode)
        

@socketio.on('my_event')
def test_message(message):
    print(message['data'])

@socketio.on('connectd')
def test_connect1():
    print('Client connecteddddddd')

@socketio.on('connect')
def test_connect2():
    print('Client connected')

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')



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
        #----modified by zzh@2017.1.11
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
        # dns_dict = dns_statistic(PCAPS)
        # dns_dict = sorted(dns_dict.iteritems(), key=lambda d:d[1], reverse=False)
        # dns_key_list = list()
        # dns_value_list = list()
        # for key, value in dns_dict:
        #     dns_key_list.append(key)
        #     dns_value_list.append(value)
        # return render_template('./dataanalyzer/protoanalyzer.html', data=data_dict.values(), pcap_len=pcap_len_dict, pcap_count=pcap_count_dict, http_key=http_key_list, http_value=http_value_list, dns_key=dns_key_list, dns_value=dns_value_list)
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
        # time_flow_dict = time_flow(PCAPS)
        # host_ip = get_host_ip(PCAPS)
        # data_flow_dict = data_flow(PCAPS, host_ip)
        # data_ip_dict = data_in_out_ip(PCAPS, host_ip)
        # proto_flow_dict = proto_flow(PCAPS)
        # most_flow_dict = most_flow_statistic(PCAPS, PD)
        # most_flow_dict = sorted(most_flow_dict.iteritems(), key=lambda d:d[1], reverse=True)
        # if len(most_flow_dict) > 10:
        #     most_flow_dict = most_flow_dict[0:10]
        # most_flow_key = list()
        # for key, value in most_flow_dict:
        #     most_flow_key.append(key)
        # global SYS_CONFIG
        # return render_template('./dataanalyzer/trafficanalyzer.html', time_flow=time_flow_dict, data_flow=data_flow_dict, ip_flow=data_ip_dict, proto_flow=proto_flow_dict.values(), most_flow_key=most_flow_key, most_flow_dict=most_flow_dict)
        # templist=str(lists[1])+','+str(lists[2])+','+str(lists[3])+','+str(lists[4])+','+str(lists[5])+','+str(lists[6])
        # tempstr='''                    {
        #                 name:'4 minute',
        #                 type:'bar',
        #                 stack: 'total',
        #                 itemStyle : { 
        #                 normal:{
        #                 color: '#fff',
        #                 barBorderColor: 'tomato',
        #                 barBorderWidth: 6,
        #                 barBorderRadius:0,
        #                 label :{ 
        #                             show: true, 
        #                             position:top,
        #                             formatter: function (params) 
        #                             {
        #                                 for (var i = 0, l = option.xAxis[0].data.length; i < l; i++) 
        #                                 {
        #                                     if (option.xAxis[0].data[i] == params.name) 
        #                                     {
        #                                         var total=0;
        #                                         for(var j=0,h=option.series.length;j<h;j++)
        #                                           total += option.series[j].data[i] ; 
        #                                           return total 
        #                                     }
        #                                 }
        #                             },
        #                             textStyle: {color: 'tomato'}
        #                         }
        #                         }
        #                     },
        #                 data:{{last_list}}

        #             }'''
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

# ----------------------------------------------文件提取---------------------------------------------
# #WEB文件提取
# @app.route('/webfile/', methods=['POST', 'GET'])
# def webfile():
#     if PCAPS == None:
#         flash(u"请完成认证登陆!")
#         return redirect(url_for('login'))
#     else:
#         host_ip = get_host_ip(PCAPS)
#         web_list = web_file(PCAPS, host_ip, app.config['FILE_FOLDER'] + 'Web/')
#         file_dict = dict()
#         for web in web_list:
#             file_dict[os.path.split(web['filename'])[-1]] = web['filename']
#         file = request.args.get('file')
#         if file in file_dict:
#             return send_from_directory(app.config['FILE_FOLDER'] + 'Web/', file.encode('utf-8'), as_attachment=True)
#         else:
#             return render_template('./fileextract/webfile.html', web_list=web_list)

# #Mail文件提取
# @app.route('/mailfile/', methods=['POST', 'GET'])
# def mailfile():
#     if PCAPS == None:
#         flash(u"请完成认证登陆!")
#         return redirect(url_for('login'))
#     else:
#         host_ip = get_host_ip(PCAPS)
#         mail_list = mail_file(PCAPS, host_ip, app.config['FILE_FOLDER'] + 'Mail/')
#         file_dict = dict()
#         for mail in mail_list:
#             file_dict[os.path.split(mail['filename'])[-1]] = mail['filename']
#         file = request.args.get('file')
#         if file in file_dict:
#             return send_from_directory(app.config['FILE_FOLDER'] + 'Mail/', file, as_attachment=True)
#         else:
#             return render_template('./fileextract/mailfile.html', mail_list=mail_list)


# #FTP文件提取
# @app.route('/ftpfile/', methods=['POST', 'GET'])
# def ftpfile():
#     if PCAPS == None:
#         flash(u"请完成认证登陆!")
#         return redirect(url_for('login'))
#     else:
#         host_ip = get_host_ip(PCAPS)
#         ftp_list = ftp_file(PCAPS, host_ip, app.config['FILE_FOLDER'] + 'FTP/')
#         file_dict = dict()
#         for ftp in ftp_list:
#             file_dict[os.path.split(ftp['filename'])[-1]] = ftp['filename']
#         file = request.args.get('file')
#         if file in file_dict:
#             return send_from_directory(app.config['FILE_FOLDER'] + 'FTP/', file, as_attachment=True)
#         else:
#             return render_template('./fileextract/ftpfile.html', ftp_list=ftp_list)

# #所有二进制文件提取
# @app.route('/allfile/', methods=['POST', 'GET'])
# def allfile():
#     if PCAPS == None:
#         flash(u"请完成认证登陆!")
#         return redirect(url_for('login'))
#     else:
#         allfiles_dict = all_files(PCAPS, app.config['FILE_FOLDER'] + 'All/')
#         file = request.args.get('file')
#         if file in allfiles_dict:
#             return send_from_directory(app.config['FILE_FOLDER'] + 'All/', file, as_attachment=True)
#         else:
#             return render_template('./fileextract/allfile.html', allfiles_dict=allfiles_dict)








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







#-------------------------------upload----------------------------------------------- 
        # return selectime
        # return render_template('./upload/timestamp.html')
        # return render_template('./upload/upload.html')
        # pcap = upload.pcap.data
        # if upload.validate_on_submit():
        #     pcapname = pcap.filename
        #     if allowed_file(pcapname):
        #         name1 = random_name()
        #         name2 = get_filetype(pcapname)
        #         global PCAP_NAME, PCAPS
        #         PCAP_NAME = name1 + name2
        #         try:
        #             pcap.save(os.path.join(app.config['UPLOAD_FOLDER'], PCAP_NAME))
        #             PCAPS = rdpcap(os.path.join(app.config['UPLOAD_FOLDER'], PCAP_NAME))
        #             print PCAPS
        #             flash(u'恭喜你,上传成功！')
        #             return render_template('./upload/upload.html')
        #         except Exception as e:
        #             flash(u'上传错误,错误信息:' + unicode(e.message))
        #             return render_template('./upload/upload.html')
        #     else:
        #         flash(u'上传失败,请上传允许的数据包格式!')
        #         return render_template('./upload/upload.html')
        # else:
        #     return render_template('./upload/upload.html')
