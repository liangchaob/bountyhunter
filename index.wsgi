#!/usr/bin/env python
# encoding: utf-8
'''
* liangchaob@163.com 
* 2016.8.4
'''
#设置中文字符
import sys
sys.path.append("./")
reload(sys)
sys.setdefaultencoding( "utf-8" )


import sae
from weichatweb import app

application = sae.create_wsgi_app(app)