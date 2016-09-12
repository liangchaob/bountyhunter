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
# 新建用户
payload={
    'openid':2,
    'intro':'',
    'role':'admin',
    'feedback':'',
    'level':'',
    'skill':'',
    'mission_published':'',
    'mission_accept':'',
    'state':'',
    'spent':'',
    'income':'',
    'email':'',
    'mobile':''
    }




r=requests.post('http://0.0.0.0:8080/api/user/',data=payload)


print r.text


# 激活用户
payload={
    'openid':2,
    'intro':'tt',
    'role':'user',
    'feedback':'',
    'level':'',
    'skill':'',
    'mission_published':'',
    'mission_accept':'',
    'state':'',
    'spent':'',
    'income':'',
    'email':'',
    'mobile':''
    }

r=requests.put('http://0.0.0.0:8080/api/user/2',data=payload)


print r.text








# 新建项目
payload={
    'mission_id':'004',
    'name':'测试项目4',
    'mission_type':'IT',
    'deadline':'',
    'description':'就是个简单的测试4',
    'skill_need':['测试'],
    'bounty':'',
    'state':1,
    'comment':'',
    'bidder':'',
    'publisher':'3',
    'acceptor':'',
    'feedback':''
    }

r=requests.post('http://0.0.0.0:8080/api/mission/',data=payload)


print r.text




