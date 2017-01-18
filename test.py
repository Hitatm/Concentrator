# -*- coding: utf-8 -*-
# @Author: Guoxuenan
# @Date:   2016-12-22 16:58:50
# @Last Modified by:   Guoxuenan
# @Last Modified time: 2017-01-02 19:01:38
# import xmlrpclib
# import time
# server=xmlrpclib.Server('http://localhost:9001/RPC2')
# # for x in server.system.listMethods():
#     # print "## "+x+"\n\t"+server.system.methodHelp(x)
# # for x in server.supervisor.getAllConfigInfo():
#     # print x 
# for x in server.supervisor.getAllProcessInfo():
#     x['start'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(0))
#     print x 
# '''{'now': 1482462161, 
# 'group': 'aout', 
# 'description': 'Dec 22 10:31 PM',
# 'pid': 0, 
# 'stderr_logfile': '/home/wangyu/myspace/Concentrator/datalog/testsupervisor/aout.stderr.log',
# 'stop': 1482417079, 
# 'statename': 'STOPPED', 
# 'start': 1482417068, 
# 'state': 0,
# 'stdout_logfile': '/home/wangyu/myspace/Concentrator/datalog/testsupervisor/aout.stdout.log', 
# 'logfile':        '/home/wangyu/myspace/Concentrator/datalog/testsupervisor/aout.stdout.log', 
# 'exitstatus': -1, 
# 'spawnerr': '', 
# 'name': 'aout'
# }'''
# print server.supervisor.getAllProcessInfo()
# print "+++++++++++++++++++++++++"
# print server.supervisor.getIdentification()
# print server.supervisor.getPID()
# print server.supervisor.getProcessInfo('mytest')
# print server.supervisor.getState()
# print server.supervisor.readMainLog(0,0)
# print "==========================1"
# print server.supervisor.readProcessLog('mytest',0,0)
# print "==========================2"
# print server.supervisor.readProcessStderrLog('mytest',0,0)
# print "==========================3"
# print server.supervisor.readProcessStdoutLog('mytest',0,0)
# files=open("/home/wangyu/tempFile",'rb')
# # while files.read(1)!= EOF :
# content=files.read(200)
# # print len(content)
# for x in xrange(len(content)):
# 	print hex(ord(content[x]))

# files.close()

