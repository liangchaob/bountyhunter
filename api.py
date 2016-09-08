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



# 应用部分
app = Flask(__name__)
api = Api(app)

userdb=[]

userobj = {
    'openid':'openid',
    'intro':'intro',
    'role':'role',
    'feedback':'feedback',
    'level':'level',
    'skill':'skill',
    'mission_published':'mission_published',
    'mission_accept':'mission_accept',
    'mission_accomplish':'mission_accomplish',
    'state':'state',
    'spent':'spent',
    'income':'income',
    'email':'email',
    'mobile':'mobile'
}




# 解析器
# 用户对象
userobj = reqparse.RequestParser()
userobj.add_argument('openid', type=str)
userobj.add_argument('role', type=str)


# 模拟数据库操作
def filterUser(user,user_id):
    return user.openid == user_id



# 全部用户
class Users(Resource):
    def get(self):
        return userdb

    def post(self):
        args = userobj.parse_args()
        userdb.append(args)
        return userdb


# 单用户
class User(Resource):
    def get(self,user_id):
        # filter(filterUser,userdb)
        return filter(filterUser(user_id=user_id),userdb)

    def put(self, user_id):
        user_dict[user_id] = request.form['data']
        return {'user_id': user_dict[user_id]}

        
# 全部任务
class Missions(Resource):
    def get(self):
        return {'hello': 'world'}

# 单任务
class Mission(Resource):
    def get(self):
        return {'hello': 'world'}


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
api.add_resource(Mission, '/api/mission/<string:mission_id>')
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
    app.run(host='0.0.0.0',port=8080,debug=True)










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

