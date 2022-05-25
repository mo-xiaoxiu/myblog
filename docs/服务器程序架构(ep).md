# 示例：服务器程序架构

## 程序结构

* 数据库工作线程
* 日志线程
* 普通工作线程
* 主线程

## 数据库工作线程

数据库工作线程启动的时候，与mysql建立连接

每个数据库工作线程同时存在两个任务队列

![webServer_DBthread](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/webServer_DBthread.drawio.png)

* 队列 1：存放需要执行数据库增删改查操作的任务sqlTask
* 队列 2：存放sqlTask执行完成之后的结果（结果队列）

*伪代码：*

```cpp
void db_thread_func()  {  
    while (!m_bExit)  
    {  
        if (NULL != (pTask = m_sqlTask.Pop()))  
        {  
            //从m_sqlTask中取出的任务先执行完成后，pTask将携带结果数据  
            pTask->Execute();              
            //得到结果后，立刻将该任务放入结果任务队列  
            m_resultTask.Push(pTask);  
            continue;  
        }  

        sleep(1000);  
    }//end while-loop 
 } 
```



## 工作线程和主线程

服务器编程几个概念：

![webServer_worker_main_Thread](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/webServer_worker_main_Thread.drawio.png)

* `TcpServer`：`Tcp`服务，绑定`ip`地址和端口号，在此端口号上监听连接，用一个成员变量`TcpListener`监听细节；用来接收新的连接
* `TcpConnection`：管理连接信息；连接状态、本端和对端的`ip`地址和端口号
* `Channel`：记录`socket`的句柄；收发数据的真正执行者
* `TcpSession`：将`Channel`收发的数据进行解包或装包，由`Channel`收发

### 数据发送

* 业务逻辑将数据交给`TcpSession`装包（包括加密或者压缩操作）
* 调用`TcpConnection::SendData()`函数，实际是调用`Channel::SendData()`函数将数据发送出去

### 数据接收

* 通过调用`select()/poll()/epoll()`等IO复用函数，等到`TcpConnection`上有数据到来
* 调用`TcpConnection`中的`Channel`对象去`recv()/read()/recvfrom()`收取数据
* 将收到的数据交给`TcpSession`处理
* 最终交给业务逻辑层

### 工作线程和主线程工作流程

```cpp
while (!m_bQuit)  
{  
    epoll_or_select_func();  //等待IO事件

    handle_io_events();  //处理Io事件

    handle_other_things();  //处理其他事情
}
```

* `muduo`里的`epoll_wait`将超时时间设置为 1 ms（可参考）

* 主线程监听`socket`上的可读事件；主线程和工作线程都存在一个`epollfd`；新连接来了（可读事件触发），在主线程的`handle_io_events()`去接受新的连接

* 采用`round-robin`（轮询）算法，将产生的新连接的`socket`挂接到工作线程的`epollfd`

  ```cpp
  //从第一个工作线程开始挂接新的socket
  //超出索引边界则从第一个重新开始
  void attach_new_fd(int newsocketfd)  
  {  
      workerthread = get_next_worker_thread(next);  
      workerthread.attach_to_epollfd(newsocketfd);  
      ++next;  
      if (next > max_worker_thread_num)  
          next = 0;  
  } 
  ```

* **`epoll_wait`的`struct epoll_event`数量设置为多少：**

  `muduo`的做法：动态增长

  ```cpp
  //初始化代码  
  std::vector<struct epoll_event> events_(16);  
  
  //线程循环里面的代码  
  while (m_bExit)  
  {  
      int numEvents = ::epoll_wait(epollfd_, &*events_.begin(), static_cast<int>(events_.size()), 1);  
      if (numEvents > 0)  
      {  
          if (static_cast<size_t>(numEvents) == events_.size())  
          {  
              events_.resize(events_.size() * 2); //动态扩张 
          }  
      }  
  }
  ```

* 工作线程还可以做一些业务逻辑层的工作：

  在`handle_other_things()`中，**写一个队列，任务放入队列，再在`handle_other_things()`里取出任务执行**，`muduo`库的做法是**在`handle_other_things()`里调用函数指针**

  ```cpp
  void handle_other_things()  
  {  
      somefunc();  
  }
  //m_functors是一个stl::vector,其中每一个元素为一个函数指针  
  void somefunc()  
  {  
      for (size_t i = 0; i < m_functors.size(); ++i)  
      {  
          m_functors[i]();  
      }  
  
      m_functors.clear();  
  }
  ```

  * 需要将执行的任务函数指针`push_back()`到`m_functor`

  * **产生问题：几个线程同时将任务函数指针放入`m_functor`将会带来线程安全问题**，`muduo`做法：

    ```cpp
    bool bBusy = false;  
    void add_task(const Functor& cb)  
    {  
        std::unique_lock<std::mutex> lock(mutex_);  
        m_functors_.push_back(cb);  
    
        //B不忙碌时只管往篮子里面加，不要通知B  
        if (!bBusy)  
        {  
            wakeup_to_do_task();  
        }  
    }  
    
    void do_task()  
    {  
        bBusy = true;  
        std::vector<Functor> functors;  
        {  
            std::unique_lock<std::mutex> lock(mutex_);  
           
     /*b先从里面拿一部分*/       functors.swap(pendingFunctors_);  
        }  
    //b拿去的一部分先消耗，此时b状态：忙碌
        for (size_t i = 0; i < functors.size(); ++i)  
        {  
            functors[i]();  
        }  
    //拿去的一部分消耗完了，此时b的状态：空闲，去a里面拿
        bBusy = false;  
    }
    ```

    **利用一个栈变量`functors`将`m_functor`中的任务函数指针`swap`过来，减小锁粒度**

* 每个工作线程都存在一个`m_functors`，将产生的任务采用`round-robin`算法将新连接的`socket`句柄挂接到工作线程的`epollfd`上

* 任务产生时，工作线程可以立即执行任务，可以使用下文技巧：

  [one_thread_one_loop思想](https://www.zjp7071.cn/one_loop_one_thread/#_1)



## 问题

### 数据库线程任务队列生产者和消费者归属

1. 数据库线程任务队列 1 中的任务来源：业务层产生的任务（可能时工作线程中的`handle_other_things()`）交给队列 1；实际开发中有多个数据库线程，也就有多个多个队列 1，采用`round_robin`算法将任务交出去
2. 数据库线程任务队列 2 中的任务去向：同理也可能是`handle_other_things()`的调用消耗

### 业务层数据发送

* 业务层数据产生

* 经过`TcpSession`装包，需要发送

* 将产生任务放入数据库线程任务队列 2，采用`round_robin`算法丢给工作线程`handle_other_things()`

* 在工作线程中，在`TcpConnection`中的`Channel`里发送，由于没有监测可写事件，所以调用数据发送函数`send()/write()`会阻塞，解决方法是`sleep()`之后继续发送，直到发送出去

  ```cpp
  bool Channel::Send()  
  {  
      int offset = 0;  
      while (true)  
      {  
          int n = ::send(socketfd, buf + offset, length - offset);  
          if (n == -1)  
          {  
              if (errno == EWOULDBLOCK)  
              {  
                  ::sleep(100);  
                  continue;  
              }  
          }  
          //对方关闭了socket，这端建议也关闭  
          else if (n == 0)  
          {  
              close(socketfd);  
              return false;  
          }  
  
          offset += n;  
          if (offset >= length)  
              break;  
  
      }  
  
      return true;      
  }
  ```





<br>

<br>

<br>

```
参考文章https://mp.weixin.qq.com/s/MhEuI6g3xEIYgbgiPaS-QQ
```

