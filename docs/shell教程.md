# shell教程

## 初始sell

1. 编写一个shell脚本输出`hello world`

   ```shell title="helloworld.sh"
   #!/bin/bash
   
   echo "hello world!"
   ```

   在命令行窗口执行`bash helloworld.sh`或者`sh helloworld`，运行该脚本：

   输出`hello world!`

   还有一种执行方式，可以使用`./helloworld`，只不过需要给脚本加上可执行权限：

   ```
   chmod +x helloworld.sh
   ```

   或者是：

   ```
   chmod 777 helloworld.sh
   ```

   再在窗口执行`./helloworld.sh`即可输出

2. 编写一个shell脚本，要求在当前目录下创建一个文本，并在文本中写入“I love coding.”

   ```shell title="createAndWrite.sh"
   #!/bin/bash
   
   cd . # 进入当前目录
   ls   # 如果你想的话，可以随意在这里进行执行一些命令
   touch a.txt  # 创建了一个叫做a.txt的文本
   
   echo "I love coding." >> a.txt  # >> 表示追加内容到a.txt这个文本的后面
   ```

   在命令行窗口执行`bash createAndWrite.sh`，在当前目录下生成`a.txt`文件，并且在命令行窗口输出命令`ls`的内容，可以使用`cat a.txt`来查看是否将内容写入文本中



## the first day

### 变量

#### 定义变量

* 直接在shell命令行输入：`A=100`
	A：变量名
	100：变量值
* 利用`export`命令：
	`export A=100`

#### 注意

在定义变量时，中间不能有空格

#### 输出变量

* `echo $A`
* `echo ${A}`

**上述两者的区别：**

* `echo $AB`：无法输出，因为没有"AB"这个变量
* `echo ${A}B`：可以输出，输出结果为：`100B`  即在A变量后追加B这个字符

#### 环境变量和本地变量

*当前进程运行shell脚本，相当于开了一个子进程*

* 环境变量：也称为全局变量，是shell的内部变量，可以**继承**
* 本地变量：不可以继承的

随机在shell命令窗口定义的变量是本地变量

通过命令`export`变量可以将本地变量置为全局变量

```
export A=100
```

通过`type`命令可以查看A是否为shell内部命令

```
type A
```

#### 一些与变量有关的命令

* `export`：上述已经说明
* `unset`：清楚变量

```
unset A
```

* `readonly A=100`：定义一个**只读**变量；*注意：只读变量不可以修改和清除，echo定义的普通变量可以修改*
* `set`：显示所有变量
* `env`：显示当前的环境变量

### 位置参数

相当于C程序中的main函数输入参数

在脚本中使用这些参数：<br>

* `$1`表示第一个参数
* `$2`表示第二个参数
* ...
* `${10}`9以上的参数要使用"{}"

#### 常用的位置参数

* `$0` 表示当前脚本的文件名
* `$1`-`$9` 表示第一到第九个参数
* `$#` 位置参数个数
* `$*` 以单字符串形式显示所有位置参量
* `$@` 没有加双引号时和`$*`一致，加双引号时有所区别
* `$$` 脚本运行当前的进程号
* `$!` 最后一个后台运行的进程号
* `$?` 显示最后一个命令的退出状态：0表示没有错误；否则显示其他错误

#### 位置参量示例sh

```shell
#!/bin/bash
# 测试位置参数与其他特殊参数
# 使用方法 ./test.sh 参数1 参数2
# ./test.sh 1 2
# ./test.sh "1 2" 3

IFS=#
echo shell script name is:$0
echo the count of paramters:$#
echo first param=$1
echo second param=$2
echo '$*='$*
echo '"$*"='"$*"
echo '$@='$@
echo '"$@"='"$@"
echo '$$='$$
```

*在Centos8测试环境下，执行`bash test.sh 1 2`，输出如下：*

*（在我的目录下的文件为：`test_param.sh`）*

```
shell script name is:test_param.sh
the count of paramters:2
first param=1
second param=2
$*=1 2
"$*"=1#2
$@=1 2
"$@"=1 2
$$=42495
```

* 第一行表示文件名
* 第二行表示输入参数个数
* 第三行和第四行分别表示输入的两个参数（测试输入两个参数）分别是什么
* 第五行表示以单字符串形式输出参数
* 第六行测试加上双引号对于"$*"的表示：`IFS=#`表示参数之间使用的分隔符是"#"
* 第七行表示**没有加双引号**的`$@`：与`$*`没有差别
* 第八行表示**加上双引号**的`"$@"`与加上双引号的`"$*"`的差别：`"$*"`是分别输出参数；`"$@"`是单字符串输出参数
* 最后一行表示当前运行脚本的进程号

*进一步测试：执行`sh test_param.sh "1 2" 3`，输出如下：*

```
shell script name is:test_param.sh
the count of paramters:2
first param=1 2
second param=3
$*=1 2 3
"$*"=1 2#3
$@=1 2 3
"$@"=1 2 3
$$=42692
```

* 此时的输入参数还是两个，但是第一个为"1 2"，第二个为"3"
* 可以发现：没有加双引号的$*输出为单字符串连接形式参数
* 加上双引号的"$*"输出为分别输出参数，中间使用"#"作为分隔符
* 而加上双引号和没加上双引号的$@("$@")输出没有区别，都是以单字符串形式连接


测试`$?`可以在上述脚本中加上下面这条语句：

```
exit 100
```

表示退出状态为100

*测试结果如下：*

```
[zjp@localhost 变量]$ sh test_param.sh 
shell script name is:test_param.sh
the count of paramters:0
first param=
second param=
$*=
"$*"=
$@=
"$@"=
$$=42858
[zjp@localhost 变量]$ echo $?
100
```

### 数组

#### 定义数组

ep:
```
arr=(one two three)
```

输出元素的时候：

```
echo ${arr[0]}
echo ${arr[1]}
echo ${arr[2]}
echo ${arr[3]}
```

*在命令行输出分别为：*

```
[zjp@localhost 变量]$ arr=(one two three)
[zjp@localhost 变量]$ echo ${arr[0]}
one
[zjp@localhost 变量]$ echo ${arr[1]}
two
[zjp@localhost 变量]$ echo ${arr[2]}
three
[zjp@localhost 变量]$ echo ${arr[3]}

```

**可以发现，输出数组越界为空**

再定义一个超出数组范围的数组元素：

```
arr[6]=five
```

然后尝试输出所有元素：

```
...
echo ${arr[2]}
echo ${arr[3]}
echo ${arr[4]}
echo ${arr[5]}
echo ${arr[6]}
```

*输出结果为：*

```
[zjp@localhost 变量]$ arr[6]=five
[zjp@localhost 变量]$ echo ${arr[2]}
three
[zjp@localhost 变量]$ echo ${arr[3]}

[zjp@localhost 变量]$ echo ${arr[4]}

[zjp@localhost 变量]$ echo ${arr[5]}

[zjp@localhost 变量]$ echo ${arr[6]}
five
```

可以发现，自动扩张了数组，并且哉没有赋值的元素位置输出为空

此时，输出所有元素看一下元素的连续性：

```
echo ${arr[*]}
```

*输出如下：*

```
[zjp@localhost 变量]$ echo ${arr[*]}
one two three five
```

可以发现，元素的输出是不连续的。可以猜想，元素的个数也是仅仅只计算有元素值的数组个数：

```
echo ${#arr[*]}
```

*输出如下：*

```
[zjp@localhost 变量]$ echo ${#arr[*]}
4
```

验证正确

#### 重新赋值

还可以对数组进行重新赋值

在上述语句执行情况下继续执行：

```
arr[0] = zero
echo ${arr[0]}
```

*输出如下：*

```
[zjp@localhost 变量]$ arr[0]=zero
[zjp@localhost 变量]$ echo ${arr[0]}
zero
```







## the second day

### 输入

* read var：读取变量var，输入内容到var中

```
[zjp@localhost ~]$ read var
abc
[zjp@localhost ~]$ echo $var
abc
```

* 在命令行窗口单独输入read，输入的内容会被保存到内置的变量`REPLY`

```
[zjp@localhost ~]$ read
abd
[zjp@localhost ~]$ echo $REPLY
abd
```

* read -a 表示将标准输入内容输入到数组中

```
[zjp@localhost ~]$ read -a arr 
1 2 3
[zjp@localhost ~]$ echo ${arr[*]}
1 2 3
```

* read -p "print the message " -t [num] 表示输出提示符内容，在设置的超时时间之内将标准输入内容输入到后续跟的某个变量中

```
[zjp@localhost ~]$ read -p "please input: " -t 10 -a arr
please input: 1 2 3
[zjp@localhost ~]$ echo ${arr[*]}
1 2 3
```

*注意：-t 表示timeout，单位为s*

### 输出

* echo -n：表示输出内容时不需要换行

```
[zjp@localhost ~]$ echo -n $var
abc[zjp@localhost ~]$ 
```

* -e选项对于echo \t 和 echo "\t"

`echo \t`会被命令行解析为输出t，不会对其进行转义

`echo "\t"`同样不会对其进行转义，直接输出双引号之间的内容

`echo -e \t`还是会被解析为t

`echo -e "\t"`会将双引号中的\t解析为制表符

```
[zjp@localhost ~]$ echo \t
t
[zjp@localhost ~]$ echo "\t"
\t
[zjp@localhost ~]$ echo -e \t
t
[zjp@localhost ~]$ echo -e "\t"
	
[zjp@localhost ~]$ echo -e "\t"AAA
	AAA
```
*-e：表示对后续双引号之间的内容进行转义*

* 单引号、双引号和反引号的区别

**单引号：忽略所有特殊字符**

```
[zjp@localhost ~]$ x=*
[zjp@localhost ~]$ echo $x
公共 模板 视频 图片 文档 下载 音乐 桌面 cplusplus_designedPattern sometask.txt test tinyhttpd TinyWebServer
[zjp@localhost ~]$ echo '$x'
$x
```

*由于忽略所以符号，所以这里的$是一个普通的符号*

*注意：echo `*` 是打印当前目录下的所有文件名*

**双引号：忽略大多数字符，除了$和`之外**

```
[zjp@localhost ~]$ x=*
[zjp@localhost ~]$ echo $x
公共 模板 视频 图片 文档 下载 音乐 桌面 cplusplus_designedPattern sometask.txt test tinyhttpd TinyWebServer
[zjp@localhost ~]$ echo "$x"
*
```

*由于不忽略$符号，所以这里的$x会被解析为x变量*

```
[zjp@localhost ~]$ y=^
[zjp@localhost ~]$ echo $y
^
[zjp@localhost ~]$ echo "`y"
> 

```

*上述是一个不忽略反引号的例子*

**反引号：命令替换**

```
[zjp@localhost test]$ pwd
/home/zjp/test
[zjp@localhost test]$ echo `pwd`
/home/zjp/test
[zjp@localhost test]$ ls
array               Disjoint_set  lambda_test            py_spider     study_shell
C                   DNS           list                   queue         TCP_IP
C_file              gdb_test      plus                   shared_count  test
circle_queue        hello         poll_epoll             socket_op     test_strcasecmp
cpp_const_override  hello_1       process                sort          thread_test
design_pattern      hton_ntoh     process_communication  stack         UDP
[zjp@localhost test]$ echo `ls`
array C C_file circle_queue cpp_const_override design_pattern Disjoint_set DNS gdb_test hello hello_1 hton_ntoh lambda_test list plus poll_epoll process process_communication py_spider queue shared_count socket_op sort stack study_shell TCP_IP test test_strcasecmp thread_test UDP
```

* `$()` 等价于上述的反引号对于命令的替换

```
[zjp@localhost test]$ echo `pwd`
/home/zjp/test
[zjp@localhost test]$ echo $(pwd)
/home/zjp/test
```

* basename 和 dirname

basename输出路径的最后一个

dirname输出除了路径的最后一个的全部路劲

```
[zjp@localhost test]$ dirname /ho/zjp/peng
/ho/zjp
[zjp@localhost test]$ basename /ho/zjp/peng
peng
```

*注意：此处路径不一定合法*

**ep：** 使用echo对basename的内容进行输出

*注意：对于内置的符号需要转义的；对于反引号在内容中需要转义，而$()不需要*

```
[zjp@localhost test]$ echo `basename \`pwd\``
test
[zjp@localhost test]$ echo $(basename `pwd`)
test
[zjp@localhost test]$ echo $(basename $(pwd))
test
```

### 算术运算符

算术运算符

![算术运算符](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/data/%E7%AE%97%E6%9C%AF%E8%BF%90%E7%AE%97%E7%AC%A6.jpg)

算术拓展

* `$[]`：

```
[zjp@localhost test]$ n=5
[zjp@localhost test]$ echo $[$n+1]
6
[zjp@localhost test]$ echo $[$n+ 1 ]
6
```

*注意：中间无所谓空格*

* `$(())`：和上述`$[]`等价

```
[zjp@localhost test]$ echo $(($n+1))
6
[zjp@localhost test]$ echo $((n+=1))
6
[zjp@localhost test]$ echo $((n+=1))
7
[zjp@localhost test]$ echo $[$n+=1]
-bash: 7+=1: 尝试给非变量赋值 (错误符号是 "+=1")
```

*注意：`$[]`内不可以进行+=这样的操作*

* `(())`中间表达式可以改变变量的值

```
[zjp@localhost test]$ echo $n
8
[zjp@localhost test]$ ((n+=1))
[zjp@localhost test]$ echo $n
9
```

* 注意事项：

1. 不可以通过echo输出`(())`中改变变量的内容

2. 不可以通过变量赋值将`(())`的内容进行赋值

3. 可以通过`$[]`将改变的变量赋值给新的变量

```
[zjp@localhost test]$ echo ((n+=1))
-bash: 未预期的符号 `(' 附近有语法错误
[zjp@localhost test]$ r=((n+=1))
-bash: 未预期的符号 `(' 附近有语法错误
[zjp@localhost test]$ r=$[$n+1]
[zjp@localhost test]$ echo $r
10
```

* expr

```
[zjp@localhost test]$ expr 4 + 5
9
[zjp@localhost test]$ expr 4 +5
expr: syntax error: unexpected argument “+5”
[zjp@localhost test]$ expr 4+5
4+5
```

*注意：expr num + num中间的空格不可以省略，否则会发生一些错误；不可以将expr表达式赋值给新的变量；可以使用反引号转义一下赋值给新的变量;*

*特殊的，对于expr num `*` num 需要对`*`进行转义*

```
[zjp@localhost test]$ r=expr 4 + 5
bash: 4: 未找到命令...
[zjp@localhost test]$ r=`expr 4 + 5`
[zjp@localhost test]$ echo $r
9
[zjp@localhost test]$ r=$(expr 4 + 5)
[zjp@localhost test]$ echo $r
9

[zjp@localhost test]$ r=`expr 4 * 5`
expr: syntax error: unexpected argument “array”
[zjp@localhost test]$ r=`expr 4 \* 5`
[zjp@localhost test]$ echo $r
20
```







# shell示例

```shell
#!/bin/sh

# 执行指令后，会先显示该指令及所下的参数
set -x

# 脚本执行的位置是当前目录位置
SOURCE_DIR=`pwd`
# 该变量的值意思是：在上一级创建bulid
BUILD_DIR=${BUILD_DIR:-../build}
# 该变量的值意思是：当前目录创建debug
BUILD_TYPE=${BUILD_TYPE:-debug}
# 该变量的值意思是：上一级目录创建build-install
INSTALL_DIR=${INSTALL_DIR:-../${BUILD_TYPE}-install}
# 该变量的值：0
BUILD_NO_EXAMPLES=${BUILD_NO_EXAMPLES:-0}

# 创建目录 -p是表示确保目录名称存在，不存在就创建一个
# 创建的目录名为：build/debug
mkdir -p $BUILD_DIR/$BUILD_TYPE \
# 并进入到这个目录
  && cd $BUILD_DIR/$BUILD_TYPE \
  # 通过CLI生成CMake项目依赖关系图
  && cmake --graphviz=dep.dot \
           -DCMAKE_BUILD_TYPE=$BUILD_TYPE \
           -DCMAKE_INSTALL_PREFIX=$INSTALL_DIR \
           -DCMAKE_BUILD_NO_EXAMPLES=$BUILD_NO_EXAMPLES \
           $SOURCE_DIR \
  # make当前目录         
  && make $*

#cd $SOURCE_DIR && doxygen
```

