# Redis单进程多路复用

* 启动初始化`initServer()`
* 运行事件处理循环，一直到服务器关闭为止

## 启动初始化

1. 创建`epoll`
2. 绑定监听服务端口
3. 注册accept事件处理器

### 创建epoll对象

`aeCreateEventLoop`

1. 申请和创建eventLoop
2. 将来的各种回调事件都会存在`eventLoop->events`
3. 创建epoll过程`aeApiCreate`：调用`epoll_create`

### 绑定监听服务端口

`listenToPort`

1. 执行`anetTcpServer`->`_anetTcpServer`
2. 设置端口重用`anetSetReuseAddr`
3. 监听`anetListen`：调用`bind`、`listen`

### 注册accept事件处理器

`aeCreateFileEvent`设置`rfilePro`为`acceptTcpHandler`，私有数据设置为null

1. `aeCreateFileEvent`：取出一个文件事件结构（取出fd）`eventLoop->events[fd]`，监听指定fd的指定事件`aeAddEvent`，设置文件事件类型，以及事件的处理器`fe->rfileProc`（读事件回调）或者`fe->wfileProc`（写事件回调），设置私有数据
2. `aeAddEvent`：`epoll_ctl`(add or mod)



## 运行事件处理循环，直到服务器关闭

1. 通过`epoll_wait`发现`listen socket`以及其它连接上的可读、可写事件
2. 若发现`listen socket`上有新连接到达，则接收新连接，并追加到epoll进行管理
3. 若发现其他socket上有命令请求到达，则读取和处理命令，把命令结果写到缓冲中，加入到**写任务队列**
4. 每一次进入`epoll_wait`前都调用`beforesleep`来将写任务队列中的数据实际进行发送
5. 若有首次未发送完成的，当写事件发生时继续发送

### 循环

如果有需要在事件处理前执行的函数，那么运行它

#### beforesleep

处理写任务队列并实际发送之

1. 遍历写任务队列
2. 实际将`client`中的结果数据发送出去（`writeToClient`）：先发送固定缓冲区，再发送回复链表中的数据（`write`）
3. 如果一次性发送不完则准备下一次发送：注册一个写事件处理器，等待`epoll_wait`发现可写再处理`sendReplyToClient`

#### 开始等待事件并处理

`aeProcessEvents`

1. 获取最近的时间事件`tvp`
2. 处理文件事件，阻塞时间由`tvp`决定（`aeApiPoll`）：调用`epoll_wait`
3. 从就绪数组获取事件`eventLoop->events[eventLoop->fired[j].fd]`
4. 如果是读事件并且有回调函数`fe->rfileProc()`；如果是写事件并且有回调函数`fe->wfileProc()`





## 处理新连接请求和可读事件

### 处理新连接

`listen socket`上`rfileProc`注册的是`acceptTcpHandler`

如果有连接到达，回调的就是`acceptTcpHandler`

`acceptTcpHandler`

1. 调用accept系统调用把用户连接给接收回来
2. 为这个新的连接创建一个唯一的`redisClient`对象
3. 将这个新连接添加到epoll，注册一个读事件处理函数`readQueryFromClient`

### 处理客户连接上的可读事件

假设是`Get`

`readQueryFromClient`

1. 解析并查找命令
2. 调用命令处理
3. 添加写任务到队列
4. 将输出写到缓存（固定缓冲，写不下则把剩下的写到回复链表中）等待发送



---

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/Redis单进程网络.png)
