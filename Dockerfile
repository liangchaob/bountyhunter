# Using a compact OS
FROM daocloud.io/ubuntu:14.04

MAINTAINER Liangchaob <liangchaob@163.com> 


# apt-get
RUN apt-get update
RUN apt-get install -y libmysqld-dev
RUN apt-get install -y python-dev
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-pip

# pip
# RUN pip install -r /bountyhunter/requirements.txt


RUN pip install Flask==0.10.1
RUN pip install Flask-RESTful==0.3.5
RUN pip install Jinja2==2.8
RUN pip install MarkupSafe==0.23
RUN pip install Werkzeug==0.11.9
RUN pip install aniso8601==1.1.0
RUN pip install argparse==1.2.1
RUN pip install chardet==2.0.1
RUN pip install colorama==0.2.5
RUN pip install html5lib==0.999
RUN pip install itsdangerous==0.24
RUN pip install psutil==4.3.0
RUN pip install pycrypto==2.6.1
RUN pip install pymongo==3.2.2
RUN pip install python-dateutil==2.5.3
RUN pip install pytz==2016.4
RUN pip install requests==2.6.0
RUN pip install six==1.10.0
RUN pip install urllib3==1.7.1
RUN pip install virtualenv==14.0.6
RUN pip install wechat-sdk==0.6.3
RUN pip install wheel==0.24.0
RUN pip install wsgiref==0.1.2
RUN pip install xmltodict==0.9.2
RUN pip install qiniu==7.0.8


# Add stuff into daocloud server
COPY . /bountyhunter


# Open Ports
EXPOSE 80

WORKDIR /bountyhunter/
CMD python api.py 





