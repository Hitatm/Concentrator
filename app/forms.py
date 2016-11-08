#coding:UTF-8
__author__ = 'dj'

from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, AnyOf
from wtforms import StringField

class Upload(Form):
    reportrange = FileField('searchDateRange', validators=[DataRequired()])

#协议过滤表单
class ProtoFilter(Form):
    value = FileField('value')
    filter_type = FileField('filter_type', validators=[DataRequired(), AnyOf([u'all', u'proto', u'ipsrc', u'ipdst'])])
#上传用户名密码
class User_and_pwd(Form):
	username = FileField('username', validators=[DataRequired()])
	password = FileField('password', validators=[DataRequired()])