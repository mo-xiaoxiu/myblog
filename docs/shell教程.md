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

![算术运算符](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/%E7%AE%97%E6%9C%AF%E8%BF%90%E7%AE%97%E7%AC%A6.jpg)

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



## the third day

### let命令

```
[zjp@localhost ~]$ n=5
[zjp@localhost ~]$ let n=n+1
[zjp@localhost ~]$ echo $n
6
[zjp@localhost ~]$ let n= n+1
-bash: let: n=: 语法错误: 需要操作数 (错误符号是 "=")
[zjp@localhost ~]$ let "n= n+1"
[zjp@localhost ~]$ echo $n
7
```

* let可以进行运算拓展
* let后跟的算术运算不可以有空格
* let可以使用双引号将算术运算括起来
* let对于未命名的未知变量会默认为0

```
[zjp@localhost ~]$ echo $n
7
[zjp@localhost ~]$ let n=n+abc
[zjp@localhost ~]$ echo $n
7
```

### 条件测试

**命令真为0，假为1**

可以使用退出状态码对指令等进行测试

```
[zjp@localhost ~]$ grep study /etc/passwd
[zjp@localhost ~]$ echo $?
1
[zjp@localhost ~]$ grep hello /etc/passwd;echo $?
1
```

#### test

```
[zjp@localhost ~]$ x=5;y=10
[zjp@localhost ~]$ test $x -gt $y
[zjp@localhost ~]$ echo $?
1
[zjp@localhost ~]$ test $y -gt $x
[zjp@localhost ~]$ echo $?
0
```

和test等价的是`[]`

```
[zjp@localhost ~]$ [ $y -gt $x ] 
[zjp@localhost ~]$ echo $?
0
[zjp@localhost ~]$ [$y -gt $x ]
bash: [10: 未找到命令...
^C
```

**注意：[]内的语句距离两边[]一定要有空格**

#### 测试表达式的值

**[[]]可以使用通配符进行模式匹配**

```
[zjp@localhost ~]$ name=Tom
[zjp@localhost ~]$ [ $name = [Tt]?? ]
[zjp@localhost ~]$ echo $?
1
[zjp@localhost ~]$ [[ $name=[Tt]?? ]]
[zjp@localhost ~]$ echo $?
0
```

#### 字符串测试

```
[zjp@localhost ~]$ str=
[zjp@localhost ~]$ [ -z $str ]
[zjp@localhost ~]$ echo $?
0
[zjp@localhost ~]$ str=aaa
[zjp@localhost ~]$ [ -z $str ]
[zjp@localhost ~]$ echo $?
1
```

**-z：zero 是否为空；str= 字符串为空串**

**`[ -n $str ]`：no 如果字符串str长度不为0，则返回真（0）**

**`[ $str1 = $str2 ]`：两个字符串相等**

**`[ $str1 != $str2]`：两字符串不相等**

```
[zjp@localhost ~]$ str1=aaa
[zjp@localhost ~]$ str=AAA
[zjp@localhost ~]$ [ $str = $str1 ]
[zjp@localhost ~]$ echo $?
1
[zjp@localhost ~]$ str=aaa
[zjp@localhost ~]$ [ $str = $str1 ]
[zjp@localhost ~]$ echo $?
0
```

#### 整数测试

**`[ int1 -eq int2 ]`：int1等于int2** equal

**`[ int1 -ne int2 ]`：int1不等于int2** no equal

**`[ int1 -gt int2 ]`：int1大于int2** greater

**`[ int1 -ge int2 ]`：int1大于等于int2** greater equal

**`[ int1 -lt int2]`：int1小于int2** little

**`[ int1 -le int2]`：int1小于等于int2** little equal

```
[zjp@localhost ~]$ x=1;[ $x -eq 1 ];echo $?
0
[zjp@localhost ~]$ x=2;[ $x -eq 1 ];echo $?
1
```

下述方式只能用于整数测试：let命令和双圆括号的整数操作

**==、！=、>、<、>=、<=**

```
[zjp@localhost ~]$ x=1;let "$x == 1";echo $?
0
[zjp@localhost ~]$ x=1;(($x+1 >= 2));echo $?
0
[zjp@localhost ~]$ 
```

* let和双圆括号的测试方法的区别：

	* 使用的操作符不同
	* let 和 双圆括号 可以使用算术表达式，中括号不行
	* let 和 双圆括号， 操作符两边可以不留空格

#### 逻辑测试

**`[ expr1 -a expr2 ]`：与** and

**`[ expr1 -o expr2 ]`：或** or

**`[ !expr ]`：非**

```
[zjp@localhost ~]$ x=1;name=Tom
[zjp@localhost ~]$ [ $x -eq 1 -a -n $name ];echo $?
0
[zjp@localhost ~]$ [ ($x -eq )1 -a (-n $name) ];echo $?
-bash: 未预期的符号 `$x' 附近有语法错误
```

**注意：不能随便添加"()"**

下述是可以使用模式的逻辑测试：

**`[[ pattern1 && pattern2 ]]`** 与

**`[[ pattern1 || pattern2 ]]`** 或

**`[[ !pattern ]]`** 非

```
[zjp@localhost ~]$ x=1;name=Tom;
[zjp@localhost ~]$ [[ $x -eq 1 && $name = To? ]];echo $?
0
```

**检查空值：**

检查字符串是否为空

**`[ "$name" = "" ]`** 

**`[ !"$name" ]`**

**`[ "x${name}"="x" ]`** 

```
[zjp@localhost ~]$ name=
[zjp@localhost ~]$ [ "$name" = "" ]
[zjp@localhost ~]$ echo $?
0
[zjp@localhost ~]$ name=aaa
[zjp@localhost ~]$ [ "$name" = "" ]
[zjp@localhost ~]$ echo $?
1
[zjp@localhost ~]$ [ ! "$name" ];echo $?
1
[zjp@localhost ~]$ name=
[zjp@localhost ~]$ [ ! "$name" ];echo $?
0
[zjp@localhost ~]$ name=
[zjp@localhost ~]$ [ ! "$name" ];echo $?
0
[zjp@localhost ~]$ [ "x${name}" = "x" ]
[zjp@localhost ~]$ echo $?
0
[zjp@localhost ~]$ name=aaa
[zjp@localhost ~]$ [ "x${name}" = "x" ];echo $?
1
```

#### 文件测试

文件是否存在，文件属性，访问权限等

常见的文件测试操作符：

![文件测试常见的操作符](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/%E6%96%87%E4%BB%B6%E6%B5%8B%E8%AF%95%E5%B8%B8%E8%A7%81%E7%9A%84%E6%93%8D%E4%BD%9C%E7%AC%A6.jpg)

### 括号总结

**`${...}`：获取变量值**

**`$(...)`：命令替换**

**`$[...]`：让无类型的变量参与算术运算** `$[$n+1]`

**`$((...))`：同上**

**`((...))`：算术运算**

**`[...]`：条件测试，注意：变量与符号或者选项之间需要有空格**

**`[[...]]`：条件测试，与`[...]`相比之下此支持模式匹配与通配符**

### if条件语句

#### 语法结构

```
if expr1	# 如果expr1 为真（0）
then
	commands1	# 执行语句块 commands1
elif expr2	# 如果expr1 不为真
then
	commands2	# 执行语句块 commands2
......	# 可以有多个elif语句
else	# else最多只有一个
	commands4	# 执行语句块 commands4
fi
```

以下是一个简单的ifshell脚本：

```shell title="01easy_for.sh"
#!/bin/bash

if [ $# -ne 1 ]
then
	echo Usage: $0 username
	exit 1
fi

echo $1

```

*编译过程以及输出结果如下：*

```
[zjp@localhost the_fourth_day]$ sh 01easy_for.sh 
Usage: 01easy_for.sh username
[zjp@localhost the_fourth_day]$ sh 01easy_for.sh 1
1
[zjp@localhost the_fourth_day]$ sh 01easy_for.sh 2
2
```

* expr通常为条件测试表达式；也可以是多个命令，以最后一个命令的退出状态为条件值

* commands为可执行语句块，如果为空，需要使用shell提供的空命令状态":"（冒号）。该命令不做任何事情，只返回一个退出状态0





### case选择语句

#### 语法结构

```
case expr in	# expr为表达式，注意关键词in
	pattern1)	# 若expr 与 pattern1 匹配，注意括号
	commands1	# 执行语句块commands1
	;;		# 跳出 case 结构
	pattern2)	# 若expr 与 pattern2 匹配
	commands2	# 执行语句块commands2
	;;
	......		# 可以有任意多个模式匹配
	*)		# 若expr与上面的模式都不匹配
	commands	# 执行语句块commands
	;;
esac			# case语句必须以esac终止
```

* 所给的匹配模式pattern中可以含有多个通配符和“|”







## the fifth day

### for循环语句

#### 语法结构

```shell
for variable in list	# 每次循环，依次把列表list中的一个值赋给循环变量
do	# 循环开始的标志
	commands	# 循环变量每取一次值，循环体就执行一次
done	# 循环结束的标志
```

#### 说明

* list可以是命令替换、变量名替换、字符串、文件名列表（包含通配符）

* for循环执行的次数取决于列表list中单词的个数

* for循环中一般要出现循环变量，但也可以不出现

#### 示例

```shell title="01easy_for.sh"
#!bin/bash

for i in 1 2 3 4
do
	echo value of is $i
done

```

*编译并输出的结果如下：*

```
value of is 1
value of is 2
value of is 3
value of is 4
```

for循环的执行过程，是将list中的第一个词赋值给循环变量，并将这个词从list中删除，然后进入循环体，执行do和done之间的命令。下一次进入循环时，将第二个词赋值给循环变量，并将其从list中删除，以此类推

当list中的词全部被移走后，循环结束

#### 位置参量的使用

* `$* "$*"  $@  "$@"`

* 可以省略`in list`，此时使用`"$@"`

```shell title="02Parameter.sh"
#!bin/bash

for i
do
	echo value of is $i
done

```

*编译及输出结果：*

```
[zjp@localhost the_fifth_day]$ sh 02Parameter.sh 
[zjp@localhost the_fifth_day]$ sh 02Parameter.sh 1 2 3 4
value of is 1
value of is 2
value of is 3
value of is 4
```

```shell title="03otherParameter.sh"
#!bin/bash

#for i in $*
#for i in "$*"
#for i in $@
for i in "$@"
do
	echo $i
done
```

*编译及输出结果为：*

```
[zjp@localhost the_fifth_day]$ vim 03otherParameter.sh
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh 
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh 1 2 3 4
1
2
3
4
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh "1 2" 3 4
1
2
3
4
[zjp@localhost the_fifth_day]$ vim 03otherParameter.sh 
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh 1 2 3 4
1 2 3 4
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh "1 2" 3 4
1 2 3 4
[zjp@localhost the_fifth_day]$ vim 03otherParameter.sh 
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh 1 2 3 4
1
2
3
4
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh "1 2" 3 4
1
2
3
4
[zjp@localhost the_fifth_day]$ vi 03otherParameter.sh 
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh 1 2 3 4
1
2
3
4
[zjp@localhost the_fifth_day]$ sh 03otherParameter.sh "1 2" 3 4
1 2
3
4
```

从输出结果可以看出，

* `$*`总是单字符串输出，与参数列表加不加`""`没有关系

* `"$*"`总是将参数列表当作一个整体，分别输出参数

* `$@`与没有加双引号的`$*`是一样的

* `"$@"`与`"$*"`区别就是：`"$@"`是单字符串输出参数的


再来看一个for循环中有变量递增的：

```shell title="04for.sh"
#!bin/bash

counter=0

for f in *
do
	counter=$[$counter+1]
done

echo There are $counter in 'pwd'

```

*输出结果如下：*

```
[zjp@localhost the_fifth_day]$ vi 04for.sh
[zjp@localhost the_fifth_day]$ sh 04for.sh 
There are 4 in pwd
```

#### 类似于C语言的for循环

```shell
for((expr1;expr2;expr3))
do
done
```

接下来看一个打印星号图的示例：

```shell title="05printTw.sh"
#!bin/bash

if [ $# -ne 1 ]
then
	echo 'Usage:$0 <n>'
	exit 1
fi

if [ $1 -lt 5 -o $1 -gt 15 ]
then
	echo 'Usage:$0 <n>'
	echo ' where 5<=n<=15'
	exit 1
fi

for ((i=0;i<$1;i++))
do
	for ((j=0;j<$[$1-$i-1];j++))
	do
		echo -n " "
	done

	for ((j=0;j<$[2*$i+1];j++))
	do
		echo -n "*"
	done

	echo -ne '\n'
done

```

*输出的结果如下：*

```
[zjp@localhost the_fifth_day]$ vi 05printTwi.sh
[zjp@localhost the_fifth_day]$ sh 05printTwi.sh 
Usage:$0 <n>
[zjp@localhost the_fifth_day]$ sh 05printTwi.sh 16
Usage:$0 <n>
 where 5<=n<=15
[zjp@localhost the_fifth_day]$ sh 05printTwi.sh 1
Usage:$0 <n>
 where 5<=n<=15
[zjp@localhost the_fifth_day]$ sh 05printTwi.sh 8
       *
      ***
     *****
    *******
   *********
  ***********
 *************
***************
```



## the sixth day

### while循环语句

#### 语法结构

```shell
while expr	# 执行expr
do	# 若expr的退出状态为0，进入循环，否则退出
	commands	# 循环体
done	# 循环体结束的标志
```

#### 执行过程

先执行expr，如果退出状态为0，则执行循环体；执行到关键字done后，回到循坏体的顶部，while再次检查expr的退出状态...以此类推，直到expr退出状态为非0为止

下述例子同样时打印星号：

```shell
#!/bin/bash

if [ $# -ne 1 ];then
	echo "Usage:$0 <n>"
	exit 1
fi

if [ $1 -lt 5 -o $1 -gt 15 ];then
	echo "Usage:$0 <n>"
	echo "(where 5<=n<=15)"
	exit 1
fi

lines=$1
curline=0

while [ $curline -lt $lines ]
do
	nSpaces=$[$lines-$curline-1]
	while [ $nSpaces -gt 0 ]
	do
		echo -n " "
		nSpaces=$[$nSpaces-1]
	done
	nStars=$[2*$curline+1]
	while [ $nStars -gt 0 ]
	do
		echo -n "*"
		nStars=$[nStars-1];
	done
	echo -ne "\n"
	curline=$[$curline+1]
done
```

*输出结果如下：*

```
[zjp@localhost the_sixth_day]$ vi 01printTw_while.sh 
[zjp@localhost the_sixth_day]$ sh 01printTw_while.sh 
Usage:01printTw_while.sh <n>
[zjp@localhost the_sixth_day]$ sh 01printTw_while.sh 16
Usage:01printTw_while.sh <n>
(where 5<=n<=15)
[zjp@localhost the_sixth_day]$ sh 01printTw_while.sh 8
       *
      ***
     *****
    *******
   *********
  ***********
 *************
***************
```

### until循环语句

#### 语法结构

```shell
until expr	# 执行expr
do	# 若expr退出状态为非0，进入循环，否则退出
	commands	# 循环体
done	# 循环结束标志
```

#### 执行过程

与while相似，只是当expr退出状态为**非0**时，执行循环体内容，直到expr为0时退出

下述是一个示例：

```shell
#!/bin/bash

counter=0

until [ $counter -eq 3 ]
do
	echo AAA
	sleep 1
	counter=$[$counter+1]
done
```

*以上程序是每隔一秒输出三行AAA，编译执行过程如下：*

```
[zjp@localhost the_sixth_day]$ vi 02until.sh
[zjp@localhost the_sixth_day]$ sh 02until.sh 
AAA
AAA
AAA
```

### break 和 continue

* `break [n]`

	* 用于强制退出当前执行状态

	* 如果是嵌套循环，则break后面可以跟着一个数字表示退出第n重循环（最里面为第一层循环）

* `continue [n]`

	* 用于忽略本次循环的剩余部分，回到循环的顶部，继续下一次循环

	* 如果是嵌套循环，continue后面可以跟着一个数字表示回到第n重循环的顶部

### exit 和 sleep

* `exit n`

exit可以用于退出脚本或者退出当前程序。n是一个从**0到255**的整数，0表示退出成功，非0表示遇到某种失败的退出，**该整数被保存在状态变量`$?`中**

* `sleep n`

暂停n秒

### select循环与菜单

#### 语法结构

```shell
select var in list
do	# 循环开始
	commands	# 循环变量每次取一次值，循环体就执行一次
done
```

#### 说明

* select循环主要用于创建菜单，按照数字顺序排列的菜单项将显示在**标准错误**上，并**显示PS3提示符，等待用户输入**

* 用户输入菜单列表中的某个数字，执行相应的命令

* 用户输入被保存在内置变量REPLY中

以下是一个select示例：

```shell
#!/bin/bash

select var in Dogs Cats Mouse
do
	case $var in	# select经常会与case搭配使用
		Dogs)
			echo "Dogs are my favorite pet"
			;;
		Cats)
			echo "Cats are my favorite pet"
			;;
		Mouse)
			echo "Mouse are my favorite pet"
			;;
		*)
			echo non of my favorite pet
	esac
done
```

*编译执行的结果如下：*

```
[zjp@localhost the_sixth_day]$ sh 03select.sh 
1) Dogs
2) Cats
3) Mouse
#? 1
Dogs are my favorite pet
#? 2
Cats are my favorite pet
#? 3
Mouse are my favorite pet
#? 4
non of my favorite pet
#? 
```

变化1：在选择喜欢其中一种自定义喜欢的动物之后退出程序（其他不是自定义喜欢的将会进入循环）：

*假设这里自定义喜欢的动物是Dogs*:

```shell
#!/bin/bash

select var in Dogs Cats Mouse
do
	case $var in	# select经常会与case搭配使用
		Dogs)
			echo "Dogs are my favorite pet";break
			;;
		Cats)
			echo "Cats are my favorite pet"
			;;
		Mouse)
			echo "Mouse are my favorite pet"
			;;
		*)
			echo non of my favorite pet
	esac
done
```

*编译执行过程如下：*

```
[zjp@localhost the_sixth_day]$ sh 03select.sh 
1) Dogs
2) Cats
3) Mouse
#? 2
Cats are my favorite pet
#? 3
Mouse are my favorite pet
#? 4
non of my favorite pet
#? 1
Dogs are my favorite pet
```

变化2：在选择任意一种动物之后退出：

```shell
#!/bin/bash

select var in Dogs Cats Mouse
do
	case $var in	# select经常会与case搭配使用
		Dogs)
			echo "Dogs are my favorite pet";#break
			;;
		Cats)
			echo "Cats are my favorite pet"
			;;
		Mouse)
			echo "Mouse are my favorite pet"
			;;
		*)
			echo non of my favorite pet
	esac
	break	# 选择之后直接退出
done
```

*编译执行的过程如下：*

```
[zjp@localhost the_sixth_day]$ sh 03select.sh 
1) Dogs
2) Cats
3) Mouse
#? 1
Dogs are my favorite pet
[zjp@localhost the_sixth_day]$ sh 03select.sh 
1) Dogs
2) Cats
3) Mouse
#? 2
Cats are my favorite pet
[zjp@localhost the_sixth_day]$ sh 03select.sh 
1) Dogs
2) Cats
3) Mouse
#? 3
Mouse are my favorite pet
[zjp@localhost the_sixth_day]$ sh 03select.sh 
1) Dogs
2) Cats
3) Mouse
#? 4
non of my favorite pet
```

变化3：还可以在用户输入前，对用户进行提示（使用PS3变量）：

```shell
#!/bin/bash

PS3="your favorite pet: "	# 使用PS3变量进行用户输入前的提示

select var in Dogs Cats Mouse
do
	case $var in	# select经常会与case搭配使用
		Dogs)
			echo "Dogs are my favorite pet";#break
			;;
		Cats)
			echo "Cats are my favorite pet"
			;;
		Mouse)
			echo "Mouse are my favorite pet"
			;;
		*)
			echo non of my favorite pet
	esac
	break	# 选择之后直接退出
done
```

*执行过程如下：*

```
[zjp@localhost the_sixth_day]$ sh 03select.sh 
1) Dogs
2) Cats
3) Mouse
your favorite pet: 1
Dogs are my favorite pet
```

#### select 与 case

* select是个无限循环，因此要记住用break命令退出循环，或用exit进行终止，也可以使用ctrl+c推出循环

* select经常金额case联合使用

* 与for循环相似，可以省略in list，此时可以使用位置参量

### 函数

函数在shell中的一般格式：

```
function function_name {
	commands
}
```

或者（一般多用下面这种）

```
function_name() {
	commands
}
```

以下是一个函数的示例：

```shell
#!/bin/bash

fun(){
	echo "Entering function."
	echo "Exiting function."
}

fun	# 通过函数名直接调用该函数


```

*执行过程和结果如下：*

```
[zjp@localhost the_sixth_day]$ sh 04function.sh 
Entering function.
Exiting function.
```

shell的函数也是可以接受参数的，函数的形式与上面所写一致：

```shell
#!/bin/bash

func() {
	echo "the parameter's count: $#"
	echo "the first parameter: $1"
	echo "the second parameter: $2"
}

func a b	# 传入两个参数分别是a、b
```

*执行过程和结果如下：*

```
[zjp@localhost the_sixth_day]$ sh 05function_para.sh 
the parameter's count: 2
the first parameter: a
the second parameter: b
```

**还可以在另一个程序中通过包含文件的方式（类似于C/C++中的#include的操作），使用该程序的函数**

```shell
#!/bin/bash

. ./tool		# 表示包含当前目录下的文件

func 		# 调用另一个程序（文件）中的函数

```

在当前目录下的文件tool

```
func() {
	echo "this is a tool."
}
```

*执行过程与结果如下：*

```
[zjp@localhost the_sixth_day]$ vi 06use_another_func.sh
[zjp@localhost the_sixth_day]$ sh 06use_another_func.sh 
this is a tool.
```

### 字符串操作

![字符串操作](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%93%8D%E4%BD%9C.jpg)

以下是一个示例：

*匹配字符串*

```shell
#!/bin/bash

var="/aa/bb/cc"		# 要进行字符串操作（匹配）的字符出变量
result1=${var#*/}	# 删除从前往后匹配（一个或者多个）第一个“/”的最少部分
result2=${var##*/}	# 删除从前往后匹配（一个或者多个）最后一个“/”的最多部分
result3=${var%/*}	# 删除从后往前匹配（一个或者多个）第一个“/”的最少部分
result4=${var%%/*}	# 删除从后往前匹配（一个或者多个）最后一个“/”的最多部分

echo $var

echo '${var#*/}'=$result1
echo '${var##*/}'=$result2
echo '${var%/*}'=$result3
echo '${var%%/*}'=$result4
```

*执行过程和输出结果如下：*

```
[zjp@localhost the_sixth_day]$ vi 07character.sh
[zjp@localhost the_sixth_day]$ sh 07character.sh 
/aa/bb/cc
${var#*/}=aa/bb/cc
${var##*/}=cc
${var%/*}=/aa/bb
${var%%/*}=
```

### eval命令

`eval arg1 [arg2] ... [argN]`

将所有参数连接成一个表达式，并计算或者执行该表达式，参数中的任何变量都将被展开

```
[zjp@localhost the_sixth_day]$ listpage="ls -l | more"
[zjp@localhost the_sixth_day]$ eval $listpage
总用量 44
-rw-rw-r--. 1 zjp zjp  456 3月  21 14:38 01printTw_while.sh
-rw-rw-r--. 1 zjp zjp  101 3月  21 14:43 02until.sh
-rw-rw-r--. 1 zjp zjp  411 3月  21 15:06 03select.sh
-rw-rw-r--. 1 zjp zjp  121 3月  21 15:29 04function.sh
-rw-rw-r--. 1 zjp zjp  168 3月  21 15:33 05function_para.sh
-rw-rw-r--. 1 zjp zjp  118 3月  21 15:40 06use_another_func.sh
-rw-rw-r--. 1 zjp zjp  619 3月  21 16:02 07character.sh
-rw-rw-r--. 1 zjp zjp 8718 3月  21 16:03 README.md
-rw-rw-r--. 1 zjp zjp   35 3月  21 15:40 tool
```

### 随机数与expr

* 生成随机数

```
echo $RANDOM
```

* expr

```
expr 5 % 3
expr 5 \* 3
```

*注意空格*

### shift

* 一般用于函数或者脚本程序参数处理，特别是参数多于10以上

* 将所有参数变量向下移动一个位置

以下是一个简单得shift示例：

```shell
#!/bin/bash

while [ "$1" != "" ]
do
	echo $1
	shift
done
```

*执行和输出结果如下：*

```
[zjp@localhost the_sixth_day]$ sh 08shift.sh 1 2 3
1
2
3
```

变化：将程序中的`echo $1`改成`echo $*`：

```shell
#!/bin/bash

while [ "$1" != "" ]
do
	echo $*
	shift
done

```

*执行和输出结果如下：*

```
[zjp@localhost the_sixth_day]$ sh 08shift.sh 1 2 3
1 2 3
2 3
3
```

### trap命令

```
trap command signal
```

* command

	* 一般情况下是Linux命令

	* ''表示发生陷阱时为空指令，不做任何动作

	* '-'表示发生陷阱时采用缺省的指令

* signal

	* HUP(1)：挂起
	
	* INT(2)：中断

	* QUIT(3)：退出‘

	* ABRT(6)：异常终止

	* ALRM(14)：闹钟

	* TREM(15)：中止（关机）

trap的异步处理能力：当程序顺序执行下来的时候，如果发生信号，将转去执行信号所关联的操作；

trap可以对信号的操作进行关联

```shell
#!/bin/bash

trap "rm -f tmp$$;exit 0" 2 3	# 捕获2、3信号，执行“”中的内容（指令）
touch tmp$$
sleep 60
```


*在一个终端执行如下：*

```
[zjp@localhost the_sixth_day]$ sh 09trap.sh 

```

*在另一个终端查看此时当前目录下有没有创建”tmp+当前进程号“的文件*：

```
[zjp@localhost the_sixth_day]$ ls
01printTw_while.sh  03select.sh    05function_para.sh     07character.sh  09trap.sh  tmp32839
02until.sh          04function.sh  06use_another_func.sh  08shift.sh      README.md  tool
```

*可以发现创建了`tmp32839`这个文件*

再在执行程序的终端`ctrl+c`对程序进行中断，然后在另一个终端查看此时的文件列表：

```
[zjp@localhost the_sixth_day]$ ls
01printTw_while.sh  03select.sh    05function_para.sh     07character.sh  09trap.sh  tool
02until.sh          04function.sh  06use_another_func.sh  08shift.sh      README.md
```

*可以发现，此时的`tmp32839`已经被删除了*



再来看一个trap的示例：

以下程序的功能是对于当前终端进行锁屏，需要输入密码才可以解锁使用：

```shell
#!/bin/bash

trap "nice_try" 2 3 15	# 捕获2、3和15信号，执行"nice_try"函数

TTY='tty'	# 保存当前终端的变量

nice_try()
{
	echo -e "\nnice try,the terminal stays locked."
}

echo -n "Enter your password to lock $TTY: "
read PASSWORD
clear

echo -n "Enter your password to unlock $TTY: "
while :
do
	read RESPONSE
	if [ "$RESPONSE" = "$PASSWORD" ];then
		echo "unlocking..."
		break
	fi
	clear

	echo "wrong password and terminal is locker..."
	echo -n "Enter your password to unlock $TTY: "
done

```

*在终端执行该脚本，得到：*

```
[zjp@localhost the_sixth_day]$ sh 10trap_tty.sh 
Enter your password to lock tty: 

```

*输入密码之后，刷新屏幕，此时输入正确的密码即可解锁：*

```
Enter your password to unlock tty: 123
unlocking...
[zjp@localhost the_sixth_day]$ 
```

*输入错误的信息试一下：*


```
wrong password and terminal is locker...
Enter your password to unlock tty: 

```


### shell内置命令总结

![shell内置命令](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/shell%E5%86%85%E7%BD%AE%E5%91%BD%E4%BB%A4%E6%80%BB%E7%BB%93.jpg)







## the seventh day

### 流编辑器sed

sed介绍

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed_%E6%B5%81%E7%BC%96%E8%BE%91%E5%99%A8sed.jpg)

sed简单用法

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed%E7%AE%80%E5%8D%95%E7%94%A8%E6%B3%95.jpg)

sed指定多个命令的三种方式

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed_%E6%8C%87%E5%AE%9A%E5%A4%9A%E4%B8%AA%E5%91%BD%E4%BB%A4%E7%9A%84%E6%96%B9%E5%BC%8F.jpg)

sed -f

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed-f.jpg)

sed命令语法

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed%E5%91%BD%E4%BB%A4%E8%AF%AD%E6%B3%95.jpg)

sed定位方式

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed%E5%AE%9A%E4%BD%8D%E6%96%B9%E5%BC%8F.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed_m,n!%20%E5%8F%96%E5%8F%8D_%E6%89%93%E5%8D%B0.jpg)

sed编辑命令

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed%E7%BC%96%E8%BE%91%E5%91%BD%E4%BB%A4.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed%E7%BC%96%E8%BE%91%E5%91%BD%E4%BB%A42.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed%E7%BC%96%E8%BE%91%E5%91%BD%E4%BB%A4_6.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed$r.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed%E7%BC%96%E8%BE%91%E5%91%BD%E4%BB%A4_7.jpg)

**sed示例**：以下两个命令的区别

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed_%E4%B8%A4%E4%B8%AA%E5%91%BD%E4%BB%A4%E7%9A%84%E5%8C%BA%E5%88%AB.jpg)

**sed编辑命令总结**

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed编辑命令总结.jpg)

#### sed命令示例

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/sed命令示例.jpg)





### awk

awk介绍

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk介绍.jpg)

awk简单用法

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk简单用法.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk_root首行匹配.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk-f.jpg)

awk_script语法

![](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/img/shell/awk_script%E8%AF%AD%E6%B3%95.jpg)

上述执行过程：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk_script语法.jpg)

**awk示例：筛选ip地址**：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk筛选信息.jpg)

BEGIN 和 END

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk_BEGIN_END.jpg)

awk模式匹配：

*使用正则表达式：*

![](https://cdn.jsdelivr.net/gh/mo-xiaoxiu/imagefrommyblog@main/img/shell/awk_%E6%A8%A1%E5%BC%8F%E5%8C%B9%E9%85%8D.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk_模式匹配.jpg)

*使用布尔表达式：*

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk_模式匹配2.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk_模式匹配3.jpg)

**字段分隔符、重定向和管道**

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk_字段分隔符、重定向和管道.jpg)

*更多awk的操作：*

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/awk_更多awk.jpg)









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

