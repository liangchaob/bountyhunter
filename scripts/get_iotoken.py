#!/usr/bin/env python
# encoding:utf-8
'''
* 赏金猎人项目
* liangchaob@163.com 
* 2016.8.3
'''

#设置中文字符
import sys
sys.path.append("./")
reload(sys)
sys.setdefaultencoding( "utf-8" )

import requests
import json

# 填写变量
APPID = 'wxa9312a82e8138370'
APPSECRET = '3f87fbd58c9013a0b0190bda28a4acc5'

url1="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+APPID+"&secret="+APPSECRET

r1 = requests.get(url1)


access_token = r1.json().get('access_token')


url2="https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token="+access_token

r2 = requests.get(url2)



weichat_serverip = r2.json().get('ip_list')


print 'access_token = ' + access_token
print 'weichat_serverip = ' + str(weichat_serverip)

