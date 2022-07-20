# GDB

为了学会使用GDB调试程序，我写了一个小小的测试代码工程。

- 功能：打印数组（vector）
- cmake（CMakerLists.txt）

我创建了一些目录，分别用于存放不同的文件：

- include：头文件
- src：源文件
- build：cmake构建项目

在头文件printarr.h中，定义一个打印数组的类：

```cpp
#ifndef __PRINTARR__
#define __PRINTARR__
#pragma once
#include <vector>
#include <iostream>

//print array
template<typename T>
class PrintArr{
public:
	PrintArr(std::vector<T>& vec): m_vec(vec) {};
	void print_add();
private:
	std::vector<T> m_vec;
};

void PrintArr<T>::print_arr() {
	for(auto v: this->m_vec) {
		std::cout<<"v = " <<v<<std::endl;
	}
	std::cout<<"print array OK."<<std::endl;
}

#endif
```

写一个测试程序test,cpp：

```cpp
#include <iostream>
#include "printarr.h"

void test() {
	std::vector<int> vec{1, 2, 3, 4};
	PrintArr<int> arr(vec);
	arr.print_add();
}

int main() {
	test();

	return 0;
}
```

将printarr.h放进include目录，将test.cpp放入src目录，在当前目录下写一个CMakeLists.txt：

```cmake
cmake_minimum_required(VERSION 3.10)
project(test_printarr)

set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FILES} -g -std=c++11")

include_directories("./include")
set(SRC_FILES "./src")

set(PROJECT_FILES "SRC_FILES/test.cpp")
add_executable(${PROJECT_NAME} ${PROJECT_FILES})
```



`更新中。。。`
