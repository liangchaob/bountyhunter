# Using a compact OS
FROM daocloud.io/liangchaob/ubuntu-liangchaob:latest

MAINTAINER Liangchaob <liangchaob@163.com> 

# Add ITdmb stuff into daocloud server
COPY . /bountyhunter

# apt-get
RUN apt-get update
RUN apt-get install -y libmysqld-dev
RUN apt-get install -y python-dev
RUN apt-get install -y python-setuptools
RUN apt-get install -y python-pip

# pip
RUN pip install -r /bountyhunter/requirements.txt


# Open Ports
EXPOSE 80

WORKDIR /bountyhunter/
CMD python api.py 