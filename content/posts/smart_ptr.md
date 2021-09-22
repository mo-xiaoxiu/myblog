---
title: "C++智能指针"
date: 2021-09-22T13:04:42+08:00
draft: true
---

# 智能指针

## unique_ptr

定义了这个对象在程序中只有一份数据，任何拷贝、赋值都是一样的，不会增加数据

*简单实现：*

```C++
template<typedef T>				// 将类中的指针类型设置成模板
class unique_ptr{
    public:
    	explicit unique_ptr(T* ptr=nullptr):ptr_(ptr){}		// 设置构造函数初始化指针 explicit防止隐式转换
    	~unique(){
            delete ptr_;
        }
    	T* get()const noexcept{return ptr_;}
    
    	// pointer-like 要表示出指针应该有的特性
    	T& operator*()const noexcept{return *ptr_;}
    	T* operator->()const noexcept{return ptr_;}
    	operator bool()const noexcept{return ptr_;}
    
    	// 释放指针所有权
    	T* release(){
            T* ptr=ptr_;
            ptr_=nullptr;
            return ptr;
        }
    
    	// 成员的交换函数（交换指针所有权）	利用的是std下的swap
    	void swap(unique_ptr& rhs){
            using std::swap;
            swap(ptr_,rhs.ptr_);
        }
    
    	// 接下来写上移动构造函数和赋值函数
    	template<typedef U>
    	unique_ptr(unique_ptr<U>&& other){
            // 函数的参数是右值引用，也就是说传入的参数必须是一个右值（将亡值）
            ptr_=other.release();		// 移动构造函数中释放传入参数指针所有权（要求不产生额外的对象）
        }
    	
    	unique_ptr& operator=(unique_ptr other){	// 传入参数为：值拷贝	调用的是移动构造函数，省去了在函数内构造临时对象的语句
            other.swap(*this);		// 拷贝一份交换指针所有权
            return *this;
        }
  		  	
    private:
    	T* ptr_;
};
```

---



## shared_ptr

多用来计数，能在不用到对象时自动释放内存，防止内存泄漏

```C++
// 计数类
class share_count{
    public:
    	explicit share_count():count(1){}			// 计数值初始化为 1
    	void add_count(){
            ++count;			// 并不关心增加了多少数
        }
    	long reduce_count(){
            return --count;			// 只关心还剩下多少数
        }
    	long use_count(){
            return count;
        }

    private:
    	long count;
};

// 指针类	设置为模板
template<typedef T>
class shared_ptr{
    template<typedef U>
    friend class shared_ptr;		// 将其他类型的指针类作为友元，方便操作其他类型的成员变量
    
    public:
    	explicit shared_ptr(T* ptr=nullptr){		// 显示初始化指针和计数器
            if(ptr){
                share_count_=new share_count();
            }
        }
    	~shared_ptr(){			// 析构函数：指针存在计数值还没减到0时，释放内存
            if(ptr_ && !share_count_->reduce_count()){
                delete ptr_;
                delete share_count_;
            }
        }
    
    	// 拷贝构造函数：计数器加1，对方指针直接赋值（共享）
    	shared_ptr(shared_ptr& other) noexcept{
            ptr_=other.ptr_;
            if(ptr_){
                other.share_count_->add_count();
                share_count_=other.share_count_;
            }
        }
    
    	// 模板类移动构造函数：指针和计数器直接转移
    	template<typedef U>
    	shared_ptr(shared_ptr<U>&& other) noexcept{
            ptr_=other.ptr_;
            if(ptr_){
                share_count_=other.share_count_;
                other.share_count_=nullptr;
            }
        }
    
    	// 赋值：传入值拷贝，调用移动构造函数还是拷贝构造函数，取决于传入的参数是右值还是左值
    	shared_ptr& operator=(shared_ptr rhs) noexcept{
            rhs.swap(*this);
            return *this;
        }
    
    	void swap(shared_ptr& rhs){
            using std::swap;
            swap(ptr_,rhs.ptr_);
            swap(share_count_,rhs.share_count_);
        }
    	T* get(){
          return ptr_;  
        }
    
    	// 为了类外几种类型转换定义需要
    	template<typedef U>
    	shared_ptr(shared_count<U>& other,T* ptr) noexcept{
            ptr_=ptr;
            if(ptr_){
                other.share_count_->add_count();
                share_count_=other.share_count_;
            }
        }
    
    
    	// 指针特征
    	T& operator*()const noexcept{
            return *ptr_;
        }
    	T* operator->()const noexcept{
            return ptr_;
        }
    	operator bool()const noexcept{
            return ptr_;
        }
    
    private:
    	T* ptr_;
    	share_count* shanre_count_;
};

// 全局的交换函数
template<typedef T>
void swap(shared_ptr<T>& lhs,shared_ptr<T>& rhs){
    lhs.swap(rhs);
}

// static_cast 转换函数定义
template<typedef T,typedef U>
shared_ptr<T> static_pointer_cast(const shared_ptr<U>& other){
    T* ptr=static_cast<T*>(other.get());	// 指针转型
    return shared_ptr(other,ptr);		// 再传回去构造生成新的类型
}

// 下同
template<typedef T,typedef U>
shared_ptr<T> dynamic_pointer_cast(const shared_ptr<U>& other){
    T* ptr=static_cast<T*>(other.get());
    return shared_ptr(other,ptr);
}

template<typedef T,typedef U>
shared_ptr<T> reinterpret_pointer_cast(const shared_ptr<U>& other){
    T* ptr=reinterpret_cast<T*>(other.get());
    return shared_ptr(other,ptr);
}

template<typedef T,typedef U>
shared_ptr<T> const_pointer_cast(const shared_ptr<U>& other){
    T* ptr=const_cast<T*>(other.get());
    return shared_ptr(other,ptr);
}

```

---



