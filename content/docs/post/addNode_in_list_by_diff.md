---
title: "换个角度思考--插入节点"
date: 2021-10-23T17:40:58+08:00
draft: true
---

# 另类的节点插入

## 问题

*一个不知道头节点的单链表，如何知道一个p节点的情况下，在p节点前插入一个节点*

## 思路

在文章[链表：删除节点，难吗？](https://myblog-gamma-olive.vercel.app/posts/list_deletenode_by_diff/)中，迁移思路：

* 由于是单向链表，所以只能考虑 p 节点之后的一个节点

* 类似的，我们需要在 p 节点之前插入，那就需要有一个节点来当“替身”，替代 p ，并且使 p 往后一个位置

* 这个替换 p 的节点可以有两种思路：

  * 用 p 的后一个节点来替换
  * 用 插入的新节点来替换

  第一种思路很明显不适合，只是适合删除节点的操作；

  来试一下第二种思路

* 但是 p 的前一个节点不能找到，所以 p 的位置不能动，只能寻求 p 的后一个节点来帮忙

* 那尝试一下将新的节点插入到 p 节点之后

* 这个时候是后插，不符合条件，借鉴上一个题的思路，可以将 p 的值和新插入的节点的值进行交换，这样 p 的值就成功的往后一个位置，且 性的节点也就成功插入了

## 解决

*代码实现：*

```C++
class Solution{
public:
    void addNodeBeforP(ListNode* P,int x){
        ListNode* newNode=new ListNode(x);	// 创建新的节点
        ListNode* afterP=P->next;	// 记录p后一个位置节点，方便插入后连接
        
        // 将新节点插入链表
        P->next=newNode;
        newNode->next=afterP;
        
        // 交换 p 和 新节点的值
        int tmp=P->val;
        p->val=x;
        newNode->val=tmp;
      
    }
    
};
```

---

