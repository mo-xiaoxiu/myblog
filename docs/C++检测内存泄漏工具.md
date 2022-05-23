# C++检测内存泄漏工具

* 通过重载`operator new`和`operator delete`来实现
* 调用`operator new`的时候记录内存信息；释放内存调用`operator delete`并删除信息

## 重载

```cpp
#define new new(__FILE__, __LINE__)
```

通过new宏定义调用重载之后的函数

* 原来的`operator new`

```cpp
void* operator new(std::size_t size);
void* operator new[](std::size_t size);
```

* 重载（记录申请内存信息）的`operator new`

```cpp
void* operator new(std::size_t size, const char* file, int line);
void* operator new[](std::size_t size, const char* file, int line);
```



## new申请内存

申请的内存块结构体信息：

```cpp
struct new_ptr_list_t
{
    new_ptr_list_t prev; //前指针
    new_ptr_list_t next; //后指针
    std::size_t size; //内存大小
    unsigned line: 31; //初始化行数
    unsigned magic; //内存是否损坏的标志
    unsigned is_array: 1; //初始化是否是内存数组的标志
    
    union
    {
        char filename[__DEBUG_NEW_FILENAME_LEN]; //文件名信息
        void* addr; //地址信息
    };
};
```



```cpp
void* operator new(std::size_t size, const char* file, int line) {
    return alloc_mem(size, file, line, false);
}
void* operator new[](std::size_t size, const char* file, int line) {
    return alloc_mem(size, file, line, true);
}

static void* alloc_mem(std::size_t size, const char* file, int line, bool is_array) {
    assert(line>=0);
    
    std::size_t s = size + ALIGNED_LIST_ITEM_SIZE;
    new_ptr_list_t* ptr = (new_ptr_list_t)malloc(s);
    
    if (ptr == nullptr) {
		std::unique_lock<std::mutex> lock(new_output_lock);
		printf("Out of memory when allocating %lu bytes\n", (unsigned long)size);
		abort();
	}
    
    void* usr_ptr = (char*)ptr + ALIGNED_LIST_ITEM_SIZE;
    
    if(line) {
        strncpy(ptr->filename, file, __DEBUG_NEW_FILENAME_LEN - 1)[__DEBUG_NEW_FILENAME_LEN - 1] = '\0';
    }else{
        ptr->addr = (void*)file;
    }
    
    ptr->line = line;
    ptr->size = size;
    ptr->is_array = is_array;
    ptr->magic = DEBUG_NEW_MAGIC;
    
    {
        std::unique_ptr<std::mutex> lock(new_ptr_lock);
        ptr->prev = new_ptr_list.prev;
        ptr->next = &new_ptr_list;
        new_ptr_list.prev->next = ptr;
        new_ptr_list.prev = ptr;
    } //将申请的内存块插入链表
    
    if (new_verbose_flag) {
		std::unique_lock<std::mutex> lock(new_output_lock);
		printf("new%s: allocated %p (size %lu, ", is_array ? "[]" : "", usr_ptr, (unsigned long)size);
		if (line != 0) {
			print_position(ptr->filename, line);
		}
		else
		{
			print_position(ptr->addr, line);
		}
		printf("\n");
	}
    
    total_mem_alloc += size;
    return usr_ptr;
}
```

**没有被new宏定义包裹（例如第三方库申请内存）**：

```cpp
void* operator new(std::size_t size) {
    return operator new(size, nullptr, 0);
} //缺点：不能记录具体内存泄漏的代码位置

//解决方法：记录调用堆栈信息，输出打印
```





## delete释放内存

```cpp
void operator delete(void* ptr) {
    free_pointer(ptr, nullptr, false);
}
void operator delete[](void* ptr) {
    free_pointer(ptr, nullptr, true);
}

void free_pointer(void* usr_ptr, void* addr, bool is_array) {
    if (usr_ptr == nullptr) {
		return;
	}
	new_ptr_list_t* ptr = (new_ptr_list_t*)((char*)usr_ptr - ALIGNED_LIST_ITEM_SIZE); //usr_ptr 还原为 new_ptr_list_t
	if (ptr->magic != DEBUG_NEW_MAGIC) { //内存损坏，加锁打印信息
		{
			std::unique_lock<std::mutex> lock(new_output_lock);
			printf("delete%s: invalid pointer %p (", is_array ? "[]" : "", usr_ptr);
			print_position(addr, 0);
			printf(")\n");
		}
		checkMemoryCorruption(); //解锁检查损坏内存
		abort();
	}

	if ((unsigned)is_array != ptr->is_array) {
		const char* msg;
		if (is_array) {
			msg = "delect[] after new";
		}
		else {
			msg = "delete after new[]";
		}
		std::unique_lock<std::mutex> lock(new_output_lock); //加锁输出信息
		printf("%s: pointer %p (size %u)\n\tat ", msg, (char*)ptr + ALIGNED_LIST_ITEM_SIZE, (unsigned long)ptr->size);
		print_position(addr, 0);
		printf("\n\torignally allocated at ");
		if (ptr->line) {
			print_position(ptr->filename, ptr->line);
		}
		else {
			print_position(ptr->addr, ptr->line);
		}
		printf("\n");
		abort();
	}

	{
		std::unique_lock<std::mutex> lock(new_ptr_lock); //加锁删除信息
		total_mem_size -= ptr->size;
		ptr->magic = 0;
		ptr->prev->next = ptr->next;
		ptr->next->prev = ptr->prev;
	}//加锁指针操作，从链表中删除释放内存块

	if (new_verbose_flag) {
		std::unique_lock<std::mutex> lock(new_output_lock);
		printf("delete%s: freed %p (size %lu, %lu bytes still allocated)\n", is_array ? "[]" : "",
			(char*)ptr + ALIGNED_LIST_ITEM_SIZE, (unsigned long)ptr->size, (unsigned long)total_mem_size);
	}
	free(ptr); //最后释放内存
}
```





## 检测是否内存泄漏

遍历内存链表，记录数量

```cpp
int checkMemoryLeaks() {
	int leak_cnt = 0;
	int whitelisted_leak_cnt = 0;
	new_ptr_list_t* ptr = new_ptr_list.next;

	while (ptr != &new_ptr_list) { //遍历链表
		const char* usr_ptr = (char*)ptr + ALIGNED_LIST_ITEM_SIZE;
		if (ptr->magic != DEBUG_NEW_MAGIC) {
			printf("warning: heap data corrupt near %p\n", usr_ptr);
		}

		printf("Leaked object at %p (size %lu, ", usr_ptr, (unsigned long)ptr->size);

		if (ptr->line) {
			print_position(ptr->filename, ptr->line);
		}
		else {
			print_position(ptr->addr, ptr->line);
		}

		printf(")\n");
		++leak_cnt;
	}

	if (new_verbose_flag || leak_cnt) {
		printf("*** %d leaks found\n", leak_cnt);
	}
	return leak_cnt;
}

//检查内存损坏
int checkMemoryCorruption() {
	int corrup_cnt = 0;
	printf("*** checking for memory corruption: START\n");
	for (new_ptr_list_t* ptr = new_ptr_list.next; ptr != &new_ptr_list; ptr = ptr->next) { //遍历链表
		const char* const usr_ptr = (char*)ptr + ALIGNED_LIST_ITEM_SIZE;
		if (ptr->magic == DEBUG_NEW_MAGIC)
			continue;
		printf("Heap data corrupt near %p (size %lu, ", usr_ptr, (unsigned long)ptr->size); //ptr->magic != __DEBUG_NEW_MAGIC

		if (ptr->line) {
			print_position(ptr->filename, ptr->line);
		}
		else
		{
			print_position(ptr->addr, ptr->line);
		}
		printf(")\n");
		++corrup_cnt;
	}
	printf("*** checking for memory corruption: %d found\n", corrup_cnt);
	return corrup_cnt;
}
```

---





## 完整代码

```cpp title="memoryDelect.h"
#pragma once

#include <stdio.h>
#include <iostream>

//重载operator new和operator new[]
void* operator new(std::size_t size, const char* file, int line);
void* operator new[](std::size_t size, const char* file, int line);

int checkMemoryLeaks();
```



```cpp title="memoryDelect.cpp"
#include "memoryDelect.h"

#ifdef new
#undef new
#endif

#include <assert.h> //assert
#include <stdlib.h> //abort
#include <string.h> //sprintf/strncpy/strcpy

#include <memory>
#include <mutex>

int checkMemoryLeaks();
int checkMemoryCorruption();

#ifndef __DEBUG_NEW_ALIGNMENT
#define __DEBUG_NEW_ALIGNMENT 16
#endif // !__DEBUG_NEW_ALIGNMENT

#ifndef __DEBUG_CALLER_ADDRESS
#ifdef __GNUC__
#define __DEBUG_CALLER_ADDRESS __builtin_return_address(0)
#else
#define __DEBUG_CALLER_ADDERSS nullptr
#endif
#endif // !__DEBUG_CALLER_ADDRESS

#ifndef __DEBUG_NEW_FILENAME_LEN
#define __DEBUG_NEW_FILENAME_LEN 200
#endif // !__DEBUG_NEW_FILENAME_LEN

#define ALIGN(s) (((s) + __DEBUG_NEW_ALIGNMENT - 1) &~ (__DEBUG_NEW_ALIGNMENT - 1)) //子节对齐

//存储内存块信息的结构体
struct new_ptr_list_t
{
	new_ptr_list_t* prev;
	new_ptr_list_t* next;
	std::size_t size;
	union 
	{
		char filename[__DEBUG_NEW_FILENAME_LEN];
		void* addr;
	};

	unsigned line : 31;
	unsigned is_array : 1;
	unsigned magic;
};

static const unsigned DEBUG_NEW_MAGIC = 0x4442474E;
static const int ALIGNED_LIST_ITEM_SIZE = ALIGN(sizeof(new_ptr_list_t));

static new_ptr_list_t new_ptr_list = { &new_ptr_list, &new_ptr_list, 0, {""}, 0, 0, DEBUG_NEW_MAGIC };

static std::mutex new_ptr_lock; //指针操作互斥
static std::mutex new_output_lock; //输出操作互斥
static std::size_t total_mem_size = 0;

static bool new_autocheck_flag = true;
static bool new_verbose_flag = false;

//有行号打印行号和地址，无行号打印地址
static void print_position(const void* ptr, int line) {
	if (line != 0) { //行号不为0，打印指针和行号
		printf("%s:%d", (const char*)ptr, line);
	}
	else if(ptr != nullptr) //行号为空，指针不为空，打印指针
	{
		printf("%p", ptr);
	}
	else //否则未知
	{
		printf("<Unknown>");
	}
}

//分配内存
static void* alloc_mem(std::size_t size, const char* file, int line, bool is_array) {
	assert(line >= 0);

	std::size_t s = size + ALIGNED_LIST_ITEM_SIZE;
	new_ptr_list_t* ptr = (new_ptr_list_t*)malloc(s);
	if (ptr == nullptr) {
		std::unique_lock<std::mutex> lock(new_output_lock);
		printf("Out of memory when allocating %lu bytes\n", (unsigned long)size);
		abort();
	}
	void* usr_ptr = (char*)ptr + ALIGNED_LIST_ITEM_SIZE;

	if (line) { //有行号，则将文件名写入
		strncpy(ptr->filename, file, __DEBUG_NEW_FILENAME_LEN - 1)[__DEBUG_NEW_FILENAME_LEN - 1] = '\0';
	}
	else //无行号，则文件作为地址
	{
		ptr->addr = (void*)file;
	}

	ptr->line = line;
	ptr->magic = DEBUG_NEW_MAGIC; //无损坏
	ptr->is_array = is_array;
	ptr->size = size;
	{
		std::unique_lock<std::mutex> lock(new_ptr_lock);
		ptr->prev = new_ptr_list.prev;
		ptr->next = &new_ptr_list;
		new_ptr_list.prev->next = ptr;
		new_ptr_list.prev = ptr;
	}//前插操作

	if (new_verbose_flag) {
		std::unique_lock<std::mutex> lock(new_output_lock);
		printf("new%s: allocated %p (size %lu, ", is_array ? "[]" : "", usr_ptr, (unsigned long)size);
		if (line != 0) {
			print_position(ptr->filename, line);
		}
		else
		{
			print_position(ptr->addr, line);
		}
		printf("\n");
	}
	total_mem_size += size;
	return usr_ptr;
}

//释放内存
static void	free_pointer(void* usr_ptr, void* addr, bool is_array) {
	if (usr_ptr == nullptr) {
		return;
	}
	new_ptr_list_t* ptr = (new_ptr_list_t*)((char*)usr_ptr - ALIGNED_LIST_ITEM_SIZE); //usr_ptr 还原为 new_ptr_list_t
	if (ptr->magic != DEBUG_NEW_MAGIC) { //内存损坏，加锁打印信息
		{
			std::unique_lock<std::mutex> lock(new_output_lock);
			printf("delete%s: invalid pointer %p (", is_array ? "[]" : "", usr_ptr);
			print_position(addr, 0);
			printf(")\n");
		}
		checkMemoryCorruption(); //解锁检查损坏内存
		abort();
	}

	if ((unsigned)is_array != ptr->is_array) {
		const char* msg;
		if (is_array) {
			msg = "delect[] after new";
		}
		else {
			msg = "delete after new[]";
		}
		std::unique_lock<std::mutex> lock(new_output_lock);
		printf("%s: pointer %p (size %u)\n\tat ", msg, (char*)ptr + ALIGNED_LIST_ITEM_SIZE, (unsigned long)ptr->size);
		print_position(addr, 0);
		printf("\n\torignally allocated at ");
		if (ptr->line) {
			print_position(ptr->filename, ptr->line);
		}
		else {
			print_position(ptr->addr, ptr->line);
		}
		printf("\n");
		abort();
	}

	{
		std::unique_lock<std::mutex> lock(new_ptr_lock);
		total_mem_size -= ptr->size;
		ptr->magic = 0;
		ptr->prev->next = ptr->next;
		ptr->next->prev = ptr->prev;
	}//加锁指针操作，从链表中删除释放内存块

	if (new_verbose_flag) {
		std::unique_lock<std::mutex> lock(new_output_lock);
		printf("delete%s: freed %p (size %lu, %lu bytes still allocated)\n", is_array ? "[]" : "",
			(char*)ptr + ALIGNED_LIST_ITEM_SIZE, (unsigned long)ptr->size, (unsigned long)total_mem_size);
	}
	free(ptr);
}

//检查内存泄漏
int checkMemoryLeaks() {
	int leak_cnt = 0;
	int whitelisted_leak_cnt = 0;
	new_ptr_list_t* ptr = new_ptr_list.next;

	while (ptr != &new_ptr_list) { //遍历链表
		const char* usr_ptr = (char*)ptr + ALIGNED_LIST_ITEM_SIZE;
		if (ptr->magic != DEBUG_NEW_MAGIC) {
			printf("warning: heap data corrupt near %p\n", usr_ptr);
		}

		printf("Leaked object at %p (size %lu, ", usr_ptr, (unsigned long)ptr->size);

		if (ptr->line) {
			print_position(ptr->filename, ptr->line);
		}
		else {
			print_position(ptr->addr, ptr->line);
		}
        
		ptr = ptr->next;
		printf(")\n");
		++leak_cnt;
	}

	if (new_verbose_flag || leak_cnt) {
		printf("*** %d leaks found\n", leak_cnt);
	}
	return leak_cnt;
}

//检查内存损坏
int checkMemoryCorruption() {
	int corrup_cnt = 0;
	printf("*** checking for memory corruption: START\n");
	for (new_ptr_list_t* ptr = new_ptr_list.next; ptr != &new_ptr_list; ptr = ptr->next) { //遍历链表
		const char* const usr_ptr = (char*)ptr + ALIGNED_LIST_ITEM_SIZE;
		if (ptr->magic == DEBUG_NEW_MAGIC)
			continue;
		printf("Heap data corrupt near %p (size %lu, ", usr_ptr, (unsigned long)ptr->size); //ptr->magic != __DEBUG_NEW_MAGIC

		if (ptr->line) {
			print_position(ptr->filename, ptr->line);
		}
		else
		{
			print_position(ptr->addr, ptr->line);
		}
		printf(")\n");
		++corrup_cnt;
	}
	printf("*** checking for memory corruption: %d found\n", corrup_cnt);
	return corrup_cnt;
}

//重载的operator new 封装 alloc_mem函数
void* operator new(std::size_t size, const char* file, int line) {
	void* ptr = alloc_mem(size, file, line, false);
	return ptr;
}

void* operator new[](std::size_t size, const char* file, int line) {
	void* ptr = alloc_mem(size, file, line, true);
	return ptr;
}

//全局的operator new 封装重载的 operator new
void* operator new(std::size_t size) {
	return operator new(size, (char*)__DEBUG_CALLER_ADDERSS, 0);
}

void* operator new[](std::size_t size) {
	return operator new[](size, (char*)__DEBUG_CALLER_ADDERSS, 0);
}

void operator delete(void* ptr) {
	free_pointer(ptr, __DEBUG_CALLER_ADDERSS, false); //free_pointer(ptr, nullptr, 0);
}

void operator delete[](void* ptr) {
	free_pointer(ptr, __DEBUG_CALLER_ADDERSS, true);
}
```

---

> 本文记录学习来源：程序喵公众号
>
> 文章代码参考[](https://github.com/chengxumiaodaren/wzq_utils/tree/master/memory)





## 测试代码

```cpp title="test.cpp"
#include "memoryDelect.h"

#include <iostream>
#include <memory>
#include <mutex>


class A
{
public:
	int a;
};

int main() {
	printf("Memory delect \n");
	int* p1 = new int;
	delete p1;

	int* p2 = new int[4];
	//delete[] p2;

	A* p3 = new A;
	delete p3;

	checkMemoryLeaks();
	return 0;
}
```

*在`VisualStudio2019`上运行的结果为：*

```
Memory delect
Leaked object at 01611DB8 (size 16, <Unknown>)
*** 1 leaks found
```

---

