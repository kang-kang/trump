# 设置


   <h3>语法:</h3>
   
	bp.settings = {
    'NO_PAGER_API': ['TABLENAME','.....'],
    'ANONYMOUS_API': ['TABLENAME','....'],
    'ACL_MODE': 'WHITE_LIST/BLACK_LIST',
    'ACL': {
        "TABLENAME": {
            "LS/GET/PUT/POST/...": {"ROLENAME","..."}
        },




框架内默认对数据进行分页(每页10条记录),可通过

### [NO_PAGER_API]
指定表名取消分页
```
'NO_PAGER_API': ['TABLENAME'],
```
----------

 
 ### [ANONYMOUS_API] 
 表操作默认登录,此字段指定表名免登录,
 
 黑白名单对该字段指定表名失效,

 该字段默认为空,为空时,所有表权限开放,黑白名单失效
```
'ANONYMOUS_API': ['TABLENAME'],
```
----------

### [ACL_MODE] 
指定黑白名单模式

BLACK_LIST(黑名单模式):无法操作ACL内指定表,但可操作其他表

WHITE_LIST(白名单模式):可以操作ACL内指定表,但不可操作其他表
```
'ACL_MODE': 'BLACK_LIST/WHITE_LIST',
'ACL': {
	'TABLE': {
		"LS/GET/PUT/POST/...":{'ROLENAME','....'},
			 },
```
----------

 
 ### [ACL] 
 指定表CRUD操作权限,配合黑白名单使用

```
'ACL': {
		'TABLE': {
			"LS/GET/PUT/POST/...":{'ROLENAME','....'},  
							##以逗号分割可指定多个角色										
				 },
				 	##以逗号分割可指定多个表名`
```
				 	

