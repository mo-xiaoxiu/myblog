---
title: "前缀树知识点"
date: 2021-10-19T11:10:28+08:00
draft: true
---

# 前缀树

**添加与搜索单词**

*参考题目：https://leetcode-cn.com/problems/design-add-and-search-words-data-structure/submissions/*

```
请你设计一个数据结构，支持 添加新单词 和 查找字符串是否与任何先前添加的字符串匹配 。

实现词典类 WordDictionary ：

WordDictionary() 初始化词典对象
void addWord(word) 将 word 添加到数据结构中，之后可以对它进行匹配
bool search(word) 如果数据结构中存在字符串与 word 匹配，则返回 true ；否则，返回  false 。word 中可能包含一些 '.' ，每个 . 都可以表示任何一个字母。
 

示例：

输入：
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
输出：
[null,null,null,null,false,true,true,true]

解释：
WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("bad");
wordDictionary.addWord("dad");
wordDictionary.addWord("mad");
wordDictionary.search("pad"); // return False
wordDictionary.search("bad"); // return True
wordDictionary.search(".ad"); // return True
wordDictionary.search("b.."); // return True
 

提示：

1 <= word.length <= 500
addWord 中的 word 由小写英文字母组成
search 中的 word 由 '.' 或小写英文字母组成
最多调用 50000 次 addWord 和 search

```



## 前缀树

前缀树根节点之下维护的是一个数组，数组中是各个该根节点下的子节点
**单词查找和添加：**
前缀树维护的是一个由26个字母组成的、类型也为前缀树的数组

### 创建前缀树

- 创建一个前缀树的类：
  - 成员：前缀树数组、判断当前节点此路径是否为单词最后一个字母（用来标记是否为单词）
  - 构造函数：初始化数组、判断标志
  - 析构函数：析构数组

### 题目的类内实现

- 构造函数：类内维护一个私有成员，即前缀树根节点，初始化根节点（指针）
- 析构函数：释放根节点指针
- 添加单词：遍历传入的单词字符串，判断遍历到的该字母是否在前缀树中已经存在，如果存在则将在存在的该字母节点下继续遍历后续的字符；如果不存在，则创建该节点；如果遍历到了字符串末尾，则将最后的节点标志为真，表示当前节点下路径存在单词
- 搜索单词：
  - 递归：以遍历单词的字符作为索引，递归前缀树
  - 递归函数返回值和参数：返回值：bool；参数：前缀树根节点、单词、遍历单词起始位置
  - 递归终止条件：遍历到空节点还没匹配，返回假；遍历到与单词长度相同的位置时，返回该节点下的标志：为真说明该节点下存在此单词，否则不存在；
  - 单层遍历逻辑：以单词字符作为递归遍历的索引，判断单词中该遍历的索引是否为“.”：是，则说明当前节点下的所有孩子都可以匹配，需要递归遍历所有孩子节点；否，则常规递归遍历

*代码实现：*

```C++
// 前缀树类
class TrieTree{
public:
    vector<TrieTree*> children; // 前缀树单词查找所设定的孩子数组（26）
    bool isWord;        // 判断路径当前节点下是否为字符串末尾（判断是否为单词）

    TrieTree():children(26,nullptr),isWord(false){}
    // 析构函数：记得释放内存
    ~TrieTree(){
        for(auto child:children){
            delete child;
        }
    }
};


class WordDictionary {
public:
    WordDictionary() {
        this->root=new TrieTree();
    }
    // 增加析构函数释放内存
    ~WordDictionary(){
        delete root;
    }
    
    void addWord(string word) {
        TrieTree* ptr=root; // 指针接管
        
        for(auto c:word){
            int index=c-'a';
            // 如果没有这个字符，则创建一个
            if(!ptr->children[index]){
                ptr->children[index]=new TrieTree();
            }
            // 指针指向最后一个单词字符：最后的孩子节点
            ptr=ptr->children[index];
        }
        // 表示该位置以上此路径为单词
        ptr->isWord=true;
    }
    
    bool search(string word) {
        return match(word,root,0);  // 递归函数
    }

    bool match(const string& s,TrieTree* root,int startIndex){
        if(!root) return false; // 递归终止条件
        if(startIndex==s.size()) return root->isWord;

        // 单层递归逻辑
        char c=s[startIndex];
        // 如果是正常字符，递归遍历对应的子树位置
        if(c!='.'){
            return match(s,root->children[c-'a'],startIndex+1);
        // 如果是“.”，则说明该节点下的子树节点都可以进行匹配    
        }else{
            for(const auto& child:root->children){
                if(match(s,child,startIndex+1)) return true;
            }
        }
        return false;
    }

private:
    TrieTree* root;
};
```

---

# 键值映射

*原题链接：https://leetcode-cn.com/problems/map-sum-pairs/submissions/*

```C++
实现一个 MapSum 类，支持两个方法，insert 和 sum：

MapSum() 初始化 MapSum 对象
void insert(String key, int val) 插入 key-val 键值对，字符串表示键 key ，整数表示值 val 。如果键 key 已经存在，那么原来的键值对将被替代成新的键值对。
int sum(string prefix) 返回所有以该前缀 prefix 开头的键 key 的值的总和。
 

示例：

输入：
["MapSum", "insert", "sum", "insert", "sum"]
[[], ["apple", 3], ["ap"], ["app", 2], ["ap"]]
输出：
[null, null, 3, null, 5]

解释：
MapSum mapSum = new MapSum();
mapSum.insert("apple", 3);  
mapSum.sum("ap");           // return 3 (apple = 3)
mapSum.insert("app", 2);    
mapSum.sum("ap");           // return 5 (apple + app = 3 + 2 = 5)
 

提示：

1 <= key.length, prefix.length <= 50
key 和 prefix 仅由小写英文字母组成
1 <= val <= 1000
最多调用 50 次 insert 和 sum

```

**思路：**

首先看到题目，要求使用一个函数根据传入的参数作为前缀，查找到所有的单词并返回单词对应的值

看到这里，我想到使用前缀树

回顾了一下前缀树的构建和操作：

* 首先是创建前缀树这个结构体：一个前缀树节点之下有一个用来存放26个字母节点的数组，还有一个标志着此节点之下构不构成单词的bool标志
* 初始化前缀树：将节点之下的数组26个位置全初始化为空，bool值全初始化为false
* 在字典这个结构体里去创建和初始化前缀树的根节点，析构函数记得去释放这个节点
* 字典的插入操作：遍历单词字符串，取出字符判断当前节点之下有没有创建好的字母节点，有则在此节点之下继续遍历单词字符串的下一个字符；没有则创建该节点，并在该节点之下继续遍历单词字符串......直到遍历到单词末尾，将当前节点标志为真，表示当前节点之下有单词
* 单词的查找：遍历目标单词，取出字符，判断在前缀树中是否有该节点，有则在该节点之下继续遍历目标单词；没有则直接返回假

在这里不需要查找，而是要做到除了能存储字符串之外，还要存放字符串对应的值；还需要能满足根据前缀向下查找到所有含有该前缀的单词的值，并计算加和

**根据以上要求进行修改：**

* 创建前缀树结构体：一个前缀树节点之下有一个用来存放26个字母节点的数组，**除去标志单词是否存在的bool值，直接使用记录当前单词的`val`值**，这样既能表示当前节点之下有没有单词，又可以记录节点值
* 初始化前缀树：将节点之下的数组26个节点位置全初始化为空，**`val`的值全初始化为-1**，-1表示当前节点之下没有单词
* 在字典这个结构体里去创建和初始化前缀树的根节点，析构函数记得去释放这个节点
* 字典的插入操作：遍历单词字符串，取出字符判断当前节点之下有没有创建好的字母节点，有则在此节点之下继续遍历单词字符串的下一个字符；没有则创建该节点，并在该节点之下继续遍历单词字符串......**直到遍历到单词末尾，记录当前节点的值为传入的`val`，表示当前节点之下有单词且记录了值**
* **计算前缀单词加和：在前缀树中查找到前缀，在前缀对应的节点之下遍历所有子节点加和所有单词的值**

上述的最后一步需要遍历所有子节点的情况，所以可以**使用`DFS`**

**看看各个模块的实现**



## 创建前缀树

```C++
class TrieTree{
public:
    TrieTree(): children(26, nullptr), val(-1) {}
    ~TrieTree() {
        for(auto& c: children) {
            delete c;
        }
    }
private:
    vector<TrieTree*> children;
    int val;
};
```

## 键值映射内部实现

```C++
class MapSum{
public:
    // 创建前缀树
    MapSum() {
        this->root = new TrieTree();
    }
    
    // 记得释放内存
    ~MapSum() {
        delete root;
    }
    
private:
    // 前缀树作为内部成员
    TrieTree* root;
    // 加和函数结果
    int res = 0;
};
```

## 插入操作

```C++
void insert(string key, int val) {
    // 由指针接管遍历
    TrieTree* ptr = root;
    for(auto& k: key) {
        if( !ptr->children[k-'a'] ) {
            ptr->children[i] = new TrieTree();
        }
        ptr = ptr->children[i];
    }
    ptr->val = val;
} // 如果没有节点则创建，在此新建节点下继续遍历；如果有则在此节点下继续遍历
```

## 计算加和

```C++
int sum (string prefix) {
    TrieTree* ptr = root;
    for(auto& c: prefix) {
        if( ptr->children[c-'a'] ) {
            ptr = ptr->children[c-'a'];
        } else {
            return 0;
        }
    } // 找到前缀
    
    // 在前缀向下遍历之前先将全局变量置为 0
    res = 0;
    
    // 前缀位置为一个单词，计和
    if( ptr->val!=-1 ) {
        res += ptr->val;
    }
    
    // DFS遍历
    dfs (ptr);
    
    return res;
}
```

## DFS

```C++
void dfs (TrieTree* ptr) {
    if(ptr == nullptr) return nullptr;
    
    // 遍历所有的子节点情况
    for(int i=0; i<26; i++) {
        if( ptr->children[i] ) {
            if( ptr->children[i]->val != -1 ) {
                res += ptr->children[i]->val;
            }
            // 递归，回溯
            dfs (ptr->children[i]);
        }
    }
    
    return;
}
```

**完整代码实现：**(包含日志调试)

```C++
class TrieTree {
public:
    TrieTree():children(26, nullptr), val(-1) {}
    ~TrieTree(){
        for(auto& child: children) {
            delete child;
        }
    }

    vector<TrieTree*> children;
    int val;    
};

class MapSum {
public:
    MapSum() {
        this->root = new TrieTree();
    }
    ~MapSum() {
        delete root;
    }
    
    void insert(string key, int val) {
        TrieTree* ptr = root;
        for(auto& k: key) {
            if(!ptr->children[k-'a']) {
                ptr->children[k-'a'] = new TrieTree();
            } 
            ptr = ptr->children[k-'a'];
        }
        //cout<<"val="<<ptr->val<<endl;
        ptr->val = val;
        //cout<<"ptr->val="<<ptr->val<<endl;
    }
    
    int sum(string prefix) {
        TrieTree* ptr = root;
        for(auto& c: prefix) {
            if(ptr->children[c-'a']) {
                ptr = ptr->children[c-'a'];
            } else {
                return 0;
            }
        }
        res = 0;
        //cout<<"ptr->val="<<ptr->val<<endl;
        if(ptr->val!=-1) {
            res += ptr->val;
        }
        
        dfs(ptr);
        //cout<<res<<endl;
        //cout<<"--------"<<endl;
        return res;
    }

    void dfs(TrieTree* ptr) {
        if(ptr == nullptr) return;

        for(int i=0;i<26;i++) {
            if(ptr->children[i]) {
                if(ptr->children[i]->val!=-1) {
                    res += ptr->children[i]->val;
                    //cout<<res<<"------"<<endl;
                }
                dfs(ptr->children[i]);
            }
        }
        return;
    }

private:
    TrieTree* root;
    int res;
};

/**
 * Your MapSum object will be instantiated and called as such:
 * MapSum* obj = new MapSum();
 * obj->insert(key,val);
 * int param_2 = obj->sum(prefix);
 */
```

---

