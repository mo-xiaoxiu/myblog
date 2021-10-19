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

## 路径总和

*原题链接：https://leetcode-cn.com/problems/path-sum/*

```
给你二叉树的根节点 root 和一个表示目标和的整数 targetSum ，判断该树中是否存在 根节点到叶子节点 的路径，这条路径上所有节点值相加等于目标和 targetSum 。

叶子节点 是指没有子节点的节点。

 

示例 1：


输入：root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22
输出：true
示例 2：


输入：root = [1,2,3], targetSum = 5
输出：false
示例 3：

输入：root = [1,2], targetSum = 0
输出：false
 

提示：

树中节点的数目在范围 [0, 5000] 内
-1000 <= Node.val <= 1000
-1000 <= targetSum <= 1000

```

### 回溯算法

#### 递归三部曲

##### 递归函数

- 递归函数返回值：函数要求返回是否满足条件的真或假（bool）
- 递归函数参数：根节点，目标值在递归函数中递减为0来判断是否满足条件

##### 递归终止条件

- 遍历到叶子节点且已经满足目标值，返回真
- 遍历到叶子节点但是不满足条件，返回假

##### 单层遍历逻辑

- 遍历到最底层只有左节点，右节点为空，判断是否满足条件，回溯
- 遍历到最底层只有右节点，左节点为空，判断是否满足条件，回溯

*代码实现：*

```C++
class Solution{
    public:
    	bool traversal(TreeNode* node,int sum){
            // 递归终止条件
            if(!node->left && !node->right && sum==0) return true;
            if(!node->left && !node->right) return false;
            
            // 单层递归逻辑：包含回溯的过程
            if(node->left){
                traversal(node->left,sum-node->left->val);
            }
            if(node->right){
                traversal(node->right,sum-node->right->val);
            }
            
            return false;
        }
    
    	bool hasPathSum(TreeNode* node,int targetSum){
            if(node==nullptr) return false;
            int sum=targetSum;
            // 递归函数参数和返回值
            return traversal(node,sum-node->val);
        }
};
```

*精简代码实现：*

```C++
class Solution{
    public:
    	bool hasPathSum(TreeNode* root,int targetSum){
            if(root==nullptr) return false;
            if(!root->left && !root->right && targetSum==root->val) return true;
            
            return hasPathSum(root->left,targetSum-root->val) && hasPathSum(root->right,targetSum-root->val);
        }
};
```

---

### 迭代法

#### 栈 + 键值对

- 键值对：第一个值是树节点；第二个值是路径总和
- 栈：先压根节点，再压左节点，再压右节点。压节点前先判断栈顶元素是否满足条件

```C++
class Solution{
    public:
    	bool hasPathSum(TreeNode* root,int targetSum){
            if(root==nullptr) return false;
            // 准备一个栈存放键值对
            stack<pair<TreeNode*,int>> st;
            
            st.push(pair<TreeNode*,int>(root,root->val));
            while(!st.empty()){
                pair<TreeNode*,int>node=st.top();
                st.pop();
                // 判断节点左右孩子是否为空，且路径总和是否相等
                if(!node.first->left && !node.first->right && node.second==targetSum){
                    return true;
                }
                // 压入左节点键值对：路径总和 = 当前节点值 + 下一次遍历的左节点的值 
                if(node.first->left){
                    st.push(pair<TreeNode*,int>(node.first->left,node.first->left->val+node.second));
                }
                // 压入右节点键值对
                if(node.first->right){
                    st.push(pair<TreeNode*,int>(node.first->right,node.second+node.first->right->val));
                }
            }
            return false;
        }
};
```

---

## 路径总和II

*原题链接：https://leetcode-cn.com/problems/path-sum-ii/submissions/*

```
给你二叉树的根节点 root 和一个整数目标和 targetSum ，找出所有 从根节点到叶子节点 路径总和等于给定目标和的路径。

叶子节点 是指没有子节点的节点。

 

示例 1：


输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
输出：[[5,4,11,2],[5,8,4,5]]
示例 2：


输入：root = [1,2,3], targetSum = 5
输出：[]
示例 3：

输入：root = [1,2], targetSum = 0
输出：[]
 

提示：

树中节点总数在范围 [0, 5000] 内
-1000 <= Node.val <= 1000
-1000 <= targetSum <= 1000

```

### 递归法

*代码实现：*

```C++
class Solution {
public:
    vector<vector<int>>res; // 结果数组
    vector<int>path;        // 存放路径的数组

    // 递归函数
    // 返回值：遍历哦整棵树收取所有结果，所以不需要返回值（遍历部分路径返回真假需要返回值）
    // 参数：根节点、路径总和（函数中递减比较）
    void traversal(TreeNode* root,int sum){
        // 递归终止条件
        if(!root->left && !root->right && sum==0){
            res.push_back(path);
            return;
        }

        if(!root->left && !root->right) return;

        // 单层递归逻辑
        // 递归左子树
        if(root->left){
            path.push_back(root->left->val);
            sum-=root->left->val;
            traversal(root->left,sum);
            sum+=root->left->val;   // 回溯
            path.pop_back();
        }
        // 递归右子树
        if(root->right){
            path.push_back(root->right->val);
            sum-=root->right->val;
            traversal(root->right,sum);
            sum+=root->right->val;  // 回溯
            path.pop_back();
        }
        return;

    }

    vector<vector<int>> pathSum(TreeNode* root, int targetSum) {
        if(root==nullptr) return res;
        path.push_back(root->val);  // 先将根节点放入路径中，之后传参时递减比较
        traversal(root,targetSum-root->val);

        return res;
    }
};
```

---

## 路径总和III：进阶

*原题链接：https://leetcode-cn.com/problems/path-sum-iii/*

```
给定一个二叉树的根节点 root ，和一个整数 targetSum ，求该二叉树里节点值之和等于 targetSum 的 路径 的数目。

路径 不需要从根节点开始，也不需要在叶子节点结束，但是路径方向必须是向下的（只能从父节点到子节点）。

 

示例 1：



输入：root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
输出：3
解释：和等于 8 的路径有 3 条，如图所示。
示例 2：

输入：root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
输出：3
 

提示:

二叉树的节点个数的范围是 [0,1000]
-109 <= Node.val <= 109 
-1000 <= targetSum <= 1000 

```

### 回溯算法

**前缀和：当前节点cur为从根节点到此节点上的路径所有节点值之和**

#### 回溯三部曲

##### 递归函数参数

* 根节点
* 目标值
* 前缀和

##### 递归终止条件

当节点为空（遍历到叶子节点时），返回0

##### 单层逻辑

不断计算当前节点的前缀和，判断是否有cur-target的值存在。若存在，说明肯定有从目标值target的节点和的路径。可以使用哈希表记录当前节点前缀和的数量，然后递归当前节点的左右子树
回溯（返回到当前节点的位置），回溯时不断返回结果值，最后返回的结果值就是所有满足目标值的路径数

*代码实现：*

```C++
class Solution{
    public:
    	unordered_map<int,int> map;
    
    	int traversal(TreeNode* node,int cur,int targetSum){
            if(!root) return 0;	// 递归终止条件
            
            int res=0;	// 结果路径数
            cur+=node->val;	// 当前路径总和
            
            // 如果在哈希表中，存在当前节点的路径总和与目标值之差的哈希值，说明存在满足题目要求的路径
            if(map.count[cur->targetSum]){
                // 结果就是这个哈希值
                res=map[cur-targetSum];
            }
            
            // 递归，回溯
            map[cur]++;
            // 分别加和递归左右子树的路径数量
            res+=traversal(node->left,cur,targetSum);
            res+=traversal(node->right,cur,targetSum);
            map[cur]--;
            
            return res;
        }
    
    	int pathSum(TreeNode* root,int targetSum){
            // 初始化哈希表
            map[0]=1;
            return traversal(root,0,targetSum);
        }
};
```

---

