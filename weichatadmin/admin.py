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



# 后台管理员界面
# 首页
@app.route('/admin', methods = ['GET', 'POST'])
def adminApproval():
    if request.method == 'GET':
        return redirect('/admin/approval')
    else:
        pass

# 管理员审批
@app.route('/admin/approval', methods = ['GET', 'POST'])
def adminApproval():
    if request.method == 'GET':
        result = db_obj.dbget('api/mission/')
        # # 更新数据库
        # headers = {'content-type': 'application/json'}
        # r = requests.get('http://liangchaob-bountyapi.daoapp.io/mission/',headers = headers)
        # result = r.json()
        mission_list = result

        # 筛选出处于发布状态的任务
        misson_publish = []
        for mission in mission_list:
            if mission.get('state') == "1":
                misson_publish.append(mission)

        return render_template('admin_approval.html',misson_publish = misson_publish)
    else:
        pass

# 管理员通过
@app.route('/admin/passed', methods = ['GET', 'POST'])
def adminPassed():
    if request.method == 'GET':
        result = db_obj.dbget('api/mission/')
        # # 更新数据库
        # headers = {'content-type': 'application/json'}
        # r = requests.get('http://liangchaob-bountyapi.daoapp.io/mission/',headers = headers)
        # result = r.json()
        mission_list = result

        # 筛选出处于已通过状态的任务
        misson_passed = []
        for mission in mission_list:
            if mission.get('state') == "2":
                misson_passed.append(mission)

        return render_template('admin_passed.html',misson_passed = misson_passed)
    else:
        pass


# 管理员驳回
@app.route('/admin/deny', methods = ['GET', 'POST'])
def adminDeny():
    if request.method == 'GET':
        result = db_obj.dbget('api/mission/')
        # # 更新数据库
        # headers = {'content-type': 'application/json'}
        # r = requests.get('http://liangchaob-bountyapi.daoapp.io/mission/',headers = headers)
        # result = r.json()
        mission_list = result

        # 筛选出处于驳回状态的任务
        misson_deny = []
        for mission in mission_list:
            if mission.get('state') == "0":
                misson_deny.append(mission)

        return render_template('admin_deny.html',misson_deny = misson_deny)
    else:
        pass


# 管理具体项目
@app.route('/admin/<mission_id>', methods = ['GET', 'POST'])
def missionApproval(mission_id):
    if request.method == 'GET':
        result = db_obj.dbget('api/mission/id/'+mission_id)
        # # 更新数据库
        # headers = {'content-type': 'application/json'}
        # r = requests.get('http://liangchaob-bountyapi.daoapp.io/mission/'+str(mission_id),headers = headers)
        # result = r.json()

        return render_template('mission_approval.html',mission_approval = result)
    elif request.method == 'POST':
        result = request.form.get('code')
        if result == 'pass':
            # 把状态置为2（审批通过）
            jsonobj = {'state':"2"}
            result = db_obj.dbput('api/mission/id/'+str(mission_id),jsonobj)
            # # 更新数据库
            # headers = {'content-type': 'application/json'}
            # r = requests.post('http://liangchaob-bountyapi.daoapp.io/mission/'+str(mission_id), data=json.dumps(jsonobj),headers = headers)
            return str(result)

        elif result == 'deny':
            # 把状态置为0（驳回状态）
            jsonobj = {'state':"0"}
            result = db_obj.dbput('api/mission/id/'+str(mission_id),jsonobj)
            # # 更新数据库
            # headers = {'content-type': 'application/json'}
            # r = requests.post('http://liangchaob-bountyapi.daoapp.io/mission/'+str(mission_id), data=json.dumps(jsonobj),headers = headers)
            return str(result)
    else:
        pass




