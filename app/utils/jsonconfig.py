#coding:UTF-8
import os
import json

class json_config:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(__file__)
		self.Config_FILE=self.BASE_DIR+'/Config/config.json'  #json配置文件
		self.loadjson = json.load(open(self.Config_FILE,'r')) # dictionary of all jsons

	# def speak(self):  
	# 	print self.loadjson

# a = json_config()
# a.speak()


