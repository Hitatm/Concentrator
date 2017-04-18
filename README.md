# Concentrator
We are creating a web server running on embedded Linux systems, and having access to the system via any connected devices such as laptops or smart phones.


# work record   

|&|time|task|     
|:--|:--|:--|    
|start|2016-11-01|begin|    
|１|2016-11-10|finished login and time select module|    
| 2|2016-11-23|finished topo analyse module and the adjust the web page to adapt to mobile phone display"|
|3 |2016-11-24|add web terminal tool for user accessing the Concentrator system"|


# 参数
1:时间
2:同步时差
3:端到端时差
4:节点标号
5:父节点
6:能耗
7:电压
8:邻居数
9:BeaconInterval
10:路由度量(rtx)



|标号|例子|index|长度|　条目|
|:--|:--|:--:|:--:|:--|
|1|2016-10-31#09:32:32 　　　|　　　0|1   |真实时间戳  |
|2|aaaa:0:0:0:12:7400:1:f4|   1|1   |节点号  |
|3| 9 32 33               |   2|3   |节点时间戳  |
|4| 0 55 					|   5|2   |父节点ID  |
|5| 0 0 0 13 48 95		|   7|6   |能耗　TYPE_CPU  |
|6| 0 0 42 33 -63 61 		|  13|6   |能耗　TYPE_LPM  |
|7| 0 0 0 0 16 -2 		|  19|6   |能耗　TYPE_TRANSMIT |
|8| 0 0 0 9 41 25 		|  25|6   |能耗　TYPE_LISTEN  |
|9| 14 101 				|  31|2   |采样电压  |
|10| 16 98					|  33|2   |BEACON_INTERVAL  |
|11| 0 60 					|  35|2   |邻居数  |
|12|  3 0 					|  37|2   |INDEX_RTMETRIC  |
|13|  -1 					|  39|1   |同步时差  |
|14|  0 					|  40|1   |重启次数  |
|15|  21 0					|  41|2   |发出同步节点ID  |
|16|  3 35 9   			|  43|3   |接收时间戳  |
|17|  34 					|  46|1   |接收序列号  |
|18| 1 					|  47|1   |时间同步level  |

#数据库格式
0. ID INTEGER PRIMARY KEY AUTOINCREMENT,
1. NodeID varchar, 16
2. ParentID varchar, 12
3. CPU bigint, 6
4. LPM bigint, 9
5. TX bigint, 13
6. RX bigint, 18
7. volage float, 11
8. syntime int, 10 
9. beacon int, 8
10. numneighbors int, 7
11. rtimetric int, 5
12. reboot int, 4
13. cycletime int, 
14. cycletimeDirection varchar,
15. Nodecurrenttime time, 15
16. currenttime time, 14
17. electric float 


##前台与后台通信
instruction1 - 读表与重启指令下发 
具体包括：
1. 周期性读表指令下发
2. 读表指令下发
3. 重启指令下发

instruction2 - 获取网络监测数据
具体包括：
1. PANID
2. channel
3. CCA
4. 发射功率
5. CCA检查周期

instruction3 - 网络参数配置指令下发(0-255之间整数)
具体包括：
data1. PANID
data2. channel
data3. CCA
data4. emitpower - 发射功率
data5. CCAcheckingperiod - CCA检查周期
data6. inactive
data7. DIO_minlen
data8. DIO_max

