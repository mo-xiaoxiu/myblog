# 单例模式
## 何为单例模式
单例模式是设计模式的一种。提供**唯一**的类的实例化对象，具有**全局变量**的特点。任何位置都可以通过接口获得这个实例。

*具体应用场景：*
1. 设备管理器：有多个设备，只有一个设备管理器，用于管理驱动；
2. 数据池：缓存数据的数据结构，需要在一处写，多处读取或者是多处写多处读取。

## 单例模式实现
### 特点
* `static`：全局只有一个实例，构造函数设置为`private`
* 线程安全
* 禁止赋值和拷贝
* 使用`static`成员函数获取`static`成员

### 懒汉式
```cpp title="singleton.cpp"
#include <iostream>
using namespace std;

/*
 * version_1:
 * 存在的问题：
 * 	线程安全；
 * 	内存泄漏
 * */

class Singleton{
	private:
		Singleton() {
			cout<<"constructor called."<<endl;
		} //构造函数设置为私有属性

		Singleton(Singleton&) = delete; //禁止拷贝构造
		Singleton& operator= (const Singleton&) = delete; //禁止赋值

		//静态成员：唯一实例
		static Singleton* m_instance_ptr;
	
	public:
		~Singleton() {
			cout<<"deconstructor called"<<endl;
		}

		static Singleton* get_instance() {
			if(m_instance_ptr == nullptr) {
				m_instance_ptr = new Singleton;
			}
			return m_instance_ptr;
		} //静态成员函数获取唯一实例
};


//静态成员类外初始化
Singleton* Singleton::m_instance_ptr = nullptr;


int main() {
	Singleton* singleton_1 = Singleton::get_instance(); //获取第一个实例
	Singleton* singleton_2 = Singleton::get_instance(); //获取第二个实例
	
	return 0;
}
```
*运行结果如下：*
```
constructor called.
```
#### 存在问题：
1. 线程安全：假设现在有两个线程分别都在获取这个实例化对象，第一个线程在进入函数体`get_instance()`之后判断`m_instance_ptr`为空，于是创建实例化对象；第二个线程在第一个线程创建对象（还未创建完成）的同时也进入`get_instance()`函数体，同时也判断`m_instance_ptr`为空，于是也创建实例化对象；
2. 内存泄漏：从运行结果中来看，只调用了一次实例化构造，没有调用析构函数；只负责new对象，没有释放对象对应的内存

#### 问题解决：
1. 使用双检锁：在进入函数`get_instance()`之后，判断`m_instance_ptr`是否为空，再使用`lock_guard`加锁，之后再判断`m_instance_ptr`是否为空，再选择创建实例化对象。使用双检锁的好处是：只有在`m_instance_ptr`为空的时候才会加锁，省去不必要的加锁开销；使用`lock_guard`的好处是：在出作用域之后会自动解锁；
2. 使用智能指针`shared_ptr`管理唯一的静态对象

鉴于**懒汉式**简单直接的做法所带来的问题以及其解决方案，得到以下version2，*线程安全、无内存泄漏的*的懒汉式单例模式。

### 线程安全、无内存泄漏的懒汉式
```cpp title="singleton_version2.cpp"
#include <iostream>
#include <memory> //shared_ptr
#include <mutex> //锁
using namespace std;

/*
 * version_1:
 * 存在的问题：
 * 	线程安全；
 * 	内存泄漏
 * */

/*
 * version_2:
 * 解决问题：
 * 	线程安全：双检锁 lock_guard
 * 	内存泄漏：智能指针 shared_ptr
 * */

class Singleton{
	private:
		Singleton() {
			cout<<"constructor called."<<endl;
		} //构造函数设置为私有属性

		Singleton(Singleton&) = delete; //禁止拷贝构造
		Singleton& operator= (const Singleton&) = delete; //禁止赋值

		//静态成员：唯一实例
		//shared_ptr管理对象
		static shared_ptr<Singleton> m_instance_ptr;
	
        //具有全局变量特性的静态互斥量
		static mutex m_mutex; 
	public:
		~Singleton() {
			cout<<"deconstructor called"<<endl;
		}

		static shared_ptr<Singleton> get_instance() { //返回智能指针对象


			//双检锁：
			if(m_instance_ptr == nullptr) {
				lock_guard<mutex> lk(m_mutex); //加锁（出作用域自动解锁）
				if(m_instance_ptr == nullptr) {
					m_instance_ptr = shared_ptr<Singleton>(new Singleton);
				}
			}
			return m_instance_ptr;
		} //静态成员函数获取唯一实例
};


//静态成员类外初始化
shared_ptr<Singleton> Singleton::m_instance_ptr = nullptr;
mutex Singleton::m_mutex;


int main() {
	shared_ptr<Singleton> singleton_1 = Singleton::get_instance(); //获取第一个实例
	shared_ptr<Singleton> singleton_2 = Singleton::get_instance(); //获取第二个实例
	
	return 0;
}
```
*运行结果如下：*
```
constructor called.
deconstructor called
```
#### 存在问题：
1. 代码中使用智能指针，**用户也需要使用智能指针**；
2. 开销较大，代码量较多；
3. 双检锁有可能失效：在不同平台和编译器的情况下，语句的执行顺序可能并不完全按照代码的语句顺序执行。原来是先构造对象再进行赋值，在编译器执行顺序下有可能就是先赋值再构造对象，这样还是会带来线程安全问题。线程A进入函数体判断`m_instance_ptr`为空之后，加锁再判断指针是否为空之后构建对象，此时如果发生执行顺序的调换，编译器先赋值再构建对象就会造成此时的对象还是空的，而线程B进入函数体之后经过判断同样还是会创建对象

### 最终版本：返回局部变量的懒汉式
```cpp title="singleton_version3.cpp"
#include <iostream>
using namespace std;

/*
 *version_3: return static local var
 * */

class Singleton {
	private:
		Singleton() {
			cout<<"constructor called."<<endl;
		}
	
	public:
		~Singleton() {
			cout<<"deconstructor called."<<endl;
		}
		//delete copy constructor
		Singleton(Singleton&) = delete;
		//delete operator=
		Singleton& operator=(const Singleton&) = delete;

        //return static local var by ref
		static Singleton& get() {
			static Singleton instance_ptr;
			return instance_ptr;
		}
};

int main() {
	Singleton& instance_1 = Singleton::get(); //use ref to get the obj
	Singleton& instance_2 = Singleton::get();

	return 0;
}
```
*运行结果如下：*
```
constructor called.
deconstructor called.
```
以上方法又称为“Mayer‘s Singleton”。好处是：**保证了并发中获取的局部静态变量一定是经过初始化的**
#### 不建议返回指针
```cpp title="return by pointer"
        static Singleton* get() {
			static Singleton instance_ptr;
			return &instance_ptr;
		}
```
原因是：**无法避免用户使用`delete instance`使对象提前销毁**


## 单例模板
实现一次单例模式代码就可以一直复用。
### 特点：
1. 基类（单例模式）设置为模板；
2. 基类的构造函数设置为protected
3. 子类继承基类，基类以子类类型为 T
4. 子类将基类设置为友元类，以便于访问基类的构造函数（与 2 对应）
5. 子类的构造函数设置为private


```cpp title="CRTP"
#include <iostream>
using namespace std;

template<typename T>
class Singleton {
    public:
        static T& get_instance() {
            static T instance;
            return instance;
        }
        virtual ~Singleton() {
            cout<<"deconstructor called."<<endl;
        }
        Singleton(Singleton&) = delete;
        Singleton& operator= (const Singleton&) = delete;
    protected:
    //将基类的构造函数设置为protected，便于子类访问
        Singleton() {
            cout<<"constructor called."<<endl;
        }
};

class Derived:public Singleton<Derived> {
    //设置基类为友元类，才可以调用基类的构造函数
    friend class Singleton<Derived>;
    public:
        //delete copy constructor and operator=
        Derived(Derived&) = delete;
        Derived& operator=(const Derived&) = delete;
    private:
        Derived() = default; //将子类的构造函数设置为private，用户不可实例化对象
};

int main() {
    Derived& instance_1 = Derived::get_instance();
    Derived& instance_2 = Derived::get_instance();

    return 0;
}
```

## 另一种单例模板
### 特点
1. **在基类中设置一个helper struct（空类）名为`token`，用于构建基类的局部静态变量**
2. 子类可以将构造函数设置为public，前提是只允许`Derived(token)`构造
*这样就不需要将基类在子类中设置为友元类*


```cpp title="don't need to declare base class as friend class"
#include <iostream>
using namespace std;

template<typename T>
class Singleton{
    public:
    //noexcept()传入的参数必须是不跑出异常的可构造类型
    //构造过程不抛出异常
        static T& get_instance() noexcept(is_nothrow_constructible<T>::value) {
            static T instance{token()};
            //这里相当于：
            /*
            token t = token(); //构造token对象，并以此构造T对象
            static T instance(t);
            */
            return instance;
        }
        virtual ~Singleton() = default;
        Singleton(Singleton&) = delete;
        Singleton& operator=(const Singleton&) = delete;
    
    protected:
        struct token{}; //helper class:empty
        Singleton() noexcept = default;
};

class Derived:public Singleton<Derived> {
    public:
    //子类只允许此构造函数：需要传递结构体token才可以构造子类，这里必须设置为public  
        Derived(token) {
            cout<<"constructor called."<<endl;
        }
        ~Derived() {
            cout<<"deconstructor called."<<endl;
        }

        Derived(Derived&) = delete;
        Derived& operator=(const Derived&) = delete;
};

int main() {
    Derived& instance_1 = Derived::get_instance();
    Derived& instance_2 = Derived::get_instance();

    return 0;
}
```
### 补充
* std::is_nothrow_constructible<T, Args...>:**用于检查给定类型T是否为是带*参数集*的可构造类型**
* std::is_nothrow_constructible<T, Args...>::value:
    * 1 -- true：类型T可以从Args构造
    * 0 -- false：类型T无法从Args构造


测试程序


```cpp title="test.cpp"
// is_nothrow_constructible example
#include <iostream>
#include <type_traits>

struct A { };
struct B {
  B(){}
  B(const A&) noexcept {}
};

int main() {
  std::cout << std::boolalpha; //将 1 和 0 转换为 true 和 false
  std::cout << "is_nothrow_constructible:" << std::endl;
  std::cout << "int(): " << std::is_nothrow_constructible<int>::value << std::endl;
  std::cout << "A(): " << std::is_nothrow_constructible<A>::value << std::endl;
  std::cout << "B(): " << std::is_nothrow_constructible<B>::value << std::endl;
  std::cout << "B(A): " << std::is_nothrow_constructible<B,A>::value << std::endl;
  return 0;
}
```

*输出：*
```
is_nothrow_constructible:
int(): true
A(): true
B(): false
B(A): true
```

*将上述B的构造函数设置为不跑出异常的*

```cpp title="将B构造函数设置为不跑出异常的"
// is_nothrow_constructible example
#include <iostream>
#include <type_traits>

struct A { };
struct B {
  B() noexcept {}
  B(const A&) noexcept {}
};

int main() {
  std::cout << std::boolalpha;
  std::cout << "is_nothrow_constructible:" << std::endl;
  std::cout << "int(): " << std::is_nothrow_constructible<int>::value << std::endl;
  std::cout << "A(): " << std::is_nothrow_constructible<A>::value << std::endl;
  std::cout << "B(): " << std::is_nothrow_constructible<B>::value << std::endl;
  std::cout << "B(A): " << std::is_nothrow_constructible<B,A>::value << std::endl;
  return 0;
}
```

*输出：*
```
is_nothrow_constructible:
int(): true
A(): true
B(): true
B(A): true
```
<br>
<br>
<br>
<br>

## 总结
1. 单例模式特点：类具有一个唯一的static成员，能通过static成员函数获取这个成员；
2. 线程安全、无内存泄漏的懒汉式单例模式：在类中提供一个static成员函数在双检锁的保护下创建类的对象（new，使用智能指针管理对象）并返回
3. 最推荐懒汉式单例模式：在类中提供一个static成员函数，在此成员函数中生成static局部变量并返回
4. 一般的单例模板：
    * 基类：（模板）
        * 禁止赋值和拷贝
        * 构造函数设置为protected
        * virtual析构函数
        * static成员函数返回static局部变量
    * 子类：public继承子类类型的基类
        * friend声明基类
        * 构造函数设置为private
        * 禁止赋值和拷贝
5. 另一种单例模式：
    * 基类：（模板）
        * 禁止赋值和拷贝
        * protected的`struct token {}` 用于辅助构造
        * `static T& get_instance() noexcept(std::is_nothrow_constructible<T>::value)`：<br>
            函数体实现：<br>
            `static T instance{token()};`<br>
            `return instance;`
    * 子类：public继承子类类型的基类
        * 只允许`Derived(token)`构造，可以将其设置为public
6. `std::is_nothrow_constructible<T, Args...>`用于检查类型T是否可以由参数表Args得出
    * `std::is_nothrow_constructible<T, Args...>::value`
        * 1：true_type
        * 0：false_type