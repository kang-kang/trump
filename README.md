# **Trump 框架** #

# 核心功能
## 示例项目结构
```
.
├── funcs
│   └── __init__.py
├── manager.py
├── middleware
│   └── __init__.py
├── resources
│   └── example.sql
├── run.py
└── views
    ├── admin
    │   ├── area.py
    │   └── __init__.py
    ├── area.py
    ├── __init__.py
    ├── login.py
    └── logout.py

```
`run.py`是启动文件，`views`是项目主要内容，其它目录可选。

如需数据库操作请引入相应的包。

`run.py`的示例内容如下
``` python
#!/usr/bin/env python
from trump import app
from sanic.response import json


if __name__ == '__main__':
        app.url_prefix = '/api'
        app.run()
```

## 配置
配置信息可通过`etcd`读取，使用方式为
```python
from trump.config import DB_CONFIG
```
运行时添加环境变量 `CONFIG_URL="192.168.1.12:2379/mjmh/local"`

## 参数（与配置相同，只是运行时修改，可以实时生效）
与配置信息相同，只是约定参数变量名必须是以"PARAMETER_"为前缀，使用方式为
```python
from trump import parameter


@anonymous
async def ls(app, request):
    return json({"status": 0, "data": parameter.PARAMETER_XXX})
```


## 视图
视图支持以下方法和装饰器
```python
from trump.decorators import no_pager, anonymous, table_headers


@anonymous
@table_headers
async def ls(app, request):
    pass


async def post(app, request):
    pass


async def get(app, request, oid):
    pass


async def put(app, request, oid):
    pass


async def delete(app, request, oid):
    pass


async def options(app, request):
    pass


async def post_ls(app, request, data):
    pass


async def post_post(app, request, data):
    pass


async def post_get(app, request, data, oid):
    pass


async def post_put(app, request, data, oid):
    pass


async def post_delete(app, request, data, oid):
    pass

```
在前处理中返回`HTTPResponse`类型会中断之后的处理，否则会执行对应表的相应操作，返回值会被忽略，表名为模块名，可在文件中用 `__table__` 显式指定表名，路径会被替换为 `_` ，模块同名的处理方法可放在 `__init__.py` 中，同时有模块和文件，文件将被忽略。后处理返回`HTTPResponse`类型可改变默认返回值。
## 会话
用户使用 `request['user']` 识别，通过 `app.user_loader` 定义用户加载的方法，请使用字典类型存储用户，如：
``` python
request['user'] = {'id': 1, 'roles': {'STAFF', 'ADMIN'}}
```
禁用默认的 session
``` python
app.session_enable = False
```
用户ID和角色请使用示例中的键名，其它数据可任意自定义。
# 外围功能
## CLI
### 用法

```bash
python -m trump.manager
```
或
```python
#!/usr/bin/env python3
# `manager.py`
from trump.manager import main

if __name__ == '__main__':
    main()
```
### 内置命令
#### config
查看修改配置
#### view
查看视图
### 命令定义
在 `trump/_command.py` 中添加方法

### TODO
#### 项目命令


## 定时任务
### 概述
支持 [CRON表达式(英文)](https://en.wikipedia.org/wiki/Cron#CRON_expression) 和定时重复，定时重复以秒为单位，对齐到Unix时间戳加0.1秒。执行当前命令会挂起当前定时线程的后续处理。

### 用法
#### 1. 建立 tasks 目录
在项目根目录下建立 `tasks` 目录，添加 `__init__.py`。
#### 2. 编写定时任务代码
示例：
```python
import time
from trump import task


@task.cron("* * * * *") # crontab规则 分 时 日 月 周(0-6，0为周日)
def countdown(n=1):
    print('cron ')
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(.5)


@task.repeat(1) # 每秒调度，不能为0
@task.cron("* * * * *") # 可使用多个定时器，每个定时器会启动一个新的定时线程
def test():
    print('repeat ')
    time.sleep(5)

```
#### 3. 启动任务

```bash
python -m trump.task
```

或
```python
# task_run.py
from trump import task


task.run()
```

## 消息队列发送
```python
from trump import amqp
# 正常消息 
await amqp.send(queue, msg, uuid=uuid):
# 延迟消息 `delay`以秒为单位
await amqp.send(queue, msg, delay=60, uuid=uuid):
```

## 内部接口调用
```python
from trump import internal
await internal.call(uuid, MJMH_INTERNAL_JST, 'order_cancel', {'order_id': 1})
```
## 日志
见`trump-log`项目


## 外部接口调用(HTTP)
```python
from trump import requests
response = await requests.post(URL, json={'foo': 'bar'})
print(respones.text, respones.json())
```

# TODO（待实现功能）
