---
title: "栈和队列"
date: 2021-10-09T20:14:35+08:00
draft: true
---

# 栈和队列

## 用栈实现队列

*原题链接：https://leetcode-cn.com/problems/implement-stack-using-queues/submissions/*

```
请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通栈的全部四种操作（push、top、pop 和 empty）。

实现 MyStack 类：

void push(int x) 将元素 x 压入栈顶。
int pop() 移除并返回栈顶元素。
int top() 返回栈顶元素。
boolean empty() 如果栈是空的，返回 true ；否则，返回 false 。
 

注意：

你只能使用队列的基本操作 —— 也就是 push to back、peek/pop from front、size 和 is empty 这些操作。
你所使用的语言也许不支持队列。 你可以使用 list （列表）或者 deque（双端队列）来模拟一个队列 , 只要是标准的队列操作即可。
 

示例：

输入：
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 2, 2, false]

解释：
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top(); // 返回 2
myStack.pop(); // 返回 2
myStack.empty(); // 返回 False
 

提示：

1 <= x <= 9
最多调用100 次 push、pop、top 和 empty
每次调用 pop 和 top 都保证栈不为空
 

进阶：你能否实现每种操作的均摊时间复杂度为 O(1) 的栈？换句话说，执行 n 个操作的总时间复杂度 O(n) ，尽管其中某个操作可能需要比其他操作更长的时间。你可以使用两个以上的队列。

```

*代码实现：*

```C++
class MyQueue{
    public:
    	stack<int>stIn;
    	stack<int>stOut;
    
    	MyQueu(){}
    
    	void push(int x){
            stIn.push(x);
        }
    
    	int pop(){
            if(stOut.empty()){
                while(!stIn.empty()){
                    int tmp=stIn.top();
                    stIn.pop();
                    stOut.push(tmp);
                }
            }
                            
            int cur=stOut.top();
            stOut.pop();
            return cur;
        }
    
    	int peek(){
            int cur=this->pop();
            stOut.push(cur);
            return cur;
        }
    
    	bool rmpty(){
            return stIn.empty() && stOut.empty();
        }
};
```

* 一个输入栈stIn，一个输出栈stOut
* `stIn`：模拟入队
* `stOut`：模拟出队
* 由于栈是先进后出的数据结构，所以输入栈的值先输入的是在出队时先出去的值，所以输出栈就是用来接收输入栈弹出的元素，相当于逆序存放输入栈的元素，利用两个栈的先进后出特性，完成队列的先进先出特性

---

## 用队列实现栈

*原题链接：https://leetcode-cn.com/problems/implement-stack-using-queues/*

```
请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通栈的全部四种操作（push、top、pop 和 empty）。

实现 MyStack 类：

void push(int x) 将元素 x 压入栈顶。
int pop() 移除并返回栈顶元素。
int top() 返回栈顶元素。
boolean empty() 如果栈是空的，返回 true ；否则，返回 false 。
 

注意：

你只能使用队列的基本操作 —— 也就是 push to back、peek/pop from front、size 和 is empty 这些操作。
你所使用的语言也许不支持队列。 你可以使用 list （列表）或者 deque（双端队列）来模拟一个队列 , 只要是标准的队列操作即可。
 

示例：

输入：
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 2, 2, false]

解释：
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top(); // 返回 2
myStack.pop(); // 返回 2
myStack.empty(); // 返回 False
 

提示：

1 <= x <= 9
最多调用100 次 push、pop、top 和 empty
每次调用 pop 和 top 都保证栈不为空
 

进阶：你能否实现每种操作的均摊时间复杂度为 O(1) 的栈？换句话说，执行 n 个操作的总时间复杂度 O(n) ，尽管其中某个操作可能需要比其他操作更长的时间。你可以使用两个以上的队列。

```

*代码实现：*

```C++
class MyStack{
    public:
    	queue<int>que_1;
    	queue<int>que_2;
    
    	MyStack(){}
    
    	void push(int x){
            que_1.push(x);
        }
    
    	int pop(){
            int n=que_1.size();
            n--;
            while(n--{
                int tmp=que_1.front();
                que_1.pop();
                que_2.push(tmp);
            }
            
            int cur=que_1.front();
            que_1.pop();
                 
            que_1=que_2;      
            while(!que_2.empty()){
                que_2.pop();
            }
                  
            return cur;
        }
                  
        int top(){
            return que_1.back();
        }
                  
        bool empty(){
            return que_1.empty();
        }
};
```

* 一个普通队列`que_1`，一个备份队列`que_2`;
* 输入：元素从正常队列入队；
* 输出：将普通队列的元素逐个拷贝到备份队列中，除了队列中的最后一个元素（为了满足栈的特性），输出使用

---

## 有效括号

*原题链接：https://leetcode-cn.com/problems/valid-parentheses/*

```
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。

有效字符串需满足：

左括号必须用相同类型的右括号闭合。
左括号必须以正确的顺序闭合。
 

示例 1：

输入：s = "()"
输出：true
示例 2：

输入：s = "()[]{}"
输出：true
示例 3：

输入：s = "(]"
输出：false
示例 4：

输入：s = "([)]"
输出：false
示例 5：

输入：s = "{[]}"
输出：true
 

提示：

1 <= s.length <= 104
s 仅由括号 '()[]{}' 组成

```

*代码实现：*

```C++
class Solution{
    public:
    	bool isVaild(string s){
            stack<int>st;
            for(int i=0;i<s.size();i++){
                if(s[i]=='(') st.push(')');
                else if(s[i]=='{') st.push('}');
                else if(s[i]=='[') st.push(']');
                else if(st.empty() || s.top()!=s[i]) return false;
                else st.pop();
            }
            
            return st.empty();
        }
};
```

* 用一个栈来接收遍历到的括号
* 如果遍历到 '('、'[' 或者 '{'，则将')'、']' 或者'}' 压入栈中，表示匹配的括号
* 如果遍历到的是 ']'、'}'或者')'，则将其与栈顶元素对比，如果能匹配，则栈顶元素弹出；不匹配则说明此为无效括号
* 最后遍历完判断栈是否为空：空则说明为有效括号

---

## 删除字符串中的所有相邻重复项

*原题链接：https://leetcode-cn.com/problems/remove-all-adjacent-duplicates-in-string/*

```
给出由小写字母组成的字符串 S，重复项删除操作会选择两个相邻且相同的字母，并删除它们。

在 S 上反复执行重复项删除操作，直到无法继续删除。

在完成所有重复项删除操作后返回最终的字符串。答案保证唯一。

 

示例：

输入："abbaca"
输出："ca"
解释：
例如，在 "abbaca" 中，我们可以删除 "bb" 由于两字母相邻且相同，这是此时唯一可以执行删除操作的重复项。之后我们得到字符串 "aaca"，其中又只有 "aa" 可以执行重复项删除操作，所以最后的字符串为 "ca"。
 

提示：

1 <= S.length <= 20000
S 仅由小写英文字母组成

```

*代码实现：（额外申请的栈）*

```C++
class Solution{
    public:
    	string removeDuplicate(string s){
            stack<char>st;
            for(int i=0;i<s.size();i++){
                if(!st.empty() && st.top()==s[i]){
                    st.pop();
                    continue;
                }
                st.push(s[i]);
            }
            
            string res;
            while(!st.empty()){
                res+=st.top();
                st.pop();
            }
            reverse(res.begin(),res.end());
            
            return res;
        }
};
```

*代码实现：（利用字符串本身，减少时间、空间复杂度）*

```C++
class Solution{
    public:
    	string removeDuplicate(string s){
            string res;
            for(int i=0;i<s.size();i++){
                if(!res.empty() && res.back()==s[i]){
                    res.pop_back();
                    continue;
                }
                res.push_back(s[i]);
            }
            return res;
        }
};
```

---

## 逆波兰表达式

*原题链接：https://leetcode-cn.com/problems/evaluate-reverse-polish-notation/submissions/*

```
根据 逆波兰表示法，求表达式的值。

有效的算符包括 +、-、*、/ 。每个运算对象可以是整数，也可以是另一个逆波兰表达式。

 

说明：

整数除法只保留整数部分。
给定逆波兰表达式总是有效的。换句话说，表达式总会得出有效数值且不存在除数为 0 的情况。
 

示例 1：

输入：tokens = ["2","1","+","3","*"]
输出：9
解释：该算式转化为常见的中缀算术表达式为：((2 + 1) * 3) = 9
示例 2：

输入：tokens = ["4","13","5","/","+"]
输出：6
解释：该算式转化为常见的中缀算术表达式为：(4 + (13 / 5)) = 6
示例 3：

输入：tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
输出：22
解释：
该算式转化为常见的中缀算术表达式为：
  ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22
 

提示：

1 <= tokens.length <= 104
tokens[i] 要么是一个算符（"+"、"-"、"*" 或 "/"），要么是一个在范围 [-200, 200] 内的整数
 

逆波兰表达式：

逆波兰表达式是一种后缀表达式，所谓后缀就是指算符写在后面。

平常使用的算式则是一种中缀表达式，如 ( 1 + 2 ) * ( 3 + 4 ) 。
该算式的逆波兰表达式写法为 ( ( 1 2 + ) ( 3 4 + ) * ) 。
逆波兰表达式主要有以下两个优点：

去掉括号后表达式无歧义，上式即便写成 1 2 + 3 4 + * 也可以依据次序计算出正确结果。
适合用栈操作运算：遇到数字则入栈；遇到算符则取出栈顶两个数字进行计算，并将结果压入栈中。

```

*代码实现（利用栈来实现）：*

```C++
class Solution{
    public:
    	int evalRPN(string& tokens){
            stack<int>st;
            int n=tokens.size();
            for(int i=0;i<n;i++){
                string& token=token[i];
                if(isNumber(token)){
                    st.push(atoi(token.c_str()));
                }else{
                    int num_1=st.top();
                    st.pop();
                    int num_2=st.top();
                    st.pop();
                    switch(token[i]){
                    	case '*':
                    		st.push(num_1*num_2);break;
                    	case '+':
                    		st.push(num_1+num_2);break;
                    	case '-':
                    		st.push(num_1-num_2);break;
                    	case '/':
                    		st.push(num_1/num_2);break;
                    }
                }
            }
            return st.top();	// 最后栈中的值就是整条式子计算完毕后的结果
        }
};
```

---

## 滑动窗口最大值

*原题链接：https://leetcode-cn.com/problems/sliding-window-maximum/*

```
给你一个整数数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。

返回滑动窗口中的最大值。

 

示例 1：

输入：nums = [1,3,-1,-3,5,3,6,7], k = 3
输出：[3,3,5,5,6,7]
解释：
滑动窗口的位置                最大值
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
示例 2：

输入：nums = [1], k = 1
输出：[1]
示例 3：

输入：nums = [1,-1], k = 1
输出：[1,-1]
示例 4：

输入：nums = [9,11], k = 2
输出：[11]
示例 5：

输入：nums = [4,-2], k = 2
输出：[4]
 

提示：

1 <= nums.length <= 105
-104 <= nums[i] <= 104
1 <= k <= nums.length

```

**双端队列：**

* 创建一个双端队列，队列中的元素维护的是逆序的（从大到小的）排列的、数组中的元素下标
* 保持队列的队首维护的是此时滑动窗口中的最大值下标
* 当滑动窗口长度超过k时，缩小窗口
	具体的，当前遍历位置和k的差值，表示初始化窗口之后遍历的长度，`dq.front()`表示的是此队列中的最大值下标，表示滑动窗口数组元素的位置，如果`i-k`超过了最大值的位置，说明超过了滑动窗口的长度，这个可以由几何关系得知

*代码实现：*

```C++
class Solution{
    public:
    	vector<int> maxSlidingWindow(vector<int>& nums,int k){
            if(k==0) return{};
            
            deque<int>dq;
            vector<int> res;
            for(int i=0;i<k;i++){
                if(!dq.empty() && nums[i]>nums[dq.front()]){
                    dq.pop_back();
                }
                dq.push_back(i);
            }
            
            res.push_back(nums[dq.front()]);
            
            for(int i=k;i<nums.size();i++){
                // 注意这里的判断滑动窗口是否超过长度的条件：可以依据几何条件来判断
                if(!dq.empty() && dq.front()<=i-k){
                    dq.pop_front();
                }
                
                while(!dq.empty() && nums[i]>nums[dq.front()]){
                    dq.pop_back();
                }
                dq.push_back(i);
                
                res.push_back(nums[dq.front()]);
            }
            
            return res;
        }
};
```

---

## 优先队列：前k个高频元素

*原题链接：https://leetcode-cn.com/problems/top-k-frequent-elements/*

```
给你一个整数数组 nums 和一个整数 k ，请你返回其中出现频率前 k 高的元素。你可以按 任意顺序 返回答案。

 

示例 1:

输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]
示例 2:

输入: nums = [1], k = 1
输出: [1]
 

提示：

1 <= nums.length <= 105
k 的取值范围是 [1, 数组中不相同的元素的个数]
题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的
 

进阶：你所设计算法的时间复杂度 必须 优于 O(n log n) ，其中 n 是数组大小。

```

**优先队列：**

* 哈希表：记录数组中元素及其出现次数，方便统计频率
* 优先队列：定义比较算法为从小到大（优先队列默认是大根堆），输出数组时弹出的键值对就是按照元素出现次数从大到小的

*代码实现：*

```C++
class Solution{
    public:
    	// 自定义比较函数
    	class Compair{
            public:
            	bool operator()(const pair<int,int>& lhs,const pair<int,int>& rhs ){
                    return lhs.second>rhs.second;
                }
        }.
    
    	vector<int> topKfrequent(vector<int>& nums,int k){
            unordeder_map<int,int>map;		// 记录数组中元素及其出现的次数
            for(int i=0;i<nums.size();i++){
                map[num[i]]++;
            }
            
            // 优先队列：自定义比较函数（默认优先队列为大根堆）
            priority_queue<pair<int,int>,vector<pair<int,int>>,myCompair> pr_que;
            
            for(auto it=map.begin();it!=map.end();it++){
                pr_que.push(*it);
                if(pr_que.size()>k){
                    pr_que.pop();
                }
            }
            
            // 结果数组：反向输出
            vector<int> res(k);
            for(int i=k-1;i>=0;i--){
                res[i]=pr_que.top().first;
                pr_que.pop();
            }
            
            return res;
        }
};
```

---

## 栈 + 键值对

*原题链接：https://leetcode-cn.com/problems/path-sum/submissions/*

```
给你二叉树的根节点 root 和一个表示目标和的整数 targetSum ，判断该树中是否存在 根节点到叶子节点 的路径，这条路径上所有节点值相加等于目标和 targetSum 。

叶子节点 是指没有子节点的节点。

```

* 键值对：第一个值是树节点；第二个值是路径总和
* 栈：先压根节点，再压左节点，再压右节点。压节点前先判断栈顶元素是否满足条件

```C++
class Solution {
public:
    bool hasPathSum(TreeNode* root, int targetSum) {
        if(root==nullptr) return false; // 先判断题目给定的树节点是否为空

        // 准备一个栈：存储键值对（当前树节点，路经值总和）
        stack<pair<TreeNode*,int>>st;

        // 根节点入栈
        st.push(pair<TreeNode*,int>(root,root->val));
        while(!st.empty()){
            pair<TreeNode*,int>node=st.top();
            st.pop();

            // 判断当前节点是否到达叶子节点且满足目标值条件，是则返回真
            if(node.first->left==nullptr && node.first->right==nullptr && node.second==targetSum )
            return true;

            // 最底层：有左节点，右节点为空，左节点入栈，加上当前节点值求下一次迭代的路径总和
            if(node.first->left){
                st.push(pair<TreeNode*,int>(node.first->left,node.second+node.first->left->val));
            }
            // 最底层：有右节点，左节点为空，右节点入栈，加上当前节点的值求下一次迭代的路径总和
            if(node.first->right){
                st.push(pair<TreeNode*,int>(node.first->right,node.second+node.first->right->val));
            }
        }
        return false;
    }
};
```

---

## 栈/队列 + 二叉树

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

*代码实现（栈）：*

```C++
class Solution{
    public:
    	bool isSymmetric(TreeNode* root){
            if(root==nullptr) return nullptr;
            stack<TreeNode*> st;
            
            st.push(root->left);
            st.push(root->right);
            while(!st.empty()){
                TreeNode* rightNode=st.top();
                st.pop();
                TreeNode* leftNode=st.top();
                st.pop();
                
                if(leftNode==nullptr && rightNode==nullptr) continue;
                
                if(!leftNode || !rightNode || leftNode->val!=rightNode->val) return false;
                
                st.push(rightNode->right);
                st.push(leftNode->left);
                st.push(rightNode->left);
                st.push(leftNode->right);
            }
            
            return root;
        }
};
```

**左右节点成对放入，成对取出**
* 成对放入的节点是空节点，说明此时满足条件（对称）
* 单独只有左节点，或者单独只有右节点，或者左右节点的值不相等
* **节点压栈顺序：**二叉树外侧和内测节点成对压入

*代码实现（队列）：*

```C++
class Solution {
public:
    bool isSymmetric(TreeNode* root) {
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

## 优先队列：有序矩阵中的第k小的值

*原题链接：https://leetcode-cn.com/problems/kth-smallest-element-in-a-sorted-matrix/*

```
给你一个 n x n 矩阵 matrix ，其中每行和每列元素均按升序排序，找到矩阵中第 k 小的元素。
请注意，它是 排序后 的第 k 小元素，而不是第 k 个 不同 的元素。

 

示例 1：

输入：matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
输出：13
解释：矩阵中的元素为 [1,5,9,10,11,12,13,13,15]，第 8 小元素是 13
示例 2：

输入：matrix = [[-5]], k = 1
输出：-5
 

提示：

n == matrix.length
n == matrix[i].length
1 <= n <= 300
-109 <= matrix[i][j] <= 109
题目数据 保证 matrix 中的所有行和列都按 非递减顺序 排列
1 <= k <= n2

```

* 明确：矩阵左上角的数是最小的，右下角的数是最大的
* 每次取出矩阵中的最小值，取到第k个元素即可
* 所以想到可以使用优先队列

**问题：如何保证每次从矩阵中取出的元素都是矩阵中最小的元素？**
* 优先队列维护左边第一列的数据，这是矩阵中最小值的所有元素

**问题：取出第一个最小元素后，第二个最小元素怎么确定？**
* 取出最小值之后，第二个最小值有可能出现在队列中，也有可能出现在取出元素所在行的右边，所以只需要将取出最小值所在行的右边一个元素加入到队列中，让优先队列重新排序，得到的堆顶元素就是第二个最小值。后续以此类推

**问题：如何确定矩阵中每个元素的值和位置，以及在加入或退出优先队列时元素的位置？**
* 可以创建一个结构体，结构体中的成员维护矩阵中元素的x、y坐标位置，以及这个元素的值
* 优先队列只需要维护这样的结构体变量即可



*代码实现：*

```C++
class Solution{
private:
    struct Point{
        int x;
        int y;
        int val;
        Point(int val1,int x1,int y1):x(x1),y(y1),val(val1){}
    };
    
public:
    int kthSmallest(vector<vector<int>>& matrix,int k){
    	int n=matrix.size();
        
        auto comp = [](Point p1,Point p2){ return p1.val>p2.val; };
        priority_queue<Point,vector<Point>,decltype(Point)> pq(comp);
        
        for(int i=0;i<n;i++){
            Point p(matrix[i][0],i,0);
            pq.push(p);
        }
        for(int i=0;i<k-1;i++){
            Point tmp = pq.top();
            pq.pop();
            if(tmp.y != n-1){
                Point p(matrix[tmp.x][tmp.y+1],tmp.x,tmp.y+1);
                pq.push(p);
            }
        }
        
        return pq.top().val;
    }
};
```

*注解版：*

```C++
class Solution {
private:
    // 写一个结构体：表示矩阵中元素的坐标及其值
    struct Point{
    int x;
    int y;
    int val;

    Point(int val1,int x1,int y1):x(x1),y(y1),val(val1){}    
    };    

public:
    int kthSmallest(vector<vector<int>>& matrix, int k) {
        int n = matrix.size();

        // 利用lambda函数写一个自己的比较函数，用于创建小根堆
        auto comp = [](Point p1,Point p2){ return p1.val>p2.val; };
        // 创建队列
        priority_queue<Point,vector<Point>,decltype(comp)> pq(comp);

        // 创建小根堆：将矩阵中的第一列初始化为优先队列
        for(int i=0;i<n;i++){
            Point p(matrix[i][0],i,0);
            pq.push(p);
        }

        // 每次弹出优先队列中最小的元素，在横向加入元素，维护小根堆
        for(int i=0;i<k-1;i++){
            Point tmp = pq.top();
            pq.pop();
            // 判断横向是否有元素，有则加入到优先队列
            if(tmp.y != n-1){
                Point p(matrix[tmp.x][tmp.y+1],tmp.x,tmp.y+1);
                pq.push(p);
            }
        }

        // 最后返回第k小元素的值
        return pq.top().val;
    }
};
```

---

