# example实例解析：
`注`：环境配置请参考《后端入职流程》

1. hello_world
> sanic最简单的使用实例，启动hello_world.py后,访问接口地址http://0.0.0.0:45680或 http://localhost:45680
```
from sanic.response import json
from trump import Trump
app = Trump()

@app.route("/", methods=["GET", "POST"])
async def test(request):
    return json({"x": request.json})

app.run(host='0.0.0.0', port=45680, debug=True)
```
2. bpmn
>	trump使用最基本事件，包含前处理、后处理、数据库

* 配置文件：config.py

```
# 连接本地数据库test，注意配置本地数据库密码用户名
DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': '',
    'port': '5432',
    'database': 'test'
}
# redis配置
REDIS_CONFIG = {'host':'localhost','port':6379}
#是否允许多个登录
ALLOW_MULTI_LOGIN = False
```

* 程序入口文件：bpmn.py

```
#权限、分页设置，
restapi.bp.settings

#登录登出请求
/login  在users表中查询帐号account，密码password
/logout  清除request中的用户有效信息

#登录后每次请求都会经过loaduser方法，做权限验证
@request_loader
async def loaduser(request):
```

