# 框架结构

> 注：简单介绍框架结构，具体使用方法见使用章节

## 文件结构
* **examples:存放使用实例**，bpmn文件夹下：
 * pre_process前处理文件夹，存放请求前处理文件，必建。
 * post_process后处理文件夹，存放请求后处理文件，必建。
 * bpmn.py:程序运行入口文件，一般为run.py
 * config.py:系统配置文件

`前后处理文件命名：<table|view|alias>.py   命名对应表/视图名`

* **trump:存放框架核心代码**
	* **restapi.py**：权限控制以及程序执行流程控制，restful风格接口 ：分为内部接口和外部接口，外部接口指对应http方法；内部接口则为封装 asyncpg实现，将在使用章节详细介绍。
	* **app.py**：获取数据库中的表信息，使用redis做数据缓存， sanic_session做session存储
	* **query.py**：实现内部CRUD
	* **db.py**：封装数据库操作，实现原始sql语句。query方法可直接执行sql语句。
