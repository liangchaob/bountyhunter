# 简介

服务于个人或自由职业者的一对一服务服务交易平台

# 用户

平台内暂时分为两种角色：买房，卖方
任何人级既可以做买方又可以做卖方，买房发布赏金项目，然后卖方可以购买该赏金服务。

# 数据结构

- 用户(id,type,publish,accept,honour,level,certity,skill)
- 项目(id,price,skillneed,time_begin,time_end,description,feedback)
- 技能库([uuid:*,uuid:*])

# 技术栈


语言：python
基础架构：docker
数据库：mongodb
框架：flask,bootstrap
其它：weichat支持

# 规划

- 实现weichat版本poc
- 完成后端版本数据库和api

# 用例

- 甲方：
登录微信-->进入公众账号—>点击『发项目』—>确认获取用户权限—>进入表单—>填写项目信息—>发布

- 乙方：
登录微信-->进入公众账号—>输入项目号显示项目详细信息—>点击项目链接—>确认获取用户权限—>查看项目信息—>选择是否承接—>确认并退出


# 二维码
![0.jpeg](https://ooo.0o0.ooo/2016/12/04/5844352053043.jpeg)
