# Concentrator
bulid a web server runing on embedded Linux system, then we can access the control the system via any connected devices such as laptop or android phone


# work record   

|&|time|task|     
|:--|:--|:--|    
|start|2016-11-01|begin|    
|１|2016-11-10|finished login and time select module|    
| 2|2016-11-23|finished topo analyse module and the adjust the web page to adapt to mobile phone display|
|3 |2016-11-24|add web terminal tool for user accessing the Concentrator system|


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

#备忘：

1. 安装shellinbox 支持命令行工具
	sudo apt-get install openssl shellinabox

2.　配置shellinabox
	sudo vim /etc/default/shellinabox 
	配置如下:
	  1 # Should shellinaboxd start automatically              
	  2 SHELLINABOX_DAEMON_START=1              
	  3               
	  4 # TCP port that shellinboxd's webserver listens on              
	  5 SHELLINABOX_PORT=6175              
	  6               
	  7 # Parameters that are managed by the system and usually should not need              
	  8 # changing:              
	  9 #SHELLINABOX_DATADIR=/var/lib/shellinabox              
	 10 #SHELLINABOX_USER=shellinabox              
	 11 #SHELLINABOX_GROUP=shellinabox              
	 12               
	 13 # Any optional arguments (e.g. extra service definitions).  Make sure              
	 14 # that that argument is quoted.              
	 15 #              
	 16 #   Beeps are disabled because of reports of the VLC plugin crashing              
	 17 #   Firefox on Linux/x86_64.              
	 18 #SHELLINABOX_ARGS="--no-beep -t -s /:SSH:192.168.1.152"              
	 19 SHELLINABOX_ARGS="--no-beep -t -s /:AUTH:HOME:/bin/bash"              

3.　重启shellinabox服务 
sudo service shellinabox restart   

４.别忘了配置服务开机自启动

