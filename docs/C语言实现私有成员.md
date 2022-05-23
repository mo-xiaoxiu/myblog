# C语言实现私有成员

如何使用C语言实现C++的私有成员属性呢？

## 需求

```c title="test.c"
#include "PersonReal.h"

void test() {
	Person* p = personNew("zjp", 18, "infor");
	int nAge = PersonGetAge(p); //无法通过p->age访问，不暴露私有成员
	printf("age = %d", nAge);
}

int main() {
	test();
	return 0;
}
```

## 解决

* 含有不想暴露的私有成员结构体，将该结构体设置为空（或者使用一个`void*`作为占位：不会浪费内存）

```c title="person.h"
#pragma once
#include <stdio.h>
#include <stdlib.h>

typedef struct
{
	void* PersonHolder;
}Person;
```

在`person.h`中，Person的私有成员不会暴露，在非必要的时候不会访问到这个文件里的内容

* 使用一个函数，传入含有不想暴露的私有成员结构体指针，在函数中**强制转换**为拥有部分该结构体私有成员相等属性的另一类型

```c title="personReal.h"
#pragma once

#include "person.h"

typedef struct 
{
	union //使用匿名联合体，等效使用字段
	{
		Person public_person;
		char const * personName;
		
	};
	int age;
	char infor[];
}PersonInternial;

//通过这个函数取出传入Person指针的年龄属性
const int PersonGetAge(Person* p) {
	return ((PersonInternial*)p)->age; //强制类型转换
}

Person* personNew(const char* name, int age, const char* infor) {
	int infor_size = (infor ? sizeof(infor) : 0);
	PersonInternial* p = (PersonInternial*)malloc(sizeof(PersonInternial) + infor_size);
	p->age= age;
	p->personName = name;
	
	if (infor) {
		strcpy(p->infor, infor); //不使用p->infor = infor，p是指针常量，通过此修改值
	}
	else {
		p->infor[0] = 0;
	}

	return p;
}
```

*这里需要注意一个小的知识点：`char const* personName`为常量指针，指针指向的值不可以被修改，而在`personNew`函数中，可以通过`p->personName = name`来改变指向，因为`name`为指针，即地址；这里的`name`为常量指针或者指针常量都可以*

*使用匿名结构体可以在赋值的时候直接访问联合体中的各个字段*

*`char*`和`char[]`的区别：首先两者都可以代表一个字符串，前者是一个指针，后者是一个char数组；前者指向字符串常量，后者指向的字符串是可以修改的，后者相当于`char *const`；两者作为函数形参效果一致；所以`char* a = "string1"`是不规范的，应该写成`const char* a = "string1"`*

**拓展知识点：**

`sizeof()`计算包含‘\0’，`strlen()`计算不包含‘\0’（识别到‘\0’）

* `char* a = "123456789"`

  ```cpp
  //sizeof(a) = 4
  //strlen(a) = 9
  ```

* `char b[] = "123456789"`

  ```cpp
  //sizeof(b) = 10
  //strlen(b) = 9
  ```

* `char c[] = {'1', '2', '3', 0}`

  ```cpp
  //sizeof(c) = 4
  //strlen(c) = 3
  ```

* `char d[] = {'1', '2', '3', '4'}`

  ```cpp
  //sizeof(d) = 4
  //strlen(d) = ??
  ```

---





## 完整代码

```cpp title="person.h"
#pragma once
#include <stdio.h>
#include <stdlib.h>

typedef struct
{
	void* PersonHolder;
}Person;
```



```cpp title="personReal.h"
#pragma once

#include "person.h"

typedef struct 
{
	union
	{
		Person public_person;
		char const * personName;
		
	};
	int age;
	char infor[];
}PersonInternial;

const int PersonGetAge(Person* p) {
	return ((PersonInternial*)p)->age;
}

Person* personNew(const char* name, int age, const char* infor) {
	int infor_size = (infor ? sizeof(infor) : 0);
	PersonInternial* p = (PersonInternial*)malloc(sizeof(PersonInternial) + infor_size);
	p->age= age;
	p->personName = name;
	
	if (infor) {
		strcpy(p->infor, infor);
	}
	else {
		p->infor[0] = 0;
	}

	return p;
}
```



```cpp title="test.c"
#include "PersonReal.h"

void test() {
	Person* p = personNew("zjp", 18, "infor");
	int nAge = PersonGetAge(p);
	printf("age = %d", nAge);
}

int main() {
	test();
	return 0;
}
```

*在VisualStudio2019上运行的结果为：*

```
age = 18
```

