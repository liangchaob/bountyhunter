#!/usr/bin/env python
# encoding:utf-8
'''
* 赏金猎人项目
* liangchaob@163.com 
* 2016.8.3
'''

#设置中文字符
import sys
sys.path.append("./")
reload(sys)
sys.setdefaultencoding( "utf-8" )

import requests
import json

# 填写变量
APPID = 'wxa9312a82e8138370'
APPSECRET = '3f87fbd58c9013a0b0190bda28a4acc5'

url1="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+APPID+"&secret="+APPSECRET

r1 = requests.get(url1)

access_token = r1.json().get('access_token')

print access_token

# headers设置
headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Encoding":"gzip",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.example.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }


# 菜单设置
menu_data =  # 菜单设置
menu_data = {
    "button": [
        {
            "type": "view", 
            "name": "发任务", 
            "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa9312a82e8138370&redirect_uri=http%3A%2F%2Fbountyunions.applinzi.com%2Fwechat%2Fnew_mission&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
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



menu_data2 =  {
     "button":[
      {
          "type": "view", 
          "name": "发任务", 
          "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa9312a82e8138370&redirect_uri=http%3A%2F%2Fbountyunions.applinzi.com%2Fwechat%2Fnew_mission&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
      },
      {  
          "type":"click",
          "name":"接任务",
          "key":"TODAY_MISSIONS"
      },
      {
           "name":"设置",
           "sub_button":[
           {  
               "type":"view",
               "name":"个人中心",
               "url":"https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxa9312a82e8138370&redirect_uri=http%3A%2F%2Fbountyunions.applinzi.com%2Fwechat%2Fuser_center&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect"
            },
            {
               "type":"click",
               "name":"帮助",
               "key":"APP_HELP"
            }]
       }]
 }




url2 = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="+access_token

r2 = requests.post(url2, data = menu_data, headers = headers)

print r2.content


