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
from flask import Flask,request, make_response,render_template,jsonify
import hashlib  
# 微信配置类
from wechat_sdk import WechatConf
# 微信接口类
from wechat_sdk import WechatBasic
# 微信xml解析类
from wechat_sdk.exceptions import ParseError

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


# 菜单设置
menu_data = {
    "button": [
        {
            "type": "view", 
            "name": "发任务", 
            "url": "http://www.baidu.com"
        }, 
        {
            "type": "view", 
            "name": "接任务", 
            "url": "http://www.baidu.com"
        }, 
        {
            "type": "view", 
            "name": "设置", 
            "url": "http://www.baidu.com"
        }
    ]
}


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


            # elif wechat.message.type == 'unsubscribe':  # 取消关注事件（无可用私有信息）
            #     pass
            # elif wechat.message.type == 'scan':  # 用户已关注时的二维码扫描事件
            #     key = wechat.message.key                        # 对应于 XML 中的 EventKey
            #     ticket = wechat.message.ticket                  # 对应于 XML 中的 Ticket
            # elif wechat.message.type == 'location':  # 上报地理位置事件
            #     latitude = wechat.message.latitude              # 对应于 XML 中的 Latitude
            #     longitude = wechat.message.longitude            # 对应于 XML 中的 Longitude
            #     precision = wechat.message.precision            # 对应于 XML 中的 Precision
            # elif wechat.message.type == 'click':  # 自定义菜单点击事件
            #     key = wechat.message.key                        # 对应于 XML 中的 EventKey
            # elif wechat.message.type == 'view':  # 自定义菜单跳转链接事件
            #     key = wechat.message.key                        # 对应于 XML 中的 EventKey
            # elif wechat.message.type == 'templatesendjobfinish':  # 模板消息事件
            #     status = wechat.message.status                  # 对应于 XML 中的 Status
            # elif wechat.message.type in ['scancode_push', 'scancode_waitmsg', 'pic_sysphoto', 
            #                              'pic_photo_or_album', 'pic_weixin', 'location_select']:  # 其他事件
            #     key = wechat.message.key                        # 对应于 XML 中的 EventKey

            

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


        return render_template('t1.html',nickname = nickname,url_openid = url_openid,
            url_userinfo = url_userinfo,sex = sex, province = province, city=city,
            country = country,headimgurl = headimgurl)


        # return url_userinfo


    elif request.method == 'POST':
        return render_template('new_mission.html')
    else:
        pass
    # 菜单设置

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




