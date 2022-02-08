---
title: "链表的拓展"
date: 2021-09-06T22:18:52+08:00
draft: true
---
# 链表的其他操作

链表的操作除了最基本的增删改查之外，还有其他一些操作，这体现在一些算法题目中。接下来列举学习了一些算法题之后的有关于链表的算法操作

## 删除链表的倒数第k个节点

* 对于双向链表而言，删除倒数第k个节点的操作非常方便，只需要创建一个指针定位到链表的最后一个节点，再往头节点方向偏移k个位置即可；对于单向链表而言，这个删除操作相对来说会复杂一些。

* 这里介绍一个简单的方法：
  1.设置一个指针从头节点开始遍历，偏移k个节点位置之后，再找一个指针指向头节点，此时，再让这两个指针同时移动，当前一个先偏移k个节点位置的指针遍历结束时，此时后来的偏移指针指向的就是倒数第k个节点。
  *以下是代码演示：*

  ```C
  #include<stdio.h>
  #include<stdlib.h>
  
  // node with head
  struct Node{
    Int data;
    struct Node*next;
  };
  // nodelist
  struct NodeList{
    int size;
    struct Node header;
  };
  
  // init nodelist and other operate
  // ...
  
  // delete the number k node back from nodelist
  void delBackOfk(struct NodeList*list){
    if(list->size==0) return;
    
    // the quick pointer
    struct NodeList*quick=list->header.next;
    
    for(int i=0;i<k;k++){
      quick=quick->next;
    }
    
    // the slow pointer
    struct NodeList*slow=list->header.next;
    // the pre pointer before slow pointer
    struct NodeList*pre=&list->header;
    while(quick!=NULL){
      pre=slow;
      slow=slow->next;
      quick=quick->next;
    }
    
    // delete the node
    pre->next=slow->next;
    free(slow);
    slow=NULL;
  } 
  
  // test
  void test(){
    // ...test code
  }
  
  int main(){
    test();
    return 0;
  }
  ```

## 指定区间反转链表

顾名思义，反转一个链表在指定区间中的节点，与之前的反转整个链表差不多。需要注意的是，我们需要在指定区间的左右两个相邻节点的地方记录位置--用指针记录，方便在反转完指定区间的节点链表之后能够将反转后的链表的头尾节点连接回原链表中。

* 指定一个前指针用来遍历找到左区间
* 记录左区间左边的节点位置，记录左区间的第一个节点（*方便连接*）
* 反转链表
* 头尾节点重新连接，还原回链表
  *以下为代码实现：*

```C++
// leetcode code mod
// The list with no head
class Solution{
 public:
  ListNode*reverseNodeList(ListNode*head,int left,int right){
    ListNode*dummy=new ListNode(0);
    dummy->next=head;
    
    ListNode*pre=dummy;ListNode*cur=head;
    int curPos=1;
    for(;curPos<left;curPos++){
      pre=cur;
      cur=cur->next;
    }
    
    ListNode*prev=pre;ListNode*tail=cur;
    ListNode*tmp=nullptr;
    for(;curPos<=right;curPos++){
      tmp=cur->next;
      cur->next=pre;
      pre=cur;
      cur=tmp;
    }
    
    tail->next=cur;
    pre->next=prev;
    
    return dummy->next;
  }
};
```


