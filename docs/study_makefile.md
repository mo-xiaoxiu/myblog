---
title: "Study_makefile"
date: 2021-09-23T16:06:33+08:00
draft: true
---

# makefile

## makefile 规则

```
target...:prerequisites...
	command
	...
	...
```

* target：目标文件。也可以是执行文件
* prerequisites：生成target所需要的文件
* command：make需要执行的命令

## 示例

假设现在有一个工程，包含3个头文件和8个C文件

```makefile
edit:main.o kbd.o command.o display.o \
	insert.o search.o files.o utils.o
	cc -o edit main.o kbd.o command.o display.o \
			insert.o search.o files.o utils.o
			
# 如果prerequisites和command在同一行，则prerequisites之后可以用‘；’与command分隔开			

main.o:main.c defs.h
	cc -c main.c
kbd.o:kbd.c defs.h command.h
	cc -c kbd.c
command.o:command.c defs.h command.h
	cc -c command.c
display.o:display.c defs.h buffer.h
	cc -c display.c
insert.o:insert.c defs.h buffer.h
	cc -c insert.c
search.o:search.c defs.h buffer.h
	cc -c search.c
fiies.o:files.c defs.h buffer.h command.h
	cc -c files.c
utils.o:utils.c defs.h
	cc -c utils.c
clean:
	rm edit main.o kbd.o command.o display.o \
		insert.o search.o files.o utils.o
		
```

*可以将此内容保存为“Makefile”或“makefile”文件中，然后再该目录下直接输入命令“make”就可以生成执行文件edit。*

*删除执行文件课所有中间目标文件，只需执行“make clean”就可以了*

---

## makefile中使用变量&make自动推导

```makefile
objects=main.o kbd.o command.o display.o \
		insert.o search.o files.o utils.o
		
# 用变量替换
edit:$(objects)
	cc -o edit $(objects)

# 自动推导出所需要的头文件和执行命令
main.o:defs.h
kbd.o:defs.h command.h
command.o:defs.h command.h
display.o:defs.h buffer.h
insert.o:defs.h buffer.h
search.o:defe.h buffer.h
files.o:defs.h buffer.h command.h
utils.o:defs.h

# ".PHONY"是一个伪标签
.PHONY:clean
clean:
	rm edit $(objects)
	
```

---

## 清空目标文件

*一般风格：*

```makefile
clean:
	rm edit $(objects)
```

*更为稳健的做法：*

```makefile
.PHONY:clean
clean:
	-rm edit $(objects)	# 再前面加上‘-’：也许某些文件出现问题，但不要管他，继续做后面的事
	
# clean不要放在文件开头
```

## 引用其他makefile

```makefile
  include<filename>		# include前面可以有多个空格，但不要是Tab
  # filename 可以是当前操作系统shell文件模式
```

*假设有这样几个makefile：a.mk、b.ma、c.mk，还有一个文件foo.make，以及一个变量$((bar)，其包含了e.mk和f.mk*：

```makefile
  include foo.make *.mk $(nar)
```

*等价于：*

```makefile
  include foo.make a.mk b.mk c.mk e.mk f.mk
```

此操作像C、C++的#include操作一样，相当于宏展开。make会在当前目录下找这些文件，如果没找到：

1. make执行时，有”-I“或”--include-dir“参数，那么make就会在这个参数所指定的目录下去寻找
2. 如果目录`<prefix>/include`（一般是：/usr/local/bin或/usr/include）存在的话，make也会去寻找

如果有文件没找到的话，make会生成一条警告信息，但不会马上出现致命错误，它会在继续寻找其他文件。如果还是没找到，就会出现致命信息

```makefile
  -include <filename>
```

*表示：无论include过程中出现什么错误，都不要报错继续执行*

---

## 在规则中使用通配符

make支持三个通配符：

” * ”、“ ？”、“ [ ... ] ”

*注意：“~”：”~test“表示当前$HOME目录下test目录*

**例子1：**

```makefile
clean:
	rm -f  *.o
```

删除所有的.o文件

**例子2：**

```makefile
print: *.c
	lpr -p $?
	touch print
```

目标print依赖于所有的.c文件；$?是一个**自动化变量**

**例子3：**

```makefile
object = *.o #makefile中的变量就是C/C++中的宏，所以这里表示的是文件名 *.o
```

```makefile
object := $(wildcard *.o) #关键字wildcard，这里才是表示以变量object代表所有的.o文件
```

## 文件搜寻

当make需要去找寻文件的依赖关系时，你可以在文件前加上路径，但最好的方法是把一个路径告诉make，让make在自动去找

Makefile文件中的特殊变量“VPATH”就是完成这个功能的，如果没有指明这个变量，make只会在当前的目录中去找寻依赖文件和目标文件。如果定义了这个变量，那么，make就会在当当前目录找不到的情况下，到所指定的目录中去找寻文件了

```makefile
VPATH = src:../headers
# 指定了两个目录”src“和”../header“，make会按照这个顺序搜索。注意：当前目录还是搜索的最高优先级
```

**vpath（全小写）关键字**

1、vpath <pattern> <directories>

为符合模式<pattern>的文件指定搜索目录<directories>

2、vpath <pattern>

清除符合模式<pattern>的文件的搜索目录

3、vpath

清除所有已被设置好了的文件搜索目录。

*<pattern>中需包含”%“，”%“表示匹配**一个或者多个**字符*

```makefile
# 要求make在“../headers”目录下搜索所有以“.h”结尾的文件。（如果某文件在当前目录没有找到的话）
vpath %.h ../headers
```

```makefile
# 表示“.c”结尾的文件，先在“foo”目录，然后是“blish”，最后是“bar”目录
vpath %.c foo
vpath % blish
vpath %.c bar
```

```makefile
# 表示“.c”结尾的文件，先在“foo”目录，然后是“bar”目录，最后才是“blish”目录
vpath %.c foo:bar
vpath % blish
```

---