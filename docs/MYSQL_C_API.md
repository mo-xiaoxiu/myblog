## MYSQL C API
包含头文件`#include <mysql/mysql.h>`
## mysql_init
**初始化**一个MYSQL连接的对象和**释放**一个MYSQL对象
```cpp title="mysql_init"
#include <mysql/mysql.h>
MYSQL* mysql_init(MYSQL* mysql); //初始化
void mysql_close(MYSQL* mysql); //释放
```
<br>

### 常见用法
1. 参数传递NULL：<br>
    mysql_init()分配资源（申请一块内存），返回首地址<br>
    `MYSQL* m_conn = mysql_init(NULL);`<br>
    记得释放内存：`mysql_close(m_conn); m_conn = NULL;`<br>
2. 参数传递对象地址：<br>
    下面情况使用栈内存<br>
    `MYSQL ms;`<br>
    `MYSQL* m_conn = mysql_init(ms);`<br>
    记得释放内存：`mysql_close(m_conn); m_conn = NULL;`

## mysql_real_connect
连接到MYSQL server<br>

```cpp title="mysql_real_connect"
#include <mysql/mysql.h>
MYSQL* mysql_real_connect(MYSQL* mysql/*mysql_init返回的地址*/, const char* host/*主机名*/, const char* user/*用户名*/, 
                        const char* passwd/*密码*/, const char* db/*DateBaseName*/, unsigned int port/*端口号*/,
                        const char* unix_socket, unsigned long client_flag);
```
**在能够执行需要有效MySQL连接句柄结构的任何其它API函数之前，`mysql_real_connect()`必须成功完成**
### 部分参数
* `unix_socket` -- 本地套接字，通常为NULL
* `client_flag` -- 通常为0
* `host` -- 写ip地址即可  localhost，null代表本地连接
* `port` -- 连接mysql服务端的端口号；if ==0，则3306
### 返回值
与`mysql_init()`一致

## mysql_query

执行一个sql语句，“增删改查“

```cpp
#include <mysql/mysql.h>

MYSQL* mysql_query(MYSQL* mysql/*mysql_real_connect()返回值*/, const char* query);
```

### 部分参数
* `query` -- 一个可以执行sql的语句

## mysql_store_result

获取结果集：

将结果集从mysql对象中取出来

对应一块内存地址，其中保存着查询结果的结果集

*将行和列取出需要其他函数*

```cpp
#include <mysql/mysql.h>

MYSQL_RES* mysql_store_result(MYSQL* mysql/*mysql_query返回值*/);
```

### 返回值

具有多个结果；出现错误返回NULL

## mysql_num_fields

获取结果集列数

```cpp
#include <mysql/mysql.h>

unsigned int mysql_num_fields(MYSQL_RES *result);
```

* 参数 -- mysql_store_result返回值
* 返回值 -- 列数




