# C++Singleton对象模型探索

前段时间思考到一个问题，就是有关于C++对象模型在实现懒汉式单例时是如何做的。引发了我强烈的思考，以下是初步探索，不过可以得到初步的答案。

## 讨论的单例模式

```c++
#include <iostream>
using namespace std;

//singleton
class Singleton{
	private:
		Singleton(){
			cout << "Singleton constructor called..." << endl;
		}
	public:
		~Singleton(){
			cout << "Singleton deconstructor called..." << endl;
		}
		Singleton(Singleton&) = delete;
		Singleton& operator=(const Singleton&) = delete;

		static Singleton& getInstance(){
			static Singleton st;
			return st;
		}
};

void test()
{
	Singleton::getInstance();
}

int main()
{
	test();
	return 0;
}
```

这里所说的单例模式，是在单例类内实现一个返回静态局部变量的方法，在这个方法中，使用调用即生成静态局部变量的方式，在C++11的前提下，保证生成的对象已经构造初始化完成，以此解决单例本身存在的线程安全和内存问题。详见如下：

[C++单例模式](https://www.zjp7071.cn/C%2B%2B%E5%8D%95%E4%BE%8B%E6%A8%A1%E5%BC%8F/)

## 单例对象在哪个段呢？

在查阅的相关资料表示，C++11保证静态局部生成即完成初始化，那么其在用户进程的启动之前是怎么样的呢？

**使用objdump工具对其进行探索：**

1. 生成`.o`文件

   ```shell
   g++ -c test.cpp
   ```

2. 使用objdump -d输出需要执行的指令

   ```shell
   objdump -d test.o
   ```

3. 可以得到如下输出：

   ```
   test.o：     文件格式 elf64-x86-64
   
   
   Disassembly of section .text:
   
   0000000000000000 <main>:
      0:	f3 0f 1e fa          	endbr64 
      4:	55                   	push   %rbp
      5:	48 89 e5             	mov    %rsp,%rbp
      8:	e8 00 00 00 00       	call   d <main+0xd>
      d:	b8 00 00 00 00       	mov    $0x0,%eax
     12:	5d                   	pop    %rbp
     13:	c3                   	ret    
   
   0000000000000014 <_Z41__static_initialization_and_destruction_0ii>:
     14:	f3 0f 1e fa          	endbr64 
     18:	55                   	push   %rbp
     19:	48 89 e5             	mov    %rsp,%rbp
     1c:	48 83 ec 10          	sub    $0x10,%rsp
     20:	89 7d fc             	mov    %edi,-0x4(%rbp)
     23:	89 75 f8             	mov    %esi,-0x8(%rbp)
     26:	83 7d fc 01          	cmpl   $0x1,-0x4(%rbp)
     2a:	75 3b                	jne    67 <_Z41__static_initialization_and_destruction_0ii+0x53>
     2c:	81 7d f8 ff ff 00 00 	cmpl   $0xffff,-0x8(%rbp)
     33:	75 32                	jne    67 <_Z41__static_initialization_and_destruction_0ii+0x53>
     35:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 3c <_Z41__static_initialization_and_destruction_0ii+0x28>
     3c:	48 89 c7             	mov    %rax,%rdi
     3f:	e8 00 00 00 00       	call   44 <_Z41__static_initialization_and_destruction_0ii+0x30>
     44:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 4b <_Z41__static_initialization_and_destruction_0ii+0x37>
     4b:	48 89 c2             	mov    %rax,%rdx
     4e:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 55 <_Z41__static_initialization_and_destruction_0ii+0x41>
     55:	48 89 c6             	mov    %rax,%rsi
     58:	48 8b 05 00 00 00 00 	mov    0x0(%rip),%rax        # 5f <_Z41__static_initialization_and_destruction_0ii+0x4b>
     5f:	48 89 c7             	mov    %rax,%rdi
     62:	e8 00 00 00 00       	call   67 <_Z41__static_initialization_and_destruction_0ii+0x53>
     67:	90                   	nop
     68:	c9                   	leave  
     69:	c3                   	ret    
   
   000000000000006a <_GLOBAL__sub_I_main>:
     6a:	f3 0f 1e fa          	endbr64 
     6e:	55                   	push   %rbp
     6f:	48 89 e5             	mov    %rsp,%rbp
     72:	be ff ff 00 00       	mov    $0xffff,%esi
     77:	bf 01 00 00 00       	mov    $0x1,%edi
     7c:	e8 93 ff ff ff       	call   14 <_Z41__static_initialization_and_destruction_0ii>
     81:	5d                   	pop    %rbp
     82:	c3                   	ret    
   
   Disassembly of section .text._ZN9SingletonC2Ev:
   
   0000000000000000 <_ZN9SingletonC1Ev>:
      0:	f3 0f 1e fa          	endbr64 
      4:	55                   	push   %rbp
      5:	48 89 e5             	mov    %rsp,%rbp
      8:	48 83 ec 10          	sub    $0x10,%rsp
      c:	48 89 7d f8          	mov    %rdi,-0x8(%rbp)
     10:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 17 <_ZN9SingletonC1Ev+0x17>
     17:	48 89 c6             	mov    %rax,%rsi
     1a:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 21 <_ZN9SingletonC1Ev+0x21>
     21:	48 89 c7             	mov    %rax,%rdi
     24:	e8 00 00 00 00       	call   29 <_ZN9SingletonC1Ev+0x29>
     29:	48 8b 15 00 00 00 00 	mov    0x0(%rip),%rdx        # 30 <_ZN9SingletonC1Ev+0x30>
     30:	48 89 d6             	mov    %rdx,%rsi
     33:	48 89 c7             	mov    %rax,%rdi
     36:	e8 00 00 00 00       	call   3b <_ZN9SingletonC1Ev+0x3b>
     3b:	90                   	nop
     3c:	c9                   	leave  
     3d:	c3                   	ret    
   
   Disassembly of section .text._ZN9SingletonD2Ev:
   
   0000000000000000 <_ZN9SingletonD1Ev>:
      0:	f3 0f 1e fa          	endbr64 
      4:	55                   	push   %rbp
      5:	48 89 e5             	mov    %rsp,%rbp
      8:	48 83 ec 10          	sub    $0x10,%rsp
      c:	48 89 7d f8          	mov    %rdi,-0x8(%rbp)
     10:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 17 <_ZN9SingletonD1Ev+0x17>
     17:	48 89 c6             	mov    %rax,%rsi
     1a:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 21 <_ZN9SingletonD1Ev+0x21>
     21:	48 89 c7             	mov    %rax,%rdi
     24:	e8 00 00 00 00       	call   29 <_ZN9SingletonD1Ev+0x29>
     29:	48 8b 15 00 00 00 00 	mov    0x0(%rip),%rdx        # 30 <_ZN9SingletonD1Ev+0x30>
     30:	48 89 d6             	mov    %rdx,%rsi
     33:	48 89 c7             	mov    %rax,%rdi
     36:	e8 00 00 00 00       	call   3b <_ZN9SingletonD1Ev+0x3b>
     3b:	90                   	nop
     3c:	c9                   	leave  
     3d:	c3                   	ret    
   
   Disassembly of section .text._ZN9Singleton11getInstanceEv:
   
   0000000000000000 <_ZN9Singleton11getInstanceEv>:
      0:	f3 0f 1e fa          	endbr64 
      4:	55                   	push   %rbp
      5:	48 89 e5             	mov    %rsp,%rbp
      8:	41 54                	push   %r12
      a:	53                   	push   %rbx
      b:	0f b6 05 00 00 00 00 	movzbl 0x0(%rip),%eax        # 12 <_ZN9Singleton11getInstanceEv+0x12>
     12:	84 c0                	test   %al,%al
     14:	0f 94 c0             	sete   %al
     17:	84 c0                	test   %al,%al
     19:	74 5f                	je     7a <_ZN9Singleton11getInstanceEv+0x7a>
     1b:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 22 <_ZN9Singleton11getInstanceEv+0x22>
     22:	48 89 c7             	mov    %rax,%rdi
     25:	e8 00 00 00 00       	call   2a <_ZN9Singleton11getInstanceEv+0x2a>
     2a:	85 c0                	test   %eax,%eax
     2c:	0f 95 c0             	setne  %al
     2f:	84 c0                	test   %al,%al
     31:	74 47                	je     7a <_ZN9Singleton11getInstanceEv+0x7a>
     33:	41 bc 00 00 00 00    	mov    $0x0,%r12d
     39:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 40 <_ZN9Singleton11getInstanceEv+0x40>
     40:	48 89 c7             	mov    %rax,%rdi
     43:	e8 00 00 00 00       	call   48 <_ZN9Singleton11getInstanceEv+0x48>
     48:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 4f <_ZN9Singleton11getInstanceEv+0x4f>
     4f:	48 89 c2             	mov    %rax,%rdx
     52:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 59 <_ZN9Singleton11getInstanceEv+0x59>
     59:	48 89 c6             	mov    %rax,%rsi
     5c:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 63 <_ZN9Singleton11getInstanceEv+0x63>
     63:	48 89 c7             	mov    %rax,%rdi
     66:	e8 00 00 00 00       	call   6b <_ZN9Singleton11getInstanceEv+0x6b>
     6b:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 72 <_ZN9Singleton11getInstanceEv+0x72>
     72:	48 89 c7             	mov    %rax,%rdi
     75:	e8 00 00 00 00       	call   7a <_ZN9Singleton11getInstanceEv+0x7a>
     7a:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 81 <_ZN9Singleton11getInstanceEv+0x81>
     81:	eb 26                	jmp    a9 <_ZN9Singleton11getInstanceEv+0xa9>
     83:	f3 0f 1e fa          	endbr64 
     87:	48 89 c3             	mov    %rax,%rbx
     8a:	45 84 e4             	test   %r12b,%r12b
     8d:	75 0f                	jne    9e <_ZN9Singleton11getInstanceEv+0x9e>
     8f:	48 8d 05 00 00 00 00 	lea    0x0(%rip),%rax        # 96 <_ZN9Singleton11getInstanceEv+0x96>
     96:	48 89 c7             	mov    %rax,%rdi
     99:	e8 00 00 00 00       	call   9e <_ZN9Singleton11getInstanceEv+0x9e>
     9e:	48 89 d8             	mov    %rbx,%rax
     a1:	48 89 c7             	mov    %rax,%rdi
     a4:	e8 00 00 00 00       	call   a9 <_ZN9Singleton11getInstanceEv+0xa9>
     a9:	5b                   	pop    %rbx
     aa:	41 5c                	pop    %r12
     ac:	5d                   	pop    %rbp
     ad:	c3                   	ret    
   
   ```

4. 在所有section信息筛选bss段

   ```shell
   zjp@zjp-Ubuntu:~/test/test_singletonMem$ objdump -D test.o | grep '.bss'
   Disassembly of section .bss:
   Disassembly of section .bss._ZZN9Singleton11getInstanceEvE2st:
   Disassembly of section .bss._ZGVZN9Singleton11getInstanceEvE2st:
   ```

5. 在所有section信息筛选data段

   ```shell
   zjp@zjp-Ubuntu:~/test/test_singletonMem$ objdump -D test.o | grep '.data'
   Disassembly of section .rodata:
   0000000000000000 <.rodata>:
   Disassembly of section .data.rel.local.DW.ref.__gxx_personality_v0:
   ```

进一步的，我将程序进行以下的修改，验证一下**静态局部变量**和**类成员局部变量**以及**类成员函数中的静态局部变量**的bss段和data段：

```c++
#include <iostream>
using namespace std;

class Singleton{
	private:
		Singleton(){
			cout << "Singleton constructor called..." << endl;
		}
	public:
		~Singleton(){
			cout << "Singleton deconstructor called..." << endl;
		}
		Singleton(Singleton&) = delete;
		Singleton& operator=(const Singleton&) = delete;

		static Singleton& getInstance(){
			static Singleton st;
			return st;
		}
};

class TestNormal{
public:
	int normalFunc(){ //static local var in class member function
		static int m;
		return m;
	}	
};

int main()
{
	Singleton::getInstance();
	static int m; //normal local var
	TestNormal tm;
	tm.normalFunc();
	return 0;
}
```

使用objdump进行验证：

```shell
zjp@zjp-Ubuntu:~/test/test_singletonMem$ objdump -t test.o | grep ".bss"
0000000000000000 l    d  .bss	0000000000000000 .bss
0000000000000000 l     O .bss	0000000000000001 _ZStL8__ioinit
0000000000000004 l     O .bss	0000000000000004 _ZZ4mainE1m
0000000000000000 u     O .bss._ZZN9Singleton11getInstanceEvE2st	0000000000000001 _ZZN9Singleton11getInstanceEvE2st
0000000000000000 u     O .bss._ZGVZN9Singleton11getInstanceEvE2st	0000000000000008 _ZGVZN9Singleton11getInstanceEvE2st
0000000000000000 u     O .bss._ZZN10TestNormal10normalFuncEvE1m	0000000000000004 _ZZN10TestNormal10normalFuncEvE1m
zjp@zjp-Ubuntu:~/test/test_singletonMem$ 

...

zjp@zjp-Ubuntu:~/test/test_singletonMem$ objdump -t test.o | grep ".data"
0000000000000000 l    d  .rodata	0000000000000000 .rodata
0000000000000000  w    O .data.rel.local.DW.ref.__gxx_personality_v0	0000000000000008 .hidden DW.ref.__gxx_personality_v0
zjp@zjp-Ubuntu:~/test/test_singletonMem$ 

```

可以看到，在都**没有初始化**的时候，类成员的静态局部变量没有出现在bss段或者data段，而是返回这个静态局部变量的成员函数在bss段，并都在后缀的地方表示返回的值（静态局部对象）；在`Singleton`的`getInstance()`为什么会出现两个呢，我猜测是第一个表示的是实际的大小，第二个则可能是对齐之后的偏移量，可能是用于表示对Singleton这个类的实例化对象的大小的一个预值吧。

我们看一下是否申明多个静态局部变量之后会有所改变：

```c++
#include <iostream>
using namespace std;

//singleton
class Singleton{
	private:
		Singleton(){
			cout << "Singleton constructor called..." << endl;
		}
	public:
		~Singleton(){
			cout << "Singleton deconstructor called..." << endl;
		}
		Singleton(Singleton&) = delete;
		Singleton& operator=(const Singleton&) = delete;

		static Singleton& getInstance(){
			static Singleton st;
			return st;
		}
};

class TestNormal{
public:
	int normalFunc(){
		static double m;
		static int m2;
		return m2;
	}	
	int normalFunc1(){
		static int m3;
		return m3;
	}
};

int main()
{
	Singleton::getInstance();
	static double m;
	static int m2;
	cout << "size of Singleton: " << sizeof(Singleton::getInstance()) << endl;
	TestNormal tm;
	tm.normalFunc();
	tm.normalFunc1();
	return 0;
}
```

```shell
zjp@zjp-Ubuntu:~/test/test_singletonMem$ objdump -t test.o | grep ".bss"
0000000000000000 l    d  .bss	0000000000000000 .bss
0000000000000000 l     O .bss	0000000000000001 _ZStL8__ioinit
0000000000000008 l     O .bss	0000000000000008 _ZZ4mainE1m
0000000000000010 l     O .bss	0000000000000004 _ZZ4mainE2m2
0000000000000000 u     O .bss._ZZN9Singleton11getInstanceEvE2st	0000000000000001 _ZZN9Singleton11getInstanceEvE2st
0000000000000000 u     O .bss._ZGVZN9Singleton11getInstanceEvE2st	0000000000000008 _ZGVZN9Singleton11getInstanceEvE2st
0000000000000000 u     O .bss._ZZN10TestNormal10normalFuncEvE2m2	0000000000000004 _ZZN10TestNormal10normalFuncEvE2m2
0000000000000000 u     O .bss._ZZN10TestNormal11normalFunc1EvE2m3	0000000000000004 _ZZN10TestNormal11normalFunc1EvE2m3
zjp@zjp-Ubuntu:~/test/test_singletonMem$ 

```

我们可以发现，并不是所有的对于静态局部变量的声明都会在bss段，只有使用到的对象才会存在。

那么如果对所有静态局部对象都进行初始化呢（除了Singleton）：

```c++
#include <iostream>
using namespace std;

//singleton
class Singleton{
	private:
		Singleton(){
			cout << "Singleton constructor called..." << endl;
		}
	public:
		~Singleton(){
			cout << "Singleton deconstructor called..." << endl;
		}
		Singleton(Singleton&) = delete;
		Singleton& operator=(const Singleton&) = delete;

		static Singleton& getInstance(){
			static Singleton st;
			return st;
		}
};

class TestNormal{
public:
	int normalFunc(){
		static double m = 8.0; //init
		return m;
	}	
	int normalFunc1(){
		static int m3 = 8; //init
		return m3;
	}
};

int main()
{
	Singleton::getInstance();
	static double m = 8.0; //init
	cout << "size of Singleton: " << sizeof(Singleton::getInstance()) << endl;
	TestNormal tm;
	tm.normalFunc();
	tm.normalFunc1();
	return 0;
}
```

```shell
zjp@zjp-Ubuntu:~/test/test_singletonMem$ objdump -t test.o | grep ".bss"
0000000000000000 l    d  .bss	0000000000000000 .bss
0000000000000000 l     O .bss	0000000000000001 _ZStL8__ioinit
0000000000000000 u     O .bss._ZZN9Singleton11getInstanceEvE2st	0000000000000001 _ZZN9Singleton11getInstanceEvE2st
0000000000000000 u     O .bss._ZGVZN9Singleton11getInstanceEvE2st	0000000000000008 _ZGVZN9Singleton11getInstanceEvE2st
zjp@zjp-Ubuntu:~/test/test_singletonMem$ 

```

现在只剩下Singleton的静态方法了。其他变量都在那里呢？我们看一下data段：

```shell
zjp@zjp-Ubuntu:~/test/test_singletonMem$ objdump -t test.o | grep ".data"
0000000000000000 l    d  .rodata	0000000000000000 .rodata
0000000000000000 l     O .data	0000000000000008 _ZZ4mainE1m
0000000000000000  w    O .data.rel.local.DW.ref.__gxx_personality_v0	0000000000000008 .hidden DW.ref.__gxx_personality_v0
0000000000000000 u     O .data._ZZN10TestNormal10normalFuncEvE1m	0000000000000008 _ZZN10TestNormal10normalFuncEvE1m
0000000000000000 u     O .data._ZZN10TestNormal11normalFunc1EvE2m3	0000000000000004 _ZZN10TestNormal11normalFunc1EvE2m3
zjp@zjp-Ubuntu:~/test/test_singletonMem$ 

```

可以看见，初始化完成的静态局部变量（包括静态成员方法返回对应的静态局部对象）会在data段

---

**初步结论：像这种经典的饿汉单例模式，静态成员方法返回的静态局部对象是在bss段，属于未初始化的“占位”操作**

<br>

## 在程序启动之后在内存空间中如何？

为了实时看到程序启动之后进程的内存空间布局，我们需要在程序结尾进行阻塞：

```c++
#include <iostream>
#include <unistd.h>
#include <stdio.h>
using namespace std;

//singleton
class Singleton{
	private:
		Singleton(){
			cout << "Singleton constructor called..." << endl;
		}
	public:
		~Singleton(){
			cout << "Singleton deconstructor called..." << endl;
		}
		Singleton(Singleton&) = delete;
		Singleton& operator=(const Singleton&) = delete;

		static Singleton& getInstance(){
			static Singleton st;
			return st;
		}
};

class TestNormal{
public:
	int normalFunc(){
		static double m = 8.0;
		cout << "normalFunc address: "<< &m << endl;
		return m;
	}	
	int normalFunc1(){
		static int m3 = 8;
		cout << "normalFunc1 address: "<< &m3 << endl;
		return m3;
	}
};

int main()
{
	Singleton::getInstance();
	cout << "Singleton address: "<< &(Singleton::getInstance()) << endl;
	static double m = 8.0;
	cout << "m address: " << &m << endl;
	TestNormal tm;
	tm.normalFunc();
	tm.normalFunc1();

	getchar();
	return 0;
}

```

分别取出他们的地址，并在运行时对虚拟内存空间进行查看：

1. 启动程序：

   ```shell
   ./a.out
   ```

2. 查看虚拟内存空间：

   ```shell
   ps -af | grep 'a.out' # use this cmd
   
   # like this
   zjp@zjp-Ubuntu:~/test/test_singletonMem$ ps -af | grep 'a.out'
   zjp        71850   71706  0 20:20 pts/1    00:00:00 ./a.out
   zjp        71858   69738  0 20:25 pts/0    00:00:00 grep --color=auto a.out
   zjp@zjp-Ubuntu:~/test/test_singletonMem$ 
   
   ```

   得到`a.out`的PID：71850

3. `pmap -X 71850`

   ![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20230115203107.png)

   ![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20230115203200.png)

从执行的结果可以看到，Singleton对象的地址在堆区之下、代码段之上，即在数据段，其他的非单例对象调用返回的静态局部变量在数据段，按照字节大小和调用顺序递增排列。

> 多次执行之后发现结果有个很奇怪的现象：Singleton都是在数据段之上152字节的地址，m的地址都是从数据段之上10开始顺序叠加递增。
>
> 为什么呢？

*这个需要进一步的探究。。。*