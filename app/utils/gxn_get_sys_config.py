#coding:UTF-8
__author__ = 'gxn'

import time,datetime
import os,json
from app import app

class Config:
    def __init__(self):
        self.Config_FILE = os.path.join(app.config['CONFIG_FOLDER'],"GSynConfig.json")
        self.TIME_DICT={0: '00:00:00', 1: '00:10:00', 2: '00:20:00', 3: '00:30:00', 4: '00:40:00', 5: '00:50:00', 6: '01:00:00', 7: '01:10:00', 8: '01:20:00', 9: '01:30:00', 10: '01:40:00', 11: '01:50:00', 12: '02:00:00', 13: '02:10:00', 14: '02:20:00', 15: '02:30:00', 16: '02:40:00', 17: '02:50:00', 18: '03:00:00', 19: '03:10:00', 20: '03:20:00', 21: '03:30:00', 22: '03:40:00', 23: '03:50:00', 24: '04:00:00', 25: '04:10:00', 26: '04:20:00', 27: '04:30:00', 28: '04:40:00', 29: '04:50:00', 30: '05:00:00', 31: '05:10:00', 32: '05:20:00', 33: '05:30:00', 34: '05:40:00', 35: '05:50:00', 36: '06:00:00', 37: '06:10:00', 38: '06:20:00', 39: '06:30:00', 40: '06:40:00', 41: '06:50:00', 42: '07:00:00', 43: '07:10:00', 44: '07:20:00', 45: '07:30:00', 46: '07:40:00', 47: '07:50:00', 48: '08:00:00', 49: '08:10:00', 50: '08:20:00', 51: '08:30:00', 52: '08:40:00', 53: '08:50:00', 54: '09:00:00', 55: '09:10:00', 56: '09:20:00', 57: '09:30:00', 58: '09:40:00', 59: '09:50:00', 60: '10:00:00', 61: '10:10:00', 62: '10:20:00', 63: '10:30:00', 64: '10:40:00', 65: '10:50:00', 66: '11:00:00', 67: '11:10:00', 68: '11:20:00', 69: '11:30:00', 70: '11:40:00', 71: '11:50:00', 72: '12:00:00', 73: '12:10:00', 74: '12:20:00', 75: '12:30:00', 76: '12:40:00', 77: '12:50:00', 78: '13:00:00', 79: '13:10:00', 80: '13:20:00', 81: '13:30:00', 82: '13:40:00', 83: '13:50:00', 84: '14:00:00', 85: '14:10:00', 86: '14:20:00', 87: '14:30:00', 88: '14:40:00', 89: '14:50:00', 90: '15:00:00', 91: '15:10:00', 92: '15:20:00', 93: '15:30:00', 94: '15:40:00', 95: '15:50:00', 96: '16:00:00', 97: '16:10:00', 98: '16:20:00', 99: '16:30:00', 100: '16:40:00', 101: '16:50:00', 102: '17:00:00', 103: '17:10:00', 104: '17:20:00', 105: '17:30:00', 106: '17:40:00', 107: '17:50:00', 108: '18:00:00', 109: '18:10:00', 110: '18:20:00', 111: '18:30:00', 112: '18:40:00', 113: '18:50:00', 114: '19:00:00', 115: '19:10:00', 116: '19:20:00', 117: '19:30:00', 118: '19:40:00', 119: '19:50:00', 120: '20:00:00', 121: '20:10:00', 122: '20:20:00', 123: '20:30:00', 124: '20:40:00', 125: '20:50:00', 126: '21:00:00', 127: '21:10:00', 128: '21:20:00', 129: '21:30:00', 130: '21:40:00', 131: '21:50:00', 132: '22:00:00', 133: '22:10:00', 134: '22:20:00', 135: '22:30:00', 136: '22:40:00', 137: '22:50:00', 138: '23:00:00', 139: '23:10:00', 140: '23:20:00', 141: '23:30:00', 142: '23:40:00', 143: '23:50:00'}

        f=open(self.Config_FILE,'r')
        self.CONFIG_DICT =json.load(f)
        f.close()
    def get_active_time(self):
        # bitlist= self.CONFIG_DICT['bitmap']
        # print self.CONFIG_DICT['bitmap']
        bitlist= self.format_To_originBitMap(self.CONFIG_DICT['bitmap'])
        # print bitlist
        activetime_dict = dict()
        for index,x in enumerate(bitlist):
            # print x,
            val=int(x)
            for y in xrange(0,8):
                if (val<<y) & 0x80==0x80:
                    activetime_dict[(index<<3)+y]=self.TIME_DICT[(index<<3)+y]
        return activetime_dict

    def get_system_time(self):
        hour = time.ctime()[11:13]
        minute = time.ctime()[14:16]
        second = time.ctime()[17:19]
        self.CONFIG_DICT['hour'] = hour
        self.CONFIG_DICT['minute'] = minute
        self.CONFIG_DICT['second'] = second
        self.write_config()
        return 

    def get_syn_period(self,period):
        syn_period = period
        self.CONFIG_DICT['period'] = syn_period
        self.write_config()
        return

    def set_SynBitMap(self,lists):
        listbitmap=[0]*18
        for x in lists:
            index   = (int(x))/8
            index_2 = (int(x))%8
            # data = int(1<<(7-index_2))
            # if data > 127:
            #     data = data - 256
            listbitmap[index]|= (1<<(7-index_2))
            
        # self.CONFIG_DICT['bitmap']=listbitmap
        self.CONFIG_DICT['bitmap']=self.format_To_SendBitMap(listbitmap)
        # print self.CONFIG_DICT
        self.write_config()
        return

    def bitmap_checkall(self):
        lists = [-1]*18
        self.CONFIG_DICT['bitmap']=lists
        self.write_config()
        return

    def bitmap_cancelall(self):
        lists = [0]*18
        self.CONFIG_DICT['bitmap']=lists
        self.write_config()
        return

    def recommend_schedule1(self):
        lists = [-86]*18
        self.CONFIG_DICT['bitmap']=lists
        self.write_config()
        return

    def recommend_schedule2(self):
        lists = [-128, 0, 0, 0, 8, 0, 0, 0, 0, -128, 0, 0, 0, 8, 0, 0, 0, 0]
        self.CONFIG_DICT['bitmap']=lists
        self.write_config()
        return

    def recommend_schedule3(self):
        lists = [-126, 8, 32, -126, 8, 32, -126, 8, 32, -126, 8, 32, -126, 8, 32, -126, 8, 32]
        self.CONFIG_DICT['bitmap']=lists
        self.write_config()
        return

    def get_active_list(self):
        # bitlist= self.CONFIG_DICT['bitmap']
        # print self.CONFIG_DICT['bitmap']
        bitlist= self.format_To_originBitMap(self.CONFIG_DICT['bitmap'])
        # print bitlist
        self.get_system_time()
        active_list = []
        for index,x in enumerate(bitlist):
            # print x,
            val=int(x)
            for y in xrange(0,8):
                if (val<<y) & 0x80==0x80:
                    active_list.append((index<<3)+y)
        return active_list

    def write_config(self):
        self.CONFIG_DICT['bitmap'] = self.format_To_SendBitMap(self.CONFIG_DICT['bitmap'])
        with open(self.Config_FILE, 'w') as f:
            f.write(json.dumps(self.CONFIG_DICT,sort_keys=True,indent =4,separators=(',', ': '),encoding="gbk",ensure_ascii=True))
            f.close()

    def get_New_Synconfig(self):
        f=open(self.Config_FILE,'r')
        self.CONFIG_DICT =json.load(f)
        f.close()
        return self.CONFIG_DICT
    def format_To_SendBitMap(self,lists):
        # print lists
        for x in xrange(0,len(lists)):
            if int(lists[x]) > 127:
                lists[x]= int(lists[x]) - 256
        # print lists
        return lists

    def format_To_originBitMap(self,lists):
        for x in xrange(0,len(lists)):
            if int(lists[x]) < 0:
                lists[x]= int(lists[x]) + 256
        # print lists
        return lists



# sysconfig=Config()
# print sysconfig.format_To_SendBitMap(sysconfig.CONFIG_DICT['bitmap'])
# lists=[1,2,3,4,5,6,7,8,143,123]
# # print "first",sysconfig.CONFIG_DICT
# sysconfig.set_SynBitMap(lists)
# print sysconfig.get_active_list()
# print sysconfig.get_active_time()
# # print "------------------------------------"
# # print "second",sysconfig.CONFIG_DICT
# # print "------------------------------------"
# # sysconfig.write_config()
# print "second",sysconfig.CONFIG_DICT

# for key ,value in sysconfig.TIME_DICT.items():
#     # print key ,value

#     print "<option value="+"\""+str(key) +"\">"+ value[:5]+ "</option>"

