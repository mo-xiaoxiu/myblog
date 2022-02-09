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

## 信号量解决

多线程程序中，使用信号量需遵守以下几条规则：

1. 信号量的值**不能小于 0**；
2. 有线程**访问资源**时，信号量执行**“减 1”**操作，访问**完成后再执行“加 1”**操作；
3. 当信号量的值**为 0 **时，想访问资源的线程必须**等待**，直至信号量的值大于 0，等待的线程才能开始访问。

* 信号量在头文件`semaphore.h`中：

  ``#include<semaphore.h>`

  `sem_t mySem;`

* 初始化：

  * 语法：`int sem_init(sem_t *sem,int pshared,usigned int value);`
    * `sem`：要初始化的目标信号量
    * `pshared`：表示该信号量是否与其他**进程**共享（其中，**1 表示共享；0 表示不共享**）
    * `value`：信号量的初值
  * 返回值：成功返回 0 ，不成功返回非零

* 信号量的函数：

  * `sem_post(sem_t* sem)`：信号量值加 1 ，唤醒其他线程
  * `sem_wait(sem_t* sem)`：信号量值减 1 ，当**信号量为 0 时，`sem_wait()`会阻塞当前线程，直到函数执行`sem_post()`，线程才开始执行**
  * `sem_trywait(sem_t* sem)`：功能与`sem_wait()`是一致的，只不过**当信号量为 0 时，`sem_trywait()不会阻塞当前线程，而是直接返回 -1 `**
  * `sem_destroy(sem_t* sem)`：销毁信号量

  以上函数执行成功，返回 0 ，否则返回非零数

### 二进制的信号量

**用于解决线程同步的问题：**

```C++
#include<stdio.h>
#include<pthread.h>
#include<semaphore.h>
#include<unistd.h>

int ticket_sum = 10;
sem_t mySem;

void* Bought(void* arg){
	printf("This is thread: %u\n",pthread_self());
	int flag;
	for(int i=0;i<10;i++){
		flag = sem_wait(&mySem);
		if(flag == 0){
			if(ticket_sum>0){
				sleep(1);
				printf("Thread %u sell ticket %d\n",pthread_self(),10-ticket_sum+1);
				ticket_sum--;
			}
			sem_post(&mySem);
			sleep(1);
		}
	}

	return "return\n";
}

int main(){
	pthread_t t[4];
	int res;
	res = sem_init(&mySem,0,1);
	if(res!=0){
		printf("Sign init failed!\n");
	}
	for(int i=0;i<4;i++){
		res = pthread_create(&t[i],NULL,Bought,NULL);
		if(res!=0){
			printf("Thread %u create failed!\n",pthread_self());
			return 0;
		}
	}

	sleep(10);
	void* msg;
	for(int i=0;i<4;i++){
		res = pthread_join(t[i],&msg);
		if(res!=0){
			printf("Thread %u join failed!\n",pthread_self());
			return 0;
		}
	}

	sem_destroy(&mySem);

	return 0;
}

```

*代码运行结果如下：*

```
This is thread: 1152108288
This is thread: 1143715584
This is thread: 1135322880
This is thread: 1160500992
Thread 1152108288 sell ticket 1
Thread 1143715584 sell ticket 2
Thread 1135322880 sell ticket 3
Thread 1160500992 sell ticket 4
Thread 1152108288 sell ticket 5
Thread 1143715584 sell ticket 6
Thread 1135322880 sell ticket 7
Thread 1160500992 sell ticket 8
Thread 1152108288 sell ticket 9
Thread 1143715584 sell ticket 10
```

### 计数信号量

用于模拟多线程办理业务，可以有多线程同时访问同个资源

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>
#include<semaphore.h>

int num = 5;
sem_t mySem;

void* get_ser(void* arg){
	int id = *((int*)arg);
	if(sem_wait(&mySem)==0){
		printf("Customer %d is servered!\n",id);
		sleep(2);
		printf("Customer %d is going!\n",id);
		sem_post(&mySem);
	}
	return 0;
}

int main(){
	pthread_t t[5];
	int flag;
	sem_init(&mySem,0,2);
	for(int i=0;i<num;i++){
		flag = pthread_create(&t[i],NULL,get_ser,&i);
		if(flag!=0){
			printf("Thread %u create failed!\n",pthread_self());
			return 0;
		}else{
			printf("Customer %d is coming!\n",i);
		}
		sleep(1);
	}

	sleep(10);
	void* msg;
	for(int i=0;i<num;i++){
		flag = pthread_join(t[i],&msg);
		if(flag!=0){
			printf("Thread %u join failed!\n",pthread_self());
			return 0;
		}
	}

	return 0;
}
```

*代码运行结果如下：*

```
Customer 0 is coming!
Customer 0 is servered!
Customer 1 is coming!
Customer 1 is servered!
Customer 0 is going!
Customer 2 is coming!
Customer 2 is servered!
Customer 1 is going!
Customer 3 is coming!
Customer 3 is servered!
Customer 2 is going!
Customer 4 is coming!
Customer 4 is servered!
Customer 3 is going!
Customer 4 is going!
```

---

## 条件变量解决

* 定义：

  `#include<pthread.h>`

  `pthread_cond_t myCond;`

* 初始化：

  1. `pthread_cond_t myCond = PTHREAD_COND_INITIALIZER;`

  2. 语法：

     `int pthread_cond_init(pthread_cond_t *cond, const pthreadattr_t attr);`

     参数 cond 用于指明要初始化的条件变量；参数 attr 用于自定义条件变量的属性，通常我们将它赋值为 NULL，表示以系统默认的属性完成初始化操作。

     pthread_cond_init() 函数初始化成功时返回数字 0，反之函数返回非零数。

     > 当 attr 参数为 NULL 时，以上两种初始化方式完全等价。

* 阻塞当前线程，等待条件成立

  `int pthread_cond_wait(pthread_cond_t *cond, pthread_mutex_t *mutex);`

  `int pthread_cond_timewait(pthread_cond_t *cond, pthread_mutex_t *mutex, const timespec* abstime);`

  * cond 参数表示已初始化好的条件变量；mutex 参数表示与条件变量配合使用的互斥锁；abstime 参数表示阻塞线程的时间

  * **abstime：绝对时间（记录系统时间 + 等待时间）**

  调用两个函数之前，我们必须先创建好一个互斥锁并完成“加锁”操作，然后才能作为实参传递给 mutex 参数。两个函数会完成以下两项工作：

  - 阻塞线程，直至接收到“条件成立”的信号；
  - 当线程被添加到等待队列上时，将互斥锁“解锁”。


  也就是说，**函数尚未接收到“条件成立”的信号之前，它将一直阻塞线程执行。注意，当函数接收到“条件成立”的信号后，它并不会立即结束对线程的阻塞，而是先完成对互斥锁的“加锁”操作，然后才解除阻塞**。

  **两个函数的主要区别：**

  * pthread_cond_wait() 函数可以**永久阻塞线程**，直到条件变量成立的那一刻；
  * pthread_cond_timedwait() 函数**只能在 abstime 参数指定的时间内阻塞线程**，超出时限后，该函数将重新对互斥锁执行“加锁”操作，并解除对线程的阻塞，函数的返回值为 ETIMEDOUT。

  如果**函数成功接收到了“条件成立”的信号，重新对互斥锁完成了“加锁”并使线程继续执行**，函数返回数字 0，反之则返回非零数

* 解除阻塞状态

  `int pthread_cond_signal(pthread_cond_t *cond);`

  `int pthread_cond_broadcast(pthread_cond_t *cond);`

  cond 参数表示初始化好的条件变量。当函数成功解除线程的“被阻塞”状态时，返回数字 0，反之返回非零数

  **两个函数的主要区别：**

  - pthread_cond_signal() 函数**至少解除一个**线程的“被阻塞”状态，如果等待队列中包含多个线程，**优先解除哪个线程将由操作系统的线程调度程序决定**；
  - pthread_cond_broadcast() 函数可以解除等待队列中**所有**线程的“被阻塞”状态。

  **由于互斥锁的存在，解除阻塞后的线程也不一定能立即执行。当互斥锁处于“加锁”状态时，解除阻塞状态的所有线程会组成等待互斥锁资源的队列，等待互斥锁“解锁”。**

* 销毁条件变量

  对于初始化好的条件变量，可以使用`pthread_cond_destroy()`销毁

  * 语法：

    `int pthread_cond_destroy(pthread_cond_t *cond);`

    cond 参数表示要销毁的条件变量。如果函数成功销毁 cond 参数指定的条件变量，返回数字 0，反之返回非零数。

    值得一提的是，销毁后的条件变量还可以调用 pthread_cond_init() 函数重新初始化后使用



*代码测试：*

```C++
#include<stdio.h>
#include<unistd.h>
#include<pthread.h>

int x = 0;
pthread_mutex_t myMutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t myCond = PTHREAD_COND_INITIALIZER;

// wait
void* waitForTrue(void* arg){
	int res;
	res = pthread_mutex_lock(&myMutex);
	if(res!=0){
		printf("waitForTrue lock failed!\n");
		return NULL;
	}
	
	printf("--------------wait for x --> 10---------------------\n");
	if(pthread_cond_wait(&myCond,&myMutex)==0){
		printf("x = %d\n",x);
	}
	
	pthread_mutex_unlock(&myMutex);
	return NULL;
}

// done
void* doneForTrue(void* arg){
	int res;
	while(x!=10){
		res = pthread_mutex_lock(&myMutex);
		if(res == 0){
			x++;
			printf("doneForTrue x = %d\n",x);
			sleep(1);
			pthread_mutex_unlock(&myMutex);
		}
	}
	
	res = pthread_cond_signal(&myCond);
	if(res!=0){
		printf("pthread_cond_sign failed!\n");
	}
	return NULL;
}


int main(){
	pthread_t t1,t2;
	int res = pthread_create(&t1,NULL,waitForTrue,NULL);
	if(res!=0){
		printf("Thread 1 create failed!\n");
		return 0; 
	}
	
	res = pthread_create(&t2,NULL,doneForTrue,NULL);
	if(res!=0){
		printf("Thread 2 create failed!\n");
		return 0;
	}
	
	res = pthread_join(t1,NULL);
	if(res!=0){
		printf("Thread 1 join failed!\n");
		return 0;
	}
	res = pthread_join(t2,NULL);
	if(res!=0){
		printf("Thread 2 join failed!\n");
		return 0;
	}
	
	pthread_cond_destroy(&myCond);
	return 0;
}
```

*代码运行结果：*

```
-------wait for x --> 10--------
doneForTrue x = 1
doneForTrue x = 2
doneForTrue x = 3
doneForTrue x = 4
doneForTrue x = 5
doneForTrue x = 6
doneForTrue x = 7
doneForTrue x = 8
doneForTrue x = 9
doneForTrue x = 10
x = 10
```

---

## 读写锁解决

* 读写锁的核心思想是：将线程访问共享数据时发出的请求分为两种，分别是：
  * 读请求：只读取共享数据，不做任何修改；
  * 写请求：存在修改共享数据的行为

| 当前读写锁的状态 | 线程发出“读”请求 | 线程发出“写”请求 |
| ---------------- | ---------------- | ---------------- |
| 无锁             | 允许占用         | 允许占用         |
| 读锁             | 允许占用         | 阻塞线程执行     |
| 写锁             | 阻塞线程执行     | 阻塞线程执行     |

* 定义：

  `pthread_rwlock_t myLock;`

* 初始化：

  * `pthread_rwlock_t myLock = PTHREAD_RWLOCK_INITIALIZER;`
  * `int pthread_rwlock_init(pthread_rwlock_t *myLock, const pthread_rwlockattr_t *attr);`

  rwlock 参数用于指定要初始化的读写锁变量；attr 参数用于自定义读写锁变量的属性，置为 NULL 时表示以默认属性初始化读写锁

  当 pthread_rwlock_init() 函数初始化成功时，返回数字 0，反之返回非零数

* **读锁请求**：

  * `int pthread_rwlock_rdlock(pthread_rwlock_t *myLock);`
  * `int pthread_rwlock_tryrdlock(pthread_rwlock_t *myLock);`

  当读写锁处于“无锁”或者“读锁”状态时，以上两个函数都能成功获得读锁；当读写锁处于“写锁”状态时：

  - pthread_rwlock_rdlock() 函数会阻塞当前线程，直至读写锁被释放；
  - pthread_rwlock_tryrdlock() 函数不会阻塞当前线程，**直接返回 EBUSY**。

  以上两个函数如果能成功获得读锁，函数返回数字 0，反之返回非零数

* **写锁操作**：

  * `int pthread_rwlock_wrlock(pthread_rwlock_t *myLock);`
  * `int pthread_rwlock_trywrlock(pthread_rwlock_t *myLock);`

  当读写锁处于“无锁”状态时，两个函数都能成功获得写锁；当读写锁处于“读锁”或“写锁”状态时：

  - pthread_rwlock_wrlock() 函数将阻塞线程，直至读写锁被释放；
  - pthread_rwlock_trywrlock() 函数不会阻塞线程，**直接返回 EBUSY**。

  以上两个函数如果能成功获得写锁，函数返回数字 0，反之返回非零数

* 释放读写锁

  `int pthread_rwlock_destroy(pthread_rwlock_t *myLock);`

  如果函数成功销毁指定的读写锁，返回数字 0，反之则返回非零数



*代码测试：*

```C++
#include<stdio.h>
#include<pthread.h>
#include<unistd.h>

int x = 0;
pthread_rwlock_t myLock = PTHREAD_RWLOCK_INITIALIZER;

// read
void* read_thread(void* arg){
	printf("-----This is read thread: %u\n",pthread_self());
	while(1){
		sleep(1);
		pthread_rwlock_rdlock(&myLock);
		printf("Thread %u is reading...   x = %d\n",pthread_self(),x);
		sleep(1);
		pthread_rwlock_unlock(&myLock);
	}

	return NULL;
}

// write
void* write_thread(void* arg){
	printf("--------This is write thread: %u\n",pthread_self());
	while(1){
		sleep(1);
		pthread_rwlock_wrlock(&myLock);
		++x;
		printf("Thread %u is writing...   x = %d\n",pthread_self(),x);
		sleep(1);
		pthread_rwlock_unlock(&myLock);
	}

	return NULL;
}

int main(){
	pthread_t r[5],w;
	int res;
	for(int i=0;i<5;i++){
		res = pthread_create(&r[i],NULL,read_thread,NULL);
		if(res!=0){
			printf("Read thread: %d create failed!\n",i);
			return 0;
		}
	}

	res = pthread_create(&w,NULL,write_thread,NULL);
	if(res!=0){
		printf("Write thread create failed!\n");
		return 0;
	}

	sleep(5);
	for(int i=0;i<5;i++){
		res = pthread_join(r[i],NULL);
		if(res!=0){
			printf("Read thread %d join failed!\n",i);
			return 0;
		}
	}

	res = pthread_join(w,NULL);
	if(res!=0){
		printf("Write thread join failed!\n");
		return 0;
	}

	res = pthread_rwlock_destroy(&myLock);
	if(res == 0){
		printf("MyLock destroyed over!\n");	
	}
	return 0;
}

```

*代码运行结果：*

```
-----This is read thread: 903649024
-----This is read thread: 895256320
--------This is write thread: 861685504
-----This is read thread: 886863616
-----This is read thread: 878470912
-----This is read thread: 870078208
Thread 903649024 is reading...   x = 0
Thread 895256320 is reading...   x = 0
Thread 886863616 is reading...   x = 0
Thread 878470912 is reading...   x = 0
Thread 870078208 is reading...   x = 0
Thread 861685504 is writing...   x = 1
Thread 870078208 is reading...   x = 1
Thread 878470912 is reading...   x = 1
Thread 886863616 is reading...   x = 1
Thread 903649024 is reading...   x = 1
Thread 895256320 is reading...   x = 1
Thread 861685504 is writing...   x = 2
Thread 870078208 is reading...   x = 2
Thread 903649024 is reading...   x = 2
Thread 895256320 is reading...   x = 2
Thread 886863616 is reading...   x = 2
Thread 878470912 is reading...   x = 2
Thread 861685504 is writing...   x = 3
Thread 886863616 is reading...   x = 3
Thread 878470912 is reading...   x = 3
Thread 895256320 is reading...   x = 3
Thread 870078208 is reading...   x = 3
Thread 903649024 is reading...   x = 3
Thread 861685504 is writing...   x = 4
Thread 903649024 is reading...   x = 4
Thread 870078208 is reading...   x = 4
Thread 895256320 is reading...   x = 4
Thread 878470912 is reading...   x = 4
Thread 886863616 is reading...   x = 4
Thread 861685504 is writing...   x = 5
Thread 878470912 is reading...   x = 5
Thread 886863616 is reading...   x = 5
// 下面通过 CTRL + C 停止运行
```

---

## 避免死锁

* 使用互斥锁、信号量、条件变量和读写锁实现线程同步时，要注意以下几点：
  * 占用**互斥锁**的线程，执行完成前必须及时**解锁**；
  * 通过 **sem_wait()** 函数占用信号量资源的线程，执行完成前必须调用 **sem_post()** 函数及时释放；
  * 当线程因**pthread_cond_wait()** 函数被阻塞时，一定要保证有其它线程**唤醒此线程**；
  * 无论线程占用的是**读锁还是写锁**，都必须及时**解锁**。

> 注意，函数中可以设置多种结束执行的路径，但无论线程选择哪个路径结束执行，都要保证能够将占用的资源释放掉。

* POSIX 标准中，很多阻塞线程执行的函数都提供有 tryxxx() 和 timexxx() 两个版本，例如 pthread_mutex_lock() 和 pthread_mutex_trylock()、sem_wait() 和 sem_trywait()、pthread_cond_wait() 和 pthread_cond_timedwait() 等，它们可以完成同样的功能，但 tryxxx() 版本的函数不会阻塞线程，timexxx() 版本的函数不会一直阻塞线程。

  实际开发中，建议您**优先选择 tryxxx() 或者 timexxx() 版本的函数，可以大大降低线程产生死锁的概率**。

* 多线程程序中，**多个线程请求资源的顺序最好保持一致**。线程 t1 先请求 mutex 锁然后再请求 mutex2 锁，而 t2 则是先请求 mutex2 锁然后再请求 mutex 锁，这就是典型的因“请求资源顺序不一致”导致发生了线程死锁的情况。

## 设置线程属性

* 定义属性变量：

  `#inlcude<pthread.h>`

  `pthread_attr_t myAttr;`

* 初始化语法：

  `int pthread_attr_init(pthread_attr_t *myAttr);`

  成功返回 0 ，否则返回非零数

* 常用属性

  * **__detachstate**

    `int pthread_attr_setdetachstate(pthread_attr_t *myAttr, int detachstate);` 获取线程的分离属性

    `int pthread_attr_getdetachstate(const pthread_attr_t *myAttr, int *detachstate);` 设置线程的分离属性

    成功返回 0 ，否则返回非零数

    **detachstate**有以下两个值：

    * PTHREAD_CREATE_JOINABLE：线程执行完不会自动释放资源
    * PTHREAD_CREATE_DETACHED：线程执行完会自动释放资源，后续不支持`pthread_join()`

  * `int pthread_detach(pthread_t thread);` 分离线程

  * **__schedpolicy**

    指定线程的调度算法：

    * SCHED_OTHER：（默认）分时调度（不支持设置优先级）
    * SCHED_FIFO：先到先得（支持）
    * SCHED_RR：轮转（支持）

    `int pthread_attr_setschedpolicy(pthread_attr_t *myAttr, int policy);`

    `int pthread_attr_getschedpolicy(const pthread_attr_t *myAttr, int *policy);`

    成功返回 0 ，否则返回非零数

  * **__schedparam**

    设置线程的优先级

    `int pthread_attr_setschedparam(pthread_attr_t *myAttr, const struct sched_param *p);`

    `int pthread_attr_getschedparam(const pthread_attr_t *myAttr, struct sched_param *p)`

    成功返回 0 ，否则返回非零数

    * `param`：`sched_param`结构体变量，在头文件`sched.h`中，内部有一个`sched_priority`变量，表示线程优先级

    * 当需要修改线程的优先级时，我们只需创建一个 sched_param 类型的变量并为其内部的 sched_priority 成员赋值，然后将其传递给 pthrerd_attr_setschedparam() 函数

    * 不同的操作系统，线程优先级的值的范围不同，您可以通过调用如下两个系统函数获得当前系统支持的**最大和最小优先级的值**：

      ```
      int sched_get_priority_max(int policy);   //获得最大优先级的值
      int sched_get_priority_min(int policy);   //获得最小优先级的值
      ```

      其中，policy 的值可以为 SCHED_FIFO、SCHED_RR 或者 SCHED_OTHER，当 policy 的值为 SCHED_OTHER 时，最大和最小优先级的值都为 0

  * **__inheritsched**

    `<pthread.h>` 头文件提供了如下两个函数，分别用于获取和修改 `__inheritsched `属性的值：

    ```
    //获取 __inheritsched 属性的值
    int pthread_attr_getinheritsched(const pthread_attr_t *attr,int *inheritsched);
    //修改 __inheritsched 属性的值
    int pthread_attr_setinheritsched(pthread_attr_t *attr,int inheritsched);
    ```

    其中在 `pthread_attr_setinheritsched()` 函数中，`inheritsched` 参数的可选值有两个，分别是：

    - PTHREAD_INHERIT_SCHED（默认值）：新线程的调度属性**继承自父线程**；
    - PTHREAD_EXPLICIT_SCHED：新线程的调度属性**继承自 myAttr 规定的值**

    成功返回 0 ，否则返回非零数

  * **__scope**

    `<pthread.h>` 头文件中提供了如下两个函数，分别用于获取和修改 __scope 属性的值：

    ```
    //获取 __scope 属性的值
    int pthread_attr_getscope(const pthread_attr_t * attr,int * scope);
    //修改 __scope 属性的值
    int pthread_attr_setscope(pthread_attr_t * attr,int * scope);
    ```

    当调用 `pthread_attr_setscope()` 函数时，`scope` 参数的可选值有两个，分别是：

    - PTHREAD_SCOPE_PROCESS：同一进程内争夺 CPU 资源；
    - PTHREAD_SCOPE_SYSTEM：系统所有线程之间争夺 CPU 资源。

    > Linux系统仅支持 PTHREAD_SCOPE_SYSTEM，即所有线程之间争夺 CPU 资源。

    成功返回 0 ，否则返回非零数

  * **__guardsize**

    每个线程中，栈内存的后面都紧挨着一块空闲的内存空间，我们通常称这块内存为**警戒缓冲区**，它的功能是：**一旦我们使用的栈空间超出了额定值，警戒缓冲区可以确保线程不会因“栈溢出”立刻执行崩溃**。

    `__guardsize` 属性专门用来设置警戒缓冲区的大小，`<pthread.h>` 头文件中提供了如下两个函数，分别用于获取和修改 __guardsize 属性的值：

    ```
    int pthread_attr_getguardsize(const pthread_attr_t *restrict attr,size_t *restrict guardsize);
    int pthread_attr_setguardsize(pthread_attr_t *attr ,size_t *guardsize);
    ```

    pthread_attr_setguardsize() 函数中，设置警戒缓冲区的大小为参数 guardsize 指定的字节数

    成功返回 0 ，否则返回非零数

*代码示例：*

```C++
#include<stdio.h>
//#include<stdlib.h>
#include<pthread.h>
#include<unistd.h>

// thread_1
void* Thread_1(void* arg){
	printf("Thread_1 is begining...\n");
	printf("I'm zjp.\n");
	printf("Thread_1 over!\n");
	return NULL;
} 

// thread_2 
void* Thread_2(void* arg){
	printf("Thread_2 is beging...\n");
	printf("I'm what I am.\n");
	printf("Thread_2 over!\n");
	return NULL;
}

int main(int argc,char *argv[]){
	int num_1,num_2,res;
	pthread_t t1,t2;
    // 创建优先级参数两个变量
	struct sched_param p1,p2;
    // 创建属性两个变量
	pthread_attr_t myAttr_1,myAttr_2;
	
    // 判断传入的参数是否满足
	if(argc!=3){
		printf("未向程序传入2个表示优先级的数字\n");
		return 0;
	}
	
    // 初始化属性变量
	res = pthread_attr_init(&myAttr_1);
	if(res!=0){
		printf("Init myAttr_1 failed!\n");
	}
	res = pthread_attr_init(&myAttr_2);
	if(res!=0){
		printf("Init myAttr_2 failed!\n");
	}
	
    // 设置属性变量 1 的分离特性
	res = pthread_attr_setdetachstate(&myAttr_1,PTHREAD_CREATE_DETACHED);
	if(res!=0){
		printf("MyAttr_1 set detachstate failed!\n");
	}
	
    // 设置属性变量 1 的线程争夺属性
	res = pthread_attr_setscope(&myAttr_1,PTHREAD_SCOPE_SYSTEM);
	if(res!=0){
		printf("MyAttr_2 set scope failed!\n");
	}
	// 设置属性变量 2 的线程调度算法属性
	res = pthread_attr_setschedpolicy(&myAttr_2,SCHED_FIFO);
	if(res!=0){
		printf("MyAttr_2 set policy failed!\n");
	}
	
    // 设置属性变量 1 的线程继承关系
	res = pthread_attr_setinheritsched(&myAttr_1,PTHREAD_EXPLICIT_SCHED);
	if(res!=0){
		printf("MyAttr_1 set_inheritsched failed!\n");
	}
	// 设置属性变量 2 的线程继承关系
	res = pthread_attr_setinheritsched(&myAttr_2,PTHREAD_EXPLICIT_SCHED);
	if(res!=0){
		printf("MyAttr_2 set_inheritsched failed!\n");
	}
	
    // 转化传入的参数
	num_1 = atoi(argv[1]);
	num_2 = atoi(argv[2]);
	// 赋值于优先级变量中的 sched_priority变量
	p1.sched_priority = num_1;
	p2.sched_priority = num_2;
	
    // 设置传入属性的优先级
	res = pthread_attr_setschedparam(&myAttr_1,&p1);
	if(res!=0){
		printf("param_1 setschedparam failed!\n");
	}
	res = pthread_attr_setschedparam(&myAttr_2,&p2);
	if(res!=0){
		printf("param_2 setschedparam failed!\n");
	}
	
    // 创建线程
	res = pthread_create(&t1,&myAttr_1,Thread_1,NULL);
	if(res!=0){
		printf("Thread_1 create failed!\n");
	}
	res = pthread_create(&t2,&myAttr_2,Thread_2,NULL);
	if(res!=0){
		printf("Thread_2 create failed!\n");
	}
	
    // 等待阻塞线程
	sleep(5);
	res = pthread_join(t1,NULL);
	if(res!=0){
		printf("Thread_1 join failed!\n");
	}
	res = pthread_join(t2,NULL);
	if(res!=0){
		printf("Thread_2 join failed!\n");
	}
	
	printf("main over!\n");
	return 0;
}	
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

**以上两个函数选其一使用在多线程上，不然的话程序会产生问题：**

* 子线程比主线程先结束
* 线程执行完毕资源未释放，产生内存泄漏

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

`<thread>`头文件中不仅定义了 thread 类，还提供了一个名为 this_thread 的命名空间，此空间中包含一些功能实用的函数

| 函数          | 功 能                                     |
| ------------- | ----------------------------------------- |
| get_id()      | 获得当前线程的 ID。                       |
| yield()       | 阻塞当前线程，直至条件成熟。              |
| sleep_until() | 阻塞当前线程，直至某个时间点为止。        |
| sleep_for()   | 阻塞当前线程指定的时间（例如阻塞 5 秒）。 |

*代码测试*

```C++
#include<iostream>
#include<mutex>	// std::mutex mt;
#include<chrono> // std::chrono::seconds(2)
#include<thread>
using namespace std;

std::mutex mt;
int x = 0;

void thread_1(){
	while(x<10){
		mt.lock();
		++x;
		cout<<"ID = "<<std::this_thread::get_id()<<" "<<"x = "<<x<<endl;
		mt.unlock();
		std::this_thread::sleep_for(std::chrono::seconds(2)); // sleep_for()
	}
}

int main(){
	thread t1(thread_1);
	thread t2(thread_1);

	t1.join();
	t2.join();
	return 0;
}

```

---

## 互斥实现线程同步

```C++
#include<iostream>
#include<thread>
#include<mutex>
#include<chrono> 
using namespace std;

int x = 0;
std::mutex mt;

void thread_1(){
	while(x<10){
		mt.lock();
		++x;
		cout<<"Thread ID: "<<std::this_thread::get_id()<<" "<<"x = "<<x<<endl;
		mt.unlock();
		std::this_thread::sleep_for(std::chrono::seconds(2));
	}
}

int main(){
	thread t1(thread_1);
	thread t2(thread_1);
	
	t1.join();
	t2.join();
	return 0;
}
```

*代码运行结果：*

```
ID = 140226457417472 x = 1
ID = 140226465810176 x = 2
ID = 140226457417472 x = 3
ID = 140226465810176 x = 4
ID = 140226457417472 x = 5
ID = 140226465810176 x = 6
ID = 140226457417472 x = 7
ID = 140226465810176 x = 8
ID = 140226457417472 x = 9
ID = 140226465810176 x = 10
```

----

## 条件变量

在头文件`<condition_variable>`中：需要与互斥锁搭配使用

* `condition_variable`：示的条件变量只能和 **unique_lock** 类表示的互斥锁（可自行加锁和解锁）搭配使用
* `condition_variable_any`：表示的条件变量可以和**任意类型的互斥锁**搭配使用（例如递归互斥锁、定时互斥锁等）

**condition_variable**:

| 成员函数     | 功 能                                                        |
| ------------ | ------------------------------------------------------------ |
| wait()       | 阻塞当前线程，等待条件成立。                                 |
| wait_for()   | 阻塞当前线程的过程中，该函数**会自动调用 unlock() 函数解锁互斥锁**，从而令其他线程使用公共资源。**当条件成立或者超过了指定的等待时间（比如 3 秒），该函数会自动调用 lock() 函数对互斥锁加锁，同时令线程继续执行。** |
| wait_until() | 和 wait_for() 功能类似，不同之处在于，wait_until() 函数可以设定一个具体时间点（例如 2021年4月8日 的某个具体时间），当条件成立或者等待时间超过了指定的时间点，函数会自动对互斥锁加锁，同时线程继续执行。 |
| notify_one() | 向其中一个正在等待的线程发送“条件成立”的信号。               |
| notify_all() | 向**所有等待**的线程发送“条件成立”的信号。                   |

*代码：*

```C++
#include<iostream>
#include<thread>
#include<condition_variable>
#include<chrono>

std::mutex mt;
std::condition_variable_any cond;

void print_id(){
	mt.lock();
	cond.wait(mt);
	std::cout<<"Thread ID: "<<std::this_thread::get_id()<<std::endl;
	// wait
	std::this_thread::sleep_for(std::chrono::seconds(2));
	mt.unlock();
}

void go(){
	std::cout<<"go running......\n";
	std::this_thread::sleep_for(std::chrono::seconds(2));
    // notify all waiting threads
	cond.notify_all();
}

int main(){
	std::thread t[4];
	for(int i=0;i<4;i++){
		t[i] = std::thread(print_id);
	}

	std::thread goThread(go);
	goThread.join();

	for(auto& th: t){
		th.join();
	}
	return 0;
}

```

*代码运行结果：*

```
go running......
Thread ID: 140588095059712
Thread ID: 140588086667008
Thread ID: 140588078274304
Thread ID: 140588103452416
```

---

