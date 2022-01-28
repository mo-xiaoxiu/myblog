---
title: "基数排序代码实现"
date: 2021-09-06T15:41:58+08:00
draft: true
---

基数排序：跟桶排序很相似，桶中记录的是数组中的各个位数。根据数组中的最大数的位数，来决定要使用桶存储位数的次数
具体实现如下：

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
    radix_sort(arr);
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
    if(NULL==arr) return;

    for(int i=0;i<NARRAY;i++){
        printf("%d ",arr[i]);
    }
    printf("\n");
}
```

## 基数排序
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


// radix_sort
void radix_sort(int arr[]){
    if(NULL==arr) return;

    int bucket[10][10];
    int bucket_count[10];
    int count=0;

    int reminder=0;int division=1;

    int max=findMax(arr);
    while(max>0){
        count++;
        max/=10;
    }

    for(int i=0;i<count;i++){

        // init buckets
        for(int i=0;i<10;i++){
            bucket_count[i]=0;
        }

        reminder=(arr[i]/division)%10;
        bucket[reminder][bucket_count[reminder]]=arr[i];
        bucket_count[reminder]++;

        // get back to the array
        int i=0;
        for(int j=0;j<bucket_count;j++){
            for(int k=bucket[j];k>=0;k--){
                arr[i++]=bucket[j][k];
            }
        }

        // Don't forget to add division
        division*=10;
    }
}
```

**后续图文解析会补全**