---
title: "C++11_多线程"
date: 2021-10-07T22:26:08+08:00
draft: true
---

# C++线程

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

