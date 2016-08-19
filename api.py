#!/usr/bin/env python
# encoding:utf-8
'''
* 赏金猎人项目
* liangchaob@163.com 
* 2016.7.25
'''

#设置中文字符
import sys
sys.path.append("./")
reload(sys)
sys.setdefaultencoding( "utf-8" )

import json
import time  
from flask import Flask,request,make_response,jsonify
# 导入pymongo模块
import pymongo
import json

# 数据部分
# 测试
# MONGODB_ADDR = '172.16.191.163'
# MONGODB_PORT = 27017
# MONGODB_DB = 'local'

# 生产
MONGODB_ADDR = '10.10.72.139'
MONGODB_PORT = 27017
MONGODB_DB = 'pF34ljJ5KYtc9sdZ'

# 设置数据库地址
client = pymongo.MongoClient(MONGODB_ADDR, MONGODB_PORT)

# 设置数据库名
db = client[MONGODB_DB]

# 生产认证
db.authenticate("uRyZYodlpcmOj74E","pyHsxuq1dCb9wXGMS")

# 设置表名,建立为索引
# 用户表
collection_user = db['user']
collection_user.ensure_index('openid', unique=True)

# 任务表
collection_mission = db['mission']
collection_mission.ensure_index('mission_id', unique=True)


# 技能表
collection_skill = db['skill']
collection_skill.ensure_index('skill_id', unique=True)

collection_comment = db['comment']
collection_comment.ensure_index('comment_id', unique=True)

collection_feedback = db['feedback']
collection_feedback.ensure_index('feedback_id', unique=True)

# 数据表
# 用户信息
class UserObj(object):
    # 依赖json生成对象
    def __init__(self, jsonobj):
        super(UserObj, self).__init__()
        self.jsonobj = {
            'openid':jsonobj.get('openid'),
            'intro':jsonobj.get('intro'),
            'role':jsonobj.get('role'),
            'feedback':jsonobj.get('feedback'),
            'level':jsonobj.get('level'),
            'skill':jsonobj.get('skill'),
            'mission_published':jsonobj.get('mission_published'),
            'mission_accept':jsonobj.get('mission_accept'),
            'mission_accomplish':jsonobj.get('mission_accomplish'),
            'state':jsonobj.get('state'),
            'spent':jsonobj.get('spent'),
            'income':jsonobj.get('income'),
            'email':jsonobj.get('email'),
            'mobile':jsonobj.get('mobile')    
        }

# 任务信息
class MissionObj(object):
    # 依赖json生成对象
    def __init__(self, jsonobj):
        super(MissionObj, self).__init__()
        self.jsonobj = {
            'mission_id':jsonobj.get('mission_id'),
            'name':jsonobj.get('name'),
            'mission_type':jsonobj.get('mission_type'),
            'deadline':jsonobj.get('deadline'),
            'description':jsonobj.get('description'),
            'obj':jsonobj.get('obj'),
            'skill_need':jsonobj.get('skill_need'),
            'bounty':jsonobj.get('bounty'),
            'state':jsonobj.get('state'),
            'comment':jsonobj.get('comment'),
            'bidder':jsonobj.get('bidder'),
            'publisher':jsonobj.get('publisher'),
            'acceptor':jsonobj.get('acceptor')
        }

# 技能信息
class SkillObj(object):
    # 依赖json生成对象
    def __init__(self, jsonobj):
        super(SkillObj, self).__init__()
        self.jsonobj = {
            'skill_id':jsonobj.get('skill_id'),
            'name':jsonobj.get('name'),
            'description':jsonobj.get('description'),
            'certification':jsonobj.get('certification')
        }

# 留言信息
class CommentObj(object):
    # 依赖json生成对象
    def __init__(self, jsonobj):
        super(CommentObj, self).__init__()
        self.jsonobj = {
            'comment_id':jsonobj.get('comment_id'),
            'mission_id':jsonobj.get('mission_id'),
            'openid':jsonobj.get('openid'),
            'content':jsonobj.get('content')
        }

# 评价信息
class FeedbackObj(object):
    # 依赖json生成对象
    def __init__(self, jsonobj):
        super(FeedbackObj, self).__init__()
        self.jsonobj = {
            'feedback_id':jsonobj.get('feedback_id'),
            'mission_id':jsonobj.get('mission_id'),
            'publisher':jsonobj.get('publisher'),
            'acceptor':jsonobj.get('acceptor'),
            'content':jsonobj.get('content'),
            'stars':jsonobj.get('stars')
        }

# web部分
# flask实例化
app = Flask(__name__)

# err返回码
class CodeReturn(object):
    def success(self):
        obj = {'errcode':0,'errmsg':'ok'}
        return json.dumps(obj)
    def failed(self):
        obj = {'errcode':1,'errmsg':'failed'}
        return json.dumps(obj)        

# 实例化返回码
errcode = CodeReturn()

# 单用户
@app.route('/user/<openid>', methods = ['GET', 'POST'])
def user(openid):
    # 获取指定用户信息
    if request.method == 'GET':
        try:
            result = collection_user.find_one({'openid':openid})
            j = UserObj(result)
            return jsonify(j.jsonobj)
        except:
            return errcode.failed()
    # 更改指定用户信息
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            # j = UserObj(result)
            collection_user.update({'openid':openid},{'$set':result})
            return errcode.success()
        except:
            return errcode.failed()
    else:
        return 'nothing happend!'

# 全部用户
@app.route('/user/', methods = ['GET', 'POST'])
def users():
    # get - 获取全部用户信息
    if request.method == 'GET':        
        jsonlist = []
        for item in collection_user.find({}):
            j = UserObj(item)
            jsonlist.append(j.jsonobj)

        result = {'user':jsonlist}
        return jsonify(result)
    # post - 添加新用户
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            j = UserObj(result)
            collection_user.insert_one(j.jsonobj)
            return errcode.success()
        except:
            return errcode.failed()     
    else:
        return 'nothing happend!'

# 任务
@app.route('/mission/<mission_id>', methods = ['GET', 'POST'])
def mission(mission_id):
    # 获取单个技能
    if request.method == 'GET':
        try:
            result = collection_mission.find_one({'mission_id':mission_id})
            j = MissionObj(result)
            return jsonify(j.jsonobj)
        except:
            return errcode.failed()
    # 更改技能信息
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            collection_mission.update({'mission_id':mission_id},{'$set':result})
            return errcode.success()
        except:
            return errcode.failed()

# 全部任务
@app.route('/mission/', methods = ['GET', 'POST'])
def missions():
    # get - 获取全部任务信息
    if request.method == 'GET':        
        jsonlist = []
        for item in collection_mission.find({}):
            j = MissionObj(item)
            jsonlist.append(j.jsonobj)

        result = {'mission':jsonlist}
        return jsonify(result)
    # post - 添加新任务
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            j = MissionObj(result)
            collection_mission.insert_one(j.jsonobj)
            return errcode.success()
        except:
            return errcode.failed()      
    else:
        return 'nothing happend!'

# 技能
@app.route('/skill/<skill_id>', methods = ['GET', 'POST'])
def skill(skill_id):
    # 获取单个技能
    if request.method == 'GET':
        try:
            result = collection_skill.find_one({'skill_id':skill_id})
            j = SkillObj(result)
            return jsonify(j.jsonobj)
        except:
            return errcode.failed()
    # 更改技能信息
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            # j = SkillObj(result)
            collection_skill.update({'skill_id':skill_id},{'$set':result})
            return errcode.success()
        except:
            return errcode.failed()
    # 其它
    else:
        return 'nothing happend!'

# 全部技能
@app.route('/skill/', methods = ['GET', 'POST'])
def skills():
    # get - 获取全部技能信息
    if request.method == 'GET':        
        jsonlist = []
        for item in collection_skill.find({}):
            j = SkillObj(item)
            jsonlist.append(j.jsonobj)

        result = {'skill':jsonlist}
        return jsonify(result)
    # post - 添加新技能
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            j = SkillObj(result)
            collection_skill.insert_one(j.jsonobj)
            return errcode.success()
        except:
            return errcode.failed()
    else:
        return 'nothing happend!'

# 留言
@app.route('/comment/<comment_id>', methods = ['GET', 'POST'])
def comment(comment_id):
    # 获取单个留言
    if request.method == 'GET':
        try:
            result = collection_comment.find_one({'comment_id':comment_id})
            j = CommentObj(result)
            return jsonify(j.jsonobj)
        except:
            return errcode.failed()
    # 更改留言
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            # j = CommentObj(result)
            collection_comment.update({'comment_id':comment_id},{'$set':result})
            return errcode.success()
        except:
            return errcode.failed()
    # 其它
    else:
        return 'nothing happend!'

# 全部留言
@app.route('/comment/', methods = ['GET', 'POST'])
def comments():
    # get - 获取全部留言信息
    if request.method == 'GET':        
        jsonlist = []
        for item in collection_comment.find({}):
            j = CommentObj(item)
            jsonlist.append(j.jsonobj)

        result = {'comment':jsonlist}
        return jsonify(result)
    # post - 添加新留言
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            j = CommentObj(result)
            collection_comment.insert_one(j.jsonobj)
            return errcode.success()
        except:
            return errcode.failed()     
    else:
        return 'nothing happend!'

# 评价
@app.route('/feedback/<feedback_id>', methods = ['GET', 'POST'])
def feedback(feedback_id):
    # 获取单个评价
    if request.method == 'GET':
        try:
            result = collection_feedback.find_one({'feedback_id':feedback_id})
            j = FeedbackObj(result)
            return jsonify(j.jsonobj)
        except:
            return errcode.failed()
    # 更改评价
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            # j = FeedbackObj(result)
            collection_feedback.update({'feedback_id':feedback_id},{'$set':result})
            return errcode.success()
        except:
            return errcode.failed()
    # 其它
    else:
        return 'nothing happend!'

# 全部评价
@app.route('/feedback/', methods = ['GET', 'POST'])
def feedbacks():
    # get - 获取全部评价信息
    if request.method == 'GET':        
        jsonlist = []
        for item in collection_feedback.find({}):
            j = FeedbackObj(item)
            jsonlist.append(j.jsonobj)

        result = {'feedback':jsonlist}
        return jsonify(result)
    # post - 添加新评价
    elif request.method == 'POST':
        # 参数接收
        try:
            result = request.json
            j = FeedbackObj(result)
            collection_feedback.insert_one(j.jsonobj)
            return errcode.success()
        except:
            return errcode.failed()     
    else:
        return 'nothing happend!'

# 运行主函数
if __name__ == '__main__':
    # 测试
    # app.run(host='0.0.0.0',port=8081,debug=True)
    # 生产
    app.run(host='0.0.0.0',port=80,debug=False)
