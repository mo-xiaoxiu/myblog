# 有关于C++字符串的问题

前段时间在工作过程中，遇到有关于字符串的一些问题，在这里做一些总结和输出。其中一个是关于在C++中使用malloc有可能会带来的问题；另一个是在C++中使用string对于减小开销的一些思考。

## malloc在C++不同软件架构中可能带来的问题

**背景：**我所在公司使用的软件架构是属于事件驱动型的，在用法上这里做一个简单的概括：

```c++
/* there is a thread runnable member in class*/
class Example{
public:
    ...
private:
    ...
    shared_ptr<Runnable> run;
};

/* in constructor, need to new 'run' */
Example::Example(){
    run = new Runnable{
        case MSG_EXAMPLE:{
            ... // you can get the msg and do something...
            break;
        }
    }
}

/* you need a msgid to define the message type */
enum Msg{
    MSG_EXAMPLE = 8;
};
class Message{
public:
   	Message(); // in Message constructor or init, you need to register this MSG_ID
};
```

**场景：**我需要在传递msg给主线程（runnable）的时候，传递字符串，我一开始的做法是：（很显然有问题）

```c++
/* in hpp */
class ForwardString{ ... };

/* in cpp */
ForwardString::ForwardString(){
    // when I get a string, I pass this string by using msg...
    const char* tmpBuf = "this is the string...";
    shared_ptr<MessageForwardString> msg = new MessageForwardString;
    memset(msg->mData, 0, MAX_DATA_NUM);
    memcpy(msg->mData, tmpBuf, strlen(tmpBuf));
    sendMsg(msg);
}

/* in msg.hpp */
enum MessageNum{
    MSG_FORWARDSTRING = 1;
}

class MessageForwardString{
    char* mData = (char*)malloc(sizeof(char) * MAX_DATA_NUM);
	...
};
```

**问题：**很显然，这里会有内存泄漏的问题，因为我没有在msg new出来之后、引用计数置为0的情况下，将申请的内存销毁，在程序长期运行的时候，会逐渐消耗内存。

**解决方法：**其实解决方法也很简单，就是在msg对应的类中实现释放内存的操作：

```c++
/* after modified... */
enum MessageNum{
    MSG_FORWARDSTRING = 1;
}

class MessageForwardString{
    char* mData = (char*)malloc(sizeof(char) * MAX_DATA_NUM);
	...
    ~MessageForwardString(){
        if(mData){
            free(mData);
        }
    }
};
```

但是这里仍然存在问题：在字符串传递过程中，还是存在申请内存释放内存多次的操作，这样可能会造成内存碎片。减少内存分配的次数相对应的释放内存的次数，解决方法之一是将内存分配的操作移动到*生产字符串或者说获取需要传递的字符串*的线程中：

```c++
/* in ForwardString.hpp */
class ForwardString{
    ...
    char* mData = nullptr;
};

/* in ForwardString.cpp */
ForwardString::ForwardString(){
    if(!mData){
        mData = (char*)malloc(sizeof(char) * MAX_DATA_NUM);
        memset(mData, 0, MAX_DATA_NUM);
    }
    ...
    // when I get a string, I pass this string by using msg...
    const char* tmpBuf = "this is the string...";
    shared_ptr<MessageForwardString> msg = new MessageForwardString;
    memset(mData, 0, MAX_DATA_NUM);
    memcpy(mData, tmpBuf, strlen(tmpBuf));
    msg->mData = mData;
    sendMsg(msg);
}

/* in ForwardString,cpp, you need to free mData*/
ForwardString::~ForwardString(){
    if(mData){
        free(mData);
    }
}
```

**思考：**这样的处理可以从一定程度上解决内存申请和对应的释放次数过多的问题，因为线程在程序运行过程不会一直释放和启动；但这样会使代码处理上显得小心翼翼起来，需要在其他异常情况也考虑到mData的释放（例如线程运行异常退出，需要及时释放资源；线程正常退出释放资源；在传递的数据上，对考虑抛出异常的方法或是方法中对一些特定条件的判断之后结果不满足的时候，需要及时调用memset将数据重新清空，防止脏数据和数据越界的情况发生等），也从一定程度上增加代码冗余性，更不便于维护。

**直接使用string：**直接使用string会让代码变得简洁易懂：

```c++
/* in msg.hpp, after modified... */
enum MessageNum{
    MSG_FORWARDSTRING = 1;
}

class MessageForwardString{
    std::string mData;
	...
};

/* in ForwardString.hpp */
class ForwardString{ ... };

/* in ForwardString.cpp */
ForwardString::ForwardString(){
    ...
    // when I get a string, I pass this string by using msg...
    const char* tmpBuf = "this is the string...";
    shared_ptr<MessageForwardString> msg = new MessageForwardString;
    std::string fowardString(tmpBuf);
    msg->mData = fowardString;
    sendMsg(msg);
}
```

**思考：**解决代码的冗余和繁琐复杂的异常条件处理，我们可以得到简洁易读的代码和不差的性能。

**但是到这里我还不满足，因为考虑到string的拷贝开销还是存在的，在实时性数据较大的时候需要考虑到这一点。**

<br>

<br>

## 在C++在使用string减小拷贝开销

要知道上述情况下，string的拷贝开销，我们可能需要分析下，构造的次数：

```c++
ForwardString::ForwardString(){
    ...
    // when I get a string, I pass this string by using msg...
    const char* tmpBuf = "this is the string...";
    shared_ptr<MessageForwardString> msg = new MessageForwardString;
    std::string fowardString(tmpBuf); // 1
    msg->mData = fowardString; // 2
    sendMsg(msg); 
}
```

最直观的方法是将 1 中构造的临时变量直接赋值于 2 上：

```c++
ForwardString::ForwardString(){
    ...
    // when I get a string, I pass this string by using msg...
    const char* tmpBuf = "this is the string...";
    shared_ptr<MessageForwardString> msg = new MessageForwardString;
    msg->mData = std::string fowardString(tmpBuf); // 1
    sendMsg(msg);
}
```

我们能否在如上 1 的赋值位值做些文章呢？

我能想到的是使用**移动语义**。将forwardString的value移动到mData上，原来的value我们并不关心。使用`std::move()`或许可以作到：

```c++
ForwardString::ForwardString(){
    ...
    // when I get a string, I pass this string by using msg...
    const char* tmpBuf = "this is the string...";
    shared_ptr<MessageForwardString> msg = new MessageForwardString;
    msg->mData = std::move(std::string fowardString(tmpBuf)); // move
    sendMsg(msg); 
}
```

但这里需要注意的是，这个`msg->mData`在使用`std::move`，会调用string的移动赋值，之后就变成了一个将亡值，需要尽快使用，而非再去操作，会产生未可知的现象。

所以在这里使用`std::move`是有问题的，因为我们需要在`sendMsg(msg)`去将msg发送到别的线程（主线程），意味着我们还需要使用这个变量和里面的value，所以肯定不行。

我们可以在`sendMsg()`中使用的时候在最后一层调用使用`std::move`，这里需要看具体的实现中怎么去处理这个value。

以上是有关于工作的架构中的优化，对于普通的类型，我在这里举个例子作为对优化的补充：

```c++
#include <iostream>
using namespace std;
#include <string>


class Tmp{
public:
    Tmp(){
        cout << "call constructor" << endl;
    }
    Tmp(const Tmp&){
        cout << "call copy constructor" << endl;
    }
    Tmp& operator=(Tmp&&){
        cout << "call movement constructor" << endl;
    }
    ~Tmp(){
        cout << "call destructor" << endl;
    }

public:
    string mString;
};

void useString(Tmp &&t){
    cout << "this is useString: " << t.mString << endl;
}


void useString(string &&t){
    cout << "this is useString: " << t << endl;
}

int main(){
    const char* tmp = "this is tmp";
    Tmp t; // print1 call constructor
    t.mString = std::move(string(tmp)); // for string movement constructor
    cout << t.mString << endl; // print2 this is tmp
    useString(std::move(t)); // print3 this is useString: this is tmp
    useString(std::move(string(tmp))); // print4 this is useString: this is tmp
    // print5 call destructor
    
    return 0;
}
```

我们可以看到，在`useString(std::move(string(tmp)))`中，将构造的string使用`std::move`转移成右值，并直接入参右值引用，开销应该是最小的。