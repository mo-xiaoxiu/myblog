# CMake

使用环境：

Centos Linux 8

## 编译程序

使用clang进行编译

首先来看一个简单的程序：

```cpp title="hello.cpp"
#include <iostream>
#include "func.h"

int main() {
    int arr[] = {1, 2, 3, 4};
    print_array(arr, sizeof(arr)/sizeof(int)); //打印整型数组内容
    
    return 0;
}
```

```cpp title="func.h"
#ifndef __FUNC__
#define __FUNC__

void print_array(int *arr, int size);

#endif
```

```cpp title="func.cpp"
#include <iostream>

void print_array(int *arr, int size) {
    if(!arr) return;
    
    int i = 0;
    for(; i < size; i++) {
        std::cout<<arr[i]<<"";
    }
    std::endl;
}
```

在终端使用clang编译上述程序，可以使用如下命令：

```
clang++ hello.cpp func.cpp -std=c++17 -DHELLO_WORLD=2
```

生成`a.out`文件，执行该文件：

```
./a.out
```

可以得到如下结果：

```
1 2 3 4
```



## Cmake编译文件

编译上述文件可以在本文件夹中写一个`CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.10)
project(my_test)

set(CMAKE_VERBOSE_MAKEFILE ON)

add_definitions(-DHELLO_WORLD=2)

set(CMAKE_C_FLAGS "-std=c11")
set(CMAKE_CXX_FLAGS "-std=c++17")

include_directories("../") #这里将编译依赖的头文件放到了当前目录的上一级目录

## link_directories("library_dir") #这里编译不需要包含库文件

set(SRC_FILES hello.cpp func.cpp)
set(PROJECT_SOURCES ${SRC_FILE})

add_executable(${PROJECT_NAME} ${PROJECT_SOURCES})

##target_link_libraries(
##	${PROJECT_NAME} PRIVATE pthread
##) #这里由于编译时不需要依赖一些库
```

### 解释

* `cmake_minimum_required(VERSION 3.10)`表示cmake最小支持版本为3.10
* `project(my_test)`表示设置该项目最后生成的目标文件为`my_test`
* `set(CMAKE_VERBOSE_MAKEFILE ON)`表示开启设置显示项目构建过程
* `set(CMAKE_C_FLAGS "-std=c11")`表示设置C语言的版本为c11
* `set(CMAKE_CXX_FLAGS "-std=c++17")`表示设置C++版本为c++17
* `include_directories("../")`表示编译该目标文件的头文件在上一级目录
* `link_directories("library_dir")`表示编译该目标文件的库文件在`library_dir`这个目录下（像终端编译的`-Lxxx(xxx表示库文件所在目录)`）
* `set(SRC_FILES hello.cpp func.cpp)`表示设置源文件包含`hello.cpp`和`func.cpp`
* `set(PROJECT_SOURCES ${SRC_FILES})`表示设置项目源文件为上述源文件
* `add_executable(${PROJECT_NAME} ${PROJECT_SOURCES})`表示由项目源文件生成可执行目标文件
* `target_link_libraries(${PROJECT_NAME} PRIVATE pthread)`表示链接生成目标文件的库文件名字（像终端编译的`-lxxx(xxx表示库文件名)`）

### 编译执行

项目中，一般需要新建一个`build`目录由于构建cmake项目：

```
mkdir build
cd build/
cmake ../
make
```

上述执行完毕，会在`build`目录下生成文件如下：

```
CMakeCache.txt  CMakeFiles  cmake_install.cmake  Makefile  my_test
```

```
./my_test
```

执行结果输出终端为：

```
1 2 3 4
```





---

