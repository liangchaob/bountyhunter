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



# 数据库相关
# 测试
MONGODB_ADDR = '172.16.191.163'
MONGODB_PORT = 27017
MONGODB_DB = 'local'

# 生产
# MONGODB_ADDR = '10.10.72.139'
# MONGODB_PORT = 27017
# MONGODB_DB = 'MC7rOHPSiyGo9qJ4'

# 设置数据库地址
client = pymongo.MongoClient(MONGODB_ADDR, MONGODB_PORT)

# 设置数据库名
db = client[MONGODB_DB]

# 生产认证
# db.authenticate("uhG05VAsSiBdRtQp","pdqBG5IHPi1E36wFC")

# 设置表名,建立为索引
# 用户表
collection_user = db['user']
collection_user.ensure_index('id', unique=True)

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



# web相关
# flask实例化
app = Flask(__name__)


# 设计err返回码
class codeReturn(object):
    def success(self):
        obj = {'errcode':0,'errmsg':'ok'}
        return json.dumps(obj)
    def failed(self):
        obj = {'errcode':1,'errmsg':'failed'}
        return json.dumps(obj)        

# 实例化返回码
errcode = codeReturn()




# 单用户
@app.route('/user/<openid>', methods = ['GET', 'POST'])
def user(openid):
    # 获取指定用户信息
    if request.method == 'GET':
        try:
            result = collection_user.find_one({'openid':openid})
            jsonobj = {
                'openid':result.get('openid'),
                'intro':result.get('intro'),
                'role':result.get('role'),
                'feedback':result.get('feedback'),
                'level':result.get('level'),
                'skill':result.get('skill'),
                'mission_published':result.get('mission_published'),
                'mission_accept':result.get('mission_accept'),
                'mission_accomplish':result.get('mission_accomplish'),
                'state':result.get('state'),
                'spent':result.get('spent'),
                'income':result.get('income'),
                'email':result.get('email'),
                'mobile':result.get('mobile')

                }
            return jsonify(jsonobj)
        except:
            return errcode.failed()
    # 更改指定用户信息
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_user.update({'openid':openid},
                {'$set':{
                    'openid':request.form['openid'],
                    'intro':request.form['intro'],
                    'role':request.form['role'],
                    'feedback':request.form['feedback'],
                    'level':request.form['level'],
                    'skill':request.form['skill'],
                    'mission_published':request.form['mission_published'],
                    'mission_accept':request.form['mission_accept'],
                    'mission_accomplish':request.form['mission_accomplish'],
                    'state':request.form['state'],
                    'spent':request.form['spent'],
                    'income':request.form['income'],
                    'email':request.form['email'],
                    'mobile':request.form['mobile']
                    }
                })
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
            jsonlist.append({
                'openid':item.get('openid'),
                'intro':item.get('intro'),
                'role':item.get('role'),
                'feedback':item.get('feedback'),
                'level':item.get('level'),
                'skill':item.get('skill'),
                'mission_published':item.get('mission_published'),
                'mission_accept':item.get('mission_accept'),
                'mission_accomplish':item.get('mission_accomplish'),
                'state':item.get('state'),
                'spent':item.get('spent'),
                'income':item.get('income'),
                'email':item.get('email'),
                'mobile':item.get('mobile')
                })

        jsonobj = {'user':jsonlist}
        return jsonify(jsonobj)
    # post - 添加新用户
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_user.insert_one({
                'openid':request.form['openid'],
                'intro':request.form['intro'],
                'role':request.form['role'],
                'feedback':request.form['feedback'],
                'level':request.form['level'],
                'skill':request.form['skill'],
                'mission_published':request.form['mission_published'],
                'mission_accept':request.form['mission_accept'],
                'mission_accomplish':request.form['mission_accomplish'],
                'state':request.form['state'],
                'spent':request.form['spent'],
                'income':request.form['income'],
                'email':request.form['email'],
                'mobile':request.form['mobile']
                })
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
            jsonobj = {
                'mission_id':result.get('mission_id'),
                'name':result.get('name'),
                'mission_type':result.get('mission_type'),
                'deadline':result.get('deadline'),
                'description':result.get('description'),
                'obj':result.get('obj'),
                'skill_need':result.get('skill_need'),
                'bounty':result.get('bounty'),
                'state':result.get('state'),
                'comment':result.get('comment'),
                'bidder':result.get('bidder'),
                'publisher':result.get('publisher'),
                'acceptor':result.get('acceptor')
                }
            return jsonify(jsonobj)
        except:
            return errcode.failed()
    # 更改技能信息
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_mission.update({'mission_id':mission_id},{
                '$set':{
                    'mission_id':request.form['mission_id'],
                    'name':request.form['name'],
                    'mission_type':request.form['mission_type'],
                    'deadline':request.form['deadline'],
                    'description':request.form['description'],
                    'obj':request.form['obj'],
                    'skill_need':request.form['skill_need'],
                    'bounty':request.form['bounty'],
                    'state':request.form['state'],
                    'comment':request.form['comment'],
                    'bidder':request.form['bidder'],
                    'publisher':request.form['publisher'],
                    'acceptor':request.form['acceptor']
                    }
                })
            return errcode.success()
        except:
            return errcode.failed()
    # 





# 全部任务
@app.route('/mission/', methods = ['GET', 'POST'])
def missions():
    # get - 获取全部任务信息
    if request.method == 'GET':        
        jsonlist = []
        for item in collection_mission.find({}):
            jsonlist.append({
                'mission_id':item.get('mission_id'),
                'name':item.get('name'),
                'mission_type':item.get('mission_type'),
                'deadline':item.get('deadline'),
                'description':item.get('description'),
                'obj':item.get('obj'),
                'skill_need':item.get('skill_need'),
                'bounty':item.get('bounty'),
                'state':item.get('state'),
                'comment':item.get('comment'),
                'bidder':item.get('bidder'),
                'publisher':item.get('publisher'),
                'acceptor':item.get('acceptor')
                })

        jsonobj = {'mission':jsonlist}
        return jsonify(jsonobj)
    # post - 添加新任务
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_mission.insert_one({
                'mission_id':request.form['mission_id'],
                'name':request.form['name'],
                'mission_type':request.form['mission_type'],
                'deadline':request.form['deadline'],
                'description':request.form['description'],
                'obj':request.form['obj'],
                'skill_need':request.form['skill_need'],
                'bounty':request.form['bounty'],
                'state':request.form['state'],
                'comment':request.form['comment'],
                'bidder':request.form['bidder'],
                'publisher':request.form['publisher'],
                'acceptor':request.form['acceptor']
                })
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
            jsonobj = {
                'skill_id':result.get('skill_id'),
                'name':result.get('name'),
                'description':result.get('description'),
                'certification':result.get('certification')
            }
            return jsonify(jsonobj)
        except:
            return errcode.failed()
    # 更改技能信息
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_skill.update({'skill_id':skill_id},{
                '$set':{
                    'skill_id':request.form['skill_id'],
                    'name':request.form['name'],
                    'description':request.form['description'],
                    'certification':request.form['certification']
                    }
                })
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
            jsonlist.append({
                'skill_id':item.get('skill_id'),
                'name':item.get('name'),
                'description':item.get('description'),
                'certification':item.get('certification')
                })
        jsonobj = {'skill':jsonlist}
        return jsonify(jsonobj)
    # post - 添加新技能
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_skill.insert_one({
                'skill_id':request.form['skill_id'],
                'name':request.form['name'],
                'description':request.form['description'],
                'certification':request.form['certification']                
                })
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
            jsonobj = {
                'comment_id':result.get('comment_id'),
                'mission_id':result.get('mission_id'),
                'openid':result.get('openid'),
                'content':result.get('content')
                }
            return jsonify(jsonobj)
        except:
            return errcode.failed()
    # 更改留言
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_comment.update({'comment_id':comment_id},{
                '$set':{
                    'comment_id':request.form['comment_id'],
                    'mission_id':request.form['mission_id'],
                    'openid':request.form['openid'],
                    'content':request.form['content']
                    }
                })
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
            jsonlist.append({
                'comment_id':item.get('comment_id'),
                'mission_id':item.get('mission_id'),
                'openid':item.get('openid'),
                'content':item.get('content')
                })
        jsonobj = {'comment':jsonlist}
        return jsonify(jsonobj)
    # post - 添加新留言
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_comment.insert_one({
                'comment_id':request.form['comment_id'],
                'mission_id':request.form['mission_id'],
                'openid':request.form['openid'],
                'content':request.form['content']
                })
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
            jsonobj = {
                'feedback_id':result.get('feedback_id'),
                'mission_id':result.get('mission_id'),
                'publisher':result.get('publisher'),
                'acceptor':result.get('acceptor'),
                'content':result.get('content'),
                'stars':result.get('stars')
                }
            return jsonify(jsonobj)
        except:
            return errcode.failed()
    # 更改评价
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_feedback.update({'feedback_id':feedback_id},{
                '$set':{
                    'feedback_id':request.form['feedback_id'],
                    'mission_id':request.form['mission_id'],
                    'publisher':request.form['publisher'],
                    'acceptor':request.form['acceptor'],
                    'content':request.form['content'],
                    'stars':request.form['stars']
                    }
                })
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
            jsonlist.append({
                'feedback_id':item.get('feedback_id'),
                'mission_id':item.get('mission_id'),
                'publisher':item.get('publisher'),
                'acceptor':item.get('acceptor'),
                'content':item.get('content'),
                'stars':item.get('stars')
                })
        jsonobj = {'feedback':jsonlist}
        return jsonify(jsonobj)
    # post - 添加新评价
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_feedback.insert_one({
                'feedback_id':request.form['feedback_id'],
                'mission_id':request.form['mission_id'],
                'publisher':request.form['publisher'],
                'acceptor':request.form['acceptor'],
                'content':request.form['content'],
                'stars':request.form['stars']
                })
            return errcode.success()
        except:
            return errcode.failed()     
    else:
        return 'nothing happend!'






# 运行主函数
if __name__ == '__main__':
    # 测试
    app.run(host='0.0.0.0',port=8080,debug=True)
    # 生产
    # app.run(host='0.0.0.0',port=80,debug=False)
