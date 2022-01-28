---
title: "链表的代码实现(2)"
date: 2021-09-06T10:29:50+08:00
draft: true
---
对于链表的操作还有那些呢？在这里我多列举了几种，仅供参考。

## 链表的反转
```C
// reverse list
struct ListNode*reverse(struct ListNode*mylist){
    if(mylist->size==0) return;

    struct ListNode*head=mylist->header.next;
    struct ListNode*pre=NULL;
    struct ListNode*tmp=NULL;

    while(head){
        tmp=head->next;
        head->next=pre;
        pre=head;
        head=tmp;
    }

    mylist->header=pre;
    return mylist;
}
```

## 两个链表相加
```C
// list1's val add in list2's val
struct ListNode*TwoListPlus(struct ListNode*l1,struct ListNode*l2){
    if(l1->size==0) return l2;
    if(l2->size==0) return l1;

    struct Node*head=struct Node*tail=NULL;
    struct Node*t1=l1->header.next;
    struct Node*t2=t2->header.next;

    while(t1 || t2){
        int n1=t1?t1->val:0;
        int n2=t2?t2->val:0;
        int carry=0;
        int sum=n1+n2+carry;

        if(!head){
            head=tail=(struct Node*)malloc(sizeof(struct Node));
            head->val=tail->val=sum%10;
        }
        else{
            tail->next=(struct Node*)malloc(sizeof(struct Node));
            tail->next->val=sum%10;
            tail=tail->next;
        }
        carry=sum/10;

        if(t1){
            t1=t1->next;
        }
        if(t2){
            t2=t2->next;
        }
    }
    if(carry>0){
        tail->next=(struct Node*)malloc(sizeof(struct Node));
        tail->next->val=carry;
    }
    
    struct ListNode*newlist=(struct ListNode*)malloc(sizeof(struct ListNode));
    newlist->header.next=head;
    // you can get its size
    // ...
    

    return newlist;
}
```

## 链表的快速排序
*基于快速排序算法*
```C
// swap element
void swap(struct Node*i,struct Node*j){
    int tmp=i->val;
    i->val=j->val;
    j->val=tmp;
}


// quick_sort
void quick_sort(struct Node*first,struct Node*last){
    if(first->next!=last) return;

    struct Node*i=first;
    struct Node*j=i->next;
    int pivot=first->val;

    while(j!=last){
        if(j->val<=pivot){
            i=i->next;
            swap(i,j);
        }
        j=j->next;
    }

    swap(i,first);

    quick_sort(first,i);
    quick_sort(i->next,last);
}

// ...
// when you want to use it
struct ListNode* quick_sort_(struct ListNode*mylist){
    if(mylist->size==0) return 0;

    struct Node*first=mylist->header.next;
    struct Node*last=NULL;

    quick_sort(first,last);
    return mylist;
}
```

## 链表的归并排序
*基于归并排序算法*
```C
//merge_sort
struct ListNode*merge_sort(struct ListNode*mylist){
    struct Node*head=mylist->header.next;
    mylist->header.next=sortList(head,NULL);
    return mylist;
}

// merge
struct Node*merge(struct Node*l1,struct Node*l2){
    struct Node*head;
    struct Node*tmp=head;

    while(l1 || l2){
        if(l1->val<=l2->val){
            tmp->next=l1;
            l1=l1->next;
        }
        else{
            tmp->next=l2;
            l2=l2->next;
        }
        tmp=tmp->next;
    }

    tmp->next=l1?l1:l2;
    return head->next;
}

// sort list
struct Node*sortList(struct Node*head,struct Node*tail){
    if(head==NULL) return head;
    if(head->next==tail){
        head->next=NULL;
        return head;
    }

    // quick and slow pointer
    struct Node*quick=struct Node*slow=head;

    // find the mid 
    while(quick!=NULL){
        quick=quick->next;
        slow=slow->next;
        if(quick!=NULL){
            quick=quick->next;
        }
    }

    struct ListNode*mid=slow;

    // merge 
    return merge(sortList(first,mid),sortList(mid,last));

}

```

*大家可能对有些代码不是很理解，不过没关系，这两篇文章只是对于代码的一个演示，接下来会有解析文章，用图文的方式说明解释这些内容。*
**......**