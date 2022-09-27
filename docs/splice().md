# splice()

```c
#define _GNU_SOURCE         /* See feature_test_macros(7) */
       #include <fcntl.h>

       ssize_t splice(int fd_in, loff_t *off_in, int fd_out,
                      loff_t *off_out, size_t len, unsigned int flags);

```

在man手册中描述：

Splice()在两个文件描述符之间移动数据，而不需要在内核地址空间和用户地址空间之间进行复制。它将len字节的数据从文件描述符fd_in传输到文件描述符fd_out，**其中一个文件描述符必须引用管道**

* If fd_in refers to a pipe, then off_in must be NULL.
* 如果fd_in不指向管道，且off_in为NULL，则从文件偏移量开始从fd_in读取字节，并**适当调整文件偏移量**
* 如果fd_in不指向管道并且off_in不为NULL，那么off_in必须指向一个缓冲区，该缓冲区指定从fd_in读取字节的起始偏移量;在这种情况下，fd_in的**文件偏移量不会改变**

## 使用

```c
/*发送文件给客户端*/
int send_file_to_client(int fd, char* file_name) {
    int m_fd;
    struct stat fstat;
    int blocks, remain;
    int pipefd[2];
    
    m_fd = open(file_name, O_RDONLY);
    if(m_fd == -1) {
        return -1;
    }
    
    stat(file, &fstat);
    
    blocks = fstat.st_size / 4096;
    remain = fstat.st_size % 4096;
    
    pipe(pipefd); //创建管道作为中转
    
    for(int i = 0; i < blocks; i++) {
        // 将文件内容读取到管道
        splice(m_fd, NULL, pipefd[1], NULL, 4096, SPLICE_F_MOVE | SPLICE_F_MORE);
        // 将管道内容发送给客户端
        splice(pipefd[0], NULL, fd, NULL, 4096, SPLICE_F_MOVE | SPLICE_F_MORE);
    }
    
    if(remain) {
        splice(m_fd, NULL, pipefd[1], NULL, remain, SPLICE_F_MOVE | SPLICE_F_MORE);
        splice(pipefd[0], NULL, fd, NULL, remain, SPLICE_F_MOVE | SPLICE_F_MORE);
    }
    
    return 0;
}
```

## 原理

要将文件内容发送到客户端：

1. 使用splice()系统调用将文件内容与管道绑定
2. 使用splice()系统调用将管道的数据拷贝到客户端连接的socket

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/splice().png)