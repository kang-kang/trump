# Trump 设计文档

## 简介

Trump是一个通过数据库自动发现生成restful风格接口的框架，他使用blueprint 构架多版本api；集成asyncpg，并使用连接池；封装 asyncpg, 实现CRUD（内部接口）。使用者仅专注于业务逻辑的研发，极大简化了工作量。

## 地址

 http://git.yaoyingli.cn/kangruide/trump

## 原则

DRY

## 依赖关系

[sanic](https://github.com/channelcat/sanic)

可能是有史以来最快的 Python 网页框架，而且似乎也远远超过其它框架。它是一个专为速度而设计的类 Flask 的 Python 3.5+网页服务器。

[asyncpg](https://github.com/MagicStack/asyncpg)

高效的异步（目前只支持 CPython 3.5）数据库接口库，其是专门为 PostgreSQL 设计的。

## 配置

用户表： _user

地区表： area

