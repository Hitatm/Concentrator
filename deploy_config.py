#coding=UTF-8

bind='0.0.0.0:8001'
workers = 4
pidfile = '/tmp/gunicorn.pid'
loglevel = 'debug'
access_logformat = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s" 
log_level = 'info'   
#chdir= '/var/www/Concentrator'
daemon= False 
access_log_format= "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
default_proc_name="run:app"
