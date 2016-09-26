#!/usr/bin/env python
# encoding:utf-8
'''
* 赏金猎人项目
* liangchaob@163.com 
* 2016.7.21
'''

#设置中文字符
import sys
sys.path.append("./")
reload(sys)
sys.setdefaultencoding( "utf-8" )

import requests
import time  
from flask import Flask,request, make_response,render_template,jsonify,redirect
import hashlib  
# 微信配置类
from wechat_sdk import WechatConf
# 微信接口类
from wechat_sdk import WechatBasic
# 微信xml解析类
from wechat_sdk.exceptions import ParseError


import json
import uuid
import time
# 排序相关
import operator

APPID = 'wxa9312a82e8138370'
APPSECRET = '3f87fbd58c9013a0b0190bda28a4acc5'



# 配置参数
conf = WechatConf(
    token='g7824tgfhew0g', 
    appid='wxa9312a82e8138370', 
    appsecret='3f87fbd58c9013a0b0190bda28a4acc5',
    encrypt_mode='normal'  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    # encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)
wechat = WechatBasic(conf=conf)


# flask实例化
app = Flask(__name__)



# test
@app.route('/test/newmission', methods = ['GET', 'POST'])
def t2():
    if request.method == 'GET':
        return render_template('new_mission.html')

# test
@app.route('/test/usercenter', methods = ['GET', 'POST'])
def t3():
    if request.method == 'GET':
        return render_template('usercenter.html')

# test
@app.route('/test/usercenter_published', methods = ['GET', 'POST'])
def t4():
    if request.method == 'GET':
        return render_template('published_mission.html')



# test
@app.route('/test/allusers', methods = ['GET', 'POST'])
def t5():
    if request.method == 'GET':
        # return 'hehe'
        result = db_obj.dbget('api/user/')
        result = {'comment':result}
        return jsonify(result)



# test
@app.route('/test/user_mission/<openid>', methods = ['GET', 'POST'])
def t6(openid):
    if request.method == 'GET':
        result = db_obj.dbget('api/user/'+openid)
        return result


# test
@app.route('/test/missions/<publisher>', methods = ['GET', 'POST'])
def t7(publisher):
    if request.method == 'GET':
        result = db_obj.dbget('api/mission/publisher/'+publisher)
        return result


# test
@app.route('/test/allmissions', methods = ['GET', 'POST'])
def t8():
    if request.method == 'GET':
        # return 'hehe'
        result = db_obj.dbget('api/mission/')
        result = {'comment':result}
        return jsonify(result)

# test
@app.route('/test/missioncheck/<mission_id>', methods = ['GET', 'POST'])
def t9(mission_id):
    if request.method == 'GET':
        # return 'hehe'
        result = db_obj.dbget('api/mission/id/' + mission_id)
        # result = {'comment':result}
        # return jsonify(result)
        return render_template('mission.html',mission_obj=result)

# test
@app.route('/test/comment', methods = ['GET', 'POST'])
def t10():
    if request.method == 'GET':
        # return 'hehe'
        result = db_obj.dbget('api/comment/')
        result = {'comment':result}
        return jsonify(result)
        # return render_template('mission.html',mission_obj=result)




