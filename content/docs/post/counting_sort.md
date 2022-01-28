---
title: "计数排序代码实现"
date: 2021-09-06T14:11:24+08:00
draft: true
---

计数排序和桶排序类似。桶排序是用桶将数组中的元素归类放进，而计数排序是将数组中出现的元素个数进行计数。

## 情景
```C
#include<stdio.h>
#include<stdlib.h>
#define NARRAY 10

void test(){
    int arr[NARRAY];
    int i=0;
    for(;i<NARRAY;i++){
        arr[i]=rand()%NARRAY;
    }

    printf("Before sort:\n");
    printArray(arr);

    printf("After sort:\n");
    counting_sort(arr);
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

    for(int i=0;i<NARRAY;i++){
        printf("%d ",arr[i]);
    }
    printf("\n");
}
```

## 计数排序
```C
// find max num
int findMax(const int*arr){
    int max=0;
    for(int i=0;i<NARRAY;i++){
        if(arr[max]<=arr[i]){
            max=i;
        }
    }
    return arr[max];
}


// counting sort
void counting_sort(int*arr){
    if(NULL==arr) return;

    int max=findMax(arr);
    int*b=(int*)malloc((max+1)*sizeof(int));
    memset(b,0,sizeof(int)*(max+1));

    for(int i=0;i<NARRAY;i++) b[arr[i]]++;

    // back to the array
    int j=0;
    for(int i=0;i<max+1;i++){
        if(b[i]!=0){
            while(b[i]!=0){
                arr[j++]=i;
                b[i]--;
            }
        }
    }
}
```