---
title: "新的开始"
date: 2021-09-06T09:13:47+08:00
draft: true
---

从今天开始，我将会把近期学到的有关于C/C++的知识，以及平时学到的有关于数据结构与算法等计算机知识在这里做集合分享。加油！

# 新的开始

*微信公众号：墨小秀*

*个人博客：*https://myblog-mo-xiaoxiu.vercel.app/



## 前言

这是我新建的个人博客网站。在这里我将分享一些我学习各个邻域知识的知识点。由于本人并非专业，所以内容只能是尽自己的最大努力，写好每一篇文章。

## 介绍

大致的内容如下：

* 书法教程
* C、C++编程
* logo设计思路
* 数据结构与算法
* *期待......*

## 测试

接下来是为了测试网站效果的代码示例：

```C
//list


//create Node stuct
struct Node{
    int data;
    struct Node*next;
};
//create nodelist
struct NodeList{
    int size;
    struct Node header;
};

//init list
struct NodeList*initNodeList(){
    struct NodeList*myList
        =(struct NodeList*)malloc(sizeof(struct NodeList));
    myList->size=0;
    myList->header.next=NULL;
}

//add node
void addNode(struct NodeList*myList,int val){
    struct Node*newNode
        =(struct Node*)malloc(sizeof(struct Node));
    if(!newNode){
        return;
    }
    struct Node*cur=myList->header.next;
    struct Node*pre=&myList->header;
    pre->next=newNode;
    newNode->next=cur;
    // add over!
}

// ...
```

*测试完毕*



