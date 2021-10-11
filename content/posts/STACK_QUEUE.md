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

## 前k个高频元素

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

