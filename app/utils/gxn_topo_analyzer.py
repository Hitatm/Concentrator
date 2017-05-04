#coding:UTF-8
__author__ = 'dj'

from scapy.all import *
import collections
#数据包大小统计
from gxn_get_sys_config import Config

def pcap_len_statistic(PCAPS):
    pcap_len_dict = {'0-300':0, '301-600':0, '601-900':0, '901-1200':0, '1201-1500':0}
    for pcap in PCAPS:
        pcap_len = len(corrupt_bytes(pcap))
        if 0< pcap_len < 300:
            pcap_len_dict['0-300'] += 1
        elif 301 <= pcap_len < 600:
            pcap_len_dict['301-600'] += 1
        elif 601 <= pcap_len < 900:
            pcap_len_dict['601-900'] += 1
        elif 901 <= pcap_len < 1200:
            pcap_len_dict['901-1200'] += 1
        elif 1201 <= pcap_len <= 1500:
            pcap_len_dict['1201-1500'] += 1
        else:
            pass
    return pcap_len_dict

#常见协议统计IP,IPv6,TCP,UDP,ARP,ICMP,DNS,HTTP,HTTPS,Other
def common_proto_statistic(PCAPS):
    common_proto_dict = collections.OrderedDict()
    common_proto_dict['IP'] = 0
    common_proto_dict['IPv6'] = 0
    common_proto_dict['TCP'] = 0
    common_proto_dict['UDP'] = 0
    common_proto_dict['ARP'] = 0
    common_proto_dict['ICMP'] = 0
    common_proto_dict['DNS'] = 0
    common_proto_dict['HTTP'] = 0
    common_proto_dict['HTTPS'] = 0
    common_proto_dict['Others'] = 0
    for pcap in PCAPS:
        if pcap.haslayer(IP):
            common_proto_dict['IP'] += 1
        elif pcap.haslayer(IPv6):
            common_proto_dict['IPv6'] += 1
        if pcap.haslayer(TCP):
            common_proto_dict['TCP'] += 1
        elif pcap.haslayer(UDP):
            common_proto_dict['UDP'] += 1
        if pcap.haslayer(ARP):
            common_proto_dict['ARP'] += 1
        elif pcap.haslayer(ICMP):
            common_proto_dict['ICMP'] += 1
        elif pcap.haslayer(DNS):
            common_proto_dict['DNS'] += 1
        elif pcap.haslayer(TCP):
            tcp = pcap.getlayer(TCP)
            dport = tcp.dport
            sport = tcp.sport
            if dport == 80 or sport == 80:
                common_proto_dict['HTTP'] += 1
            elif dport == 443 or sport == 443:
                common_proto_dict['HTTPS'] += 1
            else:
                common_proto_dict['Others'] += 1
        elif pcap.haslayer(UDP):
            udp = pcap.getlayer(UDP)
            dport = udp.dport
            sport = udp.sport
            if dport == 5353 or sport == 5353:
                common_proto_dict['DNS'] += 1
            else:
                common_proto_dict['Others'] += 1
        elif pcap.haslayer(ICMPv6ND_NS):
            common_proto_dict['ICMP'] += 1
        else:
            common_proto_dict['Others'] += 1
    return common_proto_dict

#最多协议数量统计
def most_proto_statistic(PCAPS, PD):
    protos_list = list()
    for pcap in PCAPS:
        data = PD.ether_decode(pcap)
        protos_list.append(data['Procotol'])
    most_count_dict = collections.OrderedDict(collections.Counter(protos_list).most_common(10))
    return most_count_dict

#http/https协议统计
def topo_statistic(TOPODATA):
    nodes_dict = dict()
    for item in TOPODATA:
        ID= item[1] #ID
        if ID in nodes_dict:
            nodes_dict[ID]+=1
        else:
            nodes_dict[ID]=1
    return nodes_dict

def appdata_statistic(APPDATA):
    nodes_dict = dict()
    for item in APPDATA:
        ID = item[0]
        if ID in nodes_dict:
            nodes_dict[ID]+=1
        else:
            nodes_dict[ID]=1
    return nodes_dict

def topo_traffic_analyzer(TOPODICT):
    sysCongfig = Config()
    traffic_dict = collections.OrderedDict()
    # date_set=set()
    # print sysCongfig.ACTIVE_TIME
    for items in TOPODICT:
        traffic_item=items[16].split(' ') #realtimestamp
        date=traffic_item[0].replace('-','/').encode('UTF-8')
        ymd=traffic_item[1][:5]
        # print ymd, 
        traffic = date+' '+ymd
        numberof_10= int(ymd.split(':')[0])*6+(int(ymd.split(':')[1]) +2)/10 # +2 是因为允许有节点早到两分钟(的误差)
        real_minutes= int(ymd.split(':')[0])*60+int(ymd.split(':')[1]) #实际的分钟数
        if numberof_10  in sysCongfig.get_active_time():
            # print sysConfig.ACTIVE_TIME[numberof_10]
            base_time=sysCongfig.get_active_time()[numberof_10]
            tempkey= date+' '+base_time
            base_minutes=int(base_time.split(':')[0])*60+int(base_time.split(':')[1])#基准active的分钟
            real_base_diff= real_minutes-base_minutes
            # print traffic,real_base_diff
            if tempkey in traffic_dict:
                if real_base_diff==-1 :
                    traffic_dict[tempkey][1]+=1
                elif real_base_diff==0:
                    traffic_dict[tempkey][2]+=1
                elif real_base_diff==1:
                    traffic_dict[tempkey][3]+=1
                elif real_base_diff==2:
                    traffic_dict[tempkey][4]+=1
                elif real_base_diff==3:
                    traffic_dict[tempkey][5]+=1
                elif real_base_diff==4:
                    traffic_dict[tempkey][6]+=1
                else:
                    traffic_dict[tempkey][0]+=1
            else:
                traffic_dict[tempkey]=[0,0,0,0,0,0,0]
                if real_base_diff==-1 :
                    traffic_dict[tempkey][1]+=1
                elif real_base_diff==0:
                    traffic_dict[tempkey][2]+=1
                elif real_base_diff==1:
                    traffic_dict[tempkey][3]+=1
                elif real_base_diff==2:
                    traffic_dict[tempkey][4]+=1
                elif real_base_diff==3:
                    traffic_dict[tempkey][5]+=1
                elif real_base_diff==4:
                    traffic_dict[tempkey][6]+=1
                else:
                    traffic_dict[tempkey][0]+=1
    return get_traffic_list(traffic_dict)

def get_traffic_list(traffic_dict):
    resultdict=[]
    templist=[[],[],[],[],[],[],[],[]]
    for key ,value in traffic_dict.items():
        templist[0].append(key)
        templist[1].append(value[0])
        templist[2].append(value[1])
        templist[3].append(value[2])
        templist[4].append(value[3])
        templist[5].append(value[4])
        templist[6].append(value[5])
        templist[7].append(value[6])
    # print templist[1]
    tempdict1 ={
    'name':'others',
    'type':'bar',
    'stack': 'total',
    'itemStyle' : { 'normal': {'label' : {'show': 'true','textStyle':{'align':'center'}, 'position': 'inside'}}},
    'data':templist[1] 
    }
    resultdict.append(templist[0])
    resultdict.append(tempdict1)
    for x in xrange(2,8):
        tempdict2 ={
        'name':str(x-3)+' minute',
        'type':'bar',
        'stack': 'total',
        'itemStyle' : { 'normal': {'label' : {'show': 'true','textStyle':{'align':'center'}, 'position': 'inside'}}},
        'data':templist[x]
        }
        resultdict.append(tempdict2)

    return resultdict



def topo_traffic_statistic(TOPODICT):
    traffic_dict = collections.OrderedDict()
    count=0
    for items in TOPODICT:
        traffic_item=items[16].split(' ') #'realtimestamp'
        traffic = traffic_item[0].replace('-','/')+' '+traffic_item[1]
        # print traffic
        if traffic  in traffic_dict:
            traffic_dict[traffic]+=1
        else:
            traffic_dict[traffic]=count
    # print traffic_dict
    return traffic_dict

