#coding:UTF-8
import time,datetime
import os
from gxn_get_sys_config import Config
import sqlite3
from db_operate import DBClass

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

def appdatacount(start_time, end_time, NodeID):
    DATABASE = DBClass()
    exist = 0
    appdata = DATABASE.my_db_execute('select * from ApplicationData where currenttime >= ? and currenttime <= ? and NodeID == ?;',(start_time, end_time, NodeID))
    if appdata:
        exist = 1
    return exist

def netdatacount(start_time, end_time, NodeID):
    DATABASE = DBClass()
    exist = 0
    appdata = DATABASE.my_db_execute('select * from NetMonitor where currenttime >= ? and currenttime <= ? and NodeID == ?;',(start_time, end_time, NodeID))
    if appdata:
        exist = 1
    return exist

def date_addone(year, month, day):
    year = int(year)
    month = int(month)
    day = int(day)
    runnian = 0
    if year%4 == 0:
        runnian = 1
    if year%4 == 0 and year%100 == 0:
        runnian = 0
    if year%400 == 0:
        runnian = 1
    a = set([1,3,5,7,8])
    b = set([4,6,9])
    # 2月12月另算
    if (month in a and day>=31):
        newdate = str(year)+'-0'+str(month+1)+'-01'
    elif (month in b and day>=30):
        newdate = str(year)+'-0'+str(month+1)+'-01'
    elif runnian==0 and month==2 and day>=28:
        newdate = str(year)+'-0'+str(month+1)+'-01'
    elif runnian==1 and month==2 and day>=29:
        newdate = str(year)+'-0'+str(month+1)+'-01'
    elif month==10 and day>=31:
        newdate = str(year)+'-'+str(month+1)+'-01'
    elif month==11 and day>=30:
        newdate = str(year)+'-'+str(month+1)+'-01'
    elif month==12 and day>=31:
        newdate = str(year+1)+'-01-01'
    elif month>10 and day>=9:
        newdate = str(year)+'-'+str(month)+'-'+str(day+1)
    elif month>10 and day<9:
        newdate = str(year)+'-'+str(month)+'-0'+str(day+1)
    elif month<10 and day<9:
        newdate = str(year)+'-0'+str(month)+'-0'+str(day+1)
    else:
        newdate = str(year)+'-0'+str(month)+'-'+str(day+1)
    return newdate

def get_schedule_time(start_time, end_time):
    # 读取调度
    g = Config()
    get_schedule = g.get_active_time()
    get_schedule = sorted(get_schedule.items(), key=lambda d:d[0])
    schedule_list = list() #实际搜索的调度列表
    # 读取日期和时间 #2017-05-02 11:04:01
    start_date = start_time.split(' ')[0]
    start_hms = start_time.split(' ')[1]
    end_date = end_time.split(' ')[0]
    end_hms = end_time.split(' ')[1]
    start_time_second = int(start_hms.split(':')[0])*60*60 + int(start_hms.split(':')[1])*60 + int(start_hms.split(':')[2])
    end_time_second = int(end_hms.split(':')[0])*60*60 + int(end_hms.split(':')[1])*60 + int(end_hms.split(':')[2])

    days = (datetime.datetime(int(end_date.split('-')[0]), int(end_date.split('-')[1]), int(end_date.split('-')[2])) - datetime.datetime(int(start_date.split('-')[0]), int(start_date.split('-')[1]), int(start_date.split('-')[2]))).days
    # print days
    if days: #如果结束日期在开始日期后面 1:超过了24小时(2018-1-1 12:00:00 - 2018-1-2 18:00:00),2:没超过24小时(2018-1-1 12:00:00 - 2018-1-2 8:00:00)
        #(2018-1-1 12:00:00 - 2018-1-7 18:00:00)
        if (int(end_hms.split(':')[0])*60 + int(end_hms.split(':')[1])) >= (int(start_hms.split(':')[0])*60 + int(start_hms.split(':')[1])):
            start_date0 = start_date
            start_date1 = date_addone(start_date0.split('-')[0],start_date0.split('-')[1],start_date0.split('-')[2])
            for i in range(days):                
                start_year = start_date0.split('-')[0]
                start_month = start_date0.split('-')[1]
                start_day = start_date0.split('-')[2]
                for item in get_schedule:
                    bitmap_second = int(item[1].split(':')[0])*60*60 + int(item[1].split(':')[1])*60 + int(item[1].split(':')[2])
                    if (start_time_second < bitmap_second):
                        schedule_list.append(start_date0+' '+item[1])
                start_date0 = date_addone(start_year,start_month,start_day)
            for i in range(days-1):
                start_year = start_date1.split('-')[0]
                start_month = start_date1.split('-')[1]
                start_day = start_date1.split('-')[2]
                for item in get_schedule:
                    bitmap_second = int(item[1].split(':')[0])*60*60 + int(item[1].split(':')[1])*60 + int(item[1].split(':')[2])
                    if (start_time_second > bitmap_second):
                        schedule_list.append(start_date1+' '+item[1])
                start_date1 = date_addone(start_year,start_month,start_day)
            for item in get_schedule:
                bitmap_second = int(item[1].split(':')[0])*60*60 + int(item[1].split(':')[1])*60 + int(item[1].split(':')[2])
                if (start_time_second < bitmap_second and bitmap_second < end_time_second):
                    schedule_list.append(end_date+' '+item[1])
            schedule_list = sorted(schedule_list)
            # print "case1"
        #(2018-1-1 12:00:00 - 2018-1-5 8:00:00)
        else:
            start_date0 = start_date
            start_date1 = date_addone(start_date0.split('-')[0],start_date0.split('-')[1],start_date0.split('-')[2])
            for i in range(days):                
                start_year = start_date0.split('-')[0]
                start_month = start_date0.split('-')[1]
                start_day = start_date0.split('-')[2]
                for item in get_schedule:
                    bitmap_second = int(item[1].split(':')[0])*60*60 + int(item[1].split(':')[1])*60 + int(item[1].split(':')[2])
                    if (start_time_second < bitmap_second):
                        schedule_list.append(start_date0+' '+item[1])
                start_date0 = date_addone(start_year,start_month,start_day)
            for i in range(days-1):
                start_year = start_date1.split('-')[0]
                start_month = start_date1.split('-')[1]
                start_day = start_date1.split('-')[2]
                for item in get_schedule:
                    bitmap_second = int(item[1].split(':')[0])*60*60 + int(item[1].split(':')[1])*60 + int(item[1].split(':')[2])
                    if (start_time_second > bitmap_second):
                        schedule_list.append(start_date1+' '+item[1])
                start_date1 = date_addone(start_year,start_month,start_day)
            for item in get_schedule:
                bitmap_second = int(item[1].split(':')[0])*60*60 + int(item[1].split(':')[1])*60 + int(item[1].split(':')[2])
                if (bitmap_second < end_time_second):
                    schedule_list.append(end_date+' '+item[1])
            schedule_list = sorted(schedule_list)
            # print "case2"
            
    else: #2018-1-1 12:00:00 - 2018-1-1 18:00:00
        for item in get_schedule:
            bitmap_second = int(item[1].split(':')[0])*60*60 + int(item[1].split(':')[1])*60 + int(item[1].split(':')[2])
            if (start_time_second < bitmap_second and bitmap_second < end_time_second):
                #{0: '00:00:00', 4: '00:40:00', 6: '01:00:00', 138: '23:00:00'}
                schedule_list.append(start_date+' '+item[1])
        schedule_list = sorted(schedule_list)
        # print "case3"
    return schedule_list
    