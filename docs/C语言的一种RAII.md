# C语言的一种RAII

今天看书的时候看到一种RAII（资源分配即初始化）的实现，感觉非常有意思，使用起来也比较简洁，在此分享一下。

这是GNU的扩展中使用宏来实现的。通过声明一个变量然后给这个变量关联属性：

1. 一个类型（type）
2. 创建变量时执行的函数（init）
3. 变量超出作用域时执行的函数（destructor）

宏的写法如下：

```c
#define RAII_VARIABLE(vartype, varname, init, dtor) \
        void _dtor_##varname(vartype* v){ dtor(*v); } \
        vartype varname __attribute__((cleanup(_dtor_##varname))) = (init)
```

* 定义`RAII_VARIABLE`宏传入参数类型、参数名、函数指针
* 展开：函数返回类型为void，函数名前缀为`_dtor_`加上自定义的参数名，函数的入参为宏传入的参数类型指针v，函数执行体中执行destructor（变量超出作用域时执行的函数）
* 设置参数名表示的变量属性：设置cleanup为前面的展开函数
* init动作返回赋值于宏展开传入的参数名

下面展示示例代码：

```c
#include <stdlib.h>
#include <stdio.h>

#define RAII_VARIABLE(vartype, varname, init, dtor) \
	void _dtor_##varname(vartype* v){ dtor(*v); } \
	vartype varname __attribute__((cleanup(_dtor_##varname))) = (init)

/* 
 *  vartype: char*
 *  varname: name
 *  init: (char*)malloc(32)
 *  dtor: free
 */
void raiiTest(){
	RAII_VARIABLE(char*, name, (char*)malloc(32), free);
	strcpy(name, "this is ZJP");
	printf("%s\n", name);
}

int main(int argc, char** argv){
	raiiTest();
	return 0;
}
```

执行的输出为：

```shell
this is ZJP
```

---

