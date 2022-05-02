# Linux多线程服务器编程笔记

## 线程安全对象生命周期

通过`weak_ptr`探测对象生命，Observer模式的竞态条件解决：

`Observable保存weak_ptr<Observer>`

```cpp
class Observable
{
public:
    void register_(weak_ptr<Observer> x); //参数类型可用 const weak_ptr<Observer>&
    // void unregister(weak_ptr<Observer> x); //no need
    void notifyObservers();
    
private:
    mutable MutexLock mutex_;
    std::vector<weak_ptr<Observer>> observers_;
    typedef std::vector<weak_ptr<Observer> >::iterator Iterator;
};

void Observable::notifyObservers()
{
    MutexLockGuard lock(mutex_);
    Iterator it = observers_.begin();
    while(it != observers_.end()) {
        shared_ptr<Observer> obj(it->lock()); //提升尝试，进程安全
        if(obj) {
            //提升成功，引用计数至少为2（原来至少为1，提升成功之后为2）
            obj->update(); //obj在栈上。对象不会在本作用域销毁
            ++it;
        } else {
            it = observers_.erase(it); //对象已经销毁，在容器中擦除
        }
    }
}
```

**思考：如果把`vector<weak_ptr<Observer> > observers_;`替换为`vector<shared_ptr<Observer> > observers_;`会有什么样的后果？**

*后果：由于vector容器中的元素是shared_ptr，所以容器size在操作中可能只增不减，引用计数不会变为0，对象永远不会被销毁，造成内存泄漏*







要在多个线程中同时访问一个`shared_ptr`，正确的做法是mutex保护

```cpp
MutexLock mutex;
shared_ptr<Foo> globalPtr;

void doit(const shared_ptr<Foo>& pFoo);
```

为了性能考虑，使用最简单的互斥锁，使其能被多个线程看到（读写加锁）

```cpp
void read(){ //读
    shared_ptr<Foo> localPtr;
    {
        MutexLockGuard lock(mutex);
        localPtr = globalPtr;
    }
    doit(localPtr);
}

void write(){
    shared_ptr<Foo> newPtr(new Foo); //对象创建在临界区之外
    {
        MutexLockGuard lock(mutex);
        globalPtr = newPtr;
    }
    doit(newPtr);
}
```

* 上面的`read()`和`write()`在临界区之外都没有再访问`globalPtr`，而是用一个**指向同一个Foo对象的栈上`shared_ptr local copy`**，`shared_ptr`作为函数参数传递时不必复制，使用**reference to const**作为参数类型即可
* `shared_ptr<Foo> newPtr(new Foo)`中的`new Foo`是在临界区之外执行的，这种写法比在临界区内写`globalPtr.reset(new Foo)`要好，**缩短了临界区长度**
* 要销毁对象，可以在临界区中执行`globalPtr.reset()`，但是这样析构行为会发生在临界区之内，增加了临界区长度
  * **改进方法：**
    * 定义一个`localPtr`，在临界区内与`globalPtr`交换，这样可以保证对象销毁推迟到临界区之外

*write()改进：*

```cpp
void write(){
    shared_ptr<Foo> newPtr(new Foo);
    shared_ptr<Foo> localPtr;
    {
        MutexLockGuard lock(mutex);
        globalPtr = newPtr;
        localPtr = globalPtr;
    }
    doit(localPtr);
}
```









### shared_ptr技术与陷阱

* 意外延长生命周期：

  * 上述思考中“把`vector<weak_ptr<Observer> > observers_;`修改为`vector<shared_ptr<Observer> > observers_;`”

  * `boost::bind`：会把**实参**拷贝一份，如果这个实参是`shared_ptr`，那么对象的生命周期就不会短于`boost::function`对象

    ```cpp
    class Foo{
        void doit();
    };
    
    shared_ptr<Foo> pFoo(new Foo);
    boost::function<void()> func = boost::bind(&Foo::doit, pFoo); //long life foo
    ```

* 函数参数：

  修改引用计数（拷贝的时候通常是要加锁），`shared_ptr`的拷贝开销要比拷贝原始指针高。**多数情况下可以使用`const_reference`方式传递**：**一个线程只需要在最外层函数有一个实体对象，之后可以用`const reference`使用这个`shared_ptr`**。另外**由于在最外层函数中的对象是在栈上的，不会被别的线程看到，所以是线程安全的**

* 析构动作在创建时被捕获：

  * 虚析构不是必须的
  * `shared_ptr<void>`可以持有任何对象，且可以安全的释放
  * `shared_ptr`对象可以安全的跨越模块边界，比如从DLL返回，不会造成从模块A分配的内存在模块B里被释放
  * 二进制兼容性，即便Foo对象的大小变了，旧的客户代码仍然可以使用新的动态库，无需重新编译。*前提是Foo头文件不出现访问对象的成员的inline函数，并且Foo对象的由动态库中的Factory构造，返回其`shared_ptr`*
  * 析构动作可以定制：`shared_ptr<T>`只有一个模板参数，析构行为可以是函数指针、仿函数等

* 现成的RAII handle：`shared_ptr`需要注意避免循环引用，通常的做法是owner持有指向child的`shared_ptr`，child持有owner的`weak_ptr`







### 对象池

```cpp
//version 1
//问题：map存放的的是shared_ptr,Stock对象永远不会销毁
class StockFactory: boost::noncopyable
{
public:
    shared_ptr<Stock> get(const string& key);
    
private:
    mutable MutexLock mutex_;
    std::map<string, shared_ptr<Stock> > stocks_;
};
```



```cpp
//version 2
//数据成员修改为 std::map<string, weak_ptr<Stock> > socks_;
//问题：程序出现轻微内存泄露 stocks_只增不减
shared_ptr<Stock> StockFactory::get(const string& key) {
    shared_ptr<Stock> pStock;
    MutexLockGuard lock(mutex_);
    
    weak_ptr<Stock>& wkStock = stocks_[key]; //如果key不存在，会默认构造一个
    pStock = wkStock.lock(); //尝试提升
    if(!pStock) {
        pStock.reset(new Stock(key));
        wkStock = pStock; //更新stocks_[key]
    }
    return pStock;
}
```



```cpp
//version 3
//使用shared_ptr的定制析构
//问题：this指针暴露在boost::function，会有线程安全问题；
//		如果这个StockFactory先于Stock对象析构，会core dummp

class StockFactory: boost::noncopyable
{
	// ....
private:
    void deleteStock(Stock* stock){
        if(stock) {
            MutexLockGuard lock(mutex_);
            stocks_.erase(stock->key());
        }
        delete stock;
    }
    //....
};

shared_ptr<Stock> StockFactory::get(const string& key) {
    shared_ptr<Stock> pStock;
    MutexLockGuard lock(mutex_);
    
    weak_ptr<Stock>& wkStock = stocks_[key]; //如果key不存在，会默认构造一个
    pStock = wkStock.lock(); //尝试提升
    if(!pStock) {
        //pStock.reset(new Stock(key));
        pStock.reset(new Stock(key), boost::bind(&stockFactory::deleteStock, this, _1));
        wkStock = pStock; //更新stocks_[key]
    }
    return pStock;
}
```



```cpp
//version 4
//enable_shared_from_this 以其派生类为模板类型实参的基类模板
//为了使用shared_from_this，StockFactory必须是堆对象，且由shared_ptr管理生命周期
//boost::function里保存了一份shared_ptr<StackFactory>，可以保证调用StockFactory::deleteStock的时候StockFactory对象还活着

//注意：shared_from_this 不能再构造函数里调用：在构造StockFactory的时候，还没有被交给shared_ptr管理

//问题：shared_ptr绑定（boost::bind）到boost::function，回调的时候StockFactory对象始终存在，安全；
//同时延长了对象的生命周期，使之不短于boost::function对象

class StockFactory: public boost::enable_shared_from_this<StockFactory>,
						 boost::noncopyable
{
	// ....
private:
    void deleteStock(Stock* stock){
        if(stock) {
            MutexLockGuard lock(mutex_);
            stocks_.erase(stock->key());
        }
        delete stock;
    }
    //....
};

shared_ptr<Stock> StockFactory::get(const string& key) {
    shared_ptr<Stock> pStock;
    MutexLockGuard lock(mutex_);
    
    weak_ptr<Stock>& wkStock = stocks_[key]; //如果key不存在，会默认构造一个
    pStock = wkStock.lock(); //尝试提升
    if(!pStock) {
        //pStock.reset(new Stock(key));
        //pStock.reset(new Stock(key), boost::bind(&stockFactory::deleteStock, this, _1));
        pStock.reset(new Stock(key), 
                     boost::bind(&stockFactory::deleteStock, shared_from_this(), _1));
        wkStock = pStock; //更新stocks_[key]
    }
    return pStock;
}
```



```cpp
//version 5
//弱回调：“如果对象还活着，就调用它的成员函数，否则忽略”
//使用weak_ptr：把weak_ptr绑定到boost::function里
//回调的时候尝试提升一下weak_ptr为shared_ptr，提升成功说明回调对象还在，执行回调，否则忽略


class StockFactory: public boost::enable_shared_from_this<StockFactory>, boost::noncopyable
{
public:
    shared_pre<Stock> get(const string& key);
      
private:
    static void weakDeleteCallBack(const boost::weak_ptr<StockFactory>& wkFactory, Stock* stock){
        shared_ptr<StockFactory> factory(wkFactory.lock()); //尝试提升
        if(factory) {
            factory->removeStock(stock);
        }
        delete stock;
    }
    
    void removeStock(Stock* stock) {
        if(stock) {
            MutexLockGuard lock(mutex_);
            stocks_.erase(stock->key());
        }
    }
    //....
    
private:
    mutable MutexLock mutex_;
    std::map<string, weak_ptr<Stock> > stocks_;
};

shared_ptr<Stock> StockFactory::get(const string& key) {
    shared_ptr<Stock> pStock;
    MutexLockGuard lock(mutex_);
    
    weak_ptr<Stock>& wkStock = stocks_[key]; //如果key不存在，会默认构造一个;wkStock是引用
    pStock = wkStock.lock(); //尝试提升
    if(!pStock) {
        //pStock.reset(new Stock(key));
        //pStock.reset(new Stock(key), boost::bind(&stockFactory::deleteStock, this, _1));
        //pStock.reset(new Stock(key), 
        //            boost::bind(&stockFactory::deleteStock, shared_from_this(), _1));
        
        pStock.reset(new Stock(key),
                    boost::bind(&StockFactory::weakDeleteCallBack,
                               boost::weak_ptr<StockFactory>(shared_from_this()), _1));
        //上述把shared_from_this强制转换为weak_ptr，才不会延长生命周期：
        //boost::bind 拷贝的是实参类型，而不是形参类型
        wkStock = pStock; //更新stocks_[key]
    }
    return pStock;
}
```

