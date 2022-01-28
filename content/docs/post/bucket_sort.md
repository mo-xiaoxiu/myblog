---
title: "桶排序代码实现"
date: 2021-09-06T12:40:32+08:00
draft: true
---

桶排序：这里以数组作为排序对象，是将数组中的元素按照一定的规则放入对应规则的桶中，在桶中把数据进行排序，最后将桶中的数据取出，还原会数组的排序算法

## 情景
```C
#include<stdlib.h>
#include<stdio.h>
#define NARRAY 10       // array nums


// test
void test(){
    int arr[NARRAY];
    // init the array
    for(int i=0;i<NARRAY;i++){
        arr[i]=rand()%NARRAY;
    }

    printf("Before sort:\n");
    printArray(arr);    // print array

    printf("After sort:\n");
    bucket_sort(arr);   // bucket sort
    printArray(arr);
}


int main(){
    test();
    return 0;
}
```

## 打印数组
```C
void printArray(const int*arr){
    if(arr==NULL) return;

    int i=0;
    for(;i<NARRAY;i++){
        printf("%d ",arr[i]);
    }
    printf("\n");
}
```

## 桶排序
```C
// bucket :list
// create list
struct ListNode{
    int data;
    struct ListNode*next;
};


//find bucket pos
int getPos(int num){
    if(num>=0 && num<=NARRAY/3) return 0;
    else if(num>NARRAY/3 && num<=NARRAY*2/3) return 1;
    else return 2;
}

// print bucket
void printBucket(struct ListNode*mylist){
    if(mylist==NULL) return;

    struct ListNode*cur=mylist;
    while(cur!=NULL){
        printf("%d ",cur->data);
        cur=cur->next;
    }
    printf("\n")
}


// insert sort
struct ListNode* insertion_sort(struct ListNode*bucket){
    if(bucket==NULL) return;

    struct ListNode*head=(struct ListNode*)malloc(sizeof(struct ListNode));
    head->next=bucket;
    struct ListNode*lastSort=bucket;
    struct ListNode*cur=bucket->next;

    while(cur!=NULL){
        if(lastSort->data<=cur->data){
            lastSort=lastSort->next;
        }
        else{
            struct ListNode*pre=head;
            if(pre->next->data<=cur->data){
                pre=pre->next;
            }
            lastSort->next=cur->next;
            cur->next=pre->next;
            pre->next=cur;
        }
        cur=cur->next;
    }
    return head->next;
}


// bucket sort
void bucket_sort(int*arr){
    if(NULL==arr) return;

    // create 3 buckets
    struct ListNode**bucket=(struct ListNode**)malloc(3*sizeof(struct ListNode*));

    // init bucket
    for(int i=0;i<3;i++){
        bucket[i]=NULL;
    }

    // take array elements in buckets
    for(int i=0;i<NARRAY;i++){
        int pos=getPos(aarr[i]);
        struct ListNode*newNode=(struct ListNode*)malloc(sizeof(struct ListNode));
        newNode->data=arr[i];
        newNode->next=bucket[pos];
        bucket[pos]=newNode;
    }

    /* you can print every bucket to ensure all of the array's elements in different buckets
    for(int i=0;i<3;i++){
        printBucket(bucket[i]);
    }
    */

    // insert sort in every bucket's elements
    for(int i=0;i<3;i++){
        bucket[i]=insertion_sort(bucket[i]);
    }

    // take buckets'elements back to the array
    int j=0;
    for(int i=0;i<3;i++){
        struct ListNode*cur=bucket[i];
        while(cur){
            arr[j++]=cur->data;
            cur=cur->next;
        }
    }
}
```

