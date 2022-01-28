---
title: "链表的代码实现(1)"
date: 2021-09-06T09:14:59+08:00
draft: true
---

# 链表的实现

这篇文章呈现的是数据结构中的链表的一些基本操作：

* 创建链表
* 链表初始化
* 添加节点
* 删除节点
* 查找值
* 合并两个有序链表
* 对链表进行插入排序
* ......

## 创建链表

*此处演示的是头节点的链表*

```c++
// create struct named node
struct Node{
    //data
    int val;
    //pointer
    struct Node*next;
};

// create struct named listnode
struct ListNode{
    //the size of the list
    int size;
    //the head node
    struct Node header;
};
```

*以下是没有带头节点的链表演示*

```c++
// struct named node
struct NodeList{
    int val;
    struct NodeList*next;
};

// ...
```

## 链表初始化

*C语言版本初始化链表（此处以待头节点的链表为演示）：*

```C
//init list
struct ListNode*initListNode(){
    // init head pointer
    struct ListNode*mylist
        =(struct ListNode*)malloc(sizeof(struct ListNode));
    
    mylist->size=0;
    mylist->header.next=NULL;
    mylist->header.val=0;
    
    return mylist;
};
```

*C++版本初始化链表（此处以不带头结点的链表为演示）：*

```C++
// create and init at the same time

struct NodeList{
    int val;
    struct Node *header;    
};
```

## 添加节点

*为了方便统一，后续的演示使用C语言版本*

```C
// add node
void addNode(struct ListNode*mylist,int val){
    struct Node*newNode=(struct Node*)malloc(sizeof(struct Node))；
        if(!newNode){
            printf("Memeory flow!\n");
        }
    
    // add front
    newNode->val=val;
    newNode->next=mylist->header.next;
    mylist->header.next=newNode;
    mylist->size++;
    
}
```

## 删除节点

```c
// delete node
// delete front
void delListNode(struct ListNode*mylist){
    if(mylist->size==0) return;
    
    struct Node*head=&mylist->header;
    struct Node*cur=head->next;
    
    head->next=cur->next;
    free(cur);
    mylist->size--;
}
```

## 按照值查找
```c
// find element by val
int find(struct ListNode*mylist,int val){
    if(mylist->size==0) return;
    struct ListNode*head=&mylist->header;
    while(head->next!=NULL){
        if(head->next->val==val){
            return head->next->val;
        }
        head=head->next;
    }

    if(head->next==NULL){
        return -1;
        // can not find 
    }
}
```

## 合并两个有序链表
```C
struct ListNode* mergeTwoList(struct ListNode*l1,struct ListNode*l2){
    if(l1->size==0) return l2;
    if(l2->size==0) return l1;

    struct Node*t1=l1->header.next;
    struct Node*t2=l2->header.next;
    struct Node*head;
    struct Node*tmp=head;

    while(l1 || l2){
        if(t1->val<=t2->val){
            tmp->next=t1;
            t1=t1->next;
        }
        else{
            tmp->next=t2;
            t2=t2->next;
        }
        tmp=tmp->next;
    }

    tmp->next=t1?t1:t2;
    li->header.next=l2->header.next=NULL;
    return head;
}
```

## 对链表进行插入排序
1.插入节点时选择插入排序
```c
// add node by insert_sort
void addNodeByInsert(struct ListNode*mylist,int val){
    struct Node*newNode=(struct Node*)malloc(sizeof(struct Node));
    if(!newNode){
        return;
    }

    newNode->val=val;

    struct Node*head=&mylist->header;
    while(head->next){
        if(head->next->val<=val){
            head=head->next;
        }
        else{
            break;
        }
    }

    newNode->next=head->next;
    head->next=newNode;

}
```
2.对已经存在的链表进行插入排序
```c
void insert_sort(struct ListNode*mylist){
    if(mylist->size==0) return;

    struct Node*head=&mylist->header;
    struct Node*lastSort=head->next;
    struct Node*cur=lastSort->next;

    while(cur!=NULL){
        if(lastSort->val<=cur->val){
            lastSort=lastSort->next;
        }
        else{
            if(head->next->val<=cur->val){
                head=head->next;
            }
            lastSort->next=cur->next;
            cur->next=head->next;
            head->next=cur;
        }
        cur=cur->next;
    }
}
```

