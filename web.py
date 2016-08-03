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
from flask import Flask,request, make_response, render_template


# flask实例化
app = Flask(__name__)





# 菜单函数
# 微信验证
@app.route('/new_mission', methods = ['GET', 'POST'])
def new_mission():
    if request.method == 'GET':
        # 参数接收
        return render_template('web_newmission.html')

    elif request.method == 'POST':
        return render_template('new_mission.html')
    else:
        pass
    # 菜单设置


# 运行主函数
if __name__ == '__main__':
    # 对外开放80端口
    app.run(host='0.0.0.0',port=8080,debug=True)




















