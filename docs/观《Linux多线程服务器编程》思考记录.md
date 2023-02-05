# 观《Linux多线程服务器编程》思考记录

## 死锁

主线程和thread线程对于Request和Inventory类两个mutex的竞争情况：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/未命名绘图.drawio.png)

* main睡眠5s，操作全局变量g_inventory的方法printAll；thread申请创建Request对象添加到全局变量g_inventory中，等待1s析构；
* main的printAll方法调用Request的print方法，需要先加Request的锁；thread调用Request的析构方法会调用inventory的remove方法，在Request的析构方法中需要先加Request的锁
* **死锁点：main和thread其中一个加了Request的锁另一个就要等待其释放Request锁，而加了Request锁的线程需要等到另一个等待释放Request锁的线程释放inventory锁才能继续执行**

### 解决死锁方案

```cpp title="recipes/thread/test/RequestInventory_test2.c"
#include "../Mutex.h"
#include "../Thread.h"
#include <set>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <stdio.h>

class Request;
typedef boost::shared_ptr<Request> RequestPtr; /* 使用shared_ptr管理Request对象 */

class Inventory
{
 public:
  Inventory()
    : requests_(new RequestList)
  {
  }

  void add(const RequestPtr& req)
  {
    muduo::MutexLockGuard lock(mutex_);
    if (!requests_.unique())
    {
      requests_.reset(new RequestList(*requests_));
      printf("Inventory::add() copy the whole list\n");
    }
    assert(requests_.unique());
    requests_->insert(req);
  }

  void remove(const RequestPtr& req) // __attribute__ ((noinline))
  {
    muduo::MutexLockGuard lock(mutex_);
    if (!requests_.unique())
    {
      requests_.reset(new RequestList(*requests_));
      printf("Inventory::remove() copy the whole list\n");
    }
    assert(requests_.unique());
    requests_->erase(req);
  }

  void printAll() const;

 private:
  typedef std::set<RequestPtr> RequestList; /* set存放的时Request的shared_ptr */
  typedef boost::shared_ptr<RequestList> RequestListPtr;

  RequestListPtr getData() const
  {
    muduo::MutexLockGuard lock(mutex_);
    return requests_;
  }

  mutable muduo::MutexLock mutex_;
  RequestListPtr requests_;
};

Inventory g_inventory;

class Request : public boost::enable_shared_from_this<Request> /* 使用shared_ptr传递this */
{
 public:
  Request()
    : x_(0)
  {
  }

  ~Request()
  {
    x_ = -1; /* remove行为移出Request析构函数 */
  }

  void cancel() __attribute__ ((noinline)) /* 原来析构函数中的remove */
  {
    muduo::MutexLockGuard lock(mutex_);
    x_ = 1;
    sleep(1);
    printf("cancel()\n");
    g_inventory.remove(shared_from_this()); /* this指针使用智能指针进行传递 */
  }

  void process() // __attribute__ ((noinline))
  {
    muduo::MutexLockGuard lock(mutex_);
    g_inventory.add(shared_from_this()); /* add行为传递的this为智能指针 */
    // ...
  }

  void print() const __attribute__ ((noinline))
  {
    muduo::MutexLockGuard lock(mutex_);
    // ...
    printf("print Request %p x=%d\n", this, x_);
  }

 private:
  mutable muduo::MutexLock mutex_;
  int x_;
};

void Inventory::printAll() const
{
  RequestListPtr requests = getData();
  printf("printAll()\n");
  sleep(1);
  for (std::set<RequestPtr>::const_iterator it = requests->begin();
      it != requests->end();
      ++it)
  {
    (*it)->print();
  }
}

void threadFunc()
{
  RequestPtr req(new Request);
  req->process();
  req->cancel();
}

int main()
{
  muduo::Thread thread(threadFunc);
  thread.start();
  usleep(500*1000);
  g_inventory.printAll();
  thread.join();
}
```

* **使用shared_ptr管理Request对象，然后将add和remove行为进行修改，add和remove行为传递的都是shared_from_this，防止this指针在多线程操作中被delect掉，保证了操作的同步性；将原来在析构函数中的remove行为移出析构函数，因为当Request对象使用shared_ptr进行管理之后，析构函数不需要关心对象的生命周期和资源释放问题，将这种remove行为封装为cancle--一个新的函数，手动支持这种操作全局对象释放资源的操作**

## 将Request::print()移出Inventory::printAll()临界区

1. 把Request复制一份，在临界区之外遍历这个副本
2. 使用shared_ptr管理std::set，在遍历的时候先增加引用计数，阻止并发修改：

```cpp title="recipes/thread/test/Request-Inventory_test.cc"
#include "../Mutex.h"
#include "../Thread.h"
#include <set>
#include <boost/shared_ptr.hpp>
#include <stdio.h>

class Request;

class Inventory
{
 public:
  Inventory()
    : requests_(new RequestList)
  {
  }

  void add(Request* req)
  {
    muduo::MutexLockGuard lock(mutex_);
    if (!requests_.unique())
    {
      requests_.reset(new RequestList(*requests_));
      printf("Inventory::add() copy the whole list\n");
    }
    assert(requests_.unique());
    requests_->insert(req);
  }

  void remove(Request* req) // __attribute__ ((noinline))
  {
    muduo::MutexLockGuard lock(mutex_);
    if (!requests_.unique()) /* 判断shared_ptr是否存在 */
    {
      requests_.reset(new RequestList(*requests_)); /* 不存在则重置一个 */
      printf("Inventory::remove() copy the whole list\n");
    }
    assert(requests_.unique());
    requests_->erase(req);
  }

  void printAll() const;

 private:
  typedef std::set<Request*> RequestList;
  typedef boost::shared_ptr<RequestList> RequestListPtr; /* 使用shared_ptr管理set */

  RequestListPtr getData() const
  {
    muduo::MutexLockGuard lock(mutex_);
    return requests_;
  }

  mutable muduo::MutexLock mutex_;
  RequestListPtr requests_;
};

Inventory g_inventory;

class Request
{
 public:
  Request()
    : x_(0)
  {
  }

  ~Request() __attribute__ ((noinline))
  {
    muduo::MutexLockGuard lock(mutex_);
    x_ = -1;
    sleep(1);
    g_inventory.remove(this);
  }

  void process() // __attribute__ ((noinline))
  {
    muduo::MutexLockGuard lock(mutex_);
    g_inventory.add(this);
    // ...
  }

  void print() const __attribute__ ((noinline))
  {
    muduo::MutexLockGuard lock(mutex_);
    // ...
    printf("print Request %p x=%d\n", this, x_);
  }

 private:
  mutable muduo::MutexLock mutex_;
  int x_;
};

void Inventory::printAll() const
{
  RequestListPtr requests = getData();
  sleep(1);
  for (std::set<Request*>::const_iterator it = requests->begin();
      it != requests->end();
      ++it)
  {
    (*it)->print(); /* 在遍历时增加应用计数 */
  }
}

void threadFunc()
{
  Request* req = new Request;
  req->process();
  delete req;
}

int main()
{
  muduo::Thread thread(threadFunc);
  thread.start();
  usleep(500*1000);
  g_inventory.printAll();
  thread.join();
}
```



## notify和notufyAll

enqueue使用notify，而countDown使用的时notifyAll，两者互换可能会产生的问题：enqueue如果使用的是notifyAll，会唤醒多个线程，如果其中一个线程先执行dequeue，接下来另一个也被唤醒排队调度到的线程马上执行，在while中，由于已经判断为空，所以wait，之后调度可能很长一段时间都处于wait之中，导致有些线程长期不能从queue中获取元素；而countDown使用notify，则可能无法达到多个子线程同时起跑的设计目的



> 更新中...