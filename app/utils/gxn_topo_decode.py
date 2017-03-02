#coding:UTF-8
__author__ = 'dj'

import time
import os
import sqlite3

numberoftopo = 0

class TopoDecode:
    def __init__(self):
        self.BASE_DIR = os.path.dirname(__file__)        #获取当前文件夹的绝对路径
        self.PROTOCOL_FILE=self.BASE_DIR+'/protocol/TOPOGXN'  #协议配置文件
        with open(self.PROTOCOL_FILE, 'r') as f:
            items = f.readlines()
        self.TOPO_DICT = dict()
        for it in items:
            it = it.strip().strip('\n').strip('\r').strip('\r\n')
            self.TOPO_DICT[it.split(':')[0]] = it.split(':')[1]
        # print str(self.TOPO_DICT)

    #解析以太网层协议
    def topo_decode(self, p):
        data = dict()
        try:
            conn = sqlite3.connect("/home/winzzhhzzhh/lab/Concentrator/test.db")
        except Exception, e:
            print("no such database")

        c = conn.cursor()
        if self.before_decode(p):
            # print p
            q = self.odd_to_newFormat(p)
            # print q
            data['realtimestamp']   =self.getvalueof(self.TOPO_DICT['realtimestamp'],q,'bigendian','null')
            data['nodetimestamp']   =self.getvalueof(self.TOPO_DICT['nodetimestamp'],q,'bigendian',':')
            data['syntimediff']     =int(self.getvalueof(self.TOPO_DICT['syntimediff'],q,'bigendian','null'))
            data['syntimestamp']    =self.getvalueof(self.TOPO_DICT['syntimestamp'],q,'littleendian',':')
            data['ID']              =self.getvalueof(self.TOPO_DICT['ID'],q,'bigendian','null')
            data['ParentID']        =hex(int(self.getvalueof(self.TOPO_DICT['ParentID'],q,'bigendian','null')))[2:]

            data['cpu']             =float(self.getvalueof(self.TOPO_DICT['cpu'],q,'bigendian','null'))
            data['lpm']             =float(self.getvalueof(self.TOPO_DICT['lpm'],q,'bigendian','null'))
            data['transmit']        =float(self.getvalueof(self.TOPO_DICT['transmit'],q,'bigendian','null'))
            data['listen']          =float(self.getvalueof(self.TOPO_DICT['listen'],q,'bigendian','null'))

            # data['cpu']             =str(float(self.getvalueof(self.TOPO_DICT['cpu'],q,'bigendian','null'))/32768)+'s'
            # data['lpm']             =str(float(self.getvalueof(self.TOPO_DICT['lpm'],q,'bigendian','null'))/32768)+'s'
            # data['transmit']        =str(float(self.getvalueof(self.TOPO_DICT['transmit'],q,'bigendian','null'))/32768)+'s'
            # data['listen']          =str(float(self.getvalueof(self.TOPO_DICT['listen'],q,'bigendian','null'))/32768)+'s'

            data['voltage']         =float(self.getvalueof(self.TOPO_DICT['voltage'],q,'bigendian','null'))
            data['BeaconInterval']  =int(self.getvalueof(self.TOPO_DICT['BeaconInterval'],q,'bigendian','null'))
            data['num_of_neighbour']=int(self.getvalueof(self.TOPO_DICT['num_of_neighbour'],q,'bigendian','null'))
            data['rtx']             =int(self.getvalueof(self.TOPO_DICT['rtx'],q,'bigendian','null'))
            data['restarttimes']    =int(self.getvalueof(self.TOPO_DICT['restarttimes'],q,'bigendian','null'))
            data['synparentID']     =str(hex(int(self.getvalueof(self.TOPO_DICT['synparentID'],q,'littleendian','null')))[2:])
            data['synsqnum']        =int(self.getvalueof(self.TOPO_DICT['synsqnum'],q,'bigendian','null'))
            data['synlevel']        =int(self.getvalueof(self.TOPO_DICT['synlevel'],q,'bigendian','null'))
            global numberoftopo#change it to read id
            numberoftopo += 1
            c.execute("INSERT INTO topo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", \
                (numberoftopo, data['synlevel'], data['synsqnum'], data['syntimestamp'], data['restarttimes'], data['rtx'],\
                    data['cpu'], data['num_of_neighbour'], data['BeaconInterval'], data['lpm'], data['syntimediff'],\
                    data['voltage'], data['ParentID'], data['transmit'], data['realtimestamp'], data['nodetimestamp'],\
                    data['ID'], data['synparentID'], data['listen']))
            conn.commit()
            conn.close()

            return data
        else :
            data['realtimestamp']   ='null'
            data['nodetimestamp']   ='null'
            data['syntimediff']     ='null'
            data['syntimestamp']    ='null'
            data['ID']              ='null'
            data['ParentID']        ='null'

            data['cpu']             ='null'
            data['lpm']             ='null'
            data['transmit']        ='null'
            data['listen']          ='null'

            data['voltage']         ='null'
            data['BeaconInterval']  ='null'
            data['num_of_neighbour']='null'
            data['rtx']             ='null'
            data['restarttimes']    ='null'
            data['synparentID']     ='null'
            data['synsqnum']        ='null'
            data['synlevel']        ='null'
            return data

    #检查数据格式是否正确
    def before_decode(self, p):
        if( len(p.split())!=50):
            # print p.split()
            return False
        else:
            return True

    def odd_to_newFormat(self,x):
        index0= x.find('[')
        index1= x.find(']')
        templists= x[index0+1:index1].split(':')
        nodeid=templists[len(templists)-1]
        temp= str(x[0:index0-1].split()[0]+'_'+x[0:index0-1].split()[1])+' '+ nodeid+' '+x[index1+10:] 
        result=temp.split()
        result=result[0:2]+result[5:]
        strs=''
        for x in result:
            strs+=(x+' ')
        return strs
    def getvalueof(self,index,item,pattern,spliter):
        seq=index.split('-')
        start_index= int(seq[0])
        length     = int(seq[1])
        Type       = seq[2]
        items=item.split()[start_index:start_index+length]
        # print start_index,length,Type, items
        # print start_index
        if Type == 'caluate':
            result=0
            if pattern=="bigendian":
                pass
            elif pattern=="littleendian":
                items.reverse()
                pass
            for x in items:
                result=(result<<8)
                if(int(x)<0):
                    result+=(int(x)+256)
                else:
                    result+=int(x)
            return str(result)
        elif Type=='origin':
            result=''
            if pattern=="bigendian":
                for x in items:
                    if( spliter!="null"):
                        result+=(x+spliter)
                    else:
                        result+=x
                if spliter!="null":
                    result=result[0:len(result)-1]
                return result
            elif pattern=="littleendian":
                for x in items:
                    if( spliter!="null"):
                        result=(x+spliter)+result
                    else:
                        result=x+result
                if spliter!="null":
                    result=result[0:len(result)-1]
                return result
        return str(items)



# BASE_DIR = os.path.dirname(__file__)        #获取当前文件夹的绝对路径
# PROTOCOL_FILE=BASE_DIR+'/protocol/TOPOGXN'  #协议配置文件
# print PROTOCOL_FILE
# p=TopoDecode()

