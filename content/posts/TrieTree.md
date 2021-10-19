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

