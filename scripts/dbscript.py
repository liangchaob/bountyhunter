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

import requests
import json


headers = {'content-type': 'application/json'}
url = "http://liangchaob-bountyhunter.daoapp.io/"

# get
r = requests.get(url+"/mission/")
print r.json()


