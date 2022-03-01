# select、poll和epoll

## select函数

用于检测在一组socket中是否有事件就绪

事件就绪：

1. 读事件就绪：
   * socket内核中，**接收缓冲区**中的字节数**大于等于低水位`SO_RCVLOWAT`**，此时调用`recv`或`read`函数可以无阻塞地读该文件描述符，返回值大于0
   * TCP连接**对端关闭连接**，**本端**调用`recv`或`read`函数对socket进行读操作，`recv`或`read`函数**返回088
   * 监听的socket上有未处理的新的连接请求
   * socket有未处理的错误
2. 写事件就绪
   * socket内核中，**发送缓冲区**可用字节数**大于等于低水位`SO_SNDLLOWAT`**，可以无阻塞地写，返回值大于0
   * socket写操作关闭（调用close函数或者shutdown函数），对其进行写操作，出发`SIGPIPE`信号
   * socket使用非阻塞connect连接成功或失败

**签名：**

```cpp
int select(int nfds, fd_set *readfds, fd_set *writefds, fd_set *exceptfds, struct timeval *timeout);
```

​	参数：

  * nfds：将这个参数设置为所有需要使用select函数检测事件地 fd 中最大值 +1；

  * readfds：需要监听的可读事件 fd 集合

  * writefds：需要监听的可写事件 fd 集合

  * exceptfds：需要监听的异常事件 fd 集合

  * timeout：超时时间，在这个设定时间内检测 fd 事件，超过这个时间，select函数立即返回

    ```cpp
    struct timeout{
        long tv_sec; // 秒
        long tv_usec; // 微妙
    };
    ```

  * fd_set 结构体信息：该字段是一个long数组

    ```c
    /* The fd_set member is required to be an array of longs.  */
    typedef long int __fd_mask;
    
    /* Some versions of <linux/posix_types.h> define this macros.  */
    #undef	__NFDBITS
    /* It's easier to assume 8-bit bytes than to get CHAR_BIT.  */
    #define __NFDBITS	(8 * (int) sizeof (__fd_mask))
    #define	__FD_ELT(d)	((d) / __NFDBITS) 
    #define	__FD_MASK(d)	((__fd_mask) (1UL << ((d) % __NFDBITS)))
    
    /* fd_set for select and pselect.  */
    typedef struct
      {
        /* XPG4.2 requires this member name.  Otherwise avoid the name
           from the global namespace.  */
    #ifdef __USE_XOPEN
        __fd_mask fds_bits[__FD_SETSIZE / __NFDBITS];
    # define __FDS_BITS(set) ((set)->fds_bits)
    #else
        __fd_mask __fds_bits[__FD_SETSIZE / __NFDBITS];
    # define __FDS_BITS(set) ((set)->__fds_bits)
    #endif
      } fd_set;
    
    /*
     * 上面这段定义结构体代码可以简化为：
     * typedef struct
     	{
     		// __FD_SETSIZE = 1024
     		// __NFBITS = 64
     		long int __fds_bits[16]; // long int:8  8*8*16 = 1024个fd事件状态
            // 0 表示没有事件； 1 表示有事件
     	} fd_set;
    */
    
    /* Maximum number of file descriptors in `fd_set'.  */
    #define	FD_SETSIZE		__FD_SETSIZE
    
    ```

    将一个 fd 添加到 fd_set 这个集合中需要使用`FD_SET`宏：

    ```c
    #define FD_SET(fd, fdsetp) __FD_SET(fd, fdsetp)
    ```

    ```c
    // 全部置为 0
    # define __FD_ZERO(fdsp) \
      do {									      \
        int __d0, __d1;							      \
        __asm__ __volatile__ ("cld; rep; " __FD_ZERO_STOS			      \
    			  : "=c" (__d0), "=D" (__d1)			      \
    			  : "a" (0), "0" (sizeof (fd_set)		      \
    					  / sizeof (__fd_mask)),	      \
    			    "1" (&__FDS_BITS (fdsp)[0])			      \
    			  : "memory");					      \
      } while (0)
    
    #else	/* ! GNU CC */
    
    //FD_SET本质上是在一个有1024个连续bit的内存的某个bit上设置一个标志
    #define __FD_SET(d, set) \
      ((void) (__FDS_BITS (set)[__FD_ELT (d)] |= __FD_MASK (d))) 

    //删除一个fd
    #define __FD_CLR(d, set) \
      ((void) (__FDS_BITS (set)[__FD_ELT (d)] &= ~__FD_MASK (d))) 

    //判断在某个fd中是否有我们关心的事件，本质是检测对应的bit是否置位
    #define __FD_ISSET(d, set) \
      ((__FDS_BITS (set)[__FD_ELT (d)] & __FD_MASK (d)) != 0) 
    ```

### select函数——服务端

```cpp
#include <sys/types.h> 
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <iostream>
#include <string.h>
#include <sys/time.h>
#include <vector>
#include <errno.h>

//自定义代表无效fd的值
#define INVALID_FD -1

int main(int argc, char* argv[])
{
    //创建一个监听socket
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd == INVALID_FD)
    {
        std::cout << "create listen socket error." << std::endl;
        return -1;
    }

    //初始化服务器地址
    struct sockaddr_in bindaddr;
    bindaddr.sin_family = AF_INET;
    bindaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    bindaddr.sin_port = htons(3000);
    //绑定监听端口
    if (bind(listenfd, (struct sockaddr *)&bindaddr, sizeof(bindaddr)) == -1)
    {
        std::cout << "bind listen socket error." << std::endl;
    	close(listenfd);
        return -1;
    }
    
    //启动监听
    if (listen(listenfd, SOMAXCONN) == -1)
    {
        std::cout << "listen error." << std::endl;
    	close(listenfd);
        return -1;
    }
    
    //存储客户端socket的数组
    std::vector<int> clientfds;
    int maxfd;
    
    while (true) 
    {	
    	fd_set readset; //可读事件fd集合
    	FD_ZERO(&readset); // 每次循环都要间集合各位置为0
    	
    	//将侦听socket加入到待检测的可读事件中去
    	FD_SET(listenfd, &readset);
    	
    	maxfd = listenfd;
    	//将客户端fd加入到待检测的可读事件中去，并更新最大fd
    	int clientfdslength = clientfds.size();
    	for (int i = 0; i < clientfdslength; ++i)
    	{
    		if (clientfds[i] != INVALID_FD)
    		{
    			FD_SET(clientfds[i], &readset);

    			if (maxfd < clientfds[i])
    				maxfd = clientfds[i];
    		}
    	}
    	
    	timeval tm;
    	tm.tv_sec = 1;
    	tm.tv_usec = 0;
    	//暂且只检测可读事件，不检测可写和异常事件
    	int ret = select(maxfd + 1, &readset, NULL, NULL, &tm);
    	if (ret == -1)
    	{
    		//出错，退出程序。
    		if (errno != EINTR)
    			break;
    	}
    	else if (ret == 0)
    	{
    		//select 函数超时，下次继续
    		continue;
    	} 
    	else
        {
    		//检测到某个socket有事件
    		if (FD_ISSET(listenfd, &readset))
    		{
    			//侦听socket的可读事件，则表明有新的连接到来
    			struct sockaddr_in clientaddr;
    			socklen_t clientaddrlen = sizeof(clientaddr);
    			//4. 接受客户端连接
    			int clientfd = accept(listenfd, (struct sockaddr *)&clientaddr, &clientaddrlen);
    			if (clientfd == INVALID_FD)					
    			{         	
    				//接受连接出错，退出程序
    				break;
    			}
    			
    			//只接受连接，不调用recv收取任何数据
    			std:: cout << "accept a client connection, fd: " << clientfd << std::endl;
    			clientfds.push_back(clientfd);
    		} 
    		else 
    		{
    			//假设对端发来的数据长度不超过63个字符
    			char recvbuf[64];
    			int clientfdslength = clientfds.size();
    			for (int i = 0; i < clientfdslength; ++i)
    			{
    				if (clientfds[i] != INVALID_FD && FD_ISSET(clientfds[i], &readset))
    				{				
    					memset(recvbuf, 0, sizeof(recvbuf));
    					//非侦听socket，则接收数据
    					int length = recv(clientfds[i], recvbuf, 64, 0);
    					if (length <= 0)
    					{
    						//收取数据出错了
    						std::cout << "recv data error, clientfd: " << clientfds[i] << std::endl;							
    						close(clientfds[i]);
    						//不直接删除该元素，将该位置的元素置位INVALID_FD
    						clientfds[i] = INVALID_FD;
    						continue;
    					}
    					
    					std::cout << "clientfd: " << clientfds[i] << ", recv data: " << recvbuf << std::endl;					
    				}
    			}
    			
    		}
    	}
    }
    
    //关闭所有客户端socket
    int clientfdslength = clientfds.size();
    for (int i = 0; i < clientfdslength; ++i)
    {
    	if (clientfds[i] != INVALID_FD)
    	{
    		close(clientfds[i]);
    	}
    }
    
    //关闭侦听socket
    close(listenfd);
    
    return 0;
}
```

### select函数注意事项：

1. select函数在调用前后可能会修改`readfds`、`writefds`和`exceptfds`这三个集合中的内容，所以需要在下次调用前使用FD_ZERO将fd_set清零，再调用FD_SET将需要检测的事件加入到 fd_set 中
2. select函数会修改`timeval`结构体的值，同样在复用时需要重新设置timeval的值
3. **timeval结构体中的`tv_sec`和`tv_usec`如果都被置为0，则检测集合中事件时，如果没有需要的事件，则立即返回**
4. **如果将timeval设置为NULL，则select函数会一直阻塞下去，直到需要的事件触发**

### select函数的缺点：

1. 每次调用时，都需要把 fd 集合从**用户态复制到内核态**，开销大；每次需要**在内核中遍历传递来的所有fd**
2. 单个进程监视的 fd 数量存在上限，在上述中：1024
3. select函数在每次调用时需要对传入参数重新设置











## poll函数

函数签名：

```cpp
#include <poll.h>

int poll(struct pollfd* fds, nfds_t nfds, int timeout);
```

​	参数：

  * fds：指向一个结构体数组的首个元素指针，结构体：`struct pollfd`

    ```cpp
    struct pollfd{
        int fd; //待检测事件fd
        short events; //关心事件组合，有开发者设置
        short revents; //检测后事件的类型
    };
    ```

    events常见取值：

    * POLLIN：数据可读
    * POLLOUT：数据可写
    * POLLERR：错误

  * nfds：参数fds数组长度，`typedef unsigned long int nfds_t`

  * timeout：poll超时时间

### poll与select函数对比的优点：

1. poll不要求开发者计算最大文件描述符+1
2. poll处理**大数量**文件描述符**更快**
3. poll没有最大连接数量的限制
4. 调用poll，只需要对其参数设置一次

```cpp
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <fcntl.h>
#include <poll.h> //包含此头文件
#include <iostream>
#include <string.h>
#include <vector>
#include <errno.h>

//无效fd标记
#define INVALID_FD  -1

int main(int argc, char *argv[])
{
    //创建一个侦听socket
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd == INVALID_FD)
    {
        std::cout << "create listen socket error." << std::endl;
        return -1;
    }

    //将侦听socket设置为非阻塞的
    int oldSocketFlag = fcntl(listenfd, F_GETFL, 0);
    int newSocketFlag = oldSocketFlag | O_NONBLOCK;
    if (fcntl(listenfd, F_SETFL, newSocketFlag) == -1)
    {
        close(listenfd);
        std::cout << "set listenfd to nonblock error." << std::endl;
        return -1;
    }

    //复用地址和端口号
    int on = 1;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (char *) &on, sizeof(on));
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEPORT, (char *) &on, sizeof(on));

    //初始化服务器地址
    struct sockaddr_in bindaddr;
    bindaddr.sin_family = AF_INET;
    bindaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    bindaddr.sin_port = htons(3000);
    if (bind(listenfd, (struct sockaddr *) &bindaddr, sizeof(bindaddr)) == -1)
    {
        std::cout << "bind listen socket error." << std::endl;
        close(listenfd);
        return -1;
    }

    //启动侦听
    if (listen(listenfd, SOMAXCONN) == -1)
    {
        std::cout << "listen error." << std::endl;
        close(listenfd);
        return -1;
    }

    std::vector<pollfd> fds; //pollfd数组，用于存放事件
    pollfd listen_fd_info; //对结构体变量pollfd进行设置
    listen_fd_info.fd = listenfd; //绑定监听fd‘
    listen_fd_info.events = POLLIN; //数据可读
    listen_fd_info.revents = 0;
    fds.push_back(listen_fd_info);

    //是否存在无效的fd标志
    bool exist_invalid_fd;
    int n;
    while (true)
    {
        exist_invalid_fd = false;
        n = poll(&fds[0], fds.size(), 1000);
        if (n < 0)
        {
            //被信号中断
            if (errno == EINTR)
                continue;

            //出错，退出
            break;
        }
        else if (n == 0)
        {
            //超时，继续
            continue;
        }

        for (size_t i = 0; i < fds.size(); ++i)
        {
            // 事件可读
            if (fds[i].revents & POLLIN)
            {
                if (fds[i].fd == listenfd)
                {
                    //侦听socket，接受新连接
                    struct sockaddr_in clientaddr;
                    socklen_t clientaddrlen = sizeof(clientaddr);
                    //接受客户端连接, 并加入到fds集合中
                    int clientfd = accept(listenfd, (struct sockaddr *) &clientaddr, &clientaddrlen);
                    if (clientfd != -1)
                    {
                        //将客户端socket设置为非阻塞的
                        int oldSocketFlag = fcntl(clientfd, F_GETFL, 0);
                        int newSocketFlag = oldSocketFlag | O_NONBLOCK;
                        if (fcntl(clientfd, F_SETFL, newSocketFlag) == -1)
                        {
                            close(clientfd);
                            std::cout << "set clientfd to nonblock error." << std::endl;
                        }
                        else
                        {
                            struct pollfd client_fd_info;
                            client_fd_info.fd = clientfd;
                            client_fd_info.events = POLLIN;
                            client_fd_info.revents = 0;
                            fds.push_back(client_fd_info);
                            std::cout << "new client accepted, clientfd: " << clientfd << std::endl;
                        }
                    }
                }
                else
                {
                    //普通clientfd,收取数据
                    char buf[64] = {0};
                    int m = recv(fds[i].fd, buf, 64, 0);
                    if (m <= 0)
                    {
                        if (errno != EINTR && errno != EWOULDBLOCK) // EAGAIN
                        {
                            //出错或对端关闭了连接，关闭对应的clientfd，并设置无效标志位
                            for (std::vector<pollfd>::iterator iter = fds.begin(); iter != fds.end(); ++iter)
                            {
                                if (iter->fd == fds[i].fd)
                                {
                                    std::cout << "client disconnected, clientfd: " << fds[i].fd << std::endl;
                                    close(fds[i].fd);
                                    iter->fd = INVALID_FD;
                                    exist_invalid_fd = true;
                                    break;
                                }
                            }
                        }
                    }
                    else
                    {
                        std::cout << "recv from client: " << buf << ", clientfd: " << fds[i].fd << std::endl;
                    }
                }
            } else if (fds[i].revents & POLLERR) //出现错误
            {
                //TODO: 暂且不处理
            }

        }// end  outer-for-loop

        if (exist_invalid_fd)
        {
            //统一清理无效的fd
            for (std::vector<pollfd>::iterator iter = fds.begin(); iter != fds.end();)
            {
                if (iter->fd == INVALID_FD)
                    iter = fds.erase(iter);
                else
                    ++iter;
            }
        }
    }// end  while-loop


    //关闭所有socket
    for (std::vector<pollfd>::iterator iter = fds.begin(); iter != fds.end(); ++iter)
        close(iter->fd);

    return 0;
}
```

### poll函数的缺点：

1. 大量的fd数组在**用户态和内核地址空间**之间被**整体复制**
2. poll函数返回后，**需要遍历**fd获得就绪事件
3. 随着监视文件描述符数量的增长，就绪状态事件可能只有很少，效率下降









## epoll函数

使用epoll模型之前，需要创建epollfd

创建epollfd函数签名：

```cpp
#include <sys/epolll.h>

int epoll_create(int size); // size只要大于0就可以
```

​	调用成功返回 epollfd，不成功返回-1

需要将检测事件的其他 fd 绑定到这个 epollfd，或者从上面修改，或者从上面解绑

完成以上功能的函数签名：

```cpp
int epoll_ctl(int epfd, int po, int fd, struct epoll_event* event);
```

​	参数：

  * epfd：epollfd

  * op：

    * EPOLL_CTL_ADD：添加
    * EPOLL_CTL_MOD：修改
    * EPOLL_CTL_DEL：删除，此情况下，第四个参数event可以设置为NULL

  * fd：需要被操作的fd

  * event：epoll_event结构体

    ```cpp
    struct epoll_event{
        uint32_t events; //需要检测fd事件标志
        epoll_data_t data; //用户自定义数据
    };
    ```

    `epoll_data_t`本质上是一个联合体（Union）：

    ```cpp
    typedef union epoll_data{
        void* ptr;
        int fd; //设置的事件
        uint32_t u32;
        uint64_t u64;
    }epoll_data_t;
    ```

之后就是检测事件了，检测事件的函数签名：

```cpp
int epoll_wait(int epfd, struct epoll_event* events, int maxevents, int timeout);
```

​	参数：

	* epfd：epollfd
	* events：epoll_event结构体数组首地址，是一个输出参数，在函数调用成功后，在events中存放的是与就绪事件相关的epoll_event结构体数组
	* maxevents：数组元素个数
	* timeout：超出时间，将其设置为0，则会立即返回

调用成功，返回**有事件的fd数量**，**返回0，表示超时**，返回-1表示失败

### epoll新增的模式

**LT和ET模式：**

* ET：边缘触发模式，一个事件从无到有才会触发
* LT：水平触发模式，一个事件只要有，就会一直触发

*ET模式处理读事件：*

```cpp
#include<sys/types.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>
#include<fcntl.h>
#include<sys/epoll.h> //包含此头文件
#include<poll.h>
#include<iostream>
#include<string.h>
#include<vector>
#include<errno.h>
#include<iostream>

int main()
{
    //创建一个监听socket
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd == -1)
    {
        std::cout << "create listen socket error" << std::endl;
        return -1;
    }

    //设置重用ip地址和端口号
    int on = 1;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (char*)&on, sizeof(on));
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEPORT, (char*)&on, sizeof(on));


    //将监听socker设置为非阻塞的
    int oldSocketFlag = fcntl(listenfd, F_GETFL, 0);
    int newSocketFlag = oldSocketFlag | O_NONBLOCK;
    if (fcntl(listenfd, F_SETFL, newSocketFlag) == -1)
    {
        close(listenfd);
        std::cout << "set listenfd to nonblock error" << std::endl;
        return -1;
    }

    //初始化服务器地址
    struct sockaddr_in bindaddr;
    bindaddr.sin_family = AF_INET;
    bindaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    bindaddr.sin_port = htons(3000);

    if (bind(listenfd, (struct sockaddr*)&bindaddr, sizeof(bindaddr)) == -1)
    {
        std::cout << "bind listen socker error." << std::endl;
        close(listenfd);
        return -1;
    }

    //启动监听
    if (listen(listenfd, SOMAXCONN) == -1)
    {
        std::cout << "listen error." << std::endl;
        close(listenfd);
        return -1;
    }


    //创建epollfd
    int epollfd = epoll_create(1);
    if (epollfd == -1)
    {
        std::cout << "create epollfd error." << std::endl;
        close(listenfd);
        return -1;
    }

    epoll_event listen_fd_event;
    listen_fd_event.data.fd = listenfd;
    listen_fd_event.events = EPOLLIN;
    //取消注释掉这一行，则使用ET模式
    //listen_fd_event.events |= EPOLLET;

    //将监听sokcet绑定到epollfd上去
    if (epoll_ctl(epollfd, EPOLL_CTL_ADD, listenfd, &listen_fd_event) == -1)
    {
        std::cout << "epoll_ctl error" << std::endl;
        close(listenfd);
        return -1;
    }

    int n;
    while (true)
    {
        epoll_event epoll_events[1024];
        n = epoll_wait(epollfd, epoll_events, 1024, 1000);
        if (n < 0)
        {
            //被信号中断
            if (errno == EINTR) 
                continue;

            //出错,退出
            break;
        }
        else if (n == 0)
        {
            //超时,继续
            continue;
        }
		
        for (size_t i = 0; i < n; ++i)
        {
            //事件可读
            if (epoll_events[i].events & EPOLLIN)
            {
                if (epoll_events[i].data.fd == listenfd)
                {
                    //侦听socket,接受新连接
                    struct sockaddr_in clientaddr;
                    socklen_t clientaddrlen = sizeof(clientaddr);
                    int clientfd = accept(listenfd, (struct sockaddr*)&clientaddr, &clientaddrlen);
                    if (clientfd != -1)
                    {
                        int oldSocketFlag = fcntl(clientfd, F_GETFL, 0);
                        int newSocketFlag = oldSocketFlag | O_NONBLOCK;
                        if (fcntl(clientfd, F_SETFL, newSocketFlag) == -1)
                        {
                            close(clientfd);
                            std::cout << "set clientfd to nonblocking error." << std::endl;
                        }
                        else
                        {
                            epoll_event client_fd_event;
                            client_fd_event.data.fd = clientfd;
                            client_fd_event.events = EPOLLIN;
                            //取消注释这一行，则使用ET模式
                            //client_fd_event.events |= EPOLLET; 
                            if (epoll_ctl(epollfd, EPOLL_CTL_ADD, clientfd, &client_fd_event) != -1)
                            {
                                std::cout << "new client accepted,clientfd: " << clientfd << std::endl;
                            }
                            else
                            {
                                std::cout << "add client fd to epollfd error" << std::endl;
                                close(clientfd);
                            }
                        }
                    }
                }
                else
                {
                    std::cout << "client fd: " << epoll_events[i].data.fd << " recv data." << std::endl;
                    //普通clientfd
                    char ch;
                    //每次只收一个字节
                    int m = recv(epoll_events[i].data.fd, &ch, 1, 0);
                    if (m == 0)
                    {
                        //对端关闭了连接，从epollfd上移除clientfd
                        if (epoll_ctl(epollfd, EPOLL_CTL_DEL, epoll_events[i].data.fd, NULL) != -1)
                        {
                            std::cout << "client disconnected,clientfd:" << epoll_events[i].data.fd << std::endl;
                        }
                        // 并关闭此套接字
                        close(epoll_events[i].data.fd);
                    }
                    else if (m < 0)
                    {
                        //出错
                        if (errno != EWOULDBLOCK && errno != EINTR)
                        {
                            if (epoll_ctl(epollfd, EPOLL_CTL_DEL, epoll_events[i].data.fd, NULL) != -1)
                            {
                                std::cout << "client disconnected,clientfd:" << epoll_events[i].data.fd << std::endl;
                            }
                            close(epoll_events[i].data.fd);
                        }
                    }
                    else
                    {
                        //正常收到数据
                        std::cout << "recv from client:" << epoll_events[i].data.fd << ", " << ch << std::endl;
                    }
                }
            }
            else if (epoll_events[i].events & POLLERR)
            {
                // TODO 暂不处理
            }
        }
    }

    close(listenfd);
    return 0;
}
```

*ET处理写事件：*

```cpp
#include<sys/types.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>
#include<fcntl.h>
#include<sys/epoll.h>
#include<poll.h>
#include<iostream>
#include<string.h>
#include<vector>
#include<errno.h>
#include<iostream>

int main()
{
    //创建一个监听socket
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd == -1)
    {
        std::cout << "create listen socket error" << std::endl;
        return -1;
    }

    //设置重用IP地址和端口号
    int on = 1;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (char*)&on, sizeof(on));
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEPORT, (char*)&on, sizeof(on));

    //将监听socker设置为非阻塞的
    int oldSocketFlag = fcntl(listenfd, F_GETFL, 0);
    int newSocketFlag = oldSocketFlag | O_NONBLOCK;
    if (fcntl(listenfd, F_SETFL, newSocketFlag) == -1)
    {
        close(listenfd);
        std::cout << "set listenfd to nonblock error" << std::endl;
        return -1;
    }

    //初始化服务器地址
    struct sockaddr_in bindaddr;
    bindaddr.sin_family = AF_INET;
    bindaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    bindaddr.sin_port = htons(3000);

    if (bind(listenfd, (struct sockaddr*)&bindaddr, sizeof(bindaddr)) == -1)
    {
        std::cout << "bind listen socker error." << std::endl;
        close(listenfd);
        return -1;
    }

    //启动监听
    if (listen(listenfd, SOMAXCONN) == -1)
    {
        std::cout << "listen error." << std::endl;
        close(listenfd);
        return -1;
    }


    //创建epollfd
    int epollfd = epoll_create(1);
    if (epollfd == -1)
    {
        std::cout << "create epollfd error." << std::endl;
        close(listenfd);
        return -1;
    }

    epoll_event listen_fd_event;
    listen_fd_event.data.fd = listenfd;
    listen_fd_event.events = EPOLLIN;
    //取消注释这一行，则使用ET模式
    //listen_fd_event.events |= EPOLLET;

    //将监听sokcet绑定到epollfd上
    if (epoll_ctl(epollfd, EPOLL_CTL_ADD, listenfd, &listen_fd_event) == -1)
    {
        std::cout << "epoll_ctl error" << std::endl;
        close(listenfd);
        return -1;
    }

    int n;
    while (true)
    {
        epoll_event epoll_events[1024];
        n = epoll_wait(epollfd, epoll_events, 1024, 1000);
        if (n < 0)
        {
            //被信号中断
            if (errno == EINTR)
                continue;

            //出错，退出
            break;
        }
        else if (n == 0)
        {
            //超时，继续
            continue;
        }
        
        for (size_t i = 0; i < n; ++i)
        {
            //事件可读
            if (epoll_events[i].events & EPOLLIN)
            {
                if (epoll_events[i].data.fd == listenfd)
                {
                    //侦听socket，接受新连接
                    struct sockaddr_in clientaddr;
                    socklen_t clientaddrlen = sizeof(clientaddr);
                    int clientfd = accept(listenfd, (struct sockaddr*)&clientaddr, &clientaddrlen);
                    if (clientfd != -1)
                    {
                        int oldSocketFlag = fcntl(clientfd, F_GETFL, 0);
                        int newSocketFlag = oldSocketFlag | O_NONBLOCK;
                        if (fcntl(clientfd, F_SETFL, newSocketFlag) == -1)
                        {
                            close(clientfd);
                            std::cout << "set clientfd to nonblocking error." << std::endl;
                        }
                        else
                        {
                            epoll_event client_fd_event;
                            client_fd_event.data.fd = clientfd;
                            //同时侦听新来连接socket的读和写事件
                            client_fd_event.events = EPOLLIN | EPOLLOUT;
                            //取消注释这一行时，使用ET模式
                            //client_fd_event.events |= EPOLLET; 
                            if (epoll_ctl(epollfd, EPOLL_CTL_ADD, clientfd, &client_fd_event) != -1)
                            {
                                std::cout << "new client accepted,clientfd: " << clientfd << std::endl;
                            }
                            else
                            {
                                std::cout << "add client fd to epollfd error" << std::endl;
                                close(clientfd);
                            }
                        }
                    }
                }
                else
                {
                    std::cout << "client fd: " << epoll_events[i].data.fd << " recv data." << std::endl;
                    //普通clientfd
                    char recvbuf[1024] = { 0 };
                    //读取数据
                    int m = recv(epoll_events[i].data.fd, recvbuf, 1024, 0);
                    if (m == 0)
                    {
                        //对端关闭了连接，从epollfd上移除clientfd
                        if (epoll_ctl(epollfd, EPOLL_CTL_DEL, epoll_events[i].data.fd, NULL) != -1)
                        {
                            std::cout << "client disconnected,clientfd:" << epoll_events[i].data.fd << std::endl;
                        }
                        close(epoll_events[i].data.fd);
                    }
                    else if (m < 0)
                    {
                        //出错
                        if (errno != EWOULDBLOCK && errno != EINTR)
                        {
                            if (epoll_ctl(epollfd, EPOLL_CTL_DEL, epoll_events[i].data.fd, NULL) != -1)
                            {
                                std::cout << "client disconnected,clientfd:" << epoll_events[i].data.fd << std::endl;
                            }
                            close(epoll_events[i].data.fd);
                        }
                    }
                    else
                    {
                        //正常收到数据
                        std::cout << "recv from client:" << epoll_events[i].data.fd << ", " << recvbuf << std::endl;
                    }
                }
            }
            else if (epoll_events[i].events & EPOLLOUT)
            {
                //只处理客户端fd的可写事件
                if (epoll_events[i].data.fd != listenfd)
                {
                    //打印结果
                    std::cout << "EPOLLOUT triggered,clientfd: " << epoll_events[i].data.fd << std::endl;
                }
            }
            else if (epoll_events[i].events & EPOLLERR)
            {
                //TODO 暂不处理
            }
        }
    }

    close(listenfd);
    return 0;
}
```

**总结：**

* 读事件：LT模式，不用循环到recv或者read函数返回-1，错误码EWOULDBLOCK或EAGAIN；在ET模式下，读事件必须把数据读取干净
* 写事件：LT模式，不需要要及时移除；ET模式，写事件触发后，如果还需要下一次写事件触发来驱动任务（例如发送上次剩余未发送的数据），则需要再注册一次检测写事件

### epoll的EPOLLONESHOT选项

如果某个socket注册了该标志，则其注册监听事件后触发一次之后就再也不会触发了，**除非再次注册一次检测事件**

```cpp
#include<sys/types.h>
#include<sys/socket.h>
#include<arpa/inet.h>
#include<unistd.h>
#include<fcntl.h>
#include<sys/epoll.h>
#include<poll.h>
#include<iostream>
#include<string.h>
#include<vector>
#include<errno.h>
#include<iostream>

int main()
{
    //创建一个监听socket
    int listenfd = socket(AF_INET, SOCK_STREAM, 0);
    if (listenfd == -1)
    {
        std::cout << "create listen socket error" << std::endl;
        return -1;
    }

    //设置重用ip地址和端口号
    int on = 1;
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, (char*)&on, sizeof(on));
    setsockopt(listenfd, SOL_SOCKET, SO_REUSEPORT, (char*)&on, sizeof(on));


    //将监听socker设置为非阻塞的
    int oldSocketFlag = fcntl(listenfd, F_GETFL, 0);
    int newSocketFlag = oldSocketFlag | O_NONBLOCK;
    if (fcntl(listenfd, F_SETFL, newSocketFlag) == -1)
    {
        close(listenfd);
        std::cout << "set listenfd to nonblock error" << std::endl;
        return -1;
    }

    //初始化服务器地址
    struct sockaddr_in bindaddr;
    bindaddr.sin_family = AF_INET;
    bindaddr.sin_addr.s_addr = htonl(INADDR_ANY);
    bindaddr.sin_port = htons(3000);

    if (bind(listenfd, (struct sockaddr*)&bindaddr, sizeof(bindaddr)) == -1)
    {
        std::cout << "bind listen socker error." << std::endl;
        close(listenfd);
        return -1;
    }

    //启动监听
    if (listen(listenfd, SOMAXCONN) == -1)
    {
        std::cout << "listen error." << std::endl;
        close(listenfd);
        return -1;
    }


    //创建epollfd
    int epollfd = epoll_create(1);
    if (epollfd == -1)
    {
        std::cout << "create epollfd error." << std::endl;
        close(listenfd);
        return -1;
    }

    epoll_event listen_fd_event;
    listen_fd_event.data.fd = listenfd;
    listen_fd_event.events = EPOLLIN;
	
    //将监听sokcet绑定到epollfd上去
    if (epoll_ctl(epollfd, EPOLL_CTL_ADD, listenfd, &listen_fd_event) == -1)
    {
        std::cout << "epoll_ctl error" << std::endl;
        close(listenfd);
        return -1;
    }

    int n;
    while (true)
    {
        epoll_event epoll_events[1024];
        n = epoll_wait(epollfd, epoll_events, 1024, 1000);
        if (n < 0)
        {
            //被信号中断
            if (errno == EINTR) 
                continue;

            //出错,退出
            break;
        }
        else if (n == 0)
        {
            //超时,继续
            continue;
        }
        for (size_t i = 0; i < n; ++i)
        {
            //事件可读
            if (epoll_events[i].events & EPOLLIN)
            {
                if (epoll_events[i].data.fd == listenfd)
                {
                    //侦听socket,接受新连接
                    struct sockaddr_in clientaddr;
                    socklen_t clientaddrlen = sizeof(clientaddr);
                    int clientfd = accept(listenfd, (struct sockaddr*)&clientaddr, &clientaddrlen);
                    if (clientfd != -1)
                    {
                        int oldSocketFlag = fcntl(clientfd, F_GETFL, 0);
                        int newSocketFlag = oldSocketFlag | O_NONBLOCK;
                        if (fcntl(clientfd, F_SETFL, newSocketFlag) == -1)
                        {
                            close(clientfd);
                            std::cout << "set clientfd to nonblocking error." << std::endl;
                        }
                        else
                        {
                            epoll_event client_fd_event;
                            client_fd_event.data.fd = clientfd;
                            client_fd_event.events = EPOLLIN;
							//给clientfd设置EPOLLONESHOT选项
							client_fd_event.events |= EPOLLONESHOT;
                            if (epoll_ctl(epollfd, EPOLL_CTL_ADD, clientfd, &client_fd_event) != -1)
                            {
                                std::cout << "new client accepted,clientfd: " << clientfd << std::endl;
                            }
                            else
                            {
                                std::cout << "add client fd to epollfd error" << std::endl;
                                close(clientfd);
                            }
                        }
                    }
                }
                else
                {
                    std::cout << "client fd: " << epoll_events[i].data.fd << " recv data." << std::endl;
                    //普通clientfd
                    char ch;
                    //每次只收一个字节
                    int m = recv(epoll_events[i].data.fd, &ch, 1, 0);
                    if (m == 0)
                    {
                        //对端关闭了连接，从epollfd上移除clientfd
                        if (epoll_ctl(epollfd, EPOLL_CTL_DEL, epoll_events[i].data.fd, NULL) != -1)
                        {
                            std::cout << "client disconnected,clientfd:" << epoll_events[i].data.fd << std::endl;
                        }
                        close(epoll_events[i].data.fd);
                    }
                    else if (m < 0)
                    {
                        //出错
                        if (errno != EWOULDBLOCK && errno != EINTR)
                        {
                            if (epoll_ctl(epollfd, EPOLL_CTL_DEL, epoll_events[i].data.fd, NULL) != -1)
                            {
                                std::cout << "client disconnected,clientfd:" << epoll_events[i].data.fd << std::endl;
                            }
                            close(epoll_events[i].data.fd);
                        }
                    }
                    else
                    {
                        //正常收到数据
                        std::cout << "recv from client:" << epoll_events[i].data.fd << ", " << ch << std::endl;
						
						//在这里再次为clientfd再次注册EPOLLIN事件
						//epoll_event client_fd_event;
						//client_fd_event.data.fd = epoll_events[i].data.fd;
						//client_fd_event.events = EPOLLIN;					
						//if (epoll_ctl(epollfd, EPOLL_CTL_MOD, epoll_events[i].data.fd, &client_fd_event) != -1)
						//{
						//	std::cout << "rearm EPOLLIN event to clientfd: " << epoll_events[i].data.fd << std::endl;
						//}
						//else
						//{
						//	if (epoll_ctl(epollfd, EPOLL_CTL_DEL, epoll_events[i].data.fd, NULL) != -1)
						//	{
						//		std::cout << "remove clientfd from epoll fd successfully, clientfd:" << epoll_events[i].data.fd << std::endl;
						//	}
						//	close(epoll_events[i].data.fd);
						//}
                    }
                }
            }
            else if (epoll_events[i].events & POLLERR)
            {
                // TODO 暂不处理
            }
        }
    }

    close(listenfd);
    return 0;
}
```

