# C++ const 重载

c++重载一般有：

在函数名相同时，
* 参数类型不同；
* 参数个数不同；
* 参数类型和个数都不相同
* 在上述情况下，返回值不同（*单纯的返回值不同不能作为重载依据*）

## const重载

```cpp title="重载"
struct A {
    int count() {
        std::cout << "non const" << std::endl;
        return 1;
    }

    int count() const {
        std::cout << "const" << std::endl;
        return 1;
    }
};

int main() {
    A a;
    a.count();
    // 相当于：count(A* a) 传入一个this指针

    const A b;
    b.count();
} 
```

这段代码的输出我们来实践一下：

首先使用VScode连接到远端服务器，创建一个cpp文件，并执行；

![const_override](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/const_override.png)


输出为：
```
non const
const
```

上述代码相当于：

```cpp title="重载"
struct A {
    int count(A*) {
        std::cout << "non const" << std::endl;
        return 1;
    }

    int count(const A*) const {
        std::cout << "const" << std::endl;
        return 1;
    }
};

int main() {
    A a;
    a.count();
    // 相当于：count(A* a) 传入一个this指针

    const A b;
    b.count();
} 
```

下面是编写真正的const重载：

```cpp title="ep.cpp"
struct A {
    int count(const int& s) {
        std::cout << "const" << std::endl;
        return 1;
    }

    int count(int& s) {
        std::cout << "non const" << std::endl;
        return 1;
    }
};

int main() {
    A a;
    a.count(4); // 4是常量，调用参数为const的重载
    int c = 5; // c是变量，调用非const版本
    a.count(c);
}
```

![real_constOverride_ep](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/const_override_ep.png)


输出如下：

```
const
non const
```

## 结论

不只是参数类型和个数不同会产生重载，const修饰的参数也会有重载

## 问题：一定要指针或者引用类型时重载

**只有const修饰的指针或者应用才可以作为重载的依据**

以下举个例子：

```cpp title="non_ref_or_pointer_constOverride.cpp"
struct A {
    int count(const int s) { //const int: non ref or pointer
        std::cout << "const" << std::endl;
        return 1;
    }

    int count(int s) { //non_const int: non ref or pointer
        std::cout << "non const" << std::endl;
        return 1;
    }
};

int main() {
    A a;
    a.count(4);
    int c = 5;
    a.count(c);
}
```

![non_ref_pointer](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/non_ref_or_pointer.png)

编译错误

**为什么一定要指针或者引用类型时重载才可以呢？**

**解释：**

”When we pass by reference or pointer, we can modify the value referred or pointed, so we can have two versions of a function, one which can modify the referred or pointed value, other which can not.“

这句话的意思是：

当我们通过引用或指针传递时，我们可以修改引用或指向（指针指向）的值，因此我们可以有两个版本的函数，一个可以修改引用或指向的值，另一个不能。

**上述强调的是”const修饰的指针或者引用“**：

* **const修饰的指针：** const修饰的指针是常量指针，即底层const，该指针指向的值是不可修改的，所以可以使用const修饰的指针用于区分普通指针（可修改）和const修饰的指针作为参数传递的重载版本；
* **const修饰的引用：** 普通引用底层是指针常量，指针指向不可修改，指针指向的值可以修改，而const修饰的引用则是”常量指针常量“，即指针的指向不可修改，指针指向的值也不可以修改，所以可以用于区分重载版本


