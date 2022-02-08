---
title: "DFS--深度优先搜索"
date: 2021-10-27T14:14:46+08:00
draft: true
---

# 深度优先搜索

*深度优先搜索模板：*

```C++
class Solution{
public:
    return_type dfs( 递归函数参数 ){
        if( 递归终止条件 ){
            返回（值）;
        }
        
        // do something
        dfs(递归函数参数)
        // 回溯（可选）
    } 
};
```

## 图

**有向图**：u->v

**无向图**：u->v   v->u

**创建（实现）方式：**

* 二维矩阵
  * 优先：查找速度快
  * 缺点：空间复杂度高 O(n^2)
* 邻接表--链表

## 删除无效括号

*原题链接：https://leetcode-cn.com/problems/remove-invalid-parentheses/*

```
给你一个由若干括号和字母组成的字符串 s ，删除最小数量的无效括号，使得输入的字符串有效。

返回所有可能的结果。答案可以按 任意顺序 返回。

 

示例 1：

输入：s = "()())()"
输出：["(())()","()()()"]
示例 2：

输入：s = "(a)())()"
输出：["(a())()","(a)()()"]
示例 3：

输入：s = ")("
输出：[""]
 

提示：

1 <= s.length <= 25
s 由小写英文字母以及括号 '(' 和 ')' 组成
s 中至多含 20 个括号

```

### 回溯三部曲

#### 递归函数的参数和返回值

* 参数：原始字符串（作为判断是否有效字符串的本体）、递归遍历的起始位置、该移除的左右括号数（在递归函数中递减以判断条件）、实时记录左右括号数（判断条件）
* 返回值：将结果数组设置为全局的，不需要返回值（不需要从下往上返回值的）

#### 递归终止条件

* 该移除的左右括号数都被移除完毕（都为0）时，满足要求的组合放入结果并返回

#### 单层递归逻辑

* **去重操作：**判断是否有连续重复的（字符）括号，有则跳过；在跳过之前，要先记录括号数
* 从当前遍历位置开始，**如果剩余的移除括号数比剩余的括号数要大，则后续肯定不满足条件，直接返回**
* 尝试移除当前的左括号（如果当前位置是左括号）：递归，回溯
* 尝试移除当前的右括号（如果当前位置是右括号）：递归，回溯
* 实时记录此时左右括号的数量，判断是否不满足条件：当前有括号数比左括号要多；不满足则退出循环

### 判断字符串是否有效

左右括号数相等，则字符串有效

### 代码实现

```C++
class Solution {
public:
    vector<string> res; // 存放结果的数组

    // 判断字符串是否有效
    bool isValid(const string& str){
        int count=0;

        for(int i=0;i<str.size();i++){
            if(str[i]=='('){
                count++;
            }else if(str[i]==')'){
                count--;
                if(count<0) return false;
            }
        }
        // 计数为0，说明左右括号相匹配，满足条件
        return count==0;
    }

    void dfs(string str,int startIndex,int leftCount,int rightCount,int leftRemove,int rightRemove){
        // 递归终止条件：如果可移除的左右括号都移除完了，则说明这个组合满足条件
        if(leftRemove==0 && rightRemove==0){
            if(isValid(str)){
                res.push_back(str);
            }
            return;
        }

        // 单层遍历逻辑：
        // 从当前位置开始遍历
        for(int i=startIndex;i<str.size();i++){
            // 如果遇到重复的括号，更新左右括号数，跳过重复的括号
            if(i>startIndex && str[i]==str[i-1]){
                if(str[i]=='(') leftCount++;
                if(str[i]==')') rightCount++;
                continue;
            }

            // 如果待移除的括号数比剩下的括号数大，没有办法满足条件，直接返回
            if(leftRemove+rightRemove>str.size()-i) return;

            // 尝试去掉当前左括号
            if(leftRemove>0 && str[i]=='('){
                // 递归，回溯
                dfs(str.substr(0,i)+str.substr(i+1),i,leftCount,rightCount,leftRemove-1,rightRemove);
            }
            // 尝试去掉当前右括号
            if(rightRemove>0 && str[i]==')'){
                // 递归，回溯
                dfs(str.substr(0,i)+str.substr(i+1),i,leftCount,rightCount,leftRemove,rightRemove-1);
            }

            // 计算当前左右括号的数量
            if(str[i]=='('){
                leftCount++;
            }else if(str[i]==')'){
                rightCount++;
            }

            // 如果当前有括号数比左括号多，不满足条件，直接退出循环，返回
            if(rightCount>leftCount) break;
        }
    }

    vector<string> removeInvalidParentheses(string s) {
        int leftRemove=0;
        int rightRemove=0;

        // 在进行dfs之前，先遍历字符串，获得该去掉的左右括号数量
        for(auto c: s){
            if(c=='('){
                leftRemove++;
            }else if(c==')'){
                if(leftRemove==0){
                    rightRemove++;
                }else{
                    leftRemove--;
                }
            }
        }

        dfs(s,0,0,0,leftRemove,rightRemove);
        return res;
    }
};

```

---

## 喧闹和富有

*原题链接：https://leetcode-cn.com/problems/loud-and-rich/*

```
在一组 N 个人（编号为 0, 1, 2, ..., N-1）中，每个人都有不同数目的钱，以及不同程度的安静（quietness）。

为了方便起见，我们将编号为 x 的人简称为 "person x "。

如果能够肯定 person x 比 person y 更有钱的话，我们会说 richer[i] = [x, y] 。注意 richer 可能只是有效观察的一个子集。

另外，如果 person x 的安静程度为 q ，我们会说 quiet[x] = q 。

现在，返回答案 answer ，其中 answer[x] = y 的前提是，在所有拥有的钱不少于 person x 的人中，person y 是最安静的人（也就是安静值 quiet[y] 最小的人）。

示例：

输入：richer = [[1,0],[2,1],[3,1],[3,7],[4,3],[5,3],[6,3]], quiet = [3,2,5,4,6,1,7,0]
输出：[5,5,2,5,4,5,6,7]
解释： 
answer[0] = 5，
person 5 比 person 3 有更多的钱，person 3 比 person 1 有更多的钱，person 1 比 person 0 有更多的钱。
唯一较为安静（有较低的安静值 quiet[x]）的人是 person 7，
但是目前还不清楚他是否比 person 0 更有钱。

answer[7] = 7，
在所有拥有的钱肯定不少于 person 7 的人中(这可能包括 person 3，4，5，6 以及 7)，
最安静(有较低安静值 quiet[x])的人是 person 7。

其他的答案也可以用类似的推理来解释。
提示：

1 <= quiet.length = N <= 500
0 <= quiet[i] < N，所有 quiet[i] 都不相同。
0 <= richer.length <= N * (N-1) / 2
0 <= richer[i][j] < N
richer[i][0] != richer[i][1]
richer[i] 都是不同的。
对 richer 的观察在逻辑上是一致的。

```

### 代码实现

```C++
class Solution {
public:

    vector<int> loudAndRich(vector<vector<int>>& richer, vector<int>& quiet) {
        int n=quiet.size();
        vector<vector<int>> g(n);

        // 创建有向图
        for(auto& v: richer){
            g[v[1]].push_back(v[0]);
        }

        vector<int>mem(n,INT_MAX);  // 用来记录路径是否访问过以及结果
        // dfs
        for(int cur=0;cur<n;cur++){
            helper(mem,cur,g,quiet);
        } 

        return mem;
    }

    // dfs
    int helper(vector<int>& mem,int cur,vector<vector<int>>& richer,vector<int>& quiet){
        if(mem[cur]!=INT_MAX){  // 递归终止条件：如果此条件成立，说明该路径访问过，直接放回结果
            return mem[cur];
        }

        int res=cur;
        // 往下访问邻接点
        for(auto p: richer[cur]){
            int child_p=helper(mem,p,richer,quiet);
            // 哪个安静程度小，替换为哪一个
            if(quiet[child_p]<quiet[res]){
                res=child_p;
            }
        }
        // 更新记录访问过的邻接点路径，并更新结果
        return mem[cur]=res;
    }
};
```

---

## 收集树上所有苹果的最少时间

*原题链接：https://leetcode-cn.com/problems/minimum-time-to-collect-all-apples-in-a-tree/*

```
给你一棵有 n 个节点的无向树，节点编号为 0 到 n-1 ，它们中有一些节点有苹果。通过树上的一条边，需要花费 1 秒钟。你从 节点 0 出发，请你返回最少需要多少秒，可以收集到所有苹果，并回到节点 0 。

无向树的边由 edges 给出，其中 edges[i] = [fromi, toi] ，表示有一条边连接 from 和 toi 。除此以外，还有一个布尔数组 hasApple ，其中 hasApple[i] = true 代表节点 i 有一个苹果，否则，节点 i 没有苹果。

 

示例 1：



输入：n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], hasApple = [false,false,true,false,true,true,false]
输出：8 
解释：上图展示了给定的树，其中红色节点表示有苹果。一个能收集到所有苹果的最优方案由绿色箭头表示。
示例 2：



输入：n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], hasApple = [false,false,true,false,false,true,false]
输出：6
解释：上图展示了给定的树，其中红色节点表示有苹果。一个能收集到所有苹果的最优方案由绿色箭头表示。
示例 3：

输入：n = 7, edges = [[0,1],[0,2],[1,4],[1,5],[2,3],[2,6]], hasApple = [false,false,false,false,false,false,false]
输出：0
 

提示：

1 <= n <= 10^5
edges.length == n-1
edges[i].length == 2
0 <= fromi, toi <= n-1
fromi < toi
hasApple.length == n

```

### 代码实现

```C++
class Solution {
public:
    int minTime(int n, vector<vector<int>>& edges, vector<bool>& hasApple) {
        vector<vector<int>> tree(n, vector<int>()); // 构建树图
        vector<bool> visited(n, false); // 记录该路径是否访问过

        // 构建树图：无向图
        for (auto& edge: edges) {
            tree[edge[0]].push_back(edge[1]);
            tree[edge[1]].push_back(edge[0]);
        }
        
        // dfs
        int ret = dfs(0, tree, hasApple, visited);
        // 判断递归之后结果是否小于0（在递归中对于没有苹果的子树返回-1）
        return ret < 0 ? 0 : ret;
    }

    int dfs(int root, vector<vector<int>>& tree, vector<bool>& hasApple, vector<bool>& visited) {
        visited[root] = true;   // 首先将根节点处标记为真，表示访问过

        bool childrenHasApple = false;
        int ret = 0;
        
        // 访问以该节点为父节点的子节点有没有苹果
        for (auto& child : tree[root]) {
            // 访问过的路径则跳过
            if (visited[child]) {
                continue;
            }

            // 递归遍历以该节点为父节点的子节点路径
            int num = dfs(child, tree, hasApple, visited);
            // 说明子节点有苹果，记录结果（来回路径：+2）
            if (num >= 0) {
                childrenHasApple = true;
                ret += num + 2;
            }
        }

        // 如果孩子节点有苹果，则返回结果的路径数
        // 否则，判断根节点是否有苹果，有则返回0表示路径收集结果为0，无则返回-1表示从这个节点开始往下没有苹果，也就没有路径
        return childrenHasApple ? ret : (hasApple[root] ? 0 : -1);
    }
};
```

---

