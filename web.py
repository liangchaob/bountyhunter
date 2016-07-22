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

import time  
from flask import Flask,request, make_response  
import hashlib  
# 微信配置类
from wechat_sdk import WechatConf
# 微信接口类
from wechat_sdk import WechatBasic
# 微信xml解析类
from wechat_sdk.exceptions import ParseError







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
            rec_content = wechat.message.content # post的文本信息
            print "消息id:"+str(rec_id)
            print "公众号id:"+str(rec_target)
            print "用户openid:"+str(rec_source)
            print "时间戳:"+str(rec_time)
            print "消息类型:"+str(rec_type)
            # print rec_raw
            print "信息内容:"+str(rec_content)

            feedback = wechat.response_text(content=
                "消息id:"+str(rec_id)+
                "\n公众号id:"+str(rec_target)+
                "\n用户openid:"+str(rec_source)+
                "\n时间戳:"+str(rec_time)+
                "\n消息类型:"+str(rec_type)+
                "\n信息内容:"+str(rec_content)
                )
            return feedback

        except ParseError:
            print 'Invalid Body Text'
            return 'nothing'









# 运行主函数
if __name__ == '__main__':
    # 对外开放80端口
    app.run(host='0.0.0.0',port=80,debug=True)





