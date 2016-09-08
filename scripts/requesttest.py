import requests

payload={'openid':1,'role':'admin'}


r=requests.post('http://0.0.0.0:8080/api/user/',data=payload)


print r.text
