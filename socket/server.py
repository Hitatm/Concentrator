#coding=utf-8

import sys, os
import socket,time,SocketServer,struct,os,thread
host='127.0.1.1'
port=12310
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #定义socket类型
s.bind((host,port)) #绑定需要监听的Ip和端口号，tuple格式
s.listen(1)


def conn_thread(connection,address):  
    # for ct in range (10):
    #     buf0 = connection.recv(1024) # 去掉http请求头
    while True:
        try:
            connection.settimeout(600)
            connection.send('connection success')
            buf = connection.recv(65535)
            if buf:
                print buf
                #connection.close()
        except socket.timeout:
            connection.close()
def main():   
    while True:
        connection,address=s.accept()
        print('Connected by ',address)
        #thread = threading.Thread(target=conn_thread,args=(connection,address)) #使用threading也可以
        #thread.start()
        thread.start_new_thread(conn_thread,(connection,address)) 

# s.close()  
if __name__ == "__main__":  
    try:   
        pid = os.fork()   
        if pid > 0:  
            # exit first parent  
            sys.exit(0)   
    except OSError, e:   
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)   
        sys.exit(1)  
    # decouple from parent environment  
    os.chdir("/")   
    os.setsid()   
    os.umask(0)   
    # do second fork  
    try:   
        pid = os.fork()   
        if pid > 0:  
            # exit from second parent, print eventual PID before  
            print "Daemon PID %d" % pid   
            sys.exit(0)   
    except OSError, e:   
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)   
        sys.exit(1)   
    # start the daemon main loop  
    main()  
# chomd 777 to this folder

