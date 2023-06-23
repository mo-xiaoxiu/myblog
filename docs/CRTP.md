# CRTP

curiously recurring template pattern

类X继承了一个以X作为模板参数的的模板

**CRTP可用于实现静态多态：编译期已经知道具体调用**

## 具体用法举例

```cpp title="CRTP.cpp"
#include <iostream>


template<typename T>
class Base{
public:
    void interface(){
        static_cast<T*>(this)->implic(); //传入类型为子类，基类转换为子类并实现调用等
    }
};

class Derive: public Base<Derive>{
public:
    void implic(){
        std::cout << "This is Derive." << std::endl;
    }
};

class DeriveOne: public Base<DeriveOne>{
public:
    void implic(){
        std::cout << "This is DeriveOne." << std::endl;
    }
};


int main(){
    
    Derive d;
    d.interface();
    
    DeriveOne d1;
    d1.interface();
    
    return 0;
}

```

*output：*

```
This is Derive.
This is DeriveOne.
```

使用要点：

* 基类模板：传入模板参数为子类类型，开发对外统一接口
* 基类对外统一接口实现：将基类转化为子类，调用的方法具体子类需要覆写实现
* CRPT调用：子类调用基类开放的统一接口
* **基类不能有未定义的成员变量**：编译期会报错，因为基类模板在编译期需要具体的参数实例化
* 可以和组合等其他方式同时使用

## 案例

现在想想，工作中y同事遇到的一个问题可以使用CRTP进行解决：message是一个父类消息体，继承于它的子类在功能中起到流程的作用，也就是这个message的子类会进入到功能函数进行筛选之后，跳转到对应的功能逻辑进行处理。该功能模块对于外部进程来说使用gdbus进行通信，使用主loop的方式进行消息传递和通知进程中的主线程，message可以进入到主loop中进行逻辑处理。

现在需要将外部的message传递进去该功能模块并转化为内部其他功能所需要的子类message，可以使用该方法。伪代码如下：

```cpp title="message.cpp"
template<typename T>
class MessageBase{
public:
    void transformDerive(){
        static_cast<T*>(this)->deriveInterface();
    }
};

....

class MessageDerive1 : public MessageBase<MessageDerive1>{
    void deriveInterface(){
        sp<MessageDerive1> msg = new MessageDerive1;
        ...
        msg->send();
    }
};

class MessageDerive12 : public MessageBase<MessageDerive2>{
    void deriveInterface(){
        sp<MessageDerive2> msg = new MessageDerive2;
        ...
        msg->send();
    }
};

------------------
/*in service cpp*/
Service(){
    mRunnable = new Runnable([this](const Message& mp){
        sp<Message> msg = mp.get();
        if(msg->mType == DERIVE1){ //or use switch...case
            msg->deriveInterface();
            .... //operator for derive 1
        }else if(msg->mType == DERIVE2){
            msg->deriveInterface();
            ....//operator for derive 2
        }else{
            ....
        }
        
        ....
    })
}
```

