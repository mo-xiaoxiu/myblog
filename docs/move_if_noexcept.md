# move_if_noexcept

## 实验

* 环境：Centos Linux 8；gcc 8.5.0

```cpp title="test.cpp"
#include <iostream>
#include <vector>

class A{
	public:
		A() = default;
		A(const A& a) {
			std::cout<<"called copy constructor"<<std::endl;
		}
		A(A&& a) {
			std::cout<<"called move constructor"<<std::endl;
		}

		~A() = default;
};

int main(){
	std::vector<A> vec;
	int i = 0;
	for(;i < 5; i++)
		vec.emplace_back();

	return 0;
}
```

在终端进行测试：

```
g++ test.cpp
./a.out
```

编译结果：

```
called copy constructor
called copy constructor
called copy constructor
called copy constructor
called copy constructor
called copy constructor
called copy constructor
```

从上面的测试可以看出，该程序调用了拷贝构造函数调用了5次，没有一次是移动构造函数

**我们给移动构造加上保证不抛出异常noexcept**

```cpp title="test.cpp"
#include <iostream>
#include <vector>

class A{
	public:
		A() = default;
		A(const A& a) noexcept {
			std::cout<<"called copy constructor"<<std::endl;
		}
		A(A&& a) noexcept {
			std::cout<<"called move constructor"<<std::endl;
		}

		~A() = default;
};

int main(){
	std::vector<A> vec;
	int i = 0;
	for(;i < 5; i++)
		vec.emplace_back();

	return 0;
}
```

编译执行结果如下：

```
called move constructor
called move constructor
called move constructor
called move constructor
called move constructor
called move constructor
called move constructor
```

无一例外都调用了移动构造函数





## 分析

STL标准库，或者说遵循标准库编写原则的容器及其方法中，有支持移动语义的容器和方法。如`std::vector<T>`

以本例的`emplace_back()`为例，意思是将容器的最后一个元素替换成新的元素