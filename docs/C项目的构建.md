# C项目的构建

## C程序编译链接过程
以下为C程序hello.c为例：<br>
![hello.c](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/C_progranming.drawio.png)
<br>

## gcc
gcc编译文件<br>

```
gcc -E [file_name].c -o [filename].i	预编译：宏展开
gcc -S [file_name].i -o [file_name].s	编译：生成汇编文件
gcc -c [file_name].s -o [file_name].o	汇编：汇编生成二进制文件
gcc [file_name].o -o [file_name]	链接：二进制生成可执行文件

gcc [file_name].c			生成默认的可执行文件：a.out


gcc -Wall [filename].c			显示所有警告信息
gcc -Wall -Werror [filename].c		将警告信息当成错误信息处理
```

gcc的其他用法：<br>

```
处理宏：
gcc [filename].c -DEBUG			在DEBUG版本下编译（DEBUG为文件中的宏定义）


静态链接：
gcc -static [file_name].c -o [static_file]	生成静态的可执行文件



制作静态库：
gcc -c [file_name].c -o [file_name].o	先生成.o文件
ar -rcs [lib_name].a *.o		打包生成的.o文件

-r					更新文件
-c					创建文件
-s					建立索引




静态库的使用：
gcc [file_name].c -I./[file_name].h -L./[lib_name] -l[file_name]（去掉前缀和后缀）	生成a.out文件

-I:					指定头文件的路径
-L:					指定静态库文件的路径
-l:					静态库的文件名



动态库的制作：
gcc -fpic -c [file_name].c		生成与地址位置无关的目标文件（pic：position in independence）
gcc -shared [all_file_name].o -o [lib_dynamicLibName].so	生成动态库

```

## 项目搭建

一般由makefile文件管理和编译项目的文件

以下是一段makefile的项目搭建例子：

```makefile
.PHONY: clean # 伪目标

# 自定义环境变量
CC = gcc # 指定编译器

CFLAGS = -I include # 指定头文件目录
CFILES = $(shell find src -name "*.c") # 搜索所有的源文件
OBJS = $(CFILES:.c=.o) # 所有的目标文件(.o)
TARGET = main # 最终生成目标
DATA = src/data/*.txt # 搜索所有的数据文件(.txt)

RM = -rm -f # 删除方式

all: $(TARGET)
	git commit -a -m "> make"

# 项目构建方式
$(TARGET): $(OBJS)
	$(CC) -o $(TARGET) $(OBJS)

%o : %c
	$(CC) -c $(CFLAGS) $< -o $@

clean:
	$(RM) $(TARGET) $(OBJS) $(DATA)
	git commit -a -m "> make clean"
```

*约定了所有的头文件放在include文件夹里，所有的源文件放在src文件夹里，所有项目构建过程中生成的的目标文件放在对应源文件的统一目录下*

## 模块

模块：由一个头文件和**一个或者多个**源文件组成
<br>

```cpp title="hello.h"
void hello();
```

<br>

```cpp title="hello.c"
#include "hello.h"
#include <stdio.h>

void hello() {
    printf("hello!\n");
}
```

以上就是**一个模块**

可以在其他模块中通过**包含头文件**的方式使用这个模块


```cpp title="main.c"
#include "hello.h"

int main() {
    hello();
    return 0;
}
```

以上可以通过如下gcc的命令编译执行：


```
gcc -c hello.c -o hello.o
gcc -c main.c -o main.o
gcc hello.o main.o -o main

./main
```

输出：

```
hello!

```

