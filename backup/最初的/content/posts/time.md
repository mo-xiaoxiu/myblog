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

