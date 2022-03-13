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

在脚本中使用这些参数：
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
* 第七行表示没有加双引号的"$@"：与"$*"没有差别
* 第八行表示加上双引号的"$@"与加上双引号的"$*"的差别："$*"是分别输出参数；"$@"是单字符串输出参数
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

