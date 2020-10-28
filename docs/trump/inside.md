# 内部接口
##  查询(Query)
#### 多条查询(Items)

```
get_items(db, tablename, args={}, roles=['DEFAULT'],with_total=False, pager=False)

@param:
##db:传入已注册数据库链接(app.pool)
##tablename:传入表名
##args: 传入查询条件 >,<,!=.....
##roles:传入当前登录用户角色
##with_total:传入是否统计条数
##pager:传入是否进行分页

@return:list[]
```
#### 单条查询(Item)
```
get_item(db, tablename, oid, roles=[], column='id')

@param:
##db:传入已注册数据库链接池app.pool
##tablename:传入表名
##oid:传入表id
##roles:传入当前登录用户角色
##column:指定条件字段
```


----------


## 增加(Add)
 

<h3> 单条插入,批量插入</h3>

```
create_item(db, tablename, data, column='id', lock_table=False)

@param:
##db:传入已注册数据库链接
##tablename:传入表名
##data:传入插入数据集合
##column:传入返回值(插入成功后返回该列值)
##lock_table:是否进行锁表操作
```
----------


## 删除(Delete)
```
delete_item(db, tablename, oid)

@param:
##db:传入已注册数据库链接
##tablename:传入表名
##oid:传入表id
```

----------


## 修改(Modify)
```
modify_item(db, tablename, oid, data)

@param
##db:传入已注册数据库链接
##tablename:传入表名
##oid:传入表id
##data:传入修改数据
```

