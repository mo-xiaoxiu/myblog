# C语言实现虚函数机制

## 实现方式

* 虚函数指针
* 虚表
* 执行函数

## 代码实现

```C title="c_virtual_function.c"
#include <stdio.h>

struct Animal {
    const struct AnimalClass* class; //virtual ptr
};

struct AnimalClass {
    void (*Eat)(struct Animal*); //virtual function 
}; //virtual table


// normal function
void Move(struct Animal* self) {
    printf("This is nomal move: %p\n", (void*)self);
}

// virtual function
void Eat(struct Animal* self) {
    const struct AnimalClass* c = *(const void**)self;
    if(c->Eat) {
        c->Eat(self);
    }else{
        fprintf(stderr, "Eat not implement.\n");
    }
}


//function in virtual function
static void real_eat(struct Animal* self) {
    printf("This is real eat funtion: %p\n", (void*)self);
}

const struct AnimalClass Animal = {(void*)0}; //一个虚表为空：无多态
const struct AnimalClass RealEat = {real_eat}; //另一个虚表存放真正的执行函数：有多态

int main() {
    struct Animal animal = {&Animal}; //一个对象中无虚函数指针
    struct Animal realEat = {&RealEat}; //另一个对象有虚函数指针

    Move(&animal);
    Move(&realEat);

    // 虚函数执行各自真正的执行函数
    Eat(&animal);
    Eat(&realEat);

    return 0;
}
```

*在Dev C++ 中使用C99，编译结果如下：*

```
This is nomal move: 000000000062FE10
This is nomal move: 000000000062FE00
Eat not implement.
This is real eat funtion: 000000000062FE00
```