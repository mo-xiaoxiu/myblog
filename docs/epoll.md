# epoll的实现机制
## 总图
![epoll](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll.drawio.png)
<br>

## accept创建新的socket
![process](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll_accept.drawio.png)
<br>

### 初始化socket对象
![accept_init_socket](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll_accep_1.drawio.png)
<br>

### 为新的socket申请file
![accept_init_file](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll_aceept_2.drawio.png)
<br>

### 接收连接，添加新文件到当前打开文件列表中
![epoll_accpet](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll_accept_3.drawio.png)
<br>

## epoll_create的实现
### 创建eventpoll
![create_eventpoll](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll_ceventpoll.drawio.png)
<br>

### 关联到当前进程的打开文件列表中
![eventpoll_process](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll_eventpoll_process.drawio.png)
<br>

### 初始化epitem
对于每一个 socket，调用 epoll_ctl 的时候，都会为之分配一个 epitem<br>
![init_epitem](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll_initepitem_modifiy_1.drawio.png)
<br>

### 设置socket等待队列
![init_epollwaitqueue](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/epoll_socket_waitqueue.drawio.png)
<br>


