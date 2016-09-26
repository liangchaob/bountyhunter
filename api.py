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
# 留言表
collection_comment = db['comment']
collection_comment.ensure_index('comment_id',unique=True)





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



# 任务对象
missionobj = reqparse.RequestParser()
missionobj.add_argument('mission_id', type=str)
missionobj.add_argument('name', type=str)
missionobj.add_argument('mission_type', type=str)
missionobj.add_argument('deadline', type=str)
missionobj.add_argument('description', type=str)
missionobj.add_argument('skill_need', type=str ,action='append')
missionobj.add_argument('bounty', type=str)
missionobj.add_argument('state', type=str)
missionobj.add_argument('comment', type=str)
missionobj.add_argument('bidder', type=str ,action='append')
missionobj.add_argument('publisher', type=str)
missionobj.add_argument('acceptor', type=str)
missionobj.add_argument('feedback', type=str)




# 评价对象
commentobj = reqparse.RequestParser()
commentobj.add_argument('comment_id', type=str)
commentobj.add_argument('mission_id', type=str)
commentobj.add_argument('openid', type=str)
commentobj.add_argument('content', type=str)
commentobj.add_argument('currenttime', type=str)



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
        args = dict(args)
        result = {}
        for i in dict(args):
            if args[i] != '' and args[i] != None:
                result[i] = args[i]
            else:
                pass

        try:
            collection_mission.insert_one(result)
        except Exception, e:
            pass
        return args

    def delete(self):
        # args = commentobj.parse_args()
        try:
            collection_mission.remove()
        except Exception, e:
            pass
        return 'clear success!'



# 单任务通过id查询
class MissionById(Resource):
    def get(self, mission_id):
        result = collection_mission.find_one({'mission_id':mission_id},{'_id':0})
        return result

    def put(self, mission_id):
        # 获取参数
        args = missionobj.parse_args()
        # 把空值筛除
        args = dict(args)
        result = {}
        for i in args:
            if args[i] != '' and args[i] != None:
                result[i] = args[i]
            else:
                pass

        # 入库
        # # 留言列表筛选
        # if result.get('commit') !='' and result.get('commit') != None:
        #     collection_mission.update({'mission_id':mission_id},{'$push':result})
        # # 竞标列表筛选
        # elif result.get('bidder') !='' and result.get('bidder') != None:
        #     collection_mission.update({'mission_id':mission_id},{'$push':result})


        # 留言列表筛选
        # 如果是留言或者竞标参与，则用push方法应用列表更新
        if result.get('commit') != None or result.get('bidder') != None:
            collection_mission.update({'mission_id':mission_id},{'$push':result})


        else:
            try:
                collection_mission.update({'mission_id':mission_id},{'$set':result})
            except Exception, e:
                pass

        return result


    def delete(self, mission_id):
        # 操作库
        try:
            collection_mission.remove({'mission_id':mission_id})
        except Exception, e:
            pass
        return 'delete '+mission_id+' success!'

# 单任务通过用户查询
class MissionByPublisher(Resource):
    def get(self, publisher):
        result = collection_mission.find({'publisher':publisher},{'_id':0})
        t = []
        for item in result:
            t.append(item)
        return t

# 单任务通过参与人查询
# class MissionByParticipant(Resource):
#     def get(self, participant):
#         result = collection_mission.find({'publisher':publisher},{'_id':0})
#         t = []
#         for item in result:
#             t.append(item)
#         return t

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
        jsonlist = []
        for item in collection_comment.find({},{'_id':0}):
            jsonlist.append(item)
        return jsonlist

    def post(self):
        args = commentobj.parse_args()
        try:
            collection_comment.insert_one(dict(args))
        except Exception, e:
            pass
        return args

    def delete(self):
        # args = commentobj.parse_args()
        try:
            collection_comment.remove()
        except Exception, e:
            pass
        return 'clear success!'



# 单任务通过id查询
class CommentById(Resource):
    def get(self, comment_id):
        result = collection_comment.find_one({'comment_id':comment_id},{'_id':0})
        return result

    def put(self, comment_id):
        # 获取参数
        args = commentobj.parse_args()
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
            collection_comment.update({'comment_id':comment_id},{'$set':result})
        except Exception, e:
            pass
        return result


# 单留言通过mission查询
class CommentByMission(Resource):
    def get(self, mission_id):
        result = collection_comment.find({'mission_id':mission_id},{'_id':0})
        t = []
        for item in result:
            t.append(item)
        return t



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
# api.add_resource(MissionByParticipant, '/api/mission/participant/<string:participant>')
api.add_resource(Skills, '/api/skill/')
api.add_resource(Skill, '/api/skill/<string:skill_id>')
api.add_resource(Comments, '/api/comment/')
# api.add_resource(Comment, '/api/comment/<string:comment_id>')
api.add_resource(CommentById, '/api/comment/id/<string:comment_id>')
api.add_resource(CommentByMission, '/api/comment/mission/<string:mission_id>')
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


