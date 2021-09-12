---
title: "C++设计模式"
date: 2021-09-12T19:13:21+08:00
draft: true
---

# C++设计模式

## 设计模式简介

设计模式主要是针对**面向对象语言**提出的设计思想，可以提高代码的**可复用性**，**抵御变化**

## 面向对象特点

* **封装**：隐藏内部实现
* **继承**：复用现有代码
* **多态**：改写对象行为

## 设计原则

1. **依赖倒置原则**：针对接口编程，**依赖于抽象而不依赖于具体**，抽象(稳定)不应依赖于实现细节(变化)，实现细节应该依赖于抽象，因为稳定态如果依赖于变化态则会变成不稳定态。
2. **开放封闭原则**：对扩展开放，对修改关闭，业务需求是不断变化的，当程序需要扩展的时候，不要去修改原来的代码，而要**灵活使用抽象和继承**，增加程序的扩展性，使易于维护和升级，类、模块、函数等都是可以扩展的，但是不可修改。
3. **单一职责原则**：**一个类只做一件事**，一个类应该仅有一个引起它变化的原因，并且变化的方向隐含着类的责任。
4. 里氏替换原则：子类必须能够替换父类，任何引用基类的地方必须能透明的使用其子类的对象，开放关闭原则的具体实现手段之一。
5. **接口隔离原则**：接口最小化且完备，**尽量少public来减少对外交互，只把外部需要的方法暴露出来**。
6. **最少知道原则**：一个实体应该尽可能少的与其他实体发生相互作用。
7. 将变化的点进行封装，做好分界，**保持一侧变化，一侧稳定**，调用侧永远稳定，被调用测内部可以变化。
8. **优先使用组合而非继承**，继承为白箱操作，而组合为黑箱，继承某种程度上破坏了封装性，而且父类与子类之间耦合度比较高。
9. 针对接口编程，而非针对实现编程，强调**接口标准化**。

**总结:** 没有一步到位的设计模式，刚开始编程时不要把太多精力放到设计模式上，需求总是变化的，刚开始着重于实现，一般敏捷开发后为了应对变化重构再决定采取合适的设计模式。

## 设计模式

### 模板模式

* 父类定义一些算法的框架，具体实现延迟给子类去实现

<u>*在`game.h`头文件中*</u>

```C++
#ifndef __GAME__
#define __GAME__		// 防止头文件重复包含的方法之一

#include<iostream>

// 一个游戏类（父）
class Game{
public:
    Game(){}
    virtual ~Game(){}
    
    // 外界调用接口
    void Run(){
        Startgame();
        Initgame();
        Overgame();
    }
    
    // 子类重写的函数
protected:
    virtual void Startgame(){std::cout<<"This is start game\n";}
    
private:
    void Initgame(){std::cout<<"This is init game\n";}
    void Overgame(){std::cout<<"This is over game\n";}
};
```

<u>*在一个叫做`basketball.h`的头文件中*</u>

```C++
#include"game.h"

// 一个叫做篮球的游戏继承自父类
class Basketball{
    
    // 父类要求子类重写的函数
	void Startgame()override{std::cout<<"This is basketball game\n";}    
};
```

<u>*测试程序中*</u>

```C++
#include"basketball.h"

void test(){
    Game* game=new Basketball;
    game->Run();
    delete game;
}

int main(){
    test();
    return 0;
}
```

<u>*在Linux下的g++中运行结果为*</u>

```
This is basketballgame
This is init game
This is over game
```

