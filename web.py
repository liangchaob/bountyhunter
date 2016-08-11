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
from flask import Flask,request, make_response  ,render_template
import hashlib  
# 微信配置类
# from wechat_sdk import WechatConf
# # 微信接口类
# from wechat_sdk import WechatBasic
# # 微信xml解析类
# from wechat_sdk.exceptions import ParseError


# # 配置参数
# conf = WechatConf(
#     token='g7824tgfhew0g', 
#     appid='wxa9312a82e8138370', 
#     appsecret='3f87fbd58c9013a0b0190bda28a4acc5',
#     encrypt_mode='normal'  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
#     # encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
# )
# wechat = WechatBasic(conf=conf)


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





# 菜单函数
# 微信验证
@app.route('/wechat/new_mission', methods = ['GET', 'POST'])
def new_mission():
    if request.method == 'GET':
        return render_template('new_mission.html')
    elif request.method == 'POST':
        return render_template('new_mission.html')
    else:
        pass
    # 菜单设置

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
# 运行主函数
if __name__ == '__main__':
    # 对外开放80端口
    app.run(host='0.0.0.0',port=8080,debug=True)




















