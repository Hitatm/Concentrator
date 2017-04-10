#coding:UTF-8

import json
import os

class Display:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(__file__)
		self.Config_FILE=self.BASE_DIR+'/Config/displayconfig'  #json配置文件
		f=open(self.Config_FILE,'r')
		self.CONFIG_DICT =json.load(f)
		f.close()

	def send_display(self):
		data = self.CONFIG_DICT['instruction_send']
		return data

	def write_display(self):
		data = self.CONFIG_DICT['instruction_write']
		return data

	def adjtime_display(self):
		data = self.CONFIG_DICT['instruction_adjtime']
		return data

	def parameters_display(self):
		parameters = dict()
		parameters["CCA"] = self.CONFIG_DICT['CCA']
		parameters["PANID"] = self.CONFIG_DICT['PANID']
		parameters["emitpower"] = self.CONFIG_DICT['emitpower']
		parameters["CCAcheckingperiod"] = self.CONFIG_DICT['CCAcheckingperiod']
		parameters["inactive"] = self.CONFIG_DICT['inactive']
		parameters["channel"] = self.CONFIG_DICT['channel']
		parameters["DIO_minlen"] = self.CONFIG_DICT['DIO_minlen']
		parameters["DIO_max"] = self.CONFIG_DICT['DIO_max']
		return parameters
		
	def monitor_update_period_display(self):
		data = self.CONFIG_DICT['monitor_update_period']
		return data

class Modify:
	def __init__(self):
		self.BASE_DIR = os.path.dirname(__file__)
		self.Config_FILE=self.BASE_DIR+'/Config/displayconfig'  #json配置文件
		f=open(self.Config_FILE,'r')
		self.CONFIG_DICT =json.load(f)
		f.close()

	def send_modify(self, data):
		self.CONFIG_DICT['instruction_send'] = data
		self.write_config()

	def write_modify(self, data):
		self.CONFIG_DICT['instruction_write'] = data
		self.write_config()

	def adjtime_modify(self, data):
		self.CONFIG_DICT['instruction_adjtime'] = data
		self.write_config()

	def CCA_modify(self, data):
		self.CONFIG_DICT['CCA'] = data
		self.write_config()

	def PANID_modify(self, data):
		self.CONFIG_DICT['PANID'] = data
		self.write_config()

	def emitpower_modify(self, data):
		self.CONFIG_DICT['emitpower'] = data
		self.write_config()

	def CCAcheckingperiod_modify(self, data):
		self.CONFIG_DICT['CCAcheckingperiod'] = data
		self.write_config()

	def inactive_modify(self, data):
		self.CONFIG_DICT['inactive'] = data
		self.write_config()

	def channel_modify(self, data):
		self.CONFIG_DICT['channel'] = data
		self.write_config()

	def DIO_minlen_modify(self, data):
		self.CONFIG_DICT['DIO_minlen'] = data
		self.write_config()

	def DIO_max_modify(self, data):
		self.CONFIG_DICT['DIO_max'] = data
		self.write_config()
		
	def monitor_update_period_modify(self, data):
		self.CONFIG_DICT['monitor_update_period'] = data
		self.write_config()

	def write_config(self):
		with open(self.Config_FILE, 'w') as f:
			f.write(json.dumps(self.CONFIG_DICT))
			f.close()