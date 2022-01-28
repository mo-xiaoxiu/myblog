---
title: "并查集"
date: 2021-10-30T16:06:29+08:00
draft: true
---

# 并查集

并查集（Disjoint_set）

### 概念：

将有向图或者无向图，每两个节点放入到集合里：

- 如果每两个节点中，有一个节点与现有集合中的某个元素相等，则将这两个集合加入到现有的集合中；
- 如果每两个节点中，没有节点与现有集合中的任何一个元素相等，则将这两个节点单独放到一个新的集合中去
- 如果每两个节点中，两个节点在现有集合中都有出现（同一个集合），则说明这个图有环

### 问题简化

将图转化为一棵树

- 初始化：每个图元素作为节点，其父节点都为自身
- 每两个元素节点传入树中，如果其根节点不相等，则将它们相连（构建父子节点关系）
- 每两个元素节点传入树中，如果其根节点相同，则说明它们之间不能相连，因为这样转化为图来看，将它们相连会产生环

### 抽象成数据结构

使用数组可以完成相同的功能，简化模型：

- 数组中每个元素初始化为自身下标
- 每两个数（来自图），比较各自元素大小（对应的下标），不相等，则更新下标（将其中一个元素改为另一个元素的下标）：这样实现了寻找其根节点比较的功能
- 相等，则说明有环

### 代码

在centos8下的gcc 8.4.1下调试

```C++
#include<iostream>
using namespace std;
#define NPARENT 6

void init(int parent[]){
	for(int i=0;i<NPARENT+1;i++){
		parent[i] = -1;
		//cout<<"parent["<<i<<"] = "<<parent[i]<<endl;
	}
}

int find_root(int *parent,int x){
	return -1 == parent[x] ? x : parent[x] = find_root(parent,parent[x]);
}


void union_root(int *parent,int x,int y){
	int x_root = find_root(parent,x);
	int y_root = find_root(parent,y);

	cout<<"x_root = "<<x_root<<" "<<"y_root = "<<y_root<<endl;

	if(x_root == y_root){
		return;
	}else{
		parent[x_root] = y_root;
	}
}

bool is_Same(int *parent,int x,int y){
	int x_root = find_root(parent,x);
	int y_root = find_root(parent,y);
	cout<<"x_root = "<<x_root<<" "<<"y_root = "<<y_root<<endl;


	if(x_root == y_root){
		return true;
	}else{
		return false;
	}
}


void test(){
	int parent[NPARENT];

	init(parent);

	int edges[6][2] = {
		{0,1}, {0,2}, {1,3},
		{1,5}, {2,4}, {4,5}
	};

	int i=0;
	for(;i<NPARENT;i++){
		if(is_Same(parent,edges[i][0],edges[i][1])){
			cout<<"Has Cycle!\n"<<endl;
			break;
		}else{
			union_root(parent,edges[i][0],edges[i][1]);
		}
	}

	if(i == NPARENT){
		cout<<"No Cycle!\n"<<endl;
	}
}

int main(){
	test();
	return 0;
}
```



## 冗余连接

*原题连接：https://leetcode-cn.com/problems/redundant-connection/submissions/*

```
树可以看成是一个连通且 无环 的 无向 图。

给定往一棵 n 个节点 (节点值 1～n) 的树中添加一条边后的图。添加的边的两个顶点包含在 1 到 n 中间，且这条附加的边不属于树中已存在的边。图的信息记录于长度为 n 的二维数组 edges ，edges[i] = [ai, bi] 表示图中在 ai 和 bi 之间存在一条边。

请找出一条可以删去的边，删除后可使得剩余部分是一个有着 n 个节点的树。如果有多个答案，则返回数组 edges 中最后出现的边。

 

示例 1：



输入: edges = [[1,2], [1,3], [2,3]]
输出: [2,3]
示例 2：



输入: edges = [[1,2], [2,3], [3,4], [1,4], [1,5]]
输出: [1,4]
 

提示:

n == edges.length
3 <= n <= 1000
edges[i].length == 2
1 <= ai < bi <= edges.length
ai != bi
edges 中无重复元素
给定的图是连通的 

```

*代码实现：*

```C++
class Solution {
public:
    int n = 1005;
    int parent[1005];

    // 初始化为自身对应的下标
    void init(){
        for(int i=0;i<n;i++){
            parent[i] = i;
        }
    }

    // 找到元素的根节点
    int find(int x){
        // 如果与自身下标一样，则原封不动；
        // 否则，依据对应的下标继续找到其根节点
        return x == parent[x] ? x : parent[x] = find(parent[x]);
    }


    // 将两个元素相连
    void union_root(int x,int y){
        int x_root = find(x);
        int y_root = find(y);
        // 如果两个节点相同，无需相连
        if(x_root == y_root) return;
        // 不同则将其中一个节点连向另一个节点
        else parent[x_root] = y_root;
    }

    // 判断两个元素的根节点是否相同
    bool is_same_root(int x,int y){
        int x_root = find(x);
        int y_root = find(y);
        if(x_root == y_root) return true;
        else return false;
    }

    vector<int> findRedundantConnection(vector<vector<int>>& edges) {
        init();
        for(int i=0;i<edges.size();i++){
            if(is_same_root(edges[i][0],edges[i][1])){
                return edges[i];
            }else {
                union_root(edges[i][0],edges[i][1]);
            }
        }
        return {};
    }
};
```

---

