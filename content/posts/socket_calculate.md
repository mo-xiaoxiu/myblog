---
title: "Socket编程--简单计算器的实现"
date: 2021-12-15T17:43:38+08:00
draft: true
---

# socket编程

## Linux socket

**创建socket**

```cpp
int sock_id = socket(int domain, int type, int protocol);
```

* domain：套接字中使用的协议族
  * PF_INET：IPv4
* type：套接字数据传输类型
  * SOCK_STREAM：字节流
  * SOCK_DGRAM：报文流
* protocol：计算机间使用的协议
  * TCP连接：IPPROTO_TCP
  * UDP连接：IPPROTO_UDP
* 返回值：成功返回文件描述符；失败返回-1



**初始化sockaddr_in**

一般的：

```C++
memset(&ssock_addr, 0, sizeof(sock_addr));
sock_addr.sin_family = AF_INET;
sock_addr.sin_addr.s_addr = htonl(INADDR_ANY);
sock_addr.sin_port = htons(...);
```

* ```C++
  struct sockaddr_in
  {
  	sa_family_t	sin_family; // Address Family
      uint16_t	sin_port; // 16位 TCP/UDP 端口号
      struct in_addr	sin_addr; // 32位 IP 地址
      char	sin_zero[8]; // 不使用
  };
  
  struct in_addr
  {
      In_addr_t	s_addr; // 32位 IPv4 地址
  };
  ```

* 地址族：AF_INET  IPv4网络协议中的地址族

* sin_port：16位端口号，以**网络字节序**保存

* sin_addr：32位IP地址信息，**网络字节序**

* ```C++
  struct sockaddr
  {
      sa_family_t	sin_family; // 地址族信息
      char	sa_data[14]; // 地址信息
  };
  ```

  *问题：sockaddr_in保存IPv4地址信息，为何还需要通过sin_family单独指定地址族信息？*

  结构体sockaddr不止为了IPv4设计。为了保持一致性，sockaddr_in中也有地址族信息

* **网络字节序：**

  * 大端序：高位字节存放在低位地址
  * 小端序：高位字节存放在高位地址
  * 网络传输过程中，统一使用大端序

* **字节序转换：**

  h：host主机； to：向...； n：network网络； l：long； s：short

  * htonl：把long类型的数据从主机转化为网络字节序

* **字符串IP -> 32 int**：

  ```C++
  #include<arpa/inet.h>
  
  in_addr_t inet_addr(const char* string);
  ```

  成功返回32位大端序整型数值，失败返回 INADDR_NONE

  **同类函数：新增功能：会自动把结果填充到结构体变量中**

  ```C++
  #include<arpa/inet.h>
  
  int inet_aton(const char* string, struct in_addr* addr);
  ```

  *for example:*

  ```C++
  #include<stdio.h>
  #include<stdlib.h>
  #include<arpa/inet.h>
  void error_handling(char* message);
  
  int main(int argc, char* argv[]) {
      char* addr = "127.232.124.79";
      struct sockaddr_in addr_inet;
      
      if(!inet_aton(addr, &addr_inet.sin_addr)); // 结构体变量
      	error_handling("Conversion error!");
      else
          printf("Network ordered integer addr: %#x \n",
                addr_inet.sin_addr.s_addr);
      
      return 0;
  }
  
  void error_handling(char* message) {
      fputs(message, stderr);
      fputc('\n', stderr);
      exit(1);
  }
  ```

* **网络字节序 -> 字符串IP：（反）**

  ```C++
  #include<arpa/inet.h>
  
  char* inet_ntoa(struct in_addr addr);
  ```

  成功返回转换的字符串，失败返回-1

* **INADDR_ANY**

  可自动获取运行服务器端的计算机IP地址，不必亲自输入

  服务端优先考虑这种方式

  同一计算机中可以分配多个IP地址，实际IP地址的个数与计算机中安装NIC的数量相等；若只有一个NIC，直接使用INADDR_ANY



**向套接字分配网络地址**

```C++
#include<sys/socket.h>

int bind(int sockfd, struct sockaddr* myaddr, socklen_t addrlen);
```

成功返回0，失败返回-1

此函数调用成功，则将第二个参数指定的地址信息分配给第一个参数的套接字



**进入等待连接请求状态（服务端）**

```C++
#include<sys/socket.h>

int listen(int sock, int backlog);
```

成功返回0，失败返回-1

* backlog：连接请求等待队列长度，表示最多可以有多少个连接进入队列



**接收请求（服务端）**

```C++
#include<sys/socket.h>

int accept(int sock, struct sockaddr* addr, socklen_t* addrlen);
```

成功返回创建的**新的**套接字，失败返回-1



**发起连接请求（客户端）**

```C++
#include<sys/socket.h>

int connect(int sock, struct sockaddr* servaddr, socklen_t addrlen);
```



**TCP客户端与服务端调用方式**

* 客户端：socket() -> connect() -> read()/write() -> close()
* 服务端：socket() -> bind() -> listen() -> accept() -> read()/write() -> close()

客户端只能等到服务端调用listen函数后，才调用connect函数；客户端调用connect函数前，服务端可能先调用accept函数



## Window socket

```C++
#include<winsock2.h>

int WSAStartup(WORD wVersionRequested, LPWSAData); // 成功返回 0，失败返回非0错误码
```

* WORD：typedef unsigned short WORD
* wVersionRequested：高位副版本号，低位高版本号
* **MAKEWORD(1, 2)** // 主版本1，副版本2，返回 0x0201
* **LPWSADATA是WSADATA的 指针类型：传递WSADATA结构体变量地址**



```C++
#include<winsock2.h>

int WSACleanup(void); // 成功返回 0，失败返回 SOCKET_ERROR
```



```C++
#include<winsock2.h>

SOCKET socket(int af, int type, int protocal); // 成功：0 ； 失败：INVALID_SOCKET

int bind(SOCKET s, const struct sockaddr* name, int namelen);

int listen(SOCKET s, int backlog);

SOCKET accept(SOCKET s, struct sockaddr* addr, int * addrlen); // 成功：套接字句柄；失败：INVALID_SOCKET

int connect(SOCKET s, const struct sockaddr* name, int namelen); 

int closesocket(SOCKET s);



/* ----------next---------
 * windows I/O 
 */
int send(SOCKET s, const char* buf, int len, int flags);
// 成功返回传输字节数，失败返回SOCKET_ERROR

int recv(SOCKET s, const char* buf, int len, int flags);
// 成功返回接收的字节数（收到 EOF 时为 0），失败返回 SOCKET_ERROR

```

* Windows中不存在`inet_aton`函数



## 回声 客户端/服务端 实现

* 服务端在通过一时刻只与一个客户端连接，提供回声服务
* 服务端一次向5个客户端提供服务，退出
* 客户端接受用户输入的字符串并发送到服务端
* 服务端将接收的字符串数据传回客户端，“回声”
* 服务端与客户端之间的字符串回声一直执行到客户端输入”Q“为止

**回声服务端的实现：**

```C
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#define BUF_SIZE 1024
void error_handling(char* message);

int main(int argc, char* argv[]) {
    int serv_sock, clnt_sock; // 服务端套接字用于监听，客户端套接字用于接收用户连接请求
    char message[BUF_SIZE]; // 存放信息的缓冲区
    int str_len, i;
    
    struct sockaddr_in serv_addr, clnt_addr; // 服务端和客户端套接字地址信息结构体
    socklen_t clnt_addr_sz;
    
    serv_sock = socket(PF_INET, SOCK_STREAM, 0); // 创建监听连接
    if(serv_sock == -1)
        error_handling("socket() error!");
    
    // 填入服务器地址信息
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(atoi(argv[1]));
    
    // 绑定IP地址和端口号
    if(bind(serv_sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) == -1)
        error_handling("bind() error!");
    
    // 开始监听：等待连接队列长度为 5
    if(listen(serv_sock, 5) == -1)
        error_handling("listen() error!");
    
    // 建立 5 个连接
    clnt_addr_sz = sizeof(clnt_addr);
    for(i=0; i<5; i++) {
        clnt_sock = accept(serv_sock, (struct sockaddr*)&clnt_addr, &clnt_addr_sz); // 接收客户端连接请求
        if(clnt_sock == -1)
            error_handling("accept() error!");
        else
            printf("Connected client %d \n", i+1);
        
        // 循环调用 read 函数，将接收到来自客户端的信息发送回客户端
        while((str_len=read(clnt_sock, message, BUF_SIZE))!=0)
            write(clnt_sock, message, str_len);
        
        close(clnt_sock);
    }
    close(serv_sock);
    return 0;
}

void error_handling(cahr* message){
    // as the same before...
}
```

**回声客户端的实现：**

```C++
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<arpa/inet.h>
#include<sys/socket.h>
#define BUF_SIZE 1024
void error_handling(char* message);

int main(int argc, char* argv[])
{
	int sock; // 客户端套接字
	char message[BUF_SIZE];
	int str_len, recv_len, recv_cnt;

	struct sockaddr_in serv_addr; // 服务端套接字地址信息结构体变量

	if(argc!=3) {
		printf("Usage : %s <IP> <port>\n", argv[0]);
		exit(1);
	}

	sock = socket(PF_INET, SOCK_STREAM, 0); // 创建客户端套接字
	if(sock == -1)
		error_handling("sock() error!");

    // 填入服务器端地址信息
	memset(&serv_addr, 0, sizeof(serv_addr));
	serv_addr.sin_family = AF_INET;
	serv_addr.sin_addr.s_addr = inet_addr(argv[1]);
	serv_addr.sin_port = htons(atoi(argv[2]));

    // 发起连接 --> serv_addr
	if(connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) == -1)
		error_handling("connect() error!");
	else
		printf("Connected......");

    // 循环向服务器端发送信息，直到放弃输入
	while(1) {
		fputs("Input message(Q to quit): ", stdout);
		fgets(message, BUF_SIZE, stdin);
		if(!strcmp(message, "q\n") || !strcmp(message, "Q\n"))
			break;

        // 一次性发送输入的信息
		str_len = write(sock, message, strlen(message));

        // 循环调用 read 函数，读取发送给服务器的信息
		recv_len = 0;
		while(recv_len < str_len) {
            // 读取返回的信息
			recv_cnt = read(sock, &message[recv_len], BUF_SIZE-1);
			if(recv_cnt == -1)
				error_handling("read() error");
			recv_len += recv_cnt;
		}
        // 一次发送的数据接收完毕
		message[recv_len] = 0;
		printf("Message from server: %s", message);
	}
	close(sock);
	return 0;
}

void error_handling(char* message) {
	// as the same before...
}

```



---

