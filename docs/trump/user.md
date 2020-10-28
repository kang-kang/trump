# 用户

提供多种登录选项：cookie/session，header

用户信息可通过 `request.user` 获取

用户信息包括：是否登录，用户角色

用户表：  唯一标识命名为id，
	姓名字段命名为name，
	角色命名为staff_role_name，(因框架存在权限控制，所以必须有角色字段。)
