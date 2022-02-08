---
title: "C++的RRTI"
date: 2021-09-27T17:06:48+08:00
draft: true
---

# C++的RRTI机制

## RRTI简介

**RRTI(Runtime Type Idenfitication)**，意思是**运行时识别类型**。这个机制是为了能**通过基类的指针或者引用找到子类的（真实类型）的指针或者引用**。但是功能不限于此

## typeid

要想了解**typeid**，首先要了解关于**虚函数和虚继承内存模型**

### 虚函数的内存模型

虚函数是体现多态性的关键。多态性在这个层面上，分为有虚函数的继承关系和没有虚函数的继承关系

#### 没有多态性的继承

*其实没有虚函数的继承就是白给，浪费表情*

```C++
// 基类
class Base{
    public:
    	void Function(){std::cout<<"This is Base's Fountion"<<std::endl;}
};

// 子类
class Derive:public Base{
    public:
    	void derive_Funtion(){std::cout<<"This is derive's Fountion"<<std::endl;}
};
```

这样简单的继承关系，只是简单的子类拥有父类的成员数据而已，无法体现多态。没有虚函数也就没有虚指针

#### 体现多态性的继承

```C++
// 基类
class Base{
    public:
    	Base(){}
    	virtual ~Base(){std::cout<<"This is Base deconstructor"<<std::endl;}
    
    	virtual void show(){std::cout<<"Base_show"<<std::endl;}
};

// 子类
class Derive:public Base{
    public:
    	Derive(){}
    	~Derive(){std::cout<<"This is Derive deconstructor"<<std::endl;}
    
    	void show()override {
            std::cout<<"Derive_show"<<std::endl;
        }
};
```

只要简单地加上`virtual`在析构函数前，使其变成虚析构函数即可实现多态。为了体现出内存模型，此处又加上一个虚函数

**内存模型：**

* 首先需要明确，空类的内存大小是占一个字节，成员函数不占类的大小，类的大小遵循字节对齐原则
* 虚函数会在类内生成虚指针，指向一个虚表（虚函数表），虚表中有各个类的虚函数地址，虚指针会对应的找到各类对象应该调用的虚函数
* 按照继承顺序，虚函数指针也是从上往下存放，在实例化对象时，会先存放子类的变量，再按照继承顺序存放父类的变量（这在**菱形继承**时体现）
* 虚函数指针指向的虚表也是按照继承关系，先父类后子类（父类按照继承时间顺序），每一个子类对应在虚表上的内容是由：**offset to top(n) + type_info to Derive + 虚函数地址** 组成的
  * **offset to top(n)：表示当前的虚指针相对于类开头的距离，距离是当前系统下虚指针的字节倍数，this指针加上这个偏移量就可以在实例化是快速找到对应的实际类型**
  * **type_info to Derive：**表示的是子类的对象，是一个指针类型，表示在此对应的子类的区块上数据类型都是Derive
  * **虚函数地址：**指向每一个虚函数，所有的函数都存放在代码区
* 如果一个子类同时继承了几个父类，分别生成几个虚指针，每个虚指针对应的虚函数表在检索虚函数时，从低地址往高地址方向看，第一个有多态性的函数地址先指向子类对应的虚函数；后面的虚指针在对应虚表上检索的时候遇到同一个多态性的函数地址，也是对应着子类那个函数，但是此时指向的是一个代码段，**这个代码段会将this指针（原来是对应父类）转换为Derive类型，计算出偏移量在指向子类对应的虚函数**，相当于一个中介，由于this指针不是同一个父类了，并且在地址位置上在人家的上一个父类的后面，所以要先做这些操作才能找到子类虚函数

其实有关于虚函数的内存模型还是有其他几种情况的，不过都是在遵循一些基本规律下的：

1. 父类的继承是按照继承顺序来的，那么实例化对象时，生成虚指针的顺序也是一样的
2. 生成子类对象，在内存中会按地址顺序（由于可能存放在栈上，所以地址位置高低不确定）先放置子类的对象，再按照向上的继承关系放置父类的对象
3. 不同父类的this指针在访问虚函数时，都是在内存上偏移寻找的，如果由于继承顺序，子类的虚函数被之前的父类“绑定”了，那之后的虚函数地址都需要转换（算出偏移量 + 转换this指针类型）

---

*“好了，再说就烦了”*

---

### 虚继承的内存模型

虚继承就是基类Base的成员数据与继承于它的子类都是共享的，不会因为实例化而造成像多继承那种方式在菱形继承上所带来的识别对象矛盾的状况

```C++
// Base
class Base{
    public:
    	Base(const B&){}
};

// Derive
class Derive:virtual Base{
    public:
    	Derive(){}
};
```

虚继承会生成虚指针，但是虚指针指向的虚表，不会有对应子类而已

**内存模型：**

* 生成的虚指针，指向的每个基类的虚表，但是这个虚表没有子类对应的虚函数
* **vbase_offset(n) + offset  to top(n)+ type_info to Derive：**
  * **vbase_offset(n)：**由于虚继承实例化对象时，并不知道虚继承的基类在哪，所以需要记录一下该基类的偏移量，以此来记录**基类的形式类型起始地址**
  * **type_info to Derive：**子类的类型
  * **offset to top(n)：表示当前的虚指针相对于类开头的距离，距离是当前系统下虚指针的字节倍数，this指针加上这个偏移量就可以在实例化时快速找到对应的实际类型**

---

### typeid详解

#### type_info

typeid返回值类型尾type_info

*type_info源码：*

```C++
class type_info
{
public:
    virtual ~type_info();

    const char* name() const _GLIBCXX_NOEXCEPT
    { return __name[0] == '*' ? __name + 1 : __name; }

#if !__GXX_TYPEINFO_EQUALITY_INLINE
    bool before(const type_info& __arg) const _GLIBCXX_NOEXCEPT;
    bool operator==(const type_info& __arg) const _GLIBCXX_NOEXCEPT;
#else
    #if !__GXX_MERGED_TYPEINFO_NAMES
        bool before(const type_info& __arg) const _GLIBCXX_NOEXCEPT
        { return (__name[0] == '*' && __arg.__name[0] == '*') ?
              __name < __arg.__name : __builtin_strcmp (__name, __arg.__name) < 0;
        }

        bool operator==(const type_info& __arg) const _GLIBCXX_NOEXCEPT
        {
            return ((__name == __arg.__name) ||
                (__name[0] != '*' && __builtin_strcmp (__name, __arg.__name) == 0));
        }
    #else
        bool before(const type_info& __arg) const _GLIBCXX_NOEXCEPT
        { return __name < __arg.__name; }

        bool operator==(const type_info& __arg) const _GLIBCXX_NOEXCEPT
        { return __name == __arg.__name; }
    #endif
#endif

    bool operator!=(const type_info& __arg) const _GLIBCXX_NOEXCEPT
    { return !operator==(__arg); }

#if __cplusplus >= 201103L
    size_t hash_code() const noexcept
    {
    #  if !__GXX_MERGED_TYPEINFO_NAMES
        return _Hash_bytes(name(), __builtin_strlen(name()),
             static_cast<size_t>(0xc70f6907UL));
    #  else
        return reinterpret_cast<size_t>(__name);
    #  endif
    }
#endif // C++11

    virtual bool __is_pointer_p() const;

    virtual bool __is_function_p() const;

    virtual bool __do_catch(const type_info *__thr_type, void **__thr_obj,
        unsigned __outer) const;

    virtual bool __do_upcast(const __cxxabiv1::__class_type_info *__target,
        void **__obj_ptr) const;

protected:
    const char *__name;

    explicit type_info(const char *__n): __name(__n) { }	// 构造函数受保护，不可直接实例化

private:
    type_info& operator=(const type_info&);	// 赋值函数和拷贝构造函数私有
    type_info(const type_info&);
};

```

#### typeid识别静态类型

* 一个任意的类型名
* 一个基本内置类型的**变量**，或指向基本内置类型的指针或引用
* 一个任意类型的指针（指针就是指针，本身不体现多态，多指针解引用才有可能会体现多态）
* 一个具体的对象实例，无论对应的类有没有多态都可以直接在编译器确定
* 一个指向没有多态的类对象的指针的解引用
* 一个指向没有多态的类对象的引用

**用法：typeid（x）.name()：**x是上述的类型或者变量

#### typeid识别动态类型

- 一个指向含有多态的类对象的指针的解引用
- 一个指向含有多态的类对象的引用

**记得多态性是指由虚函数的继承**

```C++
#include <iostream>
#include <string>
#include <vector>
#include <typeinfo>
#include <cxxabi.h>

const char* TypeToName(const char* name)
{
    const char* __name = abi::__cxa_demangle(name, nullptr, nullptr, nullptr);
    return __name;
}

class A
{
public:
    virtual ~A(){}
    
    void print()
    {
        std::cout << "A" << std::endl;
    }

    int a;
};

class B : virtual public A
{
public:
    void print()
    {
        std::cout << "B" << std::endl;
    }

    int b;
};

class C : virtual public A
{
public:
    void print()
    {
        std::cout << "C" << std::endl;
    }

    int c;
};

class D : public B, public C
{
public:
    void print()
    {
        std::cout << "D" << std::endl;
    }

    int d;
};

int main(int argc, char* argv[])
{
    D d;
    A* a_ptr = &d;
    B* b_ptr = &d;
    C* c_ptr = &d;

    std::cout << TypeToName(typeid(d).name()) << std::endl;
    std::cout << TypeToName(typeid(*a_ptr).name()) << std::endl;
    std::cout << TypeToName(typeid(*b_ptr).name()) << std::endl;
    std::cout << TypeToName(typeid(*c_ptr).name()) << std::endl;
}

```

*输出如下：*

```
D
D
D
D
```

## 几种类型转换

### static_cast

```c++
static_cast<type>(expre);
```

```C++
#include <iostream>

int main(int argc, char* argv[])
{
    int type_int = 10;
    float* float_ptr1 = &type_int; // int* -> float* 隐式转换无效(int -> float 可以)
    float* float_ptr2 = static_cast<float*>(&type_int); // int* -> float* 使用static_cast转换无效
    char* char_ptr1 = &type_int; // int* -> char* 隐式转换无效
    char* char_ptr2 = static_cast<char*>(&type_int); // int* -> char* 使用static_cast转换无效

    void* void_ptr = &type_int; // 任何指针都可以隐式转换为void*
    float* float_ptr3 = void_ptr; // void* -> float* 隐式转换无效
    float* float_ptr4 = static_cast<float*>(void_ptr); // void* -> float* 使用static_cast转换成功
    char* char_ptr3 = void_ptr; // void* -> char* 隐式转换无效
    char* char_ptr4 = static_cast<char*>(void_ptr); // void* -> char* 使用static_cast转换成功
}
```

* **`static_cast`是直接不允许不同类型的引用进行转换的，因为没有void类型引用可以作为中间介质，这点和指针是有相当大区别的**
* **不同的指针类型之间不允许直接转换，除非使用中介`void*`转换**
* **`static_cast`不能转换掉`expression`的`const`或`volitale`属性**

```C++
#include <iostream>

class A
{
public:
    int a;
};

class B
{
public:
    int b;
};

class C : public A, public B
{
public:
    int c;
};

int main(int argc, char* argv[])
{
    C c;
    A a = static_cast<A>(c); // 上行转换正常
    B b = static_cast<B>(c); // 上行转换正常

    C c_a = static_cast<C>(a); // 下行转换无效
    C c_b = static_cast<C>(b); // 下行转换无效
}

```

* 实行向上转型是完全安全的
* 对于没有多态性的继承来说，下行转换无效，它认为向下转型的类之间没有关联

*可以做如下修改*

```C++
class C : public A, public B
{
public:
    C()
    {
    }

    C(const A& v)	// 通过增加C的有参构造函数，传入的参数是父类A和B，以此来构建联系
    {
        a = v.a;
    }

    C(const B& v)
    {
        b = v.b;
    }

    int c;
};
```

#### 对于没有多态性的指针或引用

*直接看下面的例子：*

```C++
#include <iostream>

class A
{
public:
    int a;
};

class B
{
public:
    int b;
};

class C : public A, public B
{
public:
    int c;
};

int main(int argc, char* argv[])
{
    C c;

    A* a_ptr = static_cast<A*>(&c); // 上行指针转换正常
    B* b_ptr = static_cast<B*>(&c); // 上行指针转换正常
    A& a_ref = static_cast<A&>(c);  // 上行引用转换正常
    B& b_ref = static_cast<B&>(c);  // 上行引用转换正常
    
    C* c_ptra = static_cast<C*>(a_ptr); // 下行指针转换正常
    C* c_ptrb = static_cast<C*>(b_ptr); // 下行指针转换正常
    C& c_refa = static_cast<C&>(a_ref); // 下行引用转换正常
    C& c_refb = static_cast<C&>(b_ref); // 下行引用转换正常
    
    A a;
    B b;
    
    // 以下都能转换成功，说明static_cast根本就没有安全检查，只看到有继承关系就给转换了
    C* c_ptra = static_cast<C*>(&a);
    C* c_ptrb = static_cast<C*>(&b);
    C& c_refa = static_cast<C&>(a);
    C& c_refb = static_cast<C&>(b);
}

```

* `static_cast`没有类型安全检查

#### 对于有多态性的指针或引用

```C++
#include <iostream>

class A
{
public:
    virtual void print()
    {
        std::cout << "A" << std::endl;
    }
};

class B
{
public:
    virtual void print()
    {
        std::cout << "B" << std::endl;
    }
};

class C : public A, public B
{
public:
    virtual void print() override
    {
        std::cout << "C" << std::endl;
    }
};

int main(int argc, char* argv[])
{
    C c;

    A* a_ptr = static_cast<A*>(&c); // 上行指针转换正常
    B* b_ptr = static_cast<B*>(&c); // 上行指针转换正常
    a_ptr->print();                 // 输出C，符合多态的要求
    b_ptr->print();                 // 输出C，符合多态的要求

    A& a_ref = static_cast<A&>(c); // 上行引用转换正常
    B& b_ref = static_cast<B&>(c); // 上行引用转换正常
    a_ref.print();                 // 输出C，符合多态的要求
    b_ref.print();                 // 输出C，符合多态的要求
    
}

```

上行转换安全，来看下行转换：

```C++
int main(int argc, char* argv[])
{
    C c;
    A* a_ptr = static_cast<A*>(&c);
    B* b_ptr = static_cast<B*>(&c);
    A& a_ref = static_cast<A&>(c);
    B& b_ref = static_cast<B&>(c);

    // 先上行转换，再下行转换
    C* c_ptra = static_cast<C*>(a_ptr); // 下行指针转换正常
    C* c_ptrb = static_cast<C*>(b_ptr); // 下行指针转换正常
    c_ptra->print(); // 输出C，符合多态的要求
    c_ptrb->print(); // 输出C，符合多态的要求

    C& c_refa = static_cast<C&>(a_ref); // 下行引用转换正常
    C& c_refb = static_cast<C&>(b_ref); // 下行引用转换正常
    c_refa.print(); // 输出C，符合多态的要求
    c_refb.print(); // 输出C，符合多态的要求
}
```

先上行转换为基类的指针或引用类型，再用转换后的指针或引用向下转换为子类类型，是正常的

*再来看看不正常的：*

```C++
int main(int argc, char* argv[])
{
    A a;
    B b;

    C* c_ptra = static_cast<C*>(&a);
    C* c_ptrb = static_cast<C*>(&b);
    c_ptra->print(); // 正常输出A
    c_ptrb->print(); // 段错误

    C& c_refa = static_cast<C&>(a);
    C& c_refb = static_cast<C&>(b);
    c_refa.print(); // 正常输出A
    c_refb.print(); // 段错误
}

```

以上是直接定义了父类的类型变量，然后直接将父类类型向下转换，可以看到有部分输出还是正常的，但是有些地方出了错：**出错的原因在于，C子类继承父类的顺序是先A后B，按照上面讲过的虚函数内存模型来看，A实例化时调用的虚函数是C的虚函数，在内存中，通过A的虚指针访问到的虚函数地址是直接指向子类虚函数的；而后继承的B通过虚指针访问子类虚函数地址时，访问到的是一段用于转换的代码段，而你不能要求`static_cast`去帮你完成更多的任务--就像这个转换，所以出现了错误**

---

#### 总结

* 向上转换是安全的
* 指针类型不能直接转换，要通过`void*`
* 不允许转换引用，没有void&这种东西
* 对于没有多态性的指针或者引用类型，向上转是没有问题的，向下转是不会进行安全检查的
* 对于有多态性的指针或者引用类型，向上转同样没有问题，要想向下转通过先向上转，再向下转也是可以的；但是直接向下转不会检查，所以出错的概率太大，还是不要吧 : D

---



### const_cast

**const_cast只能转换引用和指针**

```C++
#include <iostream>

int main(int argc, char* argv[])
{
    int type_int = 100;
    float type_float = const_cast<float>(type_int);        // 错误，const_cast只能转换引用或者指针
    float* type_float_ptr = const_cast<float*>(&type_int); // 错误，从int* -> float* 无效
    float& type_float_ref = const_cast<float&>(type_int);  // 错误，从int& -> float& 无效
}
// 非const无需转
```

*再看看下面的例子：*

```C++
#include <iostream>

int main(int argc, char* argv[])
{
    const int type_const_int = 100;
    int* type_const_int_ptr = const_cast<int*>(&type_const_int); // 转换正确
    int& type_const_int_ref = const_cast<int&>(type_const_int);  // 转换正确
    
    *type_const_int_ptr = 10;
    std::cout << *type_const_int_ptr << std::endl; // 输出10
    std::cout << type_const_int << std::endl;      // 输出100，没有改变

    type_const_int_ref = 20;
    std::cout << type_const_int_ref << std::endl; // 输出20
    std::cout << type_const_int << std::endl;     // 输出100，没有改变

    // 以下三个输出结果一致，说明const_cast确实只是去除了一些属性，并没有重新搞快内存把需要转换的变量给复制过去
    std::cout << "&type_const_int:\t" << &type_const_int << std::endl;
    std::cout << "type_const_int_ptr:\t" << type_const_int_ptr << std::endl;
    std::cout << "&type_const_int_ref:\t" << &type_const_int_ref << std::endl;
}

```

可以看到，转换成功后，`type_const_int_ptr`和`type_const_int_ref`试图去改变`type_const_int`的值，但是只是改变了

自身的值，而对于`type_const_int`没有改变，甚至于三者的地址也原封不动

说明：**`const_cast`没有改变变量的常量性，只是去除了一些属性，使得可以改变生成变量的值，但是原来的值和地址都没有变**

不过试图改变原始变量的值是不可取的，不同环境可能会带来不一样的结果

---

### reinterpret_cast

用法：

```C++
reinterpret_cast<type-id>expression
```

接近于C风格的强制转换。它有一些注意事项：

1. type-id和expression中**必须有一个是指针或引用类型**（可以两个都是指针或引用，指针引用在一定场景下可以混用，但是建议不要这样做，编译器也会给出相应的警告）。
2. reinterpret_cast的第一种用途是**改变指针或引用的类型**
3. reinterpret_cast的第二种用途是**将指针或引用转换为一个整型，这个整型必须与当前系统指针占的字节相等**
4. reinterpret_cast的第三种用途是**将一个整型转换为指针或引用类型**
   可以先使用reinterpret_cast**把一个指针转换成一个整数，再把该整数转换成原类型的指针**，还可以得到原先的指针值（由于这个过程中type-id和expression始终有一个参数是整型，所以另一个必须是指针或引用，并且整型所占字节数必须与当前系统环境下指针占的字节数一致）
5. 使用reinterpret_cast强制转换过程**仅仅只是比特位的拷贝**，和C风格极其相似（但是reinterpret_cast不是全能转换，详见第1点），实际上reinterpret_cast的出现就是为了让编译器强制接受static_cast不允许的类型转换，因此使用的时候要谨而慎之
6. **不能转换掉expression的const或volitale属性**。

```C++
#include <iostream>

class A
{
public:
    int a;
};

class B
{
public:
    int b;
};

int main(int argc, char* argv[])
{
    float type_float = 10.1;

    long type_long = reinterpret_cast<long>(&type_float); // 正确，float* -> long（注意事项第3点）

    float* type_float_ptr = reinterpret_cast<float*>(type_long); // 正确，long -> float*（注意事项第4点）
    std::cout << *type_float_ptr << std::endl; // 正确，仍然输出10.1（注意事项第5点）

    long* type_long_ptr = reinterpret_cast<long*>(&type_float); // 正确，float* -> long*（注意事项第1点）
    
    char type_char = 'A';
    double& type_double_ptr = reinterpret_cast<double&>(type_char); // 正确，char -> double&（注意事项第4点）

    A a;
    B b;
    long a_long = reinterpret_cast<long>(&a); // 正确，A* -> long（注意事项第3点）
    A* a_ptr1 = reinterpret_cast<A*>(type_long); // 正确，long -> A*（注意事项第4点）
    A* a_ptr2 = reinterpret_cast<A*>(&b); // 正确，B* -> A*（注意事项第1点）
}
```

**注意看`type-id`和`expression`**

---

### dynamic_cast

* `dynamic_cast`向上转换和`static_cast`是完全一样的。
* 转换成功会返回指向类的指针或者引用，不成功返回NULL
* 转换的类型必须具有多态性，不具备多态性会再编译时报错
* 下行转换是类型安全的
* 不能用于实例化类对象的转换

```C++
#include <iostream>

class A
{
public:
    virtual void print()
    {
        std::cout << "A" << std::endl;
    }
};

class B
{
public:
    virtual void print()
    {
        std::cout << "B" << std::endl;
    }
};

class C : public A, public B
{
public:
    virtual void print()
    {
        std::cout << "C" << std::endl;
    }
};

int main(int argc, char* argv[])
{
    C c;

    // 第一组
    A* a_ptr = dynamic_cast<A*>(&c);
    B* b_ptr = dynamic_cast<B*>(&c);
    C* c_ptra = dynamic_cast<C*>(a_ptr); // 成功，类C具备多态性，可以使用dynamic_cast进行下行转换
    C* c_ptrb = dynamic_cast<C*>(b_ptr); // 成功，类C具备多态性，可以使用dynamic_cast进行下行转换
    // 以下输出内容一致
    std::cout << &c << std::endl;
    std::cout << c_ptra << std::endl;
    std::cout << c_ptra << std::endl;

    // 第二组：父类对象直接向下转换，会出现上述提到的虚函数表中虚函数地址转换的问题
    A a;
    B b;
    C* c_ptra1 = dynamic_cast<C*>(&a); // 编译正常（好的编译器会给你个警告），转换结果为nullptr，说明转换失败
    C* c_ptrb1 = dynamic_cast<C*>(&b); // 编译正常（好的编译器会给你个警告），转换结果为nullptr，说明转换失败
    // 以下输出内容一致，都是0，说明c_ptra1和c_ptrb1都是nullptr
    std::cout << c_ptra1 << std::endl;
    std::cout << c_ptrb1 << std::endl;
}
```

---

## 大总结

RRTI：

* `typeid`：typeid ( type ) .name ( )
  * 没有多态性：包括编译前和编译后
  * 有多态性
* 几种cast：
  * `dynamic_cast`：动态转换，类型安全
  * `static_cast`：同类型转换，无类型安全

---

