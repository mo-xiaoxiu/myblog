---
title: "合并k个有序链表"
date: 2021-09-12T14:37:54+08:00
draft: true
---

# 合并k个有序链表

## 合并两个链表

之前的文章写过合并两个链表：

*代码如下：*

```C++
/*
struct ListNode{
	int val;
	ListNode* next;
	
	// constructor
	ListNode():val(0),next(nullptr){}
	ListNode(int x):val(x),next(nullptr){}
	ListNode(int x,ListNode* ptr):val(x),next(ptr)
	
};
*/


// merge two sorted lists
class Solution{
public:
    ListNode* mergeTwoList(ListNode* l1,ListNode* l2){
        if(!(l1) || !(l2)) return l1?l1:l2;
        
        ListNode head,*t1=l1,*t2=l2;
        ListNode* tmp=&head;
        
        while(t1 && t2){
            if(t1->val<=t2->val){
                tmp->next=t1;
                t1=t1->next;
            }else{
                tmp->next=t2;
                t2=t2->next;
            }
            tmp=tmp->next;
        }
        
        tmp->next=t1?t1:t2;
        return head.next;
    }
};
```

---

## 归并排序

之前还写过了链表的归并排序：

*代码如下：*

```C++
class Solution{
public:
    ListNode* merge(ListNode* l1,ListNode* l2){
        if(!(l1) || !(l2)) return l1?l1:l2;
        
        ListNode head;*t1=l1,*t2=l2;
        ListNode* tmp=&head;
        while(t1 && t2){
            if(t1->val<=t2->val){
                tmp->next=t1;
                t1=t1->next;
            }else{
                tmp->next=t2;
                t2=t2->next;
            }
            tmp=tmp->next;
        }
        
        tmp->next=t1?t1:t2;
        return head.next;
    }
    
    ListNode* sortList(ListNode* head,ListNode* tail){
        if(head==nullptr) return nullptr;
        if(head->next==tail){
            head->next=nullptr;
            return head;
        }
        
        ListNode* slow=head,*fast=head;
        while(fast!=nullptr){
            fast=fast->next;
            slow=slow->next;
            if(fast!=nullptr) fast=fast->next;
        }
        
        ListNode* mid=slow;
        return merge(sortList(head,mid),sortList(mid,tail));
    }
    
    ListNode* merge_sort(ListNode* head){
        return sortList(head,nullptr);
    }
};
```

---

## 合并k个有序链表

只需要调用上面两个方法，综合运用一下：

```C++
class Solution {
public:
    ListNode* mergeTwoLists(ListNode *a, ListNode *b) {
        if ((!a) || (!b)) return a ? a : b;
        ListNode head, *tail = &head, *aPtr = a, *bPtr = b;
        while (aPtr && bPtr) {
            if (aPtr->val < bPtr->val) {
                tail->next = aPtr; aPtr = aPtr->next;
            } else {
                tail->next = bPtr; bPtr = bPtr->next;
            }
            tail = tail->next;
        }
        tail->next = (aPtr ? aPtr : bPtr);
        return head.next;
    }

    ListNode* merge(vector <ListNode*> &lists, int l, int r) {
        if (l == r) return lists[l];
        if (l > r) return nullptr;
        int mid = (l + r) >> 1;
        return mergeTwoLists(merge(lists, l, mid), merge(lists, mid + 1, r));
    }

    ListNode* mergeKLists(vector<ListNode*>& lists) {
        return merge(lists, 0, lists.size() - 1);
    }
};

```

