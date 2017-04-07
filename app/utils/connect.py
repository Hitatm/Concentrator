#coding:UTF-8

import socket
import json
import os

class Connect:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(__file__)
		self.Config_FILE=self.BASE_DIR+'/Config/config.json'  #json配置文件
		f=open(self.Config_FILE,'r')
		self.CONFIG_DICT =json.load(f)
		f.close()

	def TCP_send(self, ins):
		serverip = self.CONFIG_DICT['serverIp']
		serverport = self.CONFIG_DICT['tcpPort']
		cli=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		cli.connect((serverip,serverport))
		cli.send(ins)
		cli.close()

	def UDP_send(self, ins):
		serverip = self.CONFIG_DICT['serverIp']
		serverport = self.CONFIG_DICT['udpPort']
		cli=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		cli.connect((serverip,serverport))
		cli.send(ins)
		cli.close()



