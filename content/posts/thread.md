---
title: "C++11_多线程"
date: 2021-10-07T22:26:08+08:00
draft: true
---

# C多线程

## 第一个线程程序

```C++
#include <stdio.h>
//#include <stdlib.h>
#include <pthread.h>
/* run this program using the console pauser or add your own getch, system("pause") or input loop */

// 线程 1 执行函数
void* Thread_1(void* arg){
	printf("this is thread_1.\n");
	return "Thread_1 create sucessfull!";
}

// 线程 2 执行函数
void* Thread_2(void* arg){
	printf("this is thread_2.\n");
	return "Thread_2 create sucessfull!";
}

int main(int argc, char *argv[]) {
	int res_1 = 0;
	int res_2 = 0;
    // 线程变量：返回值 pthread_t
	pthread_t t1,t2;
    // 接收创建线程函数的返回值：返回值为 0 ，说明创建成功
    // int pthrea_create(pthread_t *th, const pthread_attr_t *attr, void *(* func)(void *), void *arg )
	res_1 = pthread_create(&t1,NULL,Thread_1,NULL);
	res_2 = pthread_create(&t2,NULL,Thread_2,NULL);
	
	if(res_1!=0){
		printf("Thread_1 create failed!\n");
	}
	if(res_2!=0){
		printf("Thread_2 create failed!\n");
	}
	
	
	
	int res_3 = 0;
	int res_4 = 0;
	
	void* thread_result_1;
	void* thread_result_2;
	// 加入执行，主线程阻塞等待，直到线程执行完毕：返回值为 0 ，说明函数执行成功
    // int pthread_join(pthread_t th,void **res)
    // thread_result_n：用于接受哦函数执行的返回数据
	res_3 = pthread_join(t1,&thread_result_1);
	res_4 = pthread_join(t2,&thread_result_2);
	if(res_3!=0 || res_4!=0){
		printf("pthread_join_1 failed!\n");
	}
	
	printf("%s\n",(char*)thread_result_1);
	printf("%s\n",(char*)thread_result_2);
	printf("main thread over!\n");
	
	return 0;
}
```

*函数执行结果：*

```
this is thread_1.
this is thread_2.
Thread_1 create sucessfull!
Thread_2 create sucessfull!
main thread over!
```

如果成功创建线程，pthread_create() 函数返回数字 0，反之返回非零值。各个非零值都对应着不同的宏，指明创建失败的原因，常见的宏有以下几种：

- EAGAIN：系统资源不足，无法提供创建线程所需的资源。
- EINVAL：传递给 pthread_create() 函数的 attr 参数无效。
- EPERM：传递给 pthread_create() 函数的 attr 参数中，某些属性的设置为非法操作，程序没有相关的设置权限。

> 以上这些宏都声明在 <errno.h> 头文件中，如果程序中想使用这些宏，需提前引入此头文件。

## 创建线程

*代码实现：*

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

void* Thread_1(void* arg){
	if(arg == NULL){
		printf("arg empty!\n");
	}else{
		printf("%s\n",(char*)arg);
	}
	return "Thread_1 create sucessfull!\n";
}

int main(){
	pthread_t t1;
	char * s = "Hello Thread!";
	int res ;
	res = pthread_create(&t1,NULL,Thread_1,(void*)s);
	
	if(res!=0){
		printf("Thread_1 create failed!\n");
		return 0;
	}
	
	sleep(5);
	return 0;
}
```

*执行结果：*

```
Hello Thread!
```

---

## 获取线程的返回值

* `pthread_join()`：会一直调用阻塞它的线程值，直到目标函数执行结束（接收到目标线程的返回值）；不需要返回值，则将第二个参数设置为NULL

* 返回值为 0 ，调用成功；返回值不为 0 ：（在头文件`errno.h`头文件中）

  * EDEADLK：检测到线程发生了死锁。
  * EINVAL：分为两种情况，要么目标线程本身不允许其它线程获取它的返回值，要么事先就已经有线程调用 pthread_join() 函数获取到了目标线程的返回值。
  * ESRCH：找不到指定的 thread 线程。

* 一个线程执行结束的返回值只能由一个 pthread_join() 函数获取，当有多个线程调用 pthread_join() 函数获取同一个线程的执行结果时，哪个线程最先执行 pthread_join() 函数，执行结果就由那个线程获得，其它线程的 pthread_join() 函数都将执行失败。

  对于一个默认属性的线程 A 来说，线程占用的资源并不会因为执行结束而得到释放。而通过在其它线程中执行`pthread_join(A,NULL);`语句，可以轻松实现“及时释放线程 A 所占资源”的目的。 

*代码测试：*

```C++
#include<stdio.h>
#include<pthread.h>
#include<errno.h>

void* Thread_1(void* arg){
	printf("Thread_1 is beging!\n");
	return "Thread_1 return.\n";
}

int main(){
	pthread_t t1;
	int res;
	res = pthread_create(&t1,NULL,Thread_1,NULL);
	if(res!=0) printf("Thread_1 create failed.\n");
	
	void* msg;
	res = pthread_join(t1,&msg);
	if(res!=0) printf("Thread_1 join failed!\n");
	
	printf("%s\n",(char*)msg);
	
	res = pthread_join(t1,&msg);
	if(res == ESRCH){
		printf("Thread_1 is joined before.\n");
	}
	return 0;
}
```

---





## 终止线程

线程终止的方式：

1. 正常执行完线程退出
2. 线程调用函数 pthread_exit()  或者 return ，然后退出
3. 线程执行过程中，接收到其它线程发送的“终止执行”的信号，然后终止执行

### pthread_exit()

*代码实现：*

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

void* thread_1(void* arg){
    // 退出线程：其中返回的数据不是线程局部变量，并非线程内部的私有数据
	pthread_exit("thread_1 exit!");	
    // 以下语句不会执行到
	printf("this is thread_1\n");
	return "thread_1 created!\n";
}

int main(){
	pthread_t t1;
	int res;
	
	res = pthread_create(&t1,NULL,thread_1,NULL);
	if(res!=0){
		printf("thread_1 failed!\n");
	}
	
	void* thread_result;
	int result;
	result = pthread_join(t1,&thread_result);
	if(result!=0){
		printf("thread_1 join failed!\n");
	}
	printf("%s\n",(char*)thread_result);
	
	sleep(5);
	return 0;
}
```

*执行结果：*

```
thread_1 exit!
```



* pthread_exit()语法：`void* pthread_exit(void* retval)`
* 只能用于线程函数（return可以用于任何函数）
* retval：函数返回值（不需要返回值时 NUL ）

* 注意，retval 指针不能指向函数内部的局部数据（比如局部变量）。换句话说，**pthread_exit() 函数不能返回一个指向局部数据的指针**，否则很可能使程序运行结果出错甚至崩溃。

---

### pthread_exit() 和 return

这是使用 pthread_exit() 的执行结果：

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

void* thread_1(void* arg){
	printf("hello thread_1\n");
    // pthread_exit()
	pthread_exit("thread_1 exit");
}

int main() {
	pthread_t t1;
	void* thread_result;
	pthread_create(&t1,NULL,thread_1,NULL);
	
	pthread_join(t1,&thread_result);
	printf("%s\n",(char*)thread_result);
	
	sleep(5);
	printf("hello main\n");
	return 0;
}
```

*执行结果：*

```
hello thread_1
thread_1 exit	 
// 中间停了 5s
hello main
```

将线程函数的返回函数改成return，以下是使用 return 的执行结果：

```
hello thread_1
thread_1 exit	 
// 中间停了 5s
hello main
```

**在线程内部用于退出和返回值时，功能是一样的**





**区别：**

将上述代码注释掉一些：

*主线程函数使用`return`*

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

void* thread_1(void* arg){
	printf("hello thread_1\n");
	//pthread_exit("thread_1 exit");
	return "thread_1 exit";
}

int main() {
	pthread_t t1;
	void* thread_result;
	pthread_create(&t1,NULL,thread_1,NULL);
	
	//pthread_join(t1,&thread_result);
	//printf("%s\n",(char*)thread_result);
	
	//sleep(5);
	printf("hello main\n");
	return 0;
}
```

*执行结果：*

```
hello main

```

*主线程的函数使用`pthread_exit()`*

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

void* thread_1(void* arg){
	printf("hello thread_1\n");
	//pthread_exit("thread_1 exit");
	return "thread_1 exit";
}

int main() {
	pthread_t t1;
	void* thread_result;
	pthread_create(&t1,NULL,thread_1,NULL);
	
	//pthread_join(t1,&thread_result);
	//printf("%s\n",(char*)thread_result);
	
	//sleep(5);
	printf("hello main\n");
	//return 0;
	pthread_exit(NULL);
}
```

*执行结果：*

```
hello main
hello thread_1
```

**总结：pthread_exit() 函数只会终止当前线程，不会影响其它线程的执行**

* 此外，**pthread_exit() 函数还会自动调用线程清理程序**（本质是一个由 pthread_cleanup_push() 指定的自定义函数），而 return 不具备这个能力

---

### pthread_cancel

*代码测试：*

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

void* Thread_1(void* arg){
	printf("Thread_1 is begining!\n");
	sleep(5);
}

int main(){
	pthread_t t1;
	int res;
	res = pthread_create(&t1,NULL,Thread_1,NULL);
	if(res!=0){
		printf("Thread_1 create failed.\n");
	}
	sleep(1);
	
	int res_1;
	res_1 = pthread_cancel(t1);
	if(res_1!=0){
		printf("Thread_1 cancel failed.\n");
	}
	
	int res_2;
	void* msg;
	res_2 = pthread_join(t1,&msg);
	if(res_2!=0){
		printf("Thread_1 join failed.\n");
	}
	//printf("%s\n",(char*)msg);
	if(msg == PTHREAD_CANCELED){
		printf("Thread_1 is exited by pthread_cancel.\n");
	}else{
		printf("Error!\n");
	}
	
	return 0;
}

```

pthread_cancel 语法：

`int pthread_cancel(pthread_t thread)`：

* 返回值如果为 0 ，说明发送终止线程信号成功；如果返回值不为 0 ，返回非 0 整数；对于因为*未找到目标线程*的失败，返回ESRCH宏（包含于头文件`errno.h`中，该宏的值为 3 ）
* `pthread_t thread`：为想要终止的线程，发送终止信号之后，怎么处理时线程thread的事情
* 接收到终止信号的线程，终止之后相当于调用了`pthread_exit(PTHREAD_CANCELED)`，返回宏`PTHREAD_CANCELED`在头文件`pthread.h`中



### 使用 pthread_cancel 需要注意的

使用`pthread_cancel`对某个线程发送终止信号，目标线程可以不作任何回应，也可能等到时机合适才会执行终止线程。合适的时机一般指的是**取消点**

常见的取消点：

* `pthread_join`
* `pthread_testcancel`
* `systerm`
* `sleep`
* .....

当线程执行到这些函数（取消点）时，才会去处理接收到的终止线程的信号

---





在线程中，可以通过设置线程取消的状态来处理线程接收到终止信号之后的反应

#### pthread_setcancelstate 

pthread_setcancelstate可以让线程立即处理终止信号，也可以对于其他线程发来的终止信号不予理会

`pthread_setcancelstate` 语法：

* `int pthread_setcancelstate(int state,int *oldstate)`
  * `state`：新的状态
    * PTHREAD_CANCEL_ENABLE（默认值）：当前线程会处理其它线程发送的 Cancel 信号；
    * PTHREAD_CANCEL_DISABLE：当前线程不理会其它线程发送的 Cancel 信号，直到线程状态重新调整为 PTHREAD_CANCEL_ENABLE 后，才处理接收到的 Cancel 信号。
  * `*oldstate`：oldtate 参数用于接收线程先前所遵循的 state 值，通常用于对线程进行重置。如果不需要接收此参数的值，置为 NULL 即可
* 返回值：成功返回 0 ，否则返回非 0 

#### pthread_setcanceltype

当线程会对 Cancel 信号进行处理时，我们可以借助 pthread_setcanceltype() 函数设置线程响应 Cancel 信号的**时机**

`pthread_setcanceltype` 语法：

* `int pthread_setcanceltype(int type,int *oldtype)`
  * `type`：处理时机
    * PTHREAD_CANCEL_DEFERRED（默认值）：当线程执行到某个可作为取消点的函数时终止执行；
    * PTHREAD_CANCEL_ASYNCHRONOUS：线程接收到 Cancel 信号后立即结束执行。
  * `*oldtype`：先前遵循的type值，如果不需要对其修改，则设置为NULL
* 返回值：返回 0 成功；返回非 0 不成功

*代码测试：*

```C++
#include<stdio.h>
#include<pthread.h>

void* Thread_1(void* arg){
	printf("Thread_1 is begining!\n");
	int res;
	res = pthread_setcancelstate(PTHREAD_CANCEL_ENABLE,NULL);
	if(res!=0){
		printf("Thread_1 set state failed!\n");
		return NULL;
	}
	
	res = pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS,NULL);
	if(res!=0){
		printf("Thread_1 set typr failed!\n");
		return NULL;
	}
	while(1);
	return NULL;
}

int main(){
	pthread_t t1;
	int res = pthread_create(&t1,NULL,Thread_1,NULL);
	if(res!=0){
		printf("Thread_1 create failed.\n");
	}
	
	res = pthread_cancel(t1);
	if(res!=0){
		printf("Thread_1 cancel failed!\n");
	}
	
	void* thread_res;
	res = pthread_join(t1,&thread_res);
	if(res!=0){
		printf("Thread_1 join failed.\n");
	}
	//printf("%s\n",(char*)thread_res);
	if(thread_res == PTHREAD_CANCELED){
		printf("Thread_1 is canceled by pthread_cancel.\n");
	}
	
	return 0;
}
```

---

## 多线程的同步问题

*代码测试：*

这里创建了4个线程，分别对同一个变量 target_sum 进行修改：

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

int ticket_sum = 10;
void *Bought(void* arg){
	for(int i=0;i<10;i++){
		if(ticket_sum>0){
			sleep(1);
			printf("%u sell num %d ticket.\n",pthread_self(),10-ticket_sum+1);
			ticket_sum--;
		}
	}
	return 0;
}

int main(){
	pthread_t t[4];
	
	int res;
	for(int i=0;i<4;i++){
		res = pthread_create(&t[i],NULL,Bought,NULL);
		if(res!=0) {
			printf("Thread %d create failed!\n",i);
			return 0;
		}
	}
	
	void* msg;
	sleep(10);
	for(int i=0;i<4;i++){
		res = pthread_join(t[i],&msg);
		if(res!=0){
			printf("Thread %d join failed!\n",i);
			return 0;
		}
	}
	
	
	return 0;
}
```

同一段代码，再Dev-C++上运行结果是这样的：

```
2 sell num 1 ticket.
1 sell num 1 ticket.
3 sell num 1 ticket.
4 sell num 1 ticket.
2 sell num 5 ticket.
1 sell num 5 ticket.
4 sell num 5 ticket.
3 sell num 5 ticket.
4 sell num 9 ticket.
3 sell num 9 ticket.
1 sell num 9 ticket.
2 sell num 9 ticket.
4 sell num 13 ticket.

--------------------------------
Process exited after 10.04 seconds with return value 0
请按任意键继续. . .
```

在gcc下运行是这样的：

```
1723844352 sell num 1 ticket.
1723844352 sell num 2 ticket.
1723844352 sell num 3 ticket.
1723844352 sell num 4 ticket.
1723844352 sell num 5 ticket.
1723844352 sell num 6 ticket.
1723844352 sell num 7 ticket.
1723844352 sell num 8 ticket.
1723844352 sell num 9 ticket.
1723844352 sell num 10 ticket.
```

我们通常将“多个线程同时访问某一公共资源”的现象称为“线程间产生了资源竞争”或者“线程间抢夺公共资源”，线程间竞争资源往往会导致程序的运行结果出现异常，感到匪夷所思，严重时还会导致程序运行崩溃。

有几种解决方式：

---

## 互斥锁解决

* 定义在头文件`pthread.h`中

* 定义互斥锁（互斥变量）：`pthread_mutex_t myMutex`

  初始化互斥锁：

  * 使用特定的宏：`pthread_mutex_t myMutex = PTHREAD_MUTEX_INITIALIZER;`
  * 调用初始化的函数：`pthread_mutex_init(&myMutex,NULL);`

  宏和调用的函数都在`pthread.h`头文件中，**主要区别**：

  1. pthread_mutex_init() 函数可以自定义互斥锁的属性
  2. 对于调用 malloc() 函数分配动态内存的互斥锁，只能使用`pthread_mutex_init()`

  * `pthread_mutex_init()`语法：

    `int pthread_mutex_init(pthread_mutex_t *mutex, const pthread_mutexattr_t *attr)`

    mutex 参数表示要初始化的互斥锁；attr 参数用于自定义新建互斥锁的属性，attr 的值为 NULL 时表示以默认属性创建互斥锁

    pthread_mutex_init() 函数成功完成初始化操作时，返回数字 0；如果初始化失败，函数返回非零数

    **注意，不能对一个已经初始化过的互斥锁再进行初始化操作，否则会导致程序出现无法预料的错误**

* “加锁” 与 “解锁”：

  `pthread_mutex_lock(&myMutex)`：加锁

  `pthread_mutex_trylock(&myMutex)`：加锁

  `pthread_mutex_unlock(&myMutex)`：解锁

  参数 mutex 表示我们要操控的互斥锁。函数执行成功时返回数字 0，否则返回非零数

  **pthread_mutex_lock() 和 pthread_mutex_trylock() 的区别：**

  * pthread_mutex_lock() 和 pthread_mutex_trylock() 函数都用于实现“加锁”操作，不同之处在于**当互斥锁已经处于“加锁”状态时**：
    - 执行 pthread_mutex_lock() 函数会使线程进入等待（阻塞）状态，直至互斥锁得到释放；
    - **执行 pthread_mutex_trylock() 函数不会阻塞线程，直接返回非零数（表示加锁失败）**

* 互斥锁的“销毁”

  **对于使用动态内存分配的互斥锁：**

  `pthread_mutex_t myMutex = (pthread_mutex_t*)malloc(sizeof(pthread_mutex_t));`

  `pthread_mutex_init(&myMutex,NULL);`

  **手动释放 myMutex 占用的内存（调用 free() 函数）之前，必须先调用 pthread_mutex_destory() 函数销毁该对象**

  `pthread_mutex_destroy(&myMutex);`

  `free(myMutex);`

  * 语法：

    `int pthread_mutex_destory(pthread_mutex_t *mutex);`

    参数 mutex 表示要销毁的互斥锁。如果函数成功销毁指定的互斥锁，返回数字 0，反之返回非零数

  * **注意，对于用 PTHREAD_MUTEX_INITIALIZER 或者 pthread_mutex_init() 函数直接初始化的互斥锁，无需调用 pthread_mutex_destory() 函数手动销毁**

*代码测试：*

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

int ticket_sum = 10;
pthread_mutex_t myMutex = PTHREAD_MUTEX_INITIALIZER;

void* Bought(void* arg){
	printf("This is thread :%d\n",pthread_self());
	int isLock;
	
	if(ticket_sum>0){
		isLock = pthread_mutex_lock(&myMutex);
		if(isLock==0){
			sleep(1);
			printf("%u thread sell num %d ticket.\n",pthread_self(),10-ticket_sum+1);
		}
		isLock = pthread_mutex_unlock(&myMutex);
		if(isLock==0){
			printf("unlock!\n");
		}
		ticket_sum--;	
	}


	return "return";
}

int main(){
	pthread_t t[4];
	int res;
	for(int i=0;i<10;i++){
		res = pthread_create(&t[i % 4],NULL,Bought,NULL);
		if(res!=0){
			printf("Thread %d create failed!\n",(i%4));
			return 0;
		}
	}

	sleep(10);

	for(int i=0;i<10;i++){
		void* msg;
		res = pthread_join(t[i%4],&msg);
		if(res!=0){
			printf("Thread %d join failed!\n",i%4);
			return 0;
		}
		printf("msg = %s\n",(char*)msg);	
	}

	return 0;
}

```

*代码运行结果：*

```
This is thread :1375082240
This is thread :1366689536
This is thread :1358296832
This is thread :1349904128
This is thread :1341511424
This is thread :1333118720
This is thread :1324726016
This is thread :1316333312
This is thread :1299547904
This is thread :1307940608
1375082240 thread sell num 1 ticket.
unlock!
1366689536 thread sell num 2 ticket.
unlock!
1358296832 thread sell num 3 ticket.
unlock!
1349904128 thread sell num 4 ticket.
unlock!
1341511424 thread sell num 5 ticket.
unlock!
1333118720 thread sell num 6 ticket.
unlock!
1324726016 thread sell num 7 ticket.
unlock!
1316333312 thread sell num 8 ticket.
unlock!
1299547904 thread sell num 9 ticket.
unlock!
1307940608 thread sell num 10 ticket.
unlock!
msg = return
msg = return
msg = return
msg = return
Thread 0 join failed!

```

---



# C++多线程

## 创建线程

利用`std::thread`创建线程：提供一个线程函数，可以同时指定其参数

```C++
void fun(){
    std::cout<<"fun"<<std::endl;
}

void bar(int x){
    std::cout<<"bar::x="<<std::endl;
}

void test(){
    std::thread first(fun);
    std::thread second(bar,0);
    
    first.join();
    second.join();
    
    std::cout<<"fun and bar"<<std::endl;
}

int main(){
    test();
    return 0;
}
```

`join()`：阻塞线程，直到线程执行完毕，**如果线程函数有返回值，则返回值会被忽略**

除了`join()`之外，还有`detach`方法：创建线程之后调用，线程会和主线程进行分离，后台执行，主线程不会被阻塞

```C++
void fun(){
    while(1){
        std::cout<<"fun"<<std::endl;
        sleep(100);
    }
}

int main(){
    std::thread first(foo);
    while(1){
        std::cout<<"main"<<std::endl;
        sleep(100);
    }
    
    first.detach();
    return 0;
}
```

`std::thread`在线程函数返回前被析构会发生错误。解决：可以将线程保存在一个容器中

```C++
void fun(){
    std::cout<<"fun"<<std::endl;
}

void bar(int x){
    std::cout<<"bar"<<std::endl;
}

std::vector<std::thread> list_1;
std::vector<std::shared_ptr<std::thread>> list_2;

void createthread(){
    std::thread t(fun);
    list_1.push_back(std::move(t));
    list_2.push_back(std::make_shared<std::thread>(bar,2));
}

int main(){
    createthread();
    for(auto& thread:list_1){
        thread->join();
    }
    
    for(auto& thread:list_2){
        thread->join();
    }
    
    return 0;
}
```

## 线程基本用法

**获取线程id 和 CPU核心数量**

* `get_id()`：获取线程id
* `hardware_concurrency()`：获取CPU核心数

```C++
void fun(){
    std::cout<<"fun"<<std::endl;
}

int main(){
    std::thread first(foo);
    
    std::cout<<first.get_id()<,std::endl;
    
    std::cout<<std::thread::hareware_concurrency()<<std::endl;
    
    return 0;
}
```

