#coding=utf-8
#from app import app
import socket,os,struct

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',12310))

#    filePath=os.path.join(app.config['TOPO_FOLDER'],"topo.txt")
filepath = os.path.abspath('/home/winzzhhzzhh/lab/Concentrator/datalog/topo.txt')
  
fileinfo_size=struct.calcsize('128sl') #定义打包规则
#定义文件头信息，包含文件名和文件大小
fhead = struct.pack('128sl',os.path.basename(filepath),os.stat(filepath).st_size)
s.send(fhead) 
fo = open(filepath,'rb')
while True:
    filedata = fo.read(1024)
    if not filedata:
        break
    s.send(filedata)
fo.close()
print 'send over...'
#s.close()