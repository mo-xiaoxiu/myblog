---
title: "Lambda表达式"
date: 2021-10-22T10:03:59+08:00
draft: true
---

# lambda

**lambda语法：**

* `[捕捉变量](传递参数)mutable->返回值{函数体语句}`
  * **捕捉变量**：捕捉lambda表达式所在块（父作用域）的变量，一般情况下，在lambda表达式中是常量，不可修改
  * **传递参数**：类似于函数的参数列表
  * **`mutable`**：可变的。表达式捕获的变量可变
  * `->返回值`：利用追踪返回值的类型，来得到函数的返回值
  * `{函数体语句}`：顾名思义

## lambda与仿函数

*实例代码：*

```cpp
class A{
public:
  A(){}
  int operator()(int x){return x};
  ~A(){}
};

int main(){
  int x=10;
  A a;
  int tmp_1=a(x);
  auto tmp_2=[](x)->int{return x};
  cout<<“tmp_1 = ”<<tmp_1<<“\n”<<“tmp_2 = ”<<tmp_2<<endl;
}
```
 

 lambda表达式和这里的仿函数是等价的

 **lambda可以视为仿函数的“语法糖”**

 lambda函数在C++标准中默认是内联的

 可以像局部函数那样使用它

```C++
int Dosomething(int);
int DoWorks(int times){
  int i;
  int x;
  try{
    for(i=0;i<times;i++){
      x+=Dosmething(i);
    }
  }
  catch(...){
    x=0;
  }
  const int y=[=]{
    int i,val;
    try{
      for(i=0;i<times;i++){
        val+=Dosomething(i);
      }
      catch(...){
        val=0;
      }
      return val;
    }
  }();
}
```

 *上述函数体内两个try（）catch语句实际上是一样的*

  1. **函数功能中，x在初始化时一直在修改，不能声明为const**
  2. **lambda函数调用，仅需要其返回值，于是可以定义为常量的**
  3. **lambda函数：不需要为这段代码逻辑取函数名**

## lambda的[]

* []：什么都不捕获
* [=]：以**值传递**捕获父作用域所有的变量
* [&]：以**引用传递**捕获父作用域所有的变量
* [&a,b]：以引用传递捕获变量a，以值传递捕获变量b
* **方括号中捕获的变量传递方式不能重叠，捕获的变量也不能重叠**

## lambda的mutable

**默认情况下，lambda函数是一个const函数**
*实例代码：*

```C++
int main(){
  int a=10;
  auto const_value_lambda=[a]()->int{a=3;};  // 编译不通过
  auto const_ref_lambda=[&a]()->int{a=3;}  // 编译通过
  auto noconst_value_lambda=[a]()mutable->int{a=3;};  // 编译通过
  const_func_lambda=[](a);  // 编译通过
  
}
```

1. 以值传递的方式捕获变量a，并在函数体内修改a的值，编译不通过，因为**以值传递捕获的变量在函数体内默认是常量**，无法修改
2. 以引用的方式捕获变量a，在函数体内修改它，编译通过，这是由引用的性质决定的。**引用的本质是指针常量，指针的指向不可以修改，指针指向的值可以修改，常量修饰的是指针本身，除了改变它的指向（地址），改变值是允许的**
3. 上述相同的功能，lambda函数加上了mutable（可变的），其const在函数体内可以修改
4. 相同的功能，变量a作为函数参数传入是没有问题的

### 有关于第三点mutable

**对于常量成员函数，不能在函数体内改变class中任意成员变量**

**lambda的捕获列表中的变量都会成为等价仿函数的成员变量**



## lambda类型

lambda的类型被定义为“闭包”的类，每个lambda表达式会产生一个闭包类型的临时对象--**右值**

### 函数指针

C++11标准允许lambda表达式是向函数指针的转换

**前提：lambda函数没有捕捉任何变量，函数指针所示的函数原型，必须和lambda函数有相同的调用方式**

即：

```C++
auto p=[](int x,int y)->int{return x + y;}
typedef int (*var_1)(int x,int y);
typedef int (*var_2)(int x);

var_1 x1;
x1=p;  // 编译通过

var_2=p;  // 编译失败

decltype(p) x2=p;
decltype(p) x3=x1;  // 编译不通过

```

* `x1=p`：定义了一个函数指针，接收两个int类型参数，定义了相同类型的变量x1，将lambda函数所得的变量p赋值于它；接收参数数量和类型相同，**lambda函数类型转化为接收参数相同的函数指针类型**，编译通过
* `var_2=p`：定义了一个函数指针，接收一个int类型参数，将lambda函数获得的变量赋值于它的时候编译不通过，原因是**接收参数个数不同**
* 可以使用`decltype`来获得lambda函数的类型
* **将函数指针转化为lambda是不成功的**

---

## lambda的更多讨论

* lambda不是仿函数的完全替代品：在现行C++标准中，**捕捉列表仅能捕捉父作用域的自动变量，而对超出这个范围的变量是不能捕捉的**
* 仿函数可以被定义：**在不同的作用域范围内取得初始值**。这使得仿函数天生具有了跨作用域共享的特性
* lambda函数被设计的目的：**就地书写，就地使用、局部封装，局部共享**
* **所有捕捉的变量在lambda声明一开始就被拷贝，且拷贝的值不可被修改**，如果不想带来过大的传递开销的话，可以采用**引用传递**的方式传递参数
* 如果我们的代码存在异步操作，或者其他可能改变对象的任何操作，我们必须确定其在父作用域及lambda函数间的关系，否则也会产生一些错误



