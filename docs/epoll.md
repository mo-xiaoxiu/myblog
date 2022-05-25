# epoll的实现机制
## 总图
![epoll](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll.drawio.png)
<br>

## accept创建新的socket
![process](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_accept.drawio.png)
<br>

### 初始化socket对象
![accept_init_socket](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_accep_1.drawio.png)
<br>

### 为新的socket申请file
![accept_init_file](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_aceept_2.drawio.png)
<br>

### 接收连接，添加新文件到当前打开文件列表中
![epoll_accpet](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_accept_3.drawio.png)
<br>

## epoll_create的实现
### 创建eventpoll
![create_eventpoll](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_ceventpoll.drawio.png)
<br>

### 关联到当前进程的打开文件列表中
![eventpoll_process](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_eventpoll_process.drawio.png)
<br>

## epoll_ctl
这里以*添加*为例：<br>
在使用 epoll_ctl 注册每一个 socket 的时候，内核会做如下三件事情<br>
1. 分配一个红黑树节点对象 epitem<br>
2. 添加等待事件到 socket 的等待队列中，其回调函数是 ep_poll_callback<br>
3. 将 epitem 插入到 epoll 对象的红黑树里<br>
<br>

### 初始化epitem
对于每一个 socket，调用 epoll_ctl 的时候，都会为之分配一个 epitem<br>
![init_epitem](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_initepitem_modifiy_1.drawio.png)
<br>

### 设置socket等待队列
![init_epollwaitqueue](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_socket_waitqueue.drawio.png)
<br>

### 将epitem插入到红黑树中
![epitem_insert_in_rbt](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_insert_rbt.drawio.png)
<br>

## epoll_wait
* 判断就绪队列中是否有就绪事件
* 假设确实没有就绪的连接，定义等待事件，并把 current （当前进程）添加到 waitqueue 上
* 添加到等待队列
* 当前线程主动让出CPU进入睡眠状态，选择下一个进程调度
<br>

![epoll_wait](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_wait.drawio.png)
<br>

## data come
![data_come](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_dataCome.drawio.png)
<br>

### 接收数据到等待队列
![accept_data_in_acceptQueue](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_accept_data_in_acceptQueue.drawio.png)
<br>

### 查找就绪队列中的回调函数
![check_readyQueue_callback](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_check_readyCallBackFunc.drawio.png)
<br>

### 执行回调函数
![run_callback](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_run_callbackFunc.drawio.png)
<br>

### 执行socket就绪通知
![run_ready_notice](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/epoll_run_readyNotice.drawio.png)
<br>
<br>
<br>

## 总结
1. epoll_create创建eventpoll
2. epoll_ctl(添加)添加socket创建epitem插入到红黑树中
3. epoll_wait检查就绪队列中是否有就绪事件，如果没有则将当前线程添加到等待队列中并主动让出CPU进入睡眠
4. 数据包到达网卡，软中断执行接收数据到接收队列（socket）
5. 插入epoll就绪队列
6. 检查是否有线程阻塞
7. 唤醒用户线程，返回事件
<br>
