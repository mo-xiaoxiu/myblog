---
title: "何为指针"
date: 2021-09-07T18:27:05+08:00
draft: true
---

# 指针

指针和引用是C/C++语言中不可避免需要掌握的问题。

## 指针

指针在C/C++中是起到一个指向变量内存地址的作用，指针的表示方法为：`typename *p=&var`，`typename`表示的是变量的类型，可以是内置数据类型，也可以是自定义的数据类型；`&var`表示的是取某个变量的地址。
现在来区分几个概念：

### 指针数组&数组指针

* *指针数组：*先来谈一下我对指针数组概念的理解。指针数组的表示方法应该是:`int (*p)[10];`，表示的是一个能存放n个整型指针类型元素的数组；
* *数组指针：*数组指针表示的应该是一个用来维护数组的指针。表示为：`int *p[10]`。

### 指针常量和常量指针

* *指针常量：*

  * 表示：`int *const p=&a`
  * 解释：const常量修饰的整型指针，指针的指向不能修改，指针指向的值可以修    改

  ```C++
  int *const p=&b;  // erro
  a=100             // a(origin: 10)
  p=&a   // right
  ```

* *常量指针：*

  * 表示：`const int *p=&a`、`int const *p=&a`
  * 解释：const修饰的是指针p指向的整型数据,指针的指向可以修改，指针指向的值不可以修改

  ```C++
  int const *p=&a;  //  a=10
  a=100;            //  erro
  b=20;
  P=&b;             //  right
  ```

## 数组指针与其的退化

来看一下下面的代码：

```C++
    #include<iostream>
    using namespace std;
    
    //  quick sort
    void quick_sort(int*arr){  //  pointer
      // ...
      cout<<“In quick_sort sizeof(arr)=”<<sizeof(arr)<<endl;  //  res:  4(32bit)/8(64bit)
    }
    
    void test(){
      // quick_sort
      int arr[10];
      cout<<“sizeof(arr)=”<<sizeof(arr)<<endl;  //  res:  40
      
      for(int i=0;i<10;i++){
        arr[i]=rand()%10;
      }
      
      quick_sort(arr);
    }
    
    int main{
      test();
      return 0;
    }
```

以上程序，数组作为函数参数传入函数体内，退化成指针。

* 数组指针的类型
  数组指针的类型是`int *`吗？可以做如下实验：

  ```C++
  int arr[10];
  // init array code ...
  cout<<sizeof(arr+1)<<endl;
  ```

  以上代码的结果为：  80
  可以知道，数组的数据类型如果是int，则+1应该是偏移4个字节；所以数组的数据类型不是int*。一种最简单的查看数组数据类型的方式是在VS下编写：`int *p=arr;`，编译器回报错，报错信息显示，数组数据类型为：`int (*p)[10]`，与我们上述说的“数组指针”的概念是一样的。

## 字符指针

再来说说老生常谈的关于字符指针的问题：

* 字符指针指向的字符串可以修改吗？
  不可以。字符指针指向的字符串是常量字符串，所在区域为常量区，常量区的数值不允许修改。

  ```C++
  char *p=“abcdefg”;
  // p[2]=“i”;  erro
  
  // modify by pointer
  char *i=p;
  i+2=“4”;
  //  编译器不会报错，但在编译阶段检测到常量区的数据不允许修改，则报错
  ```

 * 区分以下字符串的表示：

   ```C++
   char *p1=“abcdef”;   //  back: ’\0’
   char p2[4]=“abcd”;   //  back: no’\0’
   char p3[10]=“abcdef”;//  back:’\0’
   char p4[]={“a”,”b”,”c”,”\0”};
   char p5[]={“a”,”b”}; //  back: no’\0’
   ```

## 高级指针修饰低级指针

现在有下面这个例子：

```C++
#include<iostream>
using namespace std;

int* Function(int *p){
  // ... modify p’s val
}

int main(){
  
  int *p=NULL;
  
  //Function(p);
}
```

在这个例子中，想要通过函数来修改p指向的值，并在外部函数体现修改结果，必须使用高级指针作为函数的接收参数类型，这个地方可以解释成，要利用地址传递的方式，在可以修改到外部函数的值。

## 智能指针

智能指针有`unique_ptr`，`share_ptr`等。

* `unique_ptr`：表示此对象唯独只有一份
  简单实现如下：

  ```C++
  // unique pointer
  template<typename T>
  class smart_ptr{
  public:
    smart_ptr(T* ptr=nullptr):ptr_=ptr{}
    ~smart_ptr(){
        delete ptr_;
    }
    
    smart_ptr(smart_ptr&&other){
      ptr_=other.release();
    }
    
    T* get() const{
      return ptr_;
    }
    
    smart_ptr& operator=(smart_ptr rhs){
      rhs.swap(*this);
      return *this;
    }
    
    // release
    T* release(){
      T* ptr=ptr_;
      ptr_=nullptr;
      return ptr;
    }
    
    // swap
    void swap(smart_ptr& rhs){
      using std::swap;
      swap(ptr_,rhs.ptr_);
    }
    
    // operator pointer’s character 
    T& operator*(){
      return *ptr_;
      }
    T* operator->(){
      return ptr_;
      }
    operator bool(){
      return ptr_;
      }
    
  private:
    T* ptr_; 
  };
  ```

* `share_ptr`：用于创建、拷贝、赋值时对对象的统计
  简单实现如下：

  ```C++
  // counter
  class share_counter{
  public:
    share_counter() noexcepet
      :share_counter(1){}
    void add_count() noexcept{
      ++share_counter_;
    }  
    long reduce_count() noexcept{
      return --share_counter_;
    }
    long get_count() noexcept{
      return share_counter_;
    }
  private:
    long share_counter_;  
  };
  
  
  // share pointer
  template<typename T>
  class smart_ptr{
  public:
    explicit smart_ptr(T* ptr=nullptr):ptr_=ptr{
      if(ptr){
        count_=new share_count();
      }
    }
    ~smart_ptr(){
      if(ptr_ && !count_->reduce_count()){
        delete ptr_;
        delete count_;
      }
    }  
    
    // copy constructor
    smart_ptr(const smart_ptr& other) noexcept{
      ptr_=other.ptr_;
      if(ptr_){
        other.count_->add_count();
        count_=other.count_;
      }
    }
    
    // other type smart_ptr
    template<typename U>
    smart_ptr(const smart_ptr<U>& other){
      ptr_=other.ptr_;
      if(ptr_){
        other.count_->add_count();
        count_=other.count_;
      }
    }
    
    // other type smart_ptr move constructor
    template<typename U>
    smart_ptr(const smart_ptr<U>&&other){
      ptr_=other.ptr_;
      if(ptr_){
        count_=other.count_;
        other.count_=nullptr;
      }
    }
    
    // type_cast
    template<typename U>
    smart_ptr(smart_ptr<U>& other,T* ptr) noexcept{
      ptr_=ptr;
      if(ptr_){
        other.count_->add_count();
        count_=other.count_;
      }
    }
    
    // swap
    void swap(smart_ptr&rhs) noexcept{
      using std::swap;
      swap(ptr_,rhs.ptr_);
      swap(count_,rhs.count_);
    }
    
    // operator=
    smart_ptr&
    operator=(smart_ptr rhs) noexcept{
      rhs.swap(*this);
      return *this;
    }
    
    // get pointer
    T* get()const noexcept{
      return ptr_;
    }
    // get count
    long use_count() const noexcept{
      if(ptr_){
       return count_->get_count(); 
      }else{
        return 0;
      }
    }
    
    
    // pointer’s character
    T* operator*(){
      return *ptr_;
    }
    T& operator->(){
      return ptr_;
    }
    operator bool(){
      return ptr_;
    }
    
  private:
    T* ptr_;
    share_counter* count_;  
  };
  
  
  // global swap
  template<typename T,typename U>
  void swap(smart_ptr<T>&lhs,smart_ptr<U>&rhs) noexcept{
    lhs.swap(rhs);
  }
  
  // static_cast
  template<typename T,typename U>
  smart_ptr<T> static_pointer_cast(const smart_ptr<U>&other) noexcept{
    T* ptr=static_cast<T*>(other.get());
    return smart_ptr<T>(other,ptr);
  }
  ```

*关于智能指针在接下来会尝试解释*

**关于指针这块这次暂时想到的就这么多，下次继续补全**