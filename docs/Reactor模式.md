# Reactor模式

C++98代码：

```cpp
/**   
  2  *@desc:用reactor模式练习服务器程序，main.cpp
  3  *@author: zhangyl （代码来源）
  4  *@date:   2016.11.23
  5  */  
  6  #include <iostream>
  7  #include <string.h>
  8  #include <sys/types.h>
  9  #include <sys/socket.h>
 10  #include <netinet/in.h>
 11  #include <arpa/inet.h>    //for htonl() and htons()
 12  #include <unistd.h>
 13  #include <fcntl.h>
 14  #include <sys/epoll.h>
 15  #include <signal.h>    //for signal()
 16  #include <pthread.h>
 17  #include <semaphore.h>
 18  #include <list>
 19  #include <errno.h>
 20  #include <time.h>
 21  #include <sstream>
 22  #include <iomanip>     //for std::setw()/setfill()
 23  #include <stdlib.h>  
 24
 25  #define WORKER_THREAD_NUM   5  //5个工作线程
 26  #define min(a, b) ((a <= b) ? (a) : (b))   
 27  int g_epollfd = 0;
 28  bool g_bStop = false;
 29  int g_listenfd = 0;
 30  pthread_t g_acceptthreadid = 0;
 31  pthread_t g_threadid[WORKER_THREAD_NUM] = { 0 };  
 32  pthread_cond_t g_acceptcond;
 33  pthread_mutex_t g_acceptmutex;  
 34  pthread_cond_t g_cond /*= PTHREAD_COND_INITIALIZER*/;  
 35  pthread_mutex_t g_mutex /*= PTHREAD_MUTEX_INITIALIZER*/;  
 36  pthread_mutex_t g_clientmutex;  
 37  std::list<int> g_listClients;  
 38  void prog_exit(int signo) //进程退出
 39  {  
 40    ::signal(SIGINT, SIG_IGN);  
 41    ::signal(SIGKILL, SIG_IGN);  
 42    ::signal(SIGTERM, SIG_IGN);  
 43
 44    std::cout << "program recv signal " << signo
 45              << " to exit." << std::endl;  
 46
 47    g_bStop = true;  
 48
 49    ::epoll_ctl(g_epollfd, EPOLL_CTL_DEL, g_listenfd, NULL);  
 50
 51    //TODO: 是否需要先调用shutdown()一下？  
 52    ::shutdown(g_listenfd, SHUT_RDWR);  //关闭一下读端和写端
 53    ::close(g_listenfd);  
 54    ::close(g_epollfd);  
 55    //销毁接收连接的信号量和互斥量
 56    ::pthread_cond_destroy(&g_acceptcond); 
 57    ::pthread_mutex_destroy(&g_acceptmutex);  
 58    //销毁搭配使用的条件变量和互斥量
 59    ::pthread_cond_destroy(&g_cond);  
 60    ::pthread_mutex_destroy(&g_mutex);  
 61
 62    ::pthread_mutex_destroy(&g_clientmutex);
 63  }  
 64  bool create_server_listener(const char* ip, short port)
 65  {  
 66    g_listenfd = ::socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, 0);  
 67    if (g_listenfd == -1)  
 68        return false;  
 69
 70    int on = 1;  
 71    ::setsockopt(g_listenfd, SOL_SOCKET, SO_REUSEADDR,
 72                 (char *)&on, sizeof(on));  
 73    ::setsockopt(g_listenfd, SOL_SOCKET, SO_REUSEPORT,
 74                 (char *)&on, sizeof(on));  //设置ip地址和端口号复用，在调试过程中解决TIME_WAIT状态带来的不能及时连接问题
 75
 76    struct sockaddr_in servaddr;  
 77    memset(&servaddr, 0, sizeof(servaddr));   
 78    servaddr.sin_family = AF_INET;  
 79    servaddr.sin_addr.s_addr = inet_addr(ip);  
 80    servaddr.sin_port = htons(port);  
 81    if (::bind(g_listenfd, (sockaddr *)&servaddr,sizeof(servaddr)) == -1)  
 82        return false;  
 83
 84    if (::listen(g_listenfd, 50) == -1)  
 85        return false;  
 86
 87    g_epollfd = ::epoll_create(1);  
 88    if (g_epollfd == -1)  
 89        return false;  
 90
 91    struct epoll_event e;  
 92    memset(&e, 0, sizeof(e));  
 93    e.events = EPOLLIN | EPOLLRDHUP;  //检测可读和挂起
 94    e.data.fd = g_listenfd;  
 95    if (::epoll_ctl(g_epollfd, EPOLL_CTL_ADD, g_listenfd, &e) == -1)  
 96        return false;  
 97
 98    return true;
 99  }  
100  void release_client(int clientfd)  //关闭客户端连接，取消监听该事件
101  {  
102    if (::epoll_ctl(g_epollfd, EPOLL_CTL_DEL, clientfd, NULL) == -1)  
103        std::cout << "release client socket failed as call epoll_ctl failed"
104                  << std::endl;  
105
106    ::close(clientfd);
107  }  
108  void* accept_thread_func(void* arg)
109  {     
110    while (!g_bStop)  
111    {  
112        ::pthread_mutex_lock(&g_acceptmutex);  
113        ::pthread_cond_wait(&g_acceptcond, &g_acceptmutex);  //阻塞（此时释放锁）直到通知到来（重新获得锁并等待就绪）
114        //::pthread_mutex_lock(&g_acceptmutex);  
115
116        //std::cout << "run loop in accept_thread_func" << std::endl;  
117
118        struct sockaddr_in clientaddr;  
119        socklen_t addrlen;  
120        int newfd = ::accept(g_listenfd,
121                             (struct sockaddr *)&clientaddr, &addrlen);  
122        ::pthread_mutex_unlock(&g_acceptmutex); //接收连接的过程是原子操作，前面获得的锁在此释放  
123        if (newfd == -1)  
124            continue;  
125
126        std::cout << "new client connected: "
127                  << ::inet_ntoa(clientaddr.sin_addr) << ":"
128                  << ::ntohs(clientaddr.sin_port) << std::endl;  
129
130        //将新socket设置为non-blocking  
131        int oldflag = ::fcntl(newfd, F_GETFL, 0);  
132        int newflag = oldflag | O_NONBLOCK;  
133        if (::fcntl(newfd, F_SETFL, newflag) == -1)  
134        {  
135            std::cout << "fcntl error, oldflag =" << oldflag
136                      << ", newflag = " << newflag << std::endl;  
137            continue;  
138        }  
139
140        struct epoll_event e;  
141        memset(&e, 0, sizeof(e));  
142        e.events = EPOLLIN | EPOLLRDHUP | EPOLLET;  //新连接监听可读、挂起，边缘触发模式
143        e.data.fd = newfd;  
144        if (::epoll_ctl(g_epollfd, EPOLL_CTL_ADD, newfd, &e) == -1)  
145        {  
146            std::cout << "epoll_ctl error, fd =" << newfd << std::endl;  
147        }  
148    }  
149
150    return NULL;
151  }  
152
153  void* worker_thread_func(void* arg)
154  {     
155    while (!g_bStop)  
156    {  
157        int clientfd;  
158        ::pthread_mutex_lock(&g_clientmutex);  
159        while (g_listClients.empty())  //防止虚假唤醒
160            ::pthread_cond_wait(&g_cond, &g_clientmutex);  
161        clientfd = g_listClients.front();  //真正的唤醒通知到来，取出客户连接（原子操作）
162        g_listClients.pop_front();    
163        pthread_mutex_unlock(&g_clientmutex);  
164
165        //gdb调试时不能实时刷新标准输出，用这个函数刷新标准输出，使信息在屏幕上实时显示出来  
166        std::cout << std::endl;  
167
168        std::string strclientmsg;  
169        char buff[256];  
170        bool bError = false;  
171        while (true)  
172        {  
173            memset(buff, 0, sizeof(buff));  
174            int nRecv = ::recv(clientfd, buff, 256, 0);  
175            if (nRecv == -1)  
176            {  
177                if (errno == EWOULDBLOCK)  
178                    break;  
179                else  
180                {  
181                    std::cout << "recv error, client disconnected, fd = "
182                              << clientfd << std::endl;  
183                    release_client(clientfd);  
184                    bError = true;  
185                    break;  
186                }  
187
188            }  
189            //对端关闭了socket，这端也关闭。  
190            else if (nRecv == 0)  
191            {  
192                std::cout << "peer closed, client disconnected, fd = "
193                          << clientfd << std::endl;  
194                release_client(clientfd);  
195                bError = true;  
196                break;  
197            }  
198
199            strclientmsg += buff;  
200        }  
201
202        //出错了，就不要再继续往下执行了  
203        if (bError)  
204            continue;  
205
206        std::cout << "client msg: " << strclientmsg;  
207
208        //将消息加上时间标签后发回  
209        time_t now = time(NULL);  
210        struct tm* nowstr = localtime(&now);  
211        std::ostringstream ostimestr;  
212        ostimestr << "[" << nowstr->tm_year + 1900 << "-"   
213                  << std::setw(2) << std::setfill('0')
214                  << nowstr->tm_mon + 1 << "-"   
215                  << std::setw(2) << std::setfill('0')
216                  << nowstr->tm_mday << " "  
217                  << std::setw(2) << std::setfill('0')
218                  << nowstr->tm_hour << ":"   
219                  << std::setw(2) << std::setfill('0')
220                  << nowstr->tm_min << ":"   
221                  << std::setw(2) << std::setfill('0')
222                  << nowstr->tm_sec << "]server reply: ";  
223
224        strclientmsg.insert(0, ostimestr.str());  
225
226        while (true)  //由于是ET模式，所以读和写数据的时候都要使用while，将该fd上的数据读取干净
227        {  
228            int nSent = ::send(clientfd, strclientmsg.c_str(), 
229                               strclientmsg.length(), 0);  
230            if (nSent == -1)  
231            {  
232                if (errno == EWOULDBLOCK)  
233                {  
234                    ::sleep(10);  
235                    continue;  
236                }  
237                else  
238                {  
239                    std::cout << "send error, fd = "
240                              << clientfd << std::endl;  
241                    release_client(clientfd);  
242                    break;  
243                }  
244
245            }            
246
247            std::cout << "send: " << strclientmsg;  
248            strclientmsg.erase(0, nSent);  
249
250            if (strclientmsg.empty())  
251                break;  
252        }  
253    }  
254
255    return NULL;
256  }  
257  void daemon_run() //守护进程运行函数（在后台运行）
258  {  
259    int pid;  
260    signal(SIGCHLD, SIG_IGN);  //子进程信号处理：忽略信号
261    //1）在父进程中，fork返回新创建子进程的进程ID；  
262    //2）在子进程中，fork返回0；  
263    //3）如果出现错误，fork返回一个负值；  
264    pid = fork();  
265    if (pid < 0)  
266    {  
267        std:: cout << "fork error" << std::endl;  
268        exit(-1);  
269    }  
270    //父进程退出，子进程独立运行  
271    else if (pid > 0) {  
272        exit(0);  
273    }  
274    //之前parent和child运行在同一个session里,parent是会话（session）的领头进程,  
275    //parent进程作为会话的领头进程，如果exit结束执行的话，那么子进程会成为孤儿进程，并被init收养。  
276    //执行setsid()之后,child将重新获得一个新的会话(session)id。  
277    //这时parent退出之后,将不会影响到child了。  
278    setsid();  
279    int fd;  
280    fd = open("/dev/null", O_RDWR, 0);  
281    if (fd != -1)  
282    {   //重定向（复制文件描述符，后者为新文件描述符，新旧都可操作）
283        dup2(fd, STDIN_FILENO);  
284        dup2(fd, STDOUT_FILENO);  
285        dup2(fd, STDERR_FILENO);  
286    }  
287    if (fd > 2)  
288        close(fd);  
289   }  
290
291  int main(int argc, char* argv[])
292  {    
293    short port = 0;  
294    int ch;  
295    bool bdaemon = false;  
296    while ((ch = getopt(argc, argv, "p:d")) != -1)  //用户选择选项
297    {  
298        switch (ch)  
299        {  
300        case 'd':  
301            bdaemon = true;  
302            break;  
303        case 'p':  
304            port = atol(optarg);  
305            break;  
306        }  
307    }  
308
309    if (bdaemon)  
310        daemon_run();  
311
312
313    if (port == 0)  
314        port = 12345;  
315
316    if (!create_server_listener("0.0.0.0", port))  
317    {  
318        std::cout << "Unable to create listen server: ip=0.0.0.0, port="
319                  << port << "." << std::endl;  
320        return -1;  
321    }  
322
323
324    //设置信号处理  
325    signal(SIGCHLD, SIG_DFL);  
326    signal(SIGPIPE, SIG_IGN);  
327    signal(SIGINT, prog_exit);  
328    signal(SIGKILL, prog_exit);  
329    signal(SIGTERM, prog_exit);  
330    //初始化接受连接条件变量和互斥量
331    ::pthread_cond_init(&g_acceptcond, NULL);  
332    ::pthread_mutex_init(&g_acceptmutex, NULL);  
333    //初始化搭配使用的（工作线程的）条件变量和互斥量
334    ::pthread_cond_init(&g_cond, NULL);  
335    ::pthread_mutex_init(&g_mutex, NULL);  
336
337    ::pthread_mutex_init(&g_clientmutex, NULL);  
338    //启动接受连接线程
339    ::pthread_create(&g_acceptthreadid, NULL, accept_thread_func, NULL);  
340    //启动工作线程 : round-robin算法
341    for (int i = 0; i < WORKER_THREAD_NUM; ++i)  
342    {  
343        ::pthread_create(&g_threadid[i], NULL, worker_thread_func, NULL);  
344    }  
345
346    while (!g_bStop)  
347    {         
348        struct epoll_event ev[1024];  
349        int n = ::epoll_wait(g_epollfd, ev, 1024, 10);  
350        if (n == 0)  
351            continue;  
352        else if (n < 0)  
353        {  
354            std::cout << "epoll_wait error" << std::endl;  
355            continue;  
356        }  
357
358        int m = min(n, 1024);  
359        for (int i = 0; i < m; ++i)  
360        {  
361            //通知接收连接线程接收新连接  
362            if (ev[i].data.fd == g_listenfd)  
363                pthread_cond_signal(&g_acceptcond);  
364            //通知普通工作线程接收数据  
365            else  
366            {                 
367                pthread_mutex_lock(&g_clientmutex);                
368                g_listClients.push_back(ev[i].data.fd);  
369                pthread_mutex_unlock(&g_clientmutex);  
370                pthread_cond_signal(&g_cond);  
371                //std::cout << "signal" << std::endl;  
372            }  
373
374        }  
375
376    }  
377
378    return 0;
379  } 
```





C++11之后代码实现：

```cpp title="myreactor.h"
1/**
 2 *@desc: myreactor头文件, myreactor.h
 3 *@author: zhangyl
 4 *@date: 2016.12.03
 5 */
 6  #ifndef __MYREACTOR_H__
 7  #define __MYREACTOR_H__  
 8  #include <list>
 9  #include <memory>
10  #include <thread>
11  #include <mutex>
12  #include <condition_variable>  
13  #define WORKER_THREAD_NUM   5  
14  class CMyReactor
15  {
16  public:  
17    CMyReactor();  
18    ~CMyReactor();  
19
20    bool init(const char* ip, short nport);  //初始化服务器连接
21    bool uninit();  //断开连接
22
23    bool close_client(int clientfd); //关闭客户端  
24
25    static void* main_loop(void* p);  
26  private:  
27    //no copyable  
28    CMyReactor(const CMyReactor& rhs);  
29    CMyReactor& operator = (const CMyReactor& rhs);  
30
31    bool create_server_listener(const char* ip, short port);  
32
33    static void accept_thread_proc(CMyReactor* pReatcor);  
34    static void worker_thread_proc(CMyReactor* pReatcor);  
35  private:  
36    //C11语法可以在这里初始化  
37    int                          m_listenfd = 0;  
38    int                          m_epollfd  = 0;  
39    bool                         m_bStop    = false;  
40    //只用智能指针管理接收连接线程资源和工作线程资源
41    std::shared_ptr<std::thread> m_acceptthread;  
42    std::shared_ptr<std::thread> m_workerthreads[WORKER_THREAD_NUM];  
43
44    std::condition_variable      m_acceptcond;  
45    std::mutex                   m_acceptmutex;  
46
47    std::condition_variable      m_workercond ;  
48    std::mutex                   m_workermutex;  
49
50    std::list<int>                 m_listClients;
51  };  
52  #endif //!__MYREACTOR_H__ 
myreactor.cpp文件内容：

  1 /**
  2  *@desc: myreactor实现文件, myreactor.cpp
  3  *@author: zhangyl
  4  *@date: 2016.12.03
  5  */  #include "myreactor.h"
  6  #include <iostream>
  7  #include <string.h>
  8  #include <sys/types.h>
  9  #include <sys/socket.h>
 10  #include <netinet/in.h>
 11  #include <arpa/inet.h>  //for htonl() and htons()
 12  #include <fcntl.h>
 13  #include <sys/epoll.h>
 14  #include <list>
 15  #include <errno.h>
 16  #include <time.h>
 17  #include <sstream>
 18  #include <iomanip>   //for std::setw()/setfill()
 19  #include <unistd.h>  
 20  #define min(a, b) ((a <= b) ? (a) : (b))  
 21  CMyReactor::CMyReactor()
 22  {  //初始化工作可以选择在上述类成员变量声明处初始化
 23    //m_listenfd = 0;  
 24    //m_epollfd = 0;  
 25    //m_bStop = false;
 26  }  
 27  CMyReactor::~CMyReactor()
 28  {  
 29  }  
 30  bool CMyReactor::init(const char* ip, short nport)
 31  {  
 32    if (!create_server_listener(ip, nport))  
 33    {  
 34        std::cout << "Unable to bind: " << ip
 35                  << ":" << nport << "." << std::endl;  
 36        return false;  
 37    }  
 38
 39
 40    std::cout << "main thread id = " << std::this_thread::get_id()
 41              << std::endl;  
 42
 43    //启动接收新连接的线程  
 44    m_acceptthread.reset(new std::thread(CMyReactor::accept_thread_proc, this));  
 45
 46    //启动工作线程：round-robin
 47    for (auto& t : m_workerthreads)  
 48    {  
 49        t.reset(new std::thread(CMyReactor::worker_thread_proc, this));  
 50    }  
 51
 52
 53    return true;
 54  }  
 55  bool CMyReactor::uninit()
 56  {  
 57    m_bStop = true;  
 58    m_acceptcond.notify_one();  //通知接收连接线程
 59    m_workercond.notify_all();  //通知所有工作线程
 60    //接受连接线程和工作线程分别分离，执行剩余，自动退出
 61    m_acceptthread->join();  
 62    for (auto& t : m_workerthreads)  
 63    {  
 64        t->join();  
 65    }  
 66
 67    ::epoll_ctl(m_epollfd, EPOLL_CTL_DEL, m_listenfd, NULL);  //取消监听事件
 68
 69    //TODO: 是否需要先调用shutdown()一下？  
 70    ::shutdown(m_listenfd, SHUT_RDWR);  //关闭一下读和写端
 71    ::close(m_listenfd);  
 72    ::close(m_epollfd);  
 73
 74    return true;
 75  }  
 76  bool CMyReactor::close_client(int clientfd) //先取消该fd的监听，再关闭fd
 77  {  
 78    if (::epoll_ctl(m_epollfd, EPOLL_CTL_DEL, clientfd, NULL) == -1)  
 79    {  
 80        std::cout << "close client socket failed as call epoll_ctl failed"
 81                  << std::endl;  
 82        //return false;  
 83    }  
 84
 85
 86    ::close(clientfd);  
 87
 88    return true;
 89  }  
 90
 91  void* CMyReactor::main_loop(void* p) //相当于上述C++98的main函数中的内容，返回值void*，参数void*
 92  {  
 93    std::cout << "main thread id = "
 94              << std::this_thread::get_id() << std::endl;  
 95
 96    CMyReactor* pReatcor = static_cast<CMyReactor*>(p);  
 97
 98    while (!pReatcor->m_bStop)  
 99    {  
100        struct epoll_event ev[1024];  
101        int n = ::epoll_wait(pReatcor->m_epollfd, ev, 1024, 10);  
102        if (n == 0)  
103            continue;  
104        else if (n < 0)  
105        {  
106            std::cout << "epoll_wait error" << std::endl;  
107            continue;  
108        }  
109
110        int m = min(n, 1024);  
111        for (int i = 0; i < m; ++i)  
112        {  
113            //通知接收连接线程接收新连接  
114            if (ev[i].data.fd == pReatcor->m_listenfd)  
115                pReatcor->m_acceptcond.notify_one();  
116            //通知普通工作线程接收数据  
117            else  
118            {  
119                {  
120                    std::unique_lock<std::mutex> guard(pReatcor->m_workermutex);  
121                    pReatcor->m_listClients.push_back(ev[i].data.fd);  
122                }  //进作用域自动加锁，出作用域自动解锁
123
124                pReatcor->m_workercond.notify_one();  
125                //std::cout << "signal" << std::endl;  
126            }// end if  
127
128        }// end for-loop  
129    }// end while  
130
131    std::cout << "main loop exit ..." << std::endl;  
132
133    return NULL;
134  }  
135  void CMyReactor::accept_thread_proc(CMyReactor* pReatcor) //参数：上述“启动线程”传递this指针
136  {  
137    std::cout << "accept thread, thread id = "
138              << std::this_thread::get_id() << std::endl;  
139
140    while (true)  
141    {  
142        int newfd;  
143        struct sockaddr_in clientaddr;  
144        socklen_t addrlen;  
145        {  
146            std::unique_lock<std::mutex> guard(pReatcor->m_acceptmutex);  
147            pReatcor->m_acceptcond.wait(guard);  
148            if (pReatcor->m_bStop)  
149                break;  
150
151            //std::cout << "run loop in accept_thread_proc" << std::endl;  
152
153            newfd = ::accept(pReatcor->m_listenfd,
154                              (struct sockaddr *)&clientaddr, &addrlen);  
155        }  
156        if (newfd == -1)  
157            continue;  
158
159        std::cout << "new client connected: "
160                  << ::inet_ntoa(clientaddr.sin_addr) << ":"      
161                  << ::ntohs(clientaddr.sin_port) << std::endl;  
162
163        //将新socket设置为non-blocking  
164        int oldflag = ::fcntl(newfd, F_GETFL, 0);  
165        int newflag = oldflag | O_NONBLOCK;  
166        if (::fcntl(newfd, F_SETFL, newflag) == -1)  
167        {  
168            std::cout << "fcntl error, oldflag =" << oldflag
169                      << ", newflag = " << newflag << std::endl;  
170            continue;  
171        }  
172
173        struct epoll_event e;  
174        memset(&e, 0, sizeof(e));  
175        e.events = EPOLLIN | EPOLLRDHUP | EPOLLET;  
176        e.data.fd = newfd;  
177        if (::epoll_ctl(pReatcor->m_epollfd, 
178            EPOLL_CTL_ADD, newfd, &e) == -1)  
179        {  
180            std::cout << "epoll_ctl error, fd =" << newfd << std::endl;  
181        }  
182    }  
183
184    std::cout << "accept thread exit ..." << std::endl;
185  }  
186  void CMyReactor::worker_thread_proc(CMyReactor* pReatcor) //同上
187  {  
188    std::cout << "new worker thread, thread id = "
189              << std::this_thread::get_id() << std::endl;  
190
191    while (true)  
192    {  
193        int clientfd;  
194        {  
195            std::unique_lock<std::mutex> guard(pReatcor->m_workermutex);  
196            while (pReatcor->m_listClients.empty())  
197            {  
198                if (pReatcor->m_bStop)  
199                {  
200                    std::cout << "worker thread exit ..." << std::endl;  
201                    return;  
202                }  
203
204                pReatcor->m_workercond.wait(guard);  //防止虚假唤醒
205            }  
206
207            clientfd = pReatcor->m_listClients.front();  
208            pReatcor->m_listClients.pop_front();  
209        }  
210
211        //gdb调试时不能实时刷新标准输出，用这个函数刷新标准输出，使信息在屏幕上实时显示出来  
212        std::cout << std::endl;  
213
214        std::string strclientmsg;  
215        char buff[256];  
216        bool bError = false;  
217        while (true)  
218        {  
219            memset(buff, 0, sizeof(buff));  
220            int nRecv = ::recv(clientfd, buff, 256, 0);  
221            if (nRecv == -1)  
222            {  
223                if (errno == EWOULDBLOCK)  
224                    break;  
225                else  
226                {  
227                    std::cout << "recv error, client disconnected, fd = "
228                              << clientfd << std::endl;  
229                    pReatcor->close_client(clientfd);  
230                    bError = true;  
231                    break;  
232                }  
233
234            }  
235            //对端关闭了socket，这端也关闭。  
236            else if (nRecv == 0)  
237            {  
238                std::cout << "peer closed, client disconnected, fd = "
239                          << clientfd << std::endl;  
240                pReatcor->close_client(clientfd);  
241                bError = true;  
242                break;  
243            }  
244
245            strclientmsg += buff;  
246        }  
247
248        //出错了，就不要再继续往下执行了  
249        if (bError)  
250            continue;  
251
252        std::cout << "client msg: " << strclientmsg;  
253
254        //将消息加上时间标签后发回  
255        time_t now = time(NULL);  
256        struct tm* nowstr = localtime(&now);  
257        std::ostringstream ostimestr;  
258        ostimestr << "[" << nowstr->tm_year + 1900 << "-"  
259            << std::setw(2) << std::setfill('0') << nowstr->tm_mon + 1 << "-"  
260            << std::setw(2) << std::setfill('0') << nowstr->tm_mday << " "  
261            << std::setw(2) << std::setfill('0') << nowstr->tm_hour << ":"  
262            << std::setw(2) << std::setfill('0') << nowstr->tm_min << ":"  
263            << std::setw(2) << std::setfill('0') << nowstr->tm_sec << "]server reply: ";  
264
265        strclientmsg.insert(0, ostimestr.str());  
266
267        while (true)  
268        {  
269            int nSent = ::send(clientfd, strclientmsg.c_str(), 
270                               strclientmsg.length(), 0);  
271            if (nSent == -1)  
272            {  
273                if (errno == EWOULDBLOCK)  
274                {  
275                    std::this_thread::sleep_for(std::chrono::milliseconds(10));  
276                    continue;  
277                }  
278                else  
279                {  
280                    std::cout << "send error, fd = "
281                              << clientfd << std::endl;  
282                    pReatcor->close_client(clientfd);  
283                    break;  
284                }  
285
286            }  
287
288            std::cout << "send: " << strclientmsg;  
289            strclientmsg.erase(0, nSent);  
290
291            if (strclientmsg.empty())  
292                break;  
293        }  
294    }
295  }  
296  bool CMyReactor::create_server_listener(const char* ip, short port)
297  {  
298    m_listenfd = ::socket(AF_INET, SOCK_STREAM | SOCK_NONBLOCK, 0);  
299    if (m_listenfd == -1)  
300        return false;  
301
302    int on = 1;  
303    ::setsockopt(m_listenfd, SOL_SOCKET, SO_REUSEADDR,
304                (char *)&on, sizeof(on));  
305    ::setsockopt(m_listenfd, SOL_SOCKET, SO_REUSEPORT,
306                (char *)&on, sizeof(on));  
307
308    struct sockaddr_in servaddr;  
309    memset(&servaddr, 0, sizeof(servaddr));  
310    servaddr.sin_family = AF_INET;  
311    servaddr.sin_addr.s_addr = inet_addr(ip);  
312    servaddr.sin_port = htons(port);  
313    if (::bind(m_listenfd, (sockaddr *)&servaddr, 
314         sizeof(servaddr)) == -1)  
315        return false;  
316
317    if (::listen(m_listenfd, 50) == -1)  
318        return false;  
319
320    m_epollfd = ::epoll_create(1);  
321    if (m_epollfd == -1)  
322        return false;  
323
324    struct epoll_event e;  
325    memset(&e, 0, sizeof(e));  
326    e.events = EPOLLIN | EPOLLRDHUP;  
327    e.data.fd = m_listenfd;  
328    if (::epoll_ctl(m_epollfd, EPOLL_CTL_ADD, m_listenfd, &e) == -1)  
329        return false;  
330
331    return true;
332  }  
```

编译上述C++11的实现代码可以使用cmake编译：

```cmake
cmake_minimum_required(VERSION 2.8)  
  ## PROJECT(projectname [CXX] [C] [Java])
  PROJECT(myreactorserver)  
  ## AUX_SOURCE_DIRECTORY(dir VAR)  发现一个目录下所有的源代码文件并将列表存储在一个变量中
  AUX_SOURCE_DIRECTORY(./ SRC_LIST)
  ## EXECUTABLE_OUTPUT_PATH  重新定义目标二进制可执行文件的存放位置
  ## SET 定义变量
  SET(EXECUTABLE_OUTPUT_PATH ./) 
  ## 向C/C++编译器添加-D定义
  ADD_DEFINITIONS(-g -W -Wall -Wno-deprecated
                  -DLINUX -D_REENTRANT -D_FILE_OFFSET_BITS=64
                  -DAC_HAS_INFO -DAC_HAS_WARNING -DAC_HAS_ERROR 
                  -DAC_HAS_CRITICAL -DTIXML_USE_STL
                  -DHAVE_CXX_STDHEADERS ${CMAKE_CXX_FLAGS}
                  -std=c++11)  
  INCLUDE_DIRECTORIES(  ./  )
  ## 添加非标准的共享库搜索路径
  LINK_DIRECTORIES(  ./  )  
  set(  main.cpp  myreator.cpp  )  
  ADD_EXECUTABLE(myreactorserver ${SRC_LIST}) 
  ## 为target添加需要链接的共享库
  TARGET_LINK_LIBRARIES(myreactorserver pthread)  
```

程序部署方法：可以使用Linux命令：

```she
nc 120.55.94.78 12345
```

或者是：

```shel
telnet 120.55.94.78 12345
```

<br>

<br>

<br>

[参考文章](https://mp.weixin.qq.com/s/Q7UyrIRUFSYSipdaJgtXmg)

