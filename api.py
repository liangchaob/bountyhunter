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




from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask.ext.restful import reqparse
import json
# 导入pymongo模块
import pymongo



# 数据部分
# 生产
MONGODB_ADDR = '10.10.72.139'
MONGODB_PORT = 27017
MONGODB_DB = '3cVNYBye7mztp8v4'
# 测试
# MONGODB_ADDR = '172.16.191.163'
# MONGODB_PORT = 27017
# MONGODB_DB = 'local'

# 设置数据库地址
client = pymongo.MongoClient(MONGODB_ADDR, MONGODB_PORT)

# 设置数据库名
db = client[MONGODB_DB]

# 生产认证
db.authenticate("uMvW5dqcFu0K6IkU","phG8sY6MtkrwIzuFp")

# 设置表名,建立为索引
# 用户表
collection_user = db['user']
collection_user.ensure_index('openid',unique=True)
# 任务表
collection_mission = db['mission']
collection_mission.ensure_index('mission_id',unique=True)





# 应用部分
app = Flask(__name__)
api = Api(app)





# 解析器
# 用户对象
userobj = reqparse.RequestParser()
userobj.add_argument('openid', type=str)
userobj.add_argument('intro', type=str)
userobj.add_argument('role', type=str)
userobj.add_argument('feedback', type=str)
userobj.add_argument('level', type=str)
userobj.add_argument('skill', type=str)
userobj.add_argument('mission_published', type=str)
userobj.add_argument('mission_accept', type=str)
userobj.add_argument('state', type=str)
userobj.add_argument('spent', type=str)
userobj.add_argument('income', type=str)
userobj.add_argument('email', type=str)
userobj.add_argument('mobile', type=str)



# 用户对象
missionobj = reqparse.RequestParser()
missionobj.add_argument('mission_id', type=str)
missionobj.add_argument('name', type=str)
missionobj.add_argument('mission_type', type=str)
missionobj.add_argument('deadline', type=str)
missionobj.add_argument('description', type=str)
missionobj.add_argument('skill_need', type=str)
missionobj.add_argument('bounty', type=str)
missionobj.add_argument('state', type=str)
missionobj.add_argument('comment', type=str)
missionobj.add_argument('bidder', type=str)
missionobj.add_argument('publisher', type=str)
missionobj.add_argument('acceptor', type=str)
missionobj.add_argument('feedback', type=str)






# 全部用户
class Users(Resource):
    def get(self):
        jsonlist = []
        for item in collection_user.find({},{'_id':0}):
            jsonlist.append(item)
        return jsonlist

    def post(self):
        args = userobj.parse_args()
        try:
            collection_user.insert_one(dict(args))
        except Exception, e:
            pass
        return args


# 单用户
class User(Resource):
    def get(self, user_id):
        result = collection_user.find_one({'openid':user_id},{'_id':0})
        return result

    def put(self, user_id):
        # 获取参数
        args = userobj.parse_args()
        # 把空值筛除
        args = dict(args)
        result = {}
        for i in args:
            if args[i] != '' and args[i] != None:
                result[i] = args[i]
            else:
                pass
        # 入库
        try:
            collection_user.update({'openid':user_id},{'$set':result})
        except Exception, e:
            pass
        return result

        
# 全部任务
class Missions(Resource):
    def get(self):
        jsonlist = []
        for item in collection_mission.find({},{'_id':0}):
            jsonlist.append(item)
        return jsonlist

    def post(self):
        args = missionobj.parse_args()
        try:
            collection_mission.insert_one(dict(args))
        except Exception, e:
            pass
        return args

# 单任务
class MissionById(Resource):
    def get(self, mission_id):
        result = collection_mission.find_one({'mission_id':mission_id},{'_id':0})
        return result

    def put(self, mission_id):
        # 获取参数
        args = mission.parse_args()
        # 把空值筛除
        args = dict(args)
        result = {}
        for i in args:
            if args[i] != '' and args[i] != None:
                result[i] = args[i]
            else:
                pass
        # 入库
        try:
            collection_mission.update({'mission_id':mission_id},{'$set':result})
        except Exception, e:
            pass
        return result

# 单任务
class MissionByPublisher(Resource):
    def get(self, publisher):
        result = collection_mission.find({'publisher':publisher},{'_id':0})
        return result

    # def put(self, publisher):
    #     # 获取参数
    #     args = mission.parse_args()
    #     # 把空值筛除
    #     args = dict(args)
    #     result = {}
    #     for i in args:
    #         if args[i] != '' and args[i] != None:
    #             result[i] = args[i]
    #         else:
    #             pass
    #     # 入库
    #     try:
    #         collection_mission.update({'publisher':publisher},{'$set':result})
    #     except Exception, e:
    #         pass
    #     return result



# 全部技能
class Skills(Resource):
    def get(self):
        return {'hello': 'world'}


# 单技能
class Skill(Resource):
    def get(self):
        return {'hello': 'world'}


# 全部留言
class Comments(Resource):
    def get(self):
        return {'hello': 'world'}

# 单条留言
class Comment(Resource):
    def get(self):
        return {'hello': 'world'}

# 全部评价
class Feedbacks(Resource):
    def get(self):
        return {'hello': 'world'}

# 单条评价
class Feedback(Resource):
    def get(self):
        return {'hello': 'world'}



# 路由表
api.add_resource(Users, '/api/user/')
api.add_resource(User, '/api/user/<string:user_id>')
api.add_resource(Missions, '/api/mission/')
api.add_resource(MissionById, '/api/mission/id/<string:mission_id>')
api.add_resource(MissionByPublisher, '/api/mission/publisher/<string:publisher>')
api.add_resource(Skills, '/api/skill/')
api.add_resource(Skill, '/api/skill/<string:skill_id>')
api.add_resource(Comments, '/api/comment/')
api.add_resource(Comment, '/api/comment/<string:comment_id>')
api.add_resource(Feedbacks, '/api/feedback/')
api.add_resource(Feedback, '/api/feedback/<string:feedback_id>')



# 开启跨域允许
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


# 服务进程
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
    # app.run(host='0.0.0.0',port=8080,debug=True)










# from flask import Flask
# from flask.ext.restful import reqparse, abort, Api, Resource

# app = Flask(__name__)
# api = Api(app)

# TODOS = {
#     'todo1': {'task': 'build an API'},
#     'todo2': {'task': '?????'},
#     'todo3': {'task': 'profit!'},
# }


# def abort_if_todo_doesnt_exist(todo_id):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))

# parser = reqparse.RequestParser()
# parser.add_argument('task', type=str)


# # Todo
# #   show a single todo item and lets you delete them
# class Todo(Resource):
#     def get(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         return TODOS[todo_id]

#     def delete(self, todo_id):
#         abort_if_todo_doesnt_exist(todo_id)
#         del TODOS[todo_id]
#         return '', 204

#     def put(self, todo_id):
#         args = parser.parse_args()
#         task = {'task': args['task']}
#         TODOS[todo_id] = task
#         return task, 201


# # TodoList
# #   shows a list of all todos, and lets you POST to add new tasks
# class TodoList(Resource):
#     def get(self):
#         return TODOS

#     def post(self):
#         args = parser.parse_args()
#         todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
#         todo_id = 'todo%i' % todo_id
#         TODOS[todo_id] = {'task': args['task']}
#         return TODOS[todo_id], 201

# ##
# ## Actually setup the Api resource routing here
# ##
# api.add_resource(TodoList, '/todos')
# api.add_resource(Todo, '/todos/<todo_id>')


# if __name__ == '__main__':
#     app.run(host='0.0.0.0',port=8080,debug=True)

