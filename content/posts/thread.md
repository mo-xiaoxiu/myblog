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

