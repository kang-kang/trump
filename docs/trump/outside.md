# 外部接口
## 查询(Query)

列表

	/<table|view>

单项

	/<table|view>/<id>

#### 查询条件

作为参数传入，和字段以 - 分隔

##### 相等

	field=value

##### 不等

	filed-ne=value


##### 大于

	filed-gt=value
	
	

##### 小于

	filed-lt=value

##### 在....之中

	field-in=value1,value2..

##### 包含

	filed-contains=value

例：staff_role_name-overlap=ADMIN,TEACHER，意为只要包含admin或teacher就为true

	filde-overlap=value

##### 不包含

例：staff_role_name-necontains=ADMIN,TEACHER，意为角色同时不为admin和teacher

	filed-necontains=value

例：staff_role_name-neoverlap=ADMIN,TEACHER，意为只要包含admin或teacher就为false

	filde-neoverlap=value

##### 区间

	field-range=min_value|max_value

大于或小于其中一个值为空，不可全为空

##### 分页及排序

	page=?&pagesize=?

----------


## 增加(Add)

 
 以POST传输方式传入JSON块,对指定表实现单条,批量插入
  
语法:

	/<tablename>

单条插入JSON:
```
{"field":"values",...}##以逗号分割可传入多个表字段
```
批量插入JSON:
```
    [
	 {"field1":"values1","field2":"values2",...},
		 ##以逗号结尾可传入多条数据
	 {"field1":"values1","field2":"values2",...}
	]
```
----------



## 删除(Delete)



	以DELETE请求,用id对指定表实现单条数据删除
  
语法:

	/<tablename>/<id>


----------

## 修改(Modify)



	以PUT传输方式传入json块,用id对指定表实现数据修改

语法:

	/<tablename>/<id>
修改JSON:

```
{"field":"values",...}##以逗号分割可传入多个表字段
```
