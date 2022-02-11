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
MYSQL* mysql_real_connect(MYSQL* mysql, const char* host/*主机名*/, const char* user/*用户名*/, 
                        const char* passwd/*密码*/, const char* db/*DateBaseName*/, unsigned int port/*端口号*/,
                        const char* unix_socket, unsigned long client_flag);
```
**在能够执行需要有效MySQL连接句柄结构的任何其它API函数之前，`mysql_real_connect()`必须成功完成**
### 部分参数
* `unix_socket` -- 通常为NULL
* `client_flag` -- 通常为0
