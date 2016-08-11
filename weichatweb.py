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

def codefix(s):
    s = s.encode('ISO-8859-1')
    s = s.decode('UTF-8')
    return s

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
                key = wechat.message.key           # 对应于 XML 中的 EventKey (普通关注事件时此值为 None)
                ticket = wechat.message.ticket     # 对应于 XML 中的 Ticket (普通关注事件时此值为 None)
                return wechat.response_text("欢迎加入赏金猎人公会!")

            elif rec_type == 'click':  # 自定义菜单点击事件
                key = wechat.message.key           # 对应于 XML 中的 EventKey
                if key == 'TODAY_MISSIONS':
                    feedback = wechat.response_news([
                        {
                            'title': u'IT类项目',
                            'picurl': u'http://o7m541j22.bkt.clouddn.com/biznetwork.png',
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
                    },{
                        'title': u'第4条新闻标题',
                        'description': u'第三条新闻描述',
                        'picurl': u'http://http://o7m541j22.bkt.clouddn.com/group.png',
                        'url': u'http://www.v2ex.com/',
                    },{
                        'title': u'第5条新闻标题',
                        'description': u'第三条新闻描述',
                        'picurl': u'http://http://o7m541j22.bkt.clouddn.com/group.png',
                        'url': u'http://www.v2ex.com/',
                    },{
                        'title': u'第6条新闻标题',
                        'description': u'第三条新闻描述',
                        'picurl': u'http://http://o7m541j22.bkt.clouddn.com/group.png',
                        'url': u'http://www.v2ex.com/',
                    },{
                        'title': u'第7条新闻标题',
                        'description': u'第三条新闻描述',
                        'picurl': u'http://http://o7m541j22.bkt.clouddn.com/group.png',
                        'url': u'http://www.v2ex.com/',
                    },{
                        'title': u'第8条新闻标题',
                        'description': u'第三条新闻描述',
                        'picurl': u'http://http://o7m541j22.bkt.clouddn.com/group.png',
                        'url': u'http://www.v2ex.com/',
                    },{
                        'title': u'第9条新闻标题',
                        'description': u'第三条新闻描述',
                        'picurl': u'http://http://o7m541j22.bkt.clouddn.com/group.png',
                        'url': u'http://www.v2ex.com/',
                    },{
                        'title': u'第10条新闻标题',
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
        print 'code:'+code
        print 'state:'+state
        print 'nsukey:'+nsukey

        # 通过code获取openid
        url_openid = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+APPID+"&secret="+APPSECRET+"&code="+code+"&grant_type=authorization_code"
        req_openid = requests.get(url_openid)

        openid = req_openid.json().get('openid')
        access_token = req_openid.json().get('access_token')
        # return openid

        # 通过openid获取用户资料
        url_userinfo = "https://api.weixin.qq.com/sns/userinfo?access_token="+access_token+"&openid="+openid+"&lang=zh_CN"
        req_userinfo = requests.get(url_userinfo)
        userinfo = req_userinfo.json()

        # 从资料中提取具体信息
        nickname = userinfo.get('nickname')
        url_openid = userinfo.get('url_openid')
        url_userinfo = userinfo.get('url_userinfo')
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

    elif request.method == 'POST':
        try:
            jsonobj = {
                'openid':request.form['openid'],
                'name':request.form['mission_name'],
                'mission_type':request.form['mission_type'],
                'deadline':request.form['deadline'],
                'description':request.form['description'],
                'obj':request.form['obj'],
                'skill_need':request.form['skill_need'],
                'bounty':request.form['bounty'],
                'state':1,
                'comment':123,
                'bidder':12,
                'publisher':12,
                'acceptor':13
                }
            # r = requests.post('http://liangchaob-bountyhunter.daoapp.io/mission/', data=json.dumps(jsonobj))
            return jsonobj.get('openid')
        except:
            return 'wrong!'
    else:
        pass


# 个人中心
@app.route('/wechat/myinfo', methods = ['GET', 'POST'])
def myinfo():
    if request.method == 'GET':
        # 参数接收获取code
        query = request.args 
        code = query.get('code', '')  
        state = query.get('state', '')
        nsukey = query.get('nsukey', '')
        print 'code:'+code
        print 'state:'+state
        print 'nsukey:'+nsukey
        # 通过code获取openid
        url_openid = "https://api.weixin.qq.com/sns/oauth2/access_token?appid="+APPID+"&secret="+APPSECRET+"&code="+code+"&grant_type=authorization_code"
        req_openid = requests.get(url_openid)
        openid = req_openid.json().get('openid')
        access_token = req_openid.json().get('access_token')
        # return openid
        # 通过openid获取用户资料
        url_userinfo = "https://api.weixin.qq.com/sns/userinfo?access_token="+access_token+"&openid="+openid+"&lang=zh_CN"
        req_userinfo = requests.get(url_userinfo)
        userinfo = req_userinfo.json()

        # 从资料中提取具体信息
        nickname = userinfo.get('nickname')
        url_openid = userinfo.get('url_openid')
        url_userinfo = userinfo.get('url_userinfo')
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

        # 返回渲染页面
        return render_template('t1.html',nickname = nickname,url_openid = url_openid,
            url_userinfo = url_userinfo,sex = sex, province = province, city=city,
            country = country,headimgurl = headimgurl)

    elif request.method == 'POST':
        return render_template('new_mission.html')
    else:
        pass











# # 新任务
# @app.route('/wechat/new_mission', methods = ['GET', 'POST'])
# def new_mission():
#     if request.method == 'GET':
#         return render_template('new_mission.html')
#     elif request.method == 'POST':
#         try:
#             jsonobj = {
#                 # 'openid':request.form['openid'],
#                 'mission_name':request.form['mission_name'],
#                 'mission_type':request.form['mission_type'],
#                 'deadline':request.form['deadline'],
#                 'description':request.form['description'],
#                 'obj':request.form['obj'],
#                 'skill_need':request.form['skill_need'],
#                 'bounty':request.form['bounty']
#                 }
#             return 'success!'
#         except:
#             return 'wrong!'

@app.route('/wechat/mission_commit', methods = ['GET', 'POST'])
def mission_commit():
    if request.method == 'GET':
        return render_template('mission_commit.html')
    elif request.method == 'POST':
        return render_template('mission_commit.html')
    else:
        pass
    # 提交表单

@app.route('/wechat/user_center', methods = ['GET', 'POST'])
def user_center():
    if request.method == 'GET':
        return render_template('user_center.html')
    elif request.method == 'POST':
        return render_template('user_center.html')
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


# 运行主函数
if __name__ == '__main__':
    # 对外开放80端口
    app.run(host='0.0.0.0',port=80,debug=True)




