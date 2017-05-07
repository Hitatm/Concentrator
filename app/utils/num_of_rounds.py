#coding:UTF-8
import time,datetime
import os
from gxn_get_sys_config import Config

# 根据调度计算所选时间段内轮数
def countrounds(start_time, end_time):
    g = Config()
    num_in_schedule = len(g.get_active_time()) # 24h中轮数
    get_schedule = g.get_active_time()
    # print get_schedule, num_in_schedule
# 先计算共有多少个小时
    minute = int((time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S')))/60) #minutes
    hour = minute/60
    minutes_left = minute%hour
    # print minute, hour, minutes_left
# 计算有几个整天(24h)
    days = hour/24
    hours_left = hour%24 #不足一天的小时数
    start_time_minutes = start_time.split(' ')[1].split(':')[0]*60 + start_time.split(' ')[1].split(':')[1]
    end_time_minutes = end_time.split(' ')[1].split(':')[0]*60 + end_time.split(' ')[1].split(':')[1]
    if hours_left: #如果不为零，按照调度具体计算落在选取时间内的轮数
        #四种情况
        #2018:1:1 16:00:00 - 2018:1:1 23:00:00
        #2018:1:1 16:00:00 - 2018:1:2 7:00:00
        #2018:1:1 16:00:00 - 2018:1:1 16:20:00
        #2018:1:1 16:20:00 - 2018:1:2 16:00:00/2018:1:1 16:00:00 - 2018:1:2 16:00:00
        if (start_time.split(' ')[1].split(':')[0] != end_time.split(' ')[1].split(':')[0]): #前2种情况
            if start_time[11:13] < end_time[11:13]: # 第一种情况
                count = 0
                #把字典中的时分转化为分，循环与starttime中的时分秒比较，在范围内即count+1
                #{0: '00:00:00', 4: '00:40:00', 6: '01:00:00', 138: '23:00:00', 12: '02:00:00', 18: '03:00:00', 24: '04:00:00', 132: '22:00:00', 30: '05:00:00', 36: '06:00:00', 42: '07:00:00', 48: '08:00:00', 54: '09:00:00', 60: '10:00:00', 66: '11:00:00', 72: '12:00:00', 78: '13:00:00', 84: '14:00:00', 90: '15:00:00', 96: '16:00:00', 102: '17:00:00', 108: '18:00:00', 114: '19:00:00', 120: '20:00:00', 126: '21:00:00'}
                for key, value in get_schedule.items():
                    bitmap_minutes = value.split(':')[0]*60 + value.split(':')[1]
                    if (start_time_minutes < bitmap_minutes and bitmap_minutes < end_time_minutes):
                        count += 1
                count += days * num_in_schedule
                return count
            else: #第二种情况
                count = 0
                for key, value in get_schedule.items():
                    bitmap_minutes = value.split(':')[0]*60 + value.split(':')[1]
                    if (start_time_minutes < bitmap_minutes or bitmap_minutes < end_time_minutes):
                        count += 1
                count += days * num_in_schedule
                return count
        else:
            if start_time[14:16] < end_time[14:16]: #第三种情况
                count = 0
                for key, value in get_schedule.items():
                    bitmap_minutes = value.split(':')[0]*60 + value.split(':')[1]
                    if (start_time_minutes < bitmap_minutes and bitmap_minutes < end_time_minutes):
                        count += 1
                count += days * num_in_schedule
                return count
            elif start_time[14:16] > end_time[14:16]: #4.1
                count = 0
                for key, value in get_schedule.items():
                    bitmap_minutes = value.split(':')[0]*60 + value.split(':')[1]
                    if (start_time_minutes < bitmap_minutes or bitmap_minutes < end_time_minutes):
                        count += 1
                count += days * num_in_schedule
                return count
            else: #为整日(24h),第4.2种情况
                count = days * num_in_schedule
                return count
    else: #第4.2种情况
        count = days * num_in_schedule
        return count