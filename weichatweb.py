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

# 编码修正
def codefix(s):
    s = s.encode('ISO-8859-1')
    s = s.decode('UTF-8')
    return s


# 获取用户基本信息
def getUserInfo(code,state,nsukey):
    # 通过code获取openid
    url_openid = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+APPID+"&secret="+APPSECRET+"&code="+code+"&grant_type=authorization_code"
    req_openid = requests.get(url_openid)
    openid = req_openid.json().get('openid')
    access_token = req_openid.json().get('access_token')

    # 通过openid获取用户资料
    url_userinfo = "https://api.weixin.qq.com/sns/userinfo?access_token="+access_token+"&openid="+openid+"&lang=zh_CN"
    req_userinfo = requests.get(url_userinfo)
    userinfo = req_userinfo.json()
    # 返回用户基本信息
    return userinfo


# 数据库操作
class dbOpt(object):
    """docstring for dbOpt"""
    def __init__(self, dburl):
        super(dbOpt, self).__init__()
        self.dburl = dburl

    # 数据查询
    def dbget(self,suburl):
        # http头
        headers = {'content-type': 'application/json'}
        r = requests.get(self.dburl + suburl, headers = headers)
        result = r.json()
        return result


    # 数据更新
    def dbpost(self,suburl,postdata):
        # http头
        headers = {'content-type': 'application/json'}
        r = requests.post(self.dburl + suburl, data=json.dumps(postdata), headers = headers)
        result = r.json()
        return result

    # 数据新建
    def dbput(self,suburl,putdata):
        # http头
        headers = {'content-type': 'application/json'}
        r = requests.put(self.dburl + suburl, data=json.dumps(putdata), headers = headers)
        result = r.json()
        return result

        
db_obj = dbOpt(dburl = 'http://liangchaob-bountyapi.daoapp.io/')




# 微信验证
@app.route('/wechat_auth', methods = ['GET', 'POST'])
def wechat_auth():
    if request.method == 'GET':
        # 参数接收
        query = request.args 
        signature = query.get('signature', '')  
        timestamp = query.get('timestamp', '')  
        nonce = query.get('nonce', '')  
        echostr = query.get('echostr', '')
        # 验证
        if wechat.check_signature(signature, timestamp, nonce):
            print 'Accept'
            return echostr
        else:
            print 'Wrong'
            return 'nothing happend!'
    elif request.method == 'POST':
        # 获取post得到的xml信息
        rec_text = request.stream.read()
        try:
            # 实例化xml的信息对象
            wechat.parse_data(rec_text)
            rec_id = wechat.message.id          # 对应于 XML 中的 MsgId
            rec_target = wechat.message.target  # 对应于 XML 中的 ToUserName
            rec_source = wechat.message.source  # 对应于 XML 中的 FromUserName
            rec_time = wechat.message.time      # 对应于 XML 中的 CreateTime
            rec_type = wechat.message.type      # 对应于 XML 中的 MsgType
            # rec_raw = wechat.message.raw        # 原始 XML 文本，方便进行其他分析
            # rec_content = wechat.message.content # post的文本信息
            print "消息id:"+str(rec_id)
            print "公众号id:"+str(rec_target)
            print "用户openid:"+str(rec_source)
            print "时间戳:"+str(rec_time)
            print "消息类型:"+str(rec_type)
            # print rec_raw
            # print "信息内容:"+str(rec_content)

            if rec_type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                try:
                    # 新添用户
                    useradd = {'openid':str(rec_source)}
                    result = db_obj.dbpost('api/user/',useradd ) 
                except Exception, e:
                    pass

                try:
                    # 激活用户
                    user_on = {'state':'on'}
                    result = db_obj.dbput('api/user/'+str(rec_source),user_on)
                except Exception, e:
                    pass

                
                # 关注获取用户openid,并将其状态置位为on
                key = wechat.message.key           # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
                ticket = wechat.message.ticket     # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
                return wechat.response_text("欢迎加入赏金猎人公会!")

            if rec_type == 'unsubscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                try:
                    # 注销用户
                    user_off = {'state':'off'}
                    result = db_obj.dbput('api/user/'+str(rec_source),user_off)
                except Exception, e:
                    raise e

            elif rec_type == 'click':  # 自定义菜单点击事件
                key = wechat.message.key           # 对应于 XML 中的 EventKey
                if key == 'TODAY_MISSIONS':
                    feedback = wechat.response_news([
                        {
                            'title': u'IT类项目',
                            'picurl': u'http://o7m541j22.bkt.clouddn.com/justdoit.jpg',
                            'description': u'Cisco、Oracle、Linux相关',
                            'url': u'http://www.baidu.com/',
                        },{
                            'title': u'非IT类项目',
                            'picurl': u'http://o7m541j22.bkt.clouddn.com/biznetwork.png',
                            'description': u'其他和IT相关的非技术性任务',
                            'url': u'http://www.baidu.com/',
                        }

                    ])
                    return feedback
                elif key == 'APP_HELP':
                    feedback = wechat.response_news([
                        {
                            'title': u'帮助',
                            'picurl': u'http://o7m541j22.bkt.clouddn.com/biznetwork.png',
                            'description': u'正确姿势',
                            'url': u'http://www.baidu.com/',
                        }

                    ])
                    return feedback
                else:
                    pass

            elif rec_type == 'text':
                rec_content = wechat.message.content
                print "消息id:"+str(rec_id)
                print "公众号id:"+str(rec_target)
                print "用户openid:"+str(rec_source)
                print "时间戳:"+str(rec_time)
                print "消息类型:"+str(rec_type)
                feedback = wechat.response_news([
                    {
                        'title': u'第1条新闻标题',
                        'picurl': u'http://o7m541j22.bkt.clouddn.com/biznetwork.png',
                        'description': u'第一条新闻描述，这条新闻没有预览图',
                        'url': u'http://www.baidu.com/',
                    }, {
                        'title': u'第2条新闻标题, 这条新闻无描述',
                        'picurl': u'http://o7m541j22.bkt.clouddn.com/biznetwork.png',
                        'url': u'http://www.github.com/',
                    }, {
                        'title': u'第3条新闻标题',
                        'description': u'第三条新闻描述',
                        'picurl': u'http://http://o7m541j22.bkt.clouddn.com/group.png',
                        'url': u'http://www.v2ex.com/',
                    }
                ])
                return feedback

        except ParseError:
            print 'Invalid Body Text'
            return 'nothing'

# 新任务
@app.route('/wechat/new_mission', methods = ['GET', 'POST'])
def new_mission():
    if request.method == 'GET':
        # 参数接收获取code
        query = request.args 
        code = query.get('code', '')  
        state = query.get('state', '')
        nsukey = query.get('nsukey', '')

        # 获取用户信息
        userinfo = getUserInfo(code,state,nsukey)

        # 从资料中提取具体信息
        nickname = userinfo.get('nickname')
        openid = userinfo.get('openid')
        sex = userinfo.get('sex')
        province = userinfo.get('province')
        city = userinfo.get('city')
        country = userinfo.get('country')
        headimgurl = userinfo.get('headimgurl')

        # 修正编码格式
        nickname = codefix(nickname)
        province = codefix(province)
        city = codefix(city)
        country = codefix(country)

        # 渲染
        return render_template('new_mission.html',openid = openid)
    # 提交任务
    elif request.method == 'POST':
        try:
            jsonobj = {
                'mission_id':str(uuid.uuid1()),
                'name':request.form['mission_name'],
                'mission_type':request.form['mission_type'],
                'deadline':request.form['deadline'],
                'description':request.form['description'],
                'skill_need':request.values.getlist('skill_need'),
                'bounty':request.form['bounty'],
                'state':1,
                'comment':'',
                'bidder':'',
                'publisher':request.form['publisher'],
                'acceptor':'',
                'feedback':''
                }

            result = db_obj.dbpost('api/mission/',jsonobj)

            # # 更新数据库
            # headers = {'content-type': 'application/json'}
            # r = requests.post('http://liangchaob-bountyapi.daoapp.io/mission/', data=json.dumps(jsonobj),headers = headers)
            # req_openid = requests.get(url_openid)

            # return json.dumps(jsonobj)
            return redirect('/wechat/mission_commit') 
        except:
            return 'wrong!'
    else:
        pass




# 确认提交完成
@app.route('/wechat/mission_commit', methods = ['GET', 'POST'])
def mission_commit():
    if request.method == 'GET':
        return render_template('mission_commit.html')
    elif request.method == 'POST':
        return render_template('mission_commit.html')
    else:
        pass
    
# 用户中心
@app.route('/wechat/user_center', methods = ['GET', 'POST'])
def user_center():
    if request.method == 'GET':
        # 参数接收获取code
        query = request.args 
        code = query.get('code', '')  
        state = query.get('state', '')
        nsukey = query.get('nsukey', '')
        # 获取用户信息
        userinfo = getUserInfo(code,state,nsukey)
        # 从资料中提取具体信息
        nickname = userinfo.get('nickname')
        openid = userinfo.get('openid')
        sex = userinfo.get('sex')
        province = userinfo.get('province')
        city = userinfo.get('city')
        country = userinfo.get('country')
        headimgurl = userinfo.get('headimgurl')
        # 修正编码格式
        nickname = codefix(nickname)
        province = codefix(province)
        city = codefix(city)
        country = codefix(country)

        # # 查询数据库
        # headers = {'content-type': 'application/json'}
        # r = requests.get('http://liangchaob-bountyapi.daoapp.io/mission/',headers = headers)
        # result = r.json()

        # mission_list = result.get('mission')

        # # 筛选出该用户发布的任务
        # user_mission = []
        # for mission in mission_list:
        #     if mission.get('openid') == openid:
        #         user_mission.append(mission)

        # # 查询已发布
        # mission_published = result.get('openid')
        # # 查询已参与
        # mission_recived
        # # 查询已完成
        # mission_finished



        # 渲染
        return render_template('usercenter.html', openid = openid, nickname = nickname, 
            country = country , province = province, city = city, headimgurl = headimgurl)

    elif request.method == 'POST':
        return render_template('usercenter.html')
    else:
        pass






# 已发布
@app.route('/wechat/usercenter_published', methods = ['GET', 'POST'])
def usercenter_published():

    if request.method == 'GET':
        # 参数接收获取code
        query = request.args 
        code = query.get('code', '')  
        state = query.get('state', '')
        nsukey = query.get('nsukey', '')

        # 获取用户信息
        userinfo = getUserInfo(code,state,nsukey)

        # 从资料中提取具体信息
        nickname = userinfo.get('nickname')
        openid = userinfo.get('openid')
        sex = userinfo.get('sex')
        province = userinfo.get('province')
        city = userinfo.get('city')
        country = userinfo.get('country')
        headimgurl = userinfo.get('headimgurl')

        # 修正编码格式
        nickname = codefix(nickname)
        province = codefix(province)
        city = codefix(city)
        country = codefix(country)

        # 数据提取
        result = db_obj.dbget('api/mission/publisher/' + openid)

        # 审核阶段
        state_0 = []
        # 发布阶段
        state_1 = []
        # 竞标阶段
        state_2 = []
        # 工作阶段
        state_3 = []
        # 评价阶段
        state_4 = []

        for item in result:
            if item["state"] == '0':
                state_0.append(item)
            elif item["state"] == '1':
                state_1.append(item)
            elif item["state"] == '2':
                state_2.append(item)
            elif item["state"] == '3':
                state_3.append(item)
            elif item["state"] == '4':
                state_4.append(item)
            else:
                pass

        # return render_template('published_mission.html',openid = openid)
        return render_template('published_mission.html',openid=openid, state_0=state_0,state_1=state_1, state_2=state_2, state_3=state_3,state_4=state_4)






@app.route('/wechat/mission/<mission_id>', methods = ['GET', 'POST'])
def mission(mission_id):
    if request.method == 'GET':
        # 参数接收获取code
        query = request.args 
        code = query.get('code', '')  
        state = query.get('state', '')
        nsukey = query.get('nsukey', '')
        # 获取用户信息
        userinfo = getUserInfo(code,state,nsukey)
        # 从资料中提取具体信息
        openid = userinfo.get('openid')

        # return 'hehe'
        result = db_obj.dbget('api/mission/id/' + mission_id)
        # 如果任务处于待修改或发布状态
        if result['state'] == '0' or result['state'] == '1':
            return render_template('mission_edit.html',mission_obj=result,openid=openid)
        elif result['state'] == '2':
            return render_template('mission_bidding.html',mission_obj=result,openid=openid)
        else:
        # result = {'comment':result}
        # return jsonify(result)
            return render_template('mission_bidding.html',mission_obj=result,openid=openid)
    else:
        pass




# 查看表单
@app.route('/wechat/check_mission', methods = ['GET', 'POST'])
def check_mission():
    if request.method == 'GET':
        return render_template('check_mission.html')
    elif request.method == 'POST':
        return render_template('check_mission.html')
    else:
        pass
# 修改表单
@app.route('/wechat/edit_mission', methods = ['GET', 'POST'])
def edit_mission():
    if request.method == 'GET':
        return render_template('edit_mission.html')
    elif request.method == 'POST':
        return render_template('edit_mission.html')
    else:
        pass
# 竞标
@app.route('/wechat/bid_mission', methods = ['GET', 'POST'])
def bid_mission():
    if request.method == 'GET':
        return render_template('bid_mission.html')
    elif request.method == 'POST':
        return render_template('bid_mission.html')
    else:
        pass

# 评论
@app.route('/wechat/comment', methods = ['GET', 'POST'])
def comment():
    # if request.method == 'POST':
    #     return render_template('bid_mission.html')
    # 提交任务
    if request.method == 'POST':
        try:
            jsonobj = {
                'comment_id':str(uuid.uuid1()),
                'mission_id':request.form['mission_id'],
                'openid':request.form['openid'],
                'content':request.form['content']
                }

            mission_id = request.form['mission_id']

            result = db_obj.dbpost('api/comment/',jsonobj)
            return 'ok'
            # return redirect(url_for('mission',mission_id=mission_id))

        except Exception, e:
            pass
            # return redirect(url_for('mission',mission_id=mission_id))
    else:
        pass
        # return redirect(url_for('mission',mission_id=mission_id))


# 确认完成
@app.route('/wechat/work_mission', methods = ['GET', 'POST'])
def work_mission():
    if request.method == 'GET':
        return render_template('work_mission.html')
    elif request.method == 'POST':
        return render_template('work_mission.html')
    else:
        pass
# 评价
@app.route('/wechat/comment_mission', methods = ['GET', 'POST'])
def comment_mission():
    if request.method == 'GET':
        return render_template('comment_mission.html')
    elif request.method == 'POST':
        return render_template('comment_mission.html')
    else:
        pass

# 注册
@app.route('/wechat/user_register', methods = ['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return render_template('user_register.html')
    elif request.method == 'POST':
        return render_template('user_register.html')
    else:
        pass


# 帮助页面
@app.route('/wechat/help', methods = ['GET', 'POST'])
def apphelp():
    if request.method == 'GET':
        return render_template('help.html')
    else:
        pass


# 帮助页面
@app.route('/wechat/t1', methods = ['GET', 'POST'])
def t2():
    if request.method == 'GET':
        return render_template('weichat_newmission.html')
    else:
        pass

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


# 9eeaa838-78b2-11e6-8cfa-d5fca37bf494






# 运行主函数
if __name__ == '__main__':
    # 对外开放80端口
    app.run(host='0.0.0.0',port=80,debug=True)




