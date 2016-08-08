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
# MONGODB_DB = 'dlR8NJgeiK3TsOkj'

# 设置数据库地址
client = pymongo.MongoClient(MONGODB_ADDR, MONGODB_PORT)

# 设置数据库名
db = client[MONGODB_DB]

# 生产认证
# db.authenticate("udkIqOwPYlfMZAXn","psfuF7gNhBriTZHWl")

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
            collection_mission.update({'missionid':missionid},{
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



# 数据库查询
def dbget(result,listobj):
    jsonobj = {}
    for item in listobj:
        jsonobj.update({item:result.get(item)})
    return jsonobj

# 数据库更新
def dbupdate(request,listobj):
    jsonobj = {}
    for item in listobj:
        jsonobj.update({item:request.form(item)})
    return jsonobj

# 任务
@app.route('/mission/<missionid>', methods = ['GET', 'POST'])
def mission(missionid):
    # 获取单个任务
    if request.method == 'GET':
        try:
            result = collection_mission.find_one({'id':missionid})
            # 创建查询到的json表单
            jsonobj = dbget(result,LIST_MISSION)
            return jsonify(jsonobj)
        except:
            return errcode.failed()
    # 更改任务信息
    elif request.method == 'POST':
        # 参数接收
        try:
            collection_mission.update({'mid':mid},{
                '$set':{
                    'mid':request.form['mid'],
                    'name':request.form['name'],
                    'mtype':request.form['mtype'],
                    'deadline':request.form['deadline'],
                    'description':request.form['description'],
                    'reward':request.form['reward'],
                    'skillneed':request.form['skillneed'],
                    'feedback':request.form['feedback'],
                    'state':request.form['stat'],
                    'publisher':request.form['publisher'],
                    'bidders':request.form['bidders'],
                    'employer':request.form['employer'],
                    'comment':request.form['comment'],
                    'feedback':request.form['feedback'],
                    'publishtime':request.form['publishtime']
                    }
                })

            return errcode.success()
        except:
            return errcode.failed()
    else:
        return 'nothing happend!'

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
@app.route('/skill/<skillid>', methods = ['GET', 'POST'])
def skill(skillid):
    # 获取单个技能
    if request.method == 'GET':
        try:
            result = collection_skill.find_one({'skillid':skillid})
            jsonobj = {'skillid':result.get('skillid'),'name':result.get('name'),
            'tag':result.get('tag'),'description':result.get('description'),'CA':result.get('CA')}
            return jsonify(jsonobj)
        except:
            return 'search fail!'
    # 更改技能信息
    elif request.method == 'POST':
        # 参数接收
        skillid = request.form['skillid']
        name = request.form['name']
        tag = request.form['tag']
        description = request.form['description']
        CA = request.form['CA']
        try:
            collection_skill.update({'skillid':skillid},{'$set':{'name':name,
                'tag':tag,'description':description,'CA':CA}})
            return 'update ok!'
        except:
            return 'update fail!'
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
            jsonlist.append({'skillid':item.get('skillid'),'name':item.get('name'),
                'tag':item.get('tag'),'description':item.get('description'),'CA':item.get('CA')})
        jsonobj = {'skill':jsonlist}
        return jsonify(jsonobj)
    # post - 添加新技能
    elif request.method == 'POST':
        # 参数接收
        skillid = request.form['skillid']
        name = request.form['name']
        tag = request.form['tag']
        description = request.form['description']
        CA = request.form['CA']
        try:
            collection_skill.insert_one({'skillid':skillid,'name':name,'tag':tag,
                'description':description,'CA':CA})
            return 'insert ok!'
        except:
            return 'insert failed!'      
    else:
        return 'nothing happend!'

# 标签
@app.route('/tag/<tagid>', methods = ['GET', 'POST'])
def tag(tagid):
    # 获取单个标签
    if request.method == 'GET':
        try:
            result = collection_tag.find_one({'tagid':tagid})
            jsonobj = {'tagid':result.get('tagid'),'name':result.get('name'),
            'description':result.get('description')}
            return jsonify(jsonobj)
        except:
            return 'search fail!'
    # 更改标签
    elif request.method == 'POST':
        # 参数接收
        tagid = request.form['tagid']
        name = request.form['name']
        description = request.form['description']
        try:
            collection_tag.update({'tagid':tagid},{'$set':{'name':name,
                'description':description}})
            return 'update ok!'
        except:
            return 'update fail!'
    # 其它
    else:
        return 'nothing happend!'

# 全部标签
@app.route('/tag/', methods = ['GET', 'POST'])
def tags():
    # get - 获取全部标签信息
    if request.method == 'GET':        
        jsonlist = []
        for item in collection_tag.find({}):
            jsonlist.append({'tagid':item.get('tagid'),'name':item.get('name'),
                'description':item.get('description'),})
        jsonobj = {'tag':jsonlist}
        return jsonify(jsonobj)
    # post - 添加新标签
    elif request.method == 'POST':
        # 参数接收
        tagid = request.form['tagid']
        name = request.form['name']
        description = request.form['description']
        try:
            collection_tag.insert_one({'tagid':tagid,'name':name,'description':description})
            return 'insert ok!'
        except:
            return 'insert failed!'      
    else:
        return 'nothing happend!'

# 运行主函数
if __name__ == '__main__':
    # 测试
    app.run(host='0.0.0.0',port=8080,debug=True)
    # 生产
    # app.run(host='0.0.0.0',port=80,debug=False)
