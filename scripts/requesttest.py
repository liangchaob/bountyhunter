import requests

# payload={
#     'openid':2,
#     'intro':'',
#     'role':'admin',
#     'feedback':'',
#     'level':'',
#     'skill':'',
#     'mission_published':'',
#     'mission_accept':'',
#     'state':'',
#     'spent':'',
#     'income':'',
#     'email':'',
#     'mobile':''
#     }




# r=requests.post('http://0.0.0.0:8080/api/user/',data=payload)


# print r.text


payload={
    'openid':2,
    'intro':'tt',
    'role':'user',
    'feedback':'',
    'level':'',
    'skill':'',
    'mission_published':'',
    'mission_accept':'',
    'state':'',
    'spent':'',
    'income':'',
    'email':'',
    'mobile':''
    }

r=requests.put('http://0.0.0.0:8080/api/user/2',data=payload)


print r.text




