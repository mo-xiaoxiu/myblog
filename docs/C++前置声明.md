# C++前置声明

在网上看到C++前置声明一般用于解决文件中头文件互相引用的问题.

即下面的这种情况：

```cpp title="A.h"
#pragma once
#include "B.h"

class A{
        public:
                A();
                ~A();
        private:
                B b;
};

```

```cpp title="B.h"
#pragma once
#include "A.h"

class B{
        public:
                B();
                ~B();
        private:
                A a;
};

```

```cpp title="A.cpp"
#include <iostream>
#include "A.h"

A::A() {
	b = new B;
	std::cout<<"This is A."<<std::endl;
}

A::~A() {
	delete b;
}
```

```cpp title="B.cpp"
#include <iostream>
#include "B.h"

B::B() {
	a = new A;
	std::cout<<"This is B."<<std::endl;
}

B::~B() {
	delete a;
}
```

上述`A.h`引用了`B.h`，`B.h`引用了`A.h`并都在各自的源文件中使用了包含头文件的对象

## 实验

我在`Centos Liunx 8`中，把上述文件写在一个叫做`false`（表示错误示范）的文件中：

```
[zjp@localhost false]$ ls
A_test  B_test  build  CMakeLists.txt  test.cpp
[zjp@localhost false]$ ls A_test/
A.cpp  A.h
[zjp@localhost false]$ ls B_test/
B.cpp  B.h
```

`test.cpp`就是对A和B的包含：

```cpp title="test.cpp"
#include <iostream>
#include "./A_test/A.h"
#include "./B_test/B.h"

int main () {
	return 0;
}
```

如上所示，书写了一个`CMakeLists.txt`用于cmake编译，内容如下：

```cmake
cmake_minimum_required(VERSION 3.10)
project(test_frontDecl)

set(CMAKE_VERBOSE_MAKEFILE ON)

set(CMAKE_CXX_FLAGS "-std=c++11")

include_directories("./B_test" "./A_test")

set(SRC_FILES test.cpp)
set(PROJECT_SOURCES ${SRC_FILES})

add_executable(${PROJECT_NAME} ${PROJECT_SOURCES})
```

接下来执行cmake，并make：

```
cd build/
cmake ../
make
```

可以发现如下错误：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/front_decl_1.jpg)

---

编译错误在意料之中，之后使用前置声明看看效果如何

现在将`A.h`和`A.cpp`修改如下：

```cpp title="A.h"
#pragma once
//#include "B.h" //取消头文件的包含

class B; //使用前置声明

class A{
	public:
		A();
		~A();
	private:
		B* b; //将“包含该对象”改为“包含该对象的指针”
};
```

```cpp title="A.cpp"
#include <iostream>
#include "A.h"
#include "B.h" //在源文件中包含B的头文件

A::A() {
	b = new B;
	std::cout<<"This is A."<<std::endl;
}

A::~A() {
	delete b;
}
```

同理，`B.h`和`B.cpp`也是这样修改处理

再执行编译，效果如下：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/front_decl_2.jpg)

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/front_decl_3.jpg)

可以发现编译成功，并且可以正常执行

---

## 说法

可以初步得出结论：使用前置声明确实可以解决文件之间头文件相互包含的编译错误问题

其实错误的原因也很容易想到：文件A需要包含文件B，而文件B需要包含文件A，在编译的过程就是一个“鸡生蛋，蛋生鸡”的问题

那为什么前置声明可以解决呢？

* 首先，`class B;`在头文件`A.h`中是前置声明，只是告诉编译器有这个类，不会去确定这个类的具体实现和实际大小
* 其次，在类A中包含类B的指针（或者引用），编译器只需要多分配给类A大小8字节（x64）的内存，具体B的大小要到创建对象A的时候调用构造函数时，才会确定B的大小

### 优点

**在头文件声明该类，在源文件包含该类**

* 在这个例子中，修改完类之后，由于前置声明，所以包含该类的头文件不需要重新编译
* 类中包含的对象是指针或者引用，而不是对象本身，减小了内存占用
* 节省了编译时间，避免了多余的头文件展开；节省了很多不必要的重新编译时间，头文件包含无关的改动会被重新编译多次

### 缺点

> 1. 前置声明隐藏了依赖关系，头文件改动时，用户的代码会跳过必要的重新编译过程。
> 2. 前置声明可能会被库的后续更改所破坏。前置声明函数或模板有时会妨碍头文件开发者变动其 API。 例如扩大形参类型，加个自带默认参数的模板形参等等。
> 3. 前置声明来自命名空间 std:: 的 symbol 时，其行为未定义（在 C++11 标准规范中明确说明）。
> 4. 前置声明了不少来自头文件的 symbol 时，就会比单单一行的 include 冗长。
> 5. 仅仅为了能前置声明而重构代码（比如用指针成员代替对象成员）会使代码变得更慢更复杂。
> 6. 很难判断什么时候该用前置声明，什么时候该用 #include ，某些场景下面前置声明和 #include 互换以后会导致意想不到的结果。
>
> 原文链接：https://blog.csdn.net/qq_36631379/article/details/119380251

