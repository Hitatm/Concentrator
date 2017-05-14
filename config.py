#coding:UTF-8

WTF_CSRF_ENABLED = False

SECRET_KEY = '!@#$%8F6F98EC3684AECA1DC44E1CB816E4A5^&*()'

#TOPO_FOLDER   = '/root/env/'
#DB_FOLDER     = '/root/env/'
#CLIENT_FOLDER = '/root/Concentrator/socket/'
#CONFIG_FOLDER = '/root/Concentrator/app/utils/Config'

# TOPO_FOLDER   = '/home/wangyu/Downloads/Concentrator/datalog/'
# DB_FOLDER     = '/home/wangyu/Downloads/Concentrator/datalog/'
# CLIENT_FOLDER = '/home/wangyu/Downloads/Concentrator/socket/'
# CONFIG_FOLDER = '/home/wangyu/Downloads/Concentrator/app/utils/Config'

TOPO_FOLDER   = '/home/winzzhhzzhh/lab/Concentrator/datalog/'
DB_FOLDER     = '/home/winzzhhzzhh/lab/Concentrator/datalog/'
CLIENT_FOLDER = '/home/winzzhhzzhh/lab/Concentrator/socket/'
CONFIG_FOLDER = '/home/winzzhhzzhh/lab/Concentrator/app/utils/Config'
'''        
        rtxlist=  list()
        Rtmetric_set = DATABASE.my_db_execute("select NodeID,rtimetric,currenttime from NetMonitor where currenttime >= ? and currenttime <= ?;",(start_time, end_time))
        
        # print Rtmetric_set
        
        for x in Rtmetric_set:
            dicts=dict()
            time_ms = int(time.mktime(time.strptime(x[2],'%Y-%m-%d %H:%M:%S'))*1000)
            dicts["name"] = x[0]
            dicts["data"] = [int(time_ms),int(x[1])]
            rtxlist.append(dicts)     
            # dicts[x[0]].append(x[1]) 
            # {'data': [1493568035000L, 835], 'name': u'0101'}
        print time.time()-time1
        dicttemp=dict()
        for x in rtxlist:
            if x["name"] in dicttemp:
                dicttemp[x["name"]].append(x["data"])
            else:
                dicttemp[x["name"]]=x["data"]
    
        print time.time()-time1
        for key,value in dicttemp.items():
            dicts = dict()
            dicts["name"] = key
            dicts["data"] = value
            rtxdata_list.append(dicts)

        print time.time()-time1
        print rtxdata_list[0]   
'''
