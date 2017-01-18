import time

if __name__ == '__main__':
	 while True:
		file=open("/home/wangyu/myspace/Concentrator/datalog/testsupervisor/data.log","a")
		now= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		print now
		file.write(now+'\n')
		file.close()
		time.sleep(1) 
