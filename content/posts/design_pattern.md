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

---

### 策略模式

将一系列相似功能的算法封装起来，使得它们之间可以相互替换。比较适用于多`if-else`语句的情况

<u>*定义一个计算类*</u>：`calculation.h`

```C++
#ifndef __CALCULATION__
#define __CALCULATION__

#include<iostream>

// calculation
class Calculation{
public:
    Calculation(){}
    virtual ~Calculation(){}
    
    virtual void operation(){std::cout<<"Base operation"<<std::endl;}
};

#endif

```

<u>*在计算加法的``add.h`头文件中*</u>

```C++
#ifndef __ADD__
#define __ADD__

#include"calculation.h"

class Add:public Calculation{
	void operation() override {std::cout<<"this is add operation."<<std::endl;}    
};

#endif

```

<u>*在计算减法的`sub.h`头文件中*</u>

```C++
#ifndef __SUB__
#define __SUD__

#include"calculation.h"

class Sub:public Calculation{
    void operation() override {std::cout<<"this is sub operation."<<std::endl;}
};

#endif

```

<u>*写一个封装各类计算的函数*</u>

```C++
#include"add.h"
#include"sub.h"

int strategy(){
    Calculation* cal=new Add();
    cal->operation();
    delete cal;
    
    Calculaion* cal_=new Sub();
    cal_->operation();
    delete cal;
}
```

在使用时只需要了解此函数

---

### 观察者模式

定义对象间的一对多的关系，当其中一个对象发生改变时，其他对象也都会被通知以发生相应的改变

<u>*在观察者`observer.h`头文件中*</u>

```C++
#ifndef __OBSERVER__
#define __OBSERVER__

#include<iostream>

class ObserverBase{
public:
    ObserverBase(){}
    virtual ~ObserverBase(){}
    
    // 表示更新内容的函数
    virtual void Update(){}
};

#endif
```

<u>*在观察者子对象`observerfirstchild.h`头文件中*</u>

```C++
#ifndef __OBSERVERFIRSTCHILD__
#define __OBSERVERFIRSTCHILD__
#include"observer.h"

class Child_1:public ObserverBase{
    void Update() override {std::cout<<"First child"<<std::endl;}
};

#endif

```

<u>*在另一个观察者子对象`observersecondchild.h`*</u>

```C++
#ifndef __OBSERVERSECONDCHILD__
#define __OBSERVERSECONDCHILD__
#include"observer.h"

class Child_2:public ObserverBase{
    void Update() override {std::cout<<"Second child"<<std::endl;}
};

#endif

```

<u>*在程序中写上通知的类*</u>

```C++
#include"obseerverfirstchild.h"
#include"observersecondchild.h"
#include<list>

class NotifyBase{
    public:
    	void Add(ObserverBase* obj){observers.emplace_back(obj);}
    
    	void Remove(ObseerverBase* obj){observers.remove(obj);}
    
    	void Notify(){
            for(auto observer:observers){
                observer->Update();
            }
        }
    private:
    	std::list<ObserverBase* > observers;
};

int main(){
    ObserverBase* base1=new Child_1();
    ObserverBase* base2=new Child_2();
    
    NotifyBase notify;
    notify.Add(base2);
    notify.Add(base1);
    notify.Notify();
    
    notify.Remove(base1);
    notify.Notify();
    
    return 0;
}
```

---

### 装饰器模式

顾名思义，装饰器模式就是建立一个装饰器，将各种相关的类继承于这个装饰器，使其完成各种组合的功能；可以针对于策略模式单一的类继承

*现在写一个能组合各种游戏技能的功能* 

<u>*在一个游戏`game.h`的头文件中*</u>

```C++
#ifndef __GAME__
#define __GAME__

#include<iostream>

class Game{
    public:
    	Game(){}
    	virtual ~Game(){}
    
    	// 游戏技能的类
    	virtual void Skill(){std::cout<<"game skill"<<std::endl;}
};

#endif

```

<u>*定义一个装饰器的类，用于继承于各个游戏*`decoration.h`</u>

```C++
#ifndef __DECORATION__
#define __DECORATION__

#include"game.h"

class Decoration:public game{
    protected:
    	Game* game_;
    public:
    //构造函数：对各个游戏技能进行组合（传进来一个跟当前不一样的游戏类对象）
    	Decoration(Game* game){game_=game;}
    
    	void Skill() override {game->Skill();}
    
    	virtual ~Decoration(){}
};

#endif

```

<u>*现在有一个篮球游戏类`basketball.h`*</u>

```C++
#ifndef __BASKETBALL__
#define __BASKETBALL__

#include"decoration.h"

// 各个游戏只需要继承负责组合的装饰器类就可以了
class Basketball:public Decoration{
    public:
    // 构造函数：对装饰器进行初始化
    	Basketball(Game* game):Decoration(game){}
    // 调用技能函数：显示各自游戏的操作，追加技能表示
    	void Skill() override{
            std::cout<<"basketball game"<<std::endl;
            Decoration::Skill();
        }
};

#endif

```

<u>*定义超级玛丽类`supermarry.h`*</u>

```C++
#ifndef __SUPERMARRY__
#define __SUPERMARRY__

#include"decoration.h"

class SuperMarry:public Decoraion{
    public:
    	SuperMarry(Game* game):Decoration(game){}
    
    	void Skill() override {
            std::cout<<"this is super_marry game"<<std::endl;
        	Decoration::Skill();
        }
};

#endif

```

<u>*定义一个Lol游戏类`Lol.h`*</u>

```C++
#ifndef __LOL__
#define __LOL__

#include"decoration.h"

class Lol:public Decoration{
    public:
    	Lol(Game* game):Decoration(game){}
    
    	void Skill() override{
            std::cout<<"this is Lol game"<<std::endl;
            Decoration::Skill();
        }
};

#endif

```



<u>*使用*</u>

```C++
#include"basketball.h"
#include"supermarry.h"
#include"Lol.h"
#include"decoration.h"

int main(){
    Game* lol=new Lol();
    Game* supermarry=new SuperMarry();
    
    // 既可以打篮球又会打超级玛丽
    Game* basketball_superMarry=new Basketball(supermarry);
    basketball_supermarry->Skill();
    std::cout<<std::endl;
    
    // 既可以打篮球又可以打lol
    Game* basketball_lol=new Basketball(lol);
    basketball_lol->Skill();
    std::cout<<std::endl;
    
    // 既可以打篮球又可以打超级玛丽，还可以打lol
    Game* all=new Lol(basketball_supermarry);
    all->Skill();
    std::cout<<std::endl;
    
    // 释放内存
    delete lol;
    delete supermarry;
    delete basketball_supermarry;
    delete basketball_lol;
    delete all;
    
    return 0;
}
```

---

### 桥接模式

定义出**实现类**和**抽象类**，实现和抽象功能分离，各自适应变化

<u>*实现一个图形画图功能，有对应形状和颜色，其中同种形状可以有不同的颜色*</u>

<u>*创建一个实现颜色的类，实现各种颜色的绘制。之后会成为抽象图形类的成员变量：`draw.h`*</u>

```C++
#ifndef __DRAW__
#define __DRAW__

#include<iostream>

class ShapeDraw{
    public:
    	virtual void Draw()=0;	// 在子类中重写
    	virtual ~ShapeDraw(){}	// 虚析构
};

#endif

```

<u>*画出红颜色：*</u>`draw_red.h`

```C++
#ifndef __RED__
#define __RED__

#include"draw.h"

class DrawRed:public ShapeDraw{
    public:
    	void Draw() override {std::cout<<"draw red"<<std::endl;}
};

#endif

```

<u>*画出黑颜色：*</u>`draw_black.h`

```C++
#ifndef __BLACK__
#define __BLACK__

#include"draw.h"

class DrawBlack:public ShapeDraw{
    public:
    	void Draw() override {std::cout<<"draw black"<<std::endl;}
};

#endif

```

<u>*接下来定义一个图形基类，可以画出多个不同的图形，也可以上不同的颜色：*</u>`shape.h`

```C++
#ifndef __SHAPE__
#define __SHAPE__

#include"draw.h"

class Shape{
    protected:
    	ShapeDraw* impl;						// 实现类对象作为抽象类的成员变量
    
    public:
    	virtual void Update(){}					// 用于重写形状
    	Shape(ShapeDraw* impl_):impl(impl_){}
};

#endif

```

<u>*接下来写一个继承于抽象的图形基类的派生类：圆形*</u>  `circle.h`

```C++
#ifndef __CIRCLE__
#define __CIRCLE__

#include"shape.h"

class Circle:public Shape{
    public:
    	void Update() override{std::cout<<"circle shape"<<std::endl;
                              impl->Draw();}
    	Circle(ShapeDraw* imp):Shape(imp){}		// 构造函数初始化实现类对象：在画出这个圆形的同时就指定其颜色
    	
};

#endif

```

<u>*写一个矩形的类*</u> `rectangle.h`

```C++
#ifndef __RECTANGLE__
#define __RECTANGLE__

#include"shape.h"

class Rectangle:public Shape{
    public:
    	void Update() override{std::cout<<"rectangle shape"<<std::endl;
                              impl->Draw();}
    	Rectangle(ShapeDraw* imp):Shape(imp){}		
};
```

<u>*一个示例测试来实现其使用：*</u>

```C++
#include"circle.h"
#include"rectangle.h"
#include"draw_red.h"
#include"draw_black.h"

int main(){
    // 要求绘制颜色：黑色
    ShapeDraw* impl=new DrawBlack();
    // 画一个黑色的圆
    Shape* cir=new Circle(impl);
    // 调用其实现
    cir->Update();
    
    delete impl;
    delete cir;
    
    return 0;
}
```

*输出：*

```
circle shape
draw black

```

**抽象类和实现类的互相配合**

---

### 工厂模式

顾名思义，想工厂一样生产不同的产品。创建一个工厂基类，再为每一个类型创建相应的工厂继承于它，每个工厂可以生产具体的产品

<u>*椅子类：`chair.h`*</u>

```C++
#ifndef __CHAIR__
#define __CHAIR__

#include<iostream>

class Chair{
    public:
    	Chair(){}
    	virtual ~Chair(){}
    
    	virtual void Show(){std::cout<<"The chair"<<std::endl;}		// 到子类中表示产品是什么类型的椅子
};

#endif

```

<u>*低端椅子类：`low_chair.h`*</u>

```C++
#ifndef __LOW_CHAIR__
#define __LOW_CHAIR__

#include"chair.h"

class LowChair:public Chair{
    public:
    	void Show() override{std::cout<<"Low chair"<<std::endl;}
};

#endif

```

<u>*高端椅子类：`high_chair.h`*</u>

```C++
#ifndef __HIGH_CHAIR__
#define __HIGH_CHAIR__

#include"chair.h"

class HighChair:public Chair{
    public:
    	void Show() override{std::cout<<"High chair"<<std::endl;}
};

#endif

```

<u>*总工厂类：`factory.h`*</u>

```C++
#ifndef __FACTORY__
#define __FACTORY__

#include"chair"

class Factory{
    public:
    	Factory(){}
    	virtual ~Factory(){}
    
    	virtual Chair* createChair(){}		// 到不同的工厂中生产不同等级的椅子
};

#endif

```

<u>*生产低端椅子的工厂，继承于总工厂（是总工厂的一部分）：`LowFactor.h`*</u>

```C++
#ifndef __LOW_FACTORY__
#define __LOW_FACTORY__

#include"factory.h"

class LowFactory:public Factory{
    public:
    	Chair* createChair() override{
            return new LowChair();
        }
};

#endif

```

<u>*生产高端椅子的工厂，继承于总工厂（总工厂的一部分）：`HighFactory.h`*</u>

```C++
#ifndef __HIGH_FACTORY__
#define __HIGH_FACTORY__

#include"factory.h"

class HighFactory:public Factory{
    public:
    	Chair* createChair() override{
            return new HighChair();
        }
};

#endif

```

<u>*现在分别生产高端椅子和低端椅子：*</u>

```C++
#include"LowChair.h"
#include"HighChair.h"
#include"LowFactory.h"
#include"HighFactory.h"

int main(){
    // 利用低端工厂创建一把低端椅子
    // 只需要将生产出的椅子返回给椅子总类就可以
    // 相当于生产方只需要看到生产出的椅子
    Factory* low_fac=new LowFactory();
    Chair* chair=low_fac->createChair();
    
    delete low_fac;
    
    // 创建一把高端椅子
    Factory* high_fac=new HighFactory();
    Chair* chair_=high_fac->createChair();
    
    delete high_fac;
    
    return 0;
}
```

---

