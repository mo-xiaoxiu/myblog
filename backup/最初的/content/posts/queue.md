---
title: "队列的操作（代码实现）"
date: 2021-09-07T22:10:31+08:00
draft: true
---
# 队列

队列是一种**先进先出**的数据结构，我们日常生活中有很多关于队列的例子。首先肯定是各种公共场合下的排队场景，我当时在学数据结构的时候就觉得这个“队列”应该就是日常生活排队场景的抽象模型。

## 队列的实现

* 用数组来模拟队列
  *代码实现：*

  ```C++
  #define NARRAY 100
  
  // By array
  struct Queue{
    int size;      // array size
    int *arr;      // array pointer
    int capacity;  // array capacity
    int head;      // queue head
    int tail;      // queue tail
    
    // init queue
    Queue():size(0),arr(nullptr),capacity(NARRAY),head(0),tail(0){
      this->arr=new int(NARRAY);
    }
  };
  
  // push in queue
  void push(Queue& myQueue,int val){
    
    if(myQueue.size==myQueue.capacity){
      int *newArr=new int(2*NARRAY);
      
      for(int i=0;i<myQueue.size;i++){
        newArr[i]=myQueue.arr[i];
      }
      
      myQueue.arr=newArr;
      myQueue.capacity*=2;
    }
    
    myQueue.arr[tail++]=val;
    myQueue.size++;
    
    return myQueue;
  }
  
  
  // pop the front element
  void pop(Queue*myQueue){
    
    if(myQueue.head==myQueue.tail) return;
    
    myQueue.head++;
    myQueue.size--;
  }
  
  
  // get the front element
  int front(Queue*myQueue){
    
    if(myQueue.head==myQueue.tail) return NULL;
    
    return myQueue.arr[head];
  }
  
  ```

 * 用链表实现队列
   *以下是代码实现：*

   ```C++
   // By list
   struct ListNode{
     struct ListNode*next;
     int data;
     
     // init ListNode
     ListNode():data(0),next(nullptr){}
   };
   
   
   // add queue node
   void push(ListNode*list,int val){
     
     ListNode*newNode=new ListNode;
     
     if(!newNode) {
       cerr<<“Memeory flow!\n”
     }
     
     newNode->data=val;
     newNode->next=nullptr;
     
     ListNode*head=list;
     while(list->next){
       list=list->next;
     }
     
     
     list->next=newNode;
     
   }
   
   
   // pop
   void pop(ListNode*list){
     if(list==nullptr) return;
     
     ListNode*tmp=list;
     list=list->next;
     delete tmp;
     tmp=nullptr;
     
   }
   
   
   // ...
   ```

## 试着还原循环队列

循环队列是将队列的头尾连接在一起的队列，可以实现循环的插值和出值。
*用数组实现可以达到阻塞队列的效果，这里我们试着用数组还原一下*

```C++
#define NARRAY 100


// By array
struct Queue{
  int size;
  int capacity;
  int head;
  int tail;
  int *arr;
  
  Queue():size(0),capacity(NARRAY),head(0),tail(0),arr(nullptr){}
};


// push
void push(Queue*myQueue,int val){
  
  myQueue->arr[tail]=val;
  myQueue->size++;
  myQueue->tail=(myQueue->tail+1)%myQueue->capacity;
  
}


// pop
void pop(Queue*myQueue){
  
  if(myQueue->head==myQueue->tail) return;
  
  myQueue->head=(myQueue->head+1)%myQueue->capacity;
}

// ...
```

*关于循环队列的关键操作大致如上，后续还会补充...*
   
