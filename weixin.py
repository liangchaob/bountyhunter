#!/usr/bin/env python
# encoding:utf-8
'''
* 赏金猎人项目
* liangchaob@163.com 
* 2016.9.9
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







from wechatpy import parse_message
from wechatpy.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException

crypto = WeChatCrypto(token, encoding_aes_key, appid)
try:
    decrypted_xml = crypto.decrypt_message(
        xml,
        msg_signature,
        timestamp,
        nonce
    )
except (InvalidAppIdException, InvalidSignatureException):
    # 处理异常或忽略
    pass

msg = parse_message(decrypted_xml)