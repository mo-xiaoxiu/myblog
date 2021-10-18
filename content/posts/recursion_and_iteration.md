---
title: "递归和迭代"
date: 2021-10-18T11:28:51+08:00
draft: true
---

# 递归和迭代

递归和迭代法都可以做的题目。一般用在二叉树的题目上

## 找树左下角的值

*原题链接：https://leetcode-cn.com/problems/find-bottom-left-tree-value/*

```
给定一个二叉树的 根节点 root，请找出该二叉树的 最底层 最左边 节点的值。

假设二叉树中至少有一个节点。

 

示例 1:



输入: root = [2,1,3]
输出: 1
示例 2:



输入: [1,2,3,4,null,5,6,null,null,7]
输出: 7
 

提示:

二叉树的节点个数的范围是 [1,104]
-231 <= Node.val <= 231 - 1 

```

**递归法：**

```C++
class Solution{
    public:
    	int maxLen=INT_MAX;
    	int maxLeftVal;
    
    	void traversal(TreeNode* root,int leftLen){
            // 递归终止条件：找到满足条件的值（最左边节点值），会覆盖全局变量，
            // 又由于是中序遍历，先处理中间节点，然后处理左子树节点，所以优先考虑的是左节点，不用担心右节点值覆盖问题
            if(root->left==nullptr && root->right==nullptr){
                if(leftLen>maxLen){
                    maxLen=leftLen;
                    maxLeftVal=root->val;
                }
                return;
            }
            
            if(root->left){
                leftLen++;
                traversal(root->left,leftLen);	// 递归
                leftLen--;	// 回溯
            }
            if(root->right){
                leftLen++;
                traversal(root->right,leftLen);	// 递归
                leftLen--;	// 回溯
            }
            return;
        }
    
    	int findBottomLeftValue{TreeNode* root}{
            traversal(root,0);
            return maxLeftVal;
        }
};
```

* 这里不用担心遍历到的是最后一行最右节点之后被替换值，因为这里采用的是中序遍历：
* 先判断该节点左右孩子是否都为空。以此来判断是否遍历到叶子节点了，然后比较、替换最后一行行数和返回值（最左叶子节点值）；
* 之后先递归遍历左子树，所以此时如果该左子树存在满足条件的节点值，则最后一行的行号和最左节点值会被覆盖；
* 而后进行对右子树进行递归遍历时，则如果没有满足条件的结果，不会覆盖之前全局变量的值！

**迭代法·：**

*类似层序遍历*

```C++
class Solution{
    public:
    	findBotomLeftVal(TreeNode* root){
            queue<TreeNode*> que;
            if(root!=nullptr) que.push(root);
            
            int res=0;
            while(!que.empty()){
                int n=que.size();
                for(int i=0;i<n;i++){
                    TreeNode* cur=que.front();
                    que.pop();
                    
                    // 最后一层的第一个节点，就是题目要求最左边节点值
                    // 关键词：最后一层，第一个节点（最左边节点值）
                    if(i==0) res=cur->val;
                    
                    if(cur->left) que.push(cur->left);
                    if(cur->right) que.push(cur->right);
                }
            }
            return res;
        }
};
```



---

## 相同的树

*原题链接：https://leetcode-cn.com/problems/same-tree/submissions/*

```
给你两棵二叉树的根节点 p 和 q ，编写一个函数来检验这两棵树是否相同。

如果两个树在结构上相同，并且节点具有相同的值，则认为它们是相同的。

 

示例 1：


输入：p = [1,2,3], q = [1,2,3]
输出：true
示例 2：


输入：p = [1,2], q = [1,null,2]
输出：false
示例 3：


输入：p = [1,2,1], q = [1,1,2]
输出：false
 

提示：

两棵树上的节点数目都在范围 [0, 100] 内
-104 <= Node.val <= 104

```

**递归法：**

```C++
class Solution{
    public:
    	bool isSameTree(TreeNode* q,TreeNode* p){
            if(q==nullptr && p!=nullptr) return false;
            else if(q!=nullptr && p==nullptr) return false;
            else if(q==nullptr && p==nullptr) return true;
            else if(q->val!=p->val) return false;
            
            return isSameTree(q->left,p->left) && isSameTree(q->right,p->right);
        }
};
```

**迭代法：**

```C++
class Solution{
	public:
    	bool isSameTree(TreeNode* p,TreeNode* q){
            if(p==nullptr && q==nullptr) return true;
            if(p==nullptr || q==nullptr) return false;
            queue<TreeNode*> que;
            que.push(p);
            que.push(q);
            
            while(!que.empty()){
                TreeNode* leftNode=que.front();
                que.pop();
                TreeNode* rightNode=que.front();
                que.pop();
                
                if(leftNode==nullptr && rightNode==nullptr) continue;
                if(!leftNode || !rightNode || leftNode->val!=rightNode->val) return false;
                
                que.push(leftNode->left);
                que.push(rightNode->left);
                que.push(leftNode->right);
                que.push(rightNode->right);
            }
            return true;
        }
};
```

---

这个题和下面这个很像

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

**递归法：**

```C++
class Solution{
    public:
    	bool function(TreeNode* root){
            if(root->left!=nullptr && root->right==nullptr) return false;
            if(root->left==nullptr && root->right!=nullptr) return false;
            if(root->left==nullptr && root->right==nullptr) return true;
            if(root->left->val!=root->right->val) return false;
            
            return function(root->left) && function(root->right);
        }
};
```

**迭代法：**

```C++
class Solution{
    public:
    	bool function(TreeNode* root){
            if(root->left==nullptr && root->right==nullptr) return true;
            if(root->left==nullptr || root->right==nullptr) return false;
            
            queue<TreeNode*> que;
            que.push(root->left);
            que.push(root->right);
            
            while(!que.empty()){
                TreeNode* leftNode=que.front();
                que.pop();
                TreeNode* rightNoe=que.front();
                que.pop();
                
                if(leftNode==nullptr && rightNode==nullptr) continue;
                if(!leftNode || !rightNode || leftNode->val!=rightNode->val) return false;
                
                que.push(leftNode->left);
                que.push(rightNode->right);
                que.push(leftNode->right);
                que.push(rightNode->left);
            }
            return true;
        }
};
```

---

## 左叶子之和

*原题链接：https://leetcode-cn.com/problems/sum-of-left-leaves/submissions/*

```
计算给定二叉树的所有左叶子之和。

示例：

    3
   / \
  9  20
    /  \
   15   7

在这个二叉树中，有两个左叶子，分别是 9 和 15，所以返回 24

```

**递归法：**

```C++
class Solution{
    public:
    	int sumOfLeftLeaves(TreeNode* root){
            // 递归终止条件
            if(root==nullptr) return 0;
            
            int sumofLeft=sumOfLeftLeaves(root->left);	// 左
            int sumOfRight=sumOfLeftLeaves(root->right);	// 右
            
            int res=0;
            if(root->left && root->left->left==nullptr && root->left->right==nullptr)	// 中
                res+=sumOfLeft+sumOfRight;
            
            return res;
        }
};
```

**迭代法：**

```C++
class Solution{
    public:
    	int sumOfLeftLeaves(TreeNode* root){
            if(root==nullptr) return 0;
            queue<TreeNode*> que;
            que.push(root);
            
            int res=0;
            while(!que.empty()){
                int n=que.size();
                for(int i=0;i<n;i++){
                    TreeNode* cur=que.front();
                    que.pop();
                    
                    // 判断该节点的左节点是否存在，且该左节点左右孩子是否为空，如果为空，则说明该左节点就是最左节点
                    // 查找的依据是最左节点的父节点
                    if(cur->left && cur->left->left==nullptr && cur->left->right==nullptr)
                        res+=cur->left->val;
                }
            }
            return res;
        }
};
```

***拓展思路：查找节点的方法可以间接地通过查找该节点的父节点，在这个题中，单纯查找满足条件的该节点来说，除了判断该节点的左右节点是否为空之外，没有什么好的办法；所以可以通过该节点的父节点来添加条件***

***在这个题当中，加上条件：满足条件的节点是其父节点的左节点，就能和条件：该节点的左右孩子都为空 合并满足题目要求***

---

