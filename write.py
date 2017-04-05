# -*- coding: utf-8 -*-
# @Author: Guoxuenan
# @Date:   2017-01-15 16:49:22
# @Last Modified by:   gxn
# @Last Modified time: 2017-04-02 20:53:17
import time,os,random,sqlite3
# CREATE TABLE NetMonitor(ID INTEGER PRIMARY KEY AUTOINCREMENT,NodeID varchar,
# ParentID varchar, CPU bigint, LPM bigint, TX bigint, RX bigint, volage float, syntime int, beacon int, numneighbors int, rtimetric int, reboot int, cycletime int, cycletimeDirection varchar, Nodecurrenttime time, currenttime time,electric float);

if __name__ == '__main__':
    # conn=sqlite3.connect("/home/winzzhhzzhh/lab/Concentrator_test/topo3.db")
    # c = conn.cursor()
    # c.execute("select distinct nodeID from NetMonitor;") # not NetMonitor but another node.db
    # nodes = list(c.fetchall()) #tuple  -- list
    # # print nodes
    # nodedic = dict()
    # # if request.method == 'POST':
    # for node in nodes:
    #     c.execute("select nodeID, count(nodeID) from NetMonitor where nodeID like ?", (node))
    #     temp = c.fetchall()
    #     print temp
    #     nodedic[temp[0][0]] = temp[0][1]
    # # print nodedic
    # total = len(nodes)
    # now = 0 #total - len(nodes)
    # # if (total > now):
    # #     for no in nodes:
    # #         c.execute("select nodeID, count(nodeID) from NetMonitor where nodeID like ?", (no))
    # #         temp1 = c.fetchall()
    # #         if (temp1[0][1] > nodedic[str(temp1[0][0]).encode('utf-8')]):
    # #             d = tuple(str(temp[0][0]).encode('utf-8'))
    # #             nodes.remove(d)
    # #     time.sleep(5)
    # # now = total - len(nodes)



    conn=sqlite3.connect("/home/winzzhhzzhh/lab/Concentrator_test/datalog/topo3.db")
    c=conn.cursor()
    
    count=0
    while True :
        count+=1
        parentID=str(hex(count%30)[2:])
        nodeid=str(hex(count%30)[2:])#random.randint()
        cpu=rx=lpm=tx=100
        volage=2.5
        syntime=1
        beacon =100
        numneighbors=100
        rtimetric=10
        reboot =2
        cycletime=10
        direction ='up'
        Nodecurrenttime='2022-10-17 13:22:22'
        currenttime="2022-2-22 22:22:22"
        electric=10.3
        t=(None,nodeid,parentID,cpu,lpm,tx,rx,volage,syntime,beacon,numneighbors,rtimetric,reboot,cycletime,direction,Nodecurrenttime,currenttime,electric)
        # print t
        c.execute("INSERT INTO NetMonitor VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",t)
        # c.execute("INSERT INTO NetMonitor VALUES (null, 2, 1, 100, 100, 100, 100, 2.5, 1, 100, 100, 10, 2, 10, 'up','2022-10-17 13:22:22', '2022-2-22 22:22:22', 10.3);")
        conn.commit()
        # c.execute("select distinct nodeID from NetMonitor;") # not NetMonitor but another node.db
        # nodes = list(c.fetchall()) #tuple  -- list
        # nodedic = dict()
        # for node in nodes:
        #     c.execute("select nodeID, count(nodeID) from NetMonitor where nodeID like ?", (node))
        #     temp = c.fetchall()
        #     print temp
        time.sleep(1)
    
    


conn.close()

