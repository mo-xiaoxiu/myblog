---
title: "C/C++记录程序时间"
date: 2021-09-12T13:03:22+08:00
draft: true
---

# C/C++记录程序时间

对于C/C++程序，记录时间我们有几种常见的方式：

1. 使用C++的`<chrono>`头文件
2. 使用C的`<ctime>`头文件

本次说说使用C++11的`<chrono>`头文件如何记录程序时间

##  < chrono >

代码如下：

```C++
#include<iostream>
#include<chrono>

int main(){
    // start time
    auto start_time=std::chrono::steay_clock:;now();
    
    // Do something
    std::cout<<"Hello world!"<<std::endl;
    
    // end time
    auto end_time=std::chrono::steady_clock::now();
    
    // end time - start time
    std::chrono::duration<float>elapsed_seconds=end_time-start_time;
    
    // print elapsed seconds
    std::cout<<elapsed_seconds.count()<<std::endl;
    
    return 0;
}
```

* 记录开始时间：使用`std::chrono::steady_clock::now()`：

  调用`std`命名空间下的`chrono`，在`steady_clock`作用域之下的`now()`这个函数在执行程序代码之前记录时间

* 执行中间程序代码（最主要的运行时间）

* 记录程序结束时间：使用方法同“记录开始时间”

* 算出差值：创建一个`chrono`下的`duration<float>`类型的变量，表示用`float`类型存储秒数

* 调用上一步创建的记录时间差值的变量的函数`count()`输出差值，即程序执行所需秒数

---

**`duration`的第一个模板参数是表示用什么数据类型存储的秒数。**

**当转换类型时不损失精度时，不同数据类型的`duration`之间可以直接转换**

**当转换类型时损失精度时，需要使用`duration_cast()`进行类型转换**



## 使用RAII封装一个时间类

* 实验环境：Centos Linux 8
* RAII

1. 创建一个文件目录：

   ```
   mkdir runtime_RAII
   cd runtime_RAII
   ```

2. 写一个timer命名空间

   ```cpp title="timer.h"
   #pragma once
   #include <fstream>
   #include <iostream>
   #include <sys/time.h>
   #include <ctime>
   #include <string>
   #include <chrono>
   
   using llong = long long;
   using namespace std::chrono;
   using std::cout;
   using std::endl;
   
   namespace timer{
   class TimerLog{
   	public:
   		TimerLog(const std::string tag) { //构造函数记录开始时间：构造对象就开始计时
   			m_tag = tag;
   			m_begin = high_resolution_clock::now();
   		}
   
   		void reset(){ //重新计算时间
   			m_begin = high_resolution_clock::now();
   		}
   
   		llong elapsed(){ //计算差值
   			return static_cast<llong>(duration_cast<std::chrono::milliseconds>(high_resolution_clock::now() - m_begin).count());
   		}
   
   		~TimerLog(){ //析构函数打印对象生命周期
   			auto time = duration_cast<std::chrono::milliseconds>(high_resolution_clock::now() - m_begin).count(); //转换不失精度
   			std::cout<<"time {"<<m_tag<<"} "<<static_cast<double>(time)<<" ms"<<std::endl;
   		}
   	private:
   		std::string m_tag;
   		std::chrono::time_point<std::chrono::high_resolution_clock> m_begin;
   };
   } //namespace timer
   ```

3. 写一个测试程序：

   ```cpp title="test.cpp"
   #include "timer.h"
   #include <iostream>
   #include <thread> //std::this_thread::sleep_for()
   
   void test() {
   	auto func = [](){ //Lambda函数循环打印间隔时间
   		for(int i = 0; i < 5; i++) {
   			std::cout<<"i = "<<i<<std::endl;
   			std::this_thread::sleep_for(std::chrono::milliseconds(1));
   		}
   	};
   	{
   		timer::TimerLog t("func");
   		func();
   	}
   }
   
   int main () {
   	test();
   	return 0;
   }
   
   ```

4. 写一个cmake文件方便编译（也可以使用直接编译，这里为了熟练书写cmake）：

   ```cmake
   cmake_minimum_required(VERSION 3.10)
   project(test)
   
   set(CMAKE_VERBOSE_MAKEFILE ON)
   set(CMAKE_CXX_FLAGS "-std=c++11")
   
   set(SRC_FILES test.cpp)
   set(PROJECT_SOURCES ${SRC_FILES})
   
   add_executable(${PROJECT_NAME} ${PROJECT_SOURCES})
   ```

5. 创建一个build目录用于构建项目，并执行：

   ```
   mkdir build
   cd build
   cmake ../
   make
   ./test
   ```

6. 程序输出如下所示：

   ```
   i = 0
   i = 1
   i = 2
   i = 3
   i = 4
   time {func} 12 ms
   ```

---

