---
title: "二叉树知识点之二"
date: 2021-10-17T11:47:45+08:00
draft: true
---

# 二叉树之周

## 对称二叉树

*原题链接：https://leetcode-cn.com/problems/symmetric-tree/*

```
给定一个二叉树，检查它是否是镜像对称的。

 

例如，二叉树 [1,2,2,3,4,4,3] 是对称的。

    1
   / \
  2   2
 / \ / \
3  4 4  3
 

但是下面这个 [1,2,2,null,3,null,3] 则不是镜像对称的:

    1
   / \
  2   2
   \   \
   3    3
 

进阶：

你可以运用递归和迭代两种方法解决这个问题吗？

```

**递归方法：**

*代码实现：*

```C++
class Solution {
public:
    bool compare(TreeNode* left,TreeNode* right){
        if(left==nullptr && right==nullptr) return true;        // 左右节点皆为空，说明已经满足
        else if(left!=nullptr && right==nullptr) return false;  // 左右节点有一不为空，不满足，返回假
        else if(left==nullptr && right!=nullptr) return false;  
        else if(left->val!=right->val) return false;            // 左右节点不相等，返回假

        // 二叉树外侧比较
        bool outSide=compare(left->left,right->right);
        // 二叉树内测比较
        bool inSode=compare(left->right,right->left);
        // 左右子树都对称才是对称
        return outSide && inSode;
    }

    bool isSymmetric(TreeNode* root) {
        if(root==nullptr) return true;
        return compare(root->left,root->right);
    }
};
```

**迭代法：**

*代码实现：*

```C++
class Solution{
    public:
    	bool isSymetric(TreeNode* root){
            if(root==nullptr) return true;
            queue<TreeNode*> que;
            que.push(root->left);
            que.push(root->right);
            while(!que.empty()){
                TreeNode* rightNode=que.front();
                que.pop();
                TreeNode* leftNode=que.front();
                que.pop();
                
                if(!leftNode && !rightNode) continue;
                if(!leftNode || !rightNode || leftNode->val!=rightNode->val) return false;
                
                que.push(rightNode->right);
                que.push(leftNode->left);
                que.push(rightNode->left);
                que.push(leftNode->right);
            }
            return true;
        }
};
```

---

## 二叉树的最大深度

*原题链接：https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/*

```
给定一个二叉树，找出其最大深度。

二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。

说明: 叶子节点是指没有子节点的节点。

示例：
给定二叉树 [3,9,20,null,null,15,7]，

    3
   / \
  9  20
    /  \
   15   7
返回它的最大深度 3 。

```

**递归法：**

*代码实现：*

```C++
class Solution{
    public:
    	int maxDepth(TreeNode* root){
            if(root==nullptr) return 0;
            return 1+max(maxDepth(root->left),max(maxDpeth(root->right)));
        }
};
```

**迭代法：**

*代码实现：（类层序遍历）*

```C++
class Solution{
    public:
    	int maxDepth(TreeNode* root){
            if(root==nullptr) return 0;
            queue<TreeNode*> que;
            int depth=0;
            que.push(root);
            
            while(!que.empty()){
                depth+=1;
                int n=que.size();
                for(int i=0;i<n;i++){
                    TreeNode* cur=que.front();
                    que.pop();
                    
                    if(cur->left) que.push(cur->left);
                    if(cur->left) que.push(cur->right);
                }
            }
            return depth;
        }
};
```

---

## 二叉树的最小深度

*原题链接：https://leetcode-cn.com/problems/minimum-depth-of-binary-tree/*

```
给定一个二叉树，找出其最小深度。

最小深度是从根节点到最近叶子节点的最短路径上的节点数量。

说明：叶子节点是指没有子节点的节点。

 

示例 1：


输入：root = [3,9,20,null,null,15,7]
输出：2
示例 2：

输入：root = [2,null,3,null,4,null,5,null,6]
输出：5
 

提示：

树中节点数的范围在 [0, 105] 内
-1000 <= Node.val <= 1000

```

**递归法：**

*代码实现：*

```C++
class Solution{
    public:
    	int minDepth(TreeNode* root){
            if(root==nullptr) return 0;
            
            int depth=0;
            if(root->left==nullptr && root->right){
                return 1+minDepth(root->right);
            }
            if(root->left && root->right==nullptr){
                return 1+minDepth(root->left);
            }
            
            return 1+min(minDepth(root->left),minDepth(root->right));
        }
};
```

**迭代法：**

*代码实现：*

```C++
class Solution{
    public:
    	int minDepth(TreeNode* root){
            queue<TreeNode*> que;
            if(root==nullptr) return 0;
            que.push(root);
            int depth=0;
            
            while(!que.empty()){
            	depth+=1;
                int n=que.size();
                for(int i=0;i<n;i++){
                    TreeNode* cur=que.front();
                    que.pop();
                    
                    if(cur->left) que.push(cur->left);
                    if(cur->right) que.push(cur->right);
                    
                    if(!cur->left && !cur->right) break;
                }
            }
            return depth;
        }
};
```

---

## 完全二叉树的节点个数

*原题链接：https://leetcode-cn.com/problems/count-complete-tree-nodes/*

```
给你一棵 完全二叉树 的根节点 root ，求出该树的节点个数。

完全二叉树 的定义如下：在完全二叉树中，除了最底层节点可能没填满外，其余每层节点数都达到最大值，并且最下面一层的节点都集中在该层最左边的若干位置。若最底层为第 h 层，则该层包含 1~ 2h 个节点。

 

示例 1：


输入：root = [1,2,3,4,5,6]
输出：6
示例 2：

输入：root = []
输出：0
示例 3：

输入：root = [1]
输出：1
 

提示：

树中节点的数目范围是[0, 5 * 104]
0 <= Node.val <= 5 * 104
题目数据保证输入的树是 完全二叉树
 

进阶：遍历树来统计节点是一种时间复杂度为 O(n) 的简单解决方案。你可以设计一个更快的算法吗？

```

### 普通树做法

**递归法：**

*代码实现：*

```C++
class Solution{
    public:
    	int countNode(TreeNode* root){
            if(root==nullptr) return 0;
            return 1+countNode(root->left)+countNode(root->right);
        }
};
```

**迭代法：**

*代码实现：*

```C++
class Solution{
    public:
    	int countNode(TreeNode* root){
            if(root==nullptr) return 0;
            queue<TreeNode*> que;
            que.push(root);
            
            int count=0;
            while(!que.empty()){
                int n=que.size();
                for(int i=0;i<n;i++){
                    TreeNode* cur=que.front();
                    que.pop();
                    count++;
                    
                    if(root->left) que.push(cur->left);
                    if(root->right) que.push(cur->right);
                }
            }
            return count;
        }
};
```

### 完全二叉树做法

*代码实现：*

```C++
class Solution{
    public:
    	int countNode(TreeNode* root){
            if(root==nullptr) return 0;
            int leftH=0,rightH=0;
            
            TreeNode* leftNode=root->left;
            TreeNode* rightNode=root->right;
            while(leftNode){
                leftNode=leftNode->next;
                leftH++;
            }
            while(rightNode){
                rightNode=rightNode->next;
                rightH++;
            }
            
            if(leftH==rightH){
                return (2<<leftH)-1;
            }
            return 1+countNode(root->left)+countNode(root->right);
        }
};
```

---

## 平衡二叉树

*原题链接：https://leetcode-cn.com/problems/balanced-binary-tree/*

```
给定一个二叉树，判断它是否是高度平衡的二叉树。

本题中，一棵高度平衡二叉树定义为：

一个二叉树每个节点 的左右两个子树的高度差的绝对值不超过 1 。

 

示例 1：


输入：root = [3,9,20,null,null,15,7]
输出：true
示例 2：


输入：root = [1,2,2,3,3,null,null,4,4]
输出：false
示例 3：

输入：root = []
输出：true
 

提示：

树中的节点数在范围 [0, 5000] 内
-104 <= Node.val <= 104

```

**递归法：**

*代码实现：*

```C++
class Solution{
    public:
    	int getDepth(TreeNode* root){
            if(root==nullptr) return 0;
            int leftH=getDepth(root->left);
            if(leftH==-1) return -1;
            int rightH=getDepth(root->right);
            if(rightH==-1) return -1;
            
            return abs(leftH-rightH)>1?-1:1+max(leftH,rightH);
        }
    
    	bool isBalanced(TreeNode* root){
            return getDepth(root)==-1:false:true;
        }
};
```

---

## 二叉树的所有路径

*原题链接：https://leetcode-cn.com/problems/binary-tree-paths/*

```
给你一个二叉树的根节点 root ，按 任意顺序 ，返回所有从根节点到叶子节点的路径。

叶子节点 是指没有子节点的节点。

 
示例 1：


输入：root = [1,2,3,null,5]
输出：["1->2->5","1->3"]
示例 2：

输入：root = [1]
输出：["1"]
 

提示：

树中节点的数目在范围 [1, 100] 内
-100 <= Node.val <= 100

```

**递归 + 回溯：**

*代码实现：*

```C++
class Solution{
    public:
    	void backTracking(TreeNode* root,vector<int>& path,vector<string>& res){
            path.push_back(root->val);
            
            // 递归终止条件：节点左右孩子不存在（叶子节点）
            if(root->left==nullptr && root->right==nullptr){
                string str;
                // 格式化存放入临时字符串
                for(int i=0;i<que.size()-1;i++){
                    str+=to_string(path[i];
                    str+="->";
                }
                str+=to_string(path[paht.size()-1]);
                re.push_back(str);
            }
            
            if(root->left){
                backTracking(root->left,path,res);	// 递归
                path.pop();	// 回溯
            }
            if(root->right){
                backTracking(root->right,path,res);
                path.pop();
            }                       
        }
    
    	vector<string> binaryTreePaths(TreeNode* root){
            vector<int> vec;		// 用于存放路径上的节点值
            vector<string> res;
            
            backTracking(root,vec,res);
            return res;
        }
};
```

---

