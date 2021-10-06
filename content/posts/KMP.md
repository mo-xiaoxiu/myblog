---
title: "字符串——KMP"
date: 2021-10-06T22:29:09+08:00
draft: true
---

# KMP算法

## KMP算法理解

**前缀**：这里的前缀是针对字符串的理解的。是指必须包含首字母、但不包含尾字母的所有子串

例如：

```
aabaaf

前缀：
a
aa
aab
aaba
aabaa

```

**后缀**：是指必须包含尾字母、但不包含首字母的所有字符串

例如：

```
aabaaf

后缀：
f
af
aaf
baaf
abaaf

```

### 前缀表

前缀表是根据前缀组合，**计算每个组合在对应字符串索引位置的前后缀字母的相等数量**

例如：

```
aabaaf

前缀表：
字母：				索引：			前后缀相等数量：
a				0			0
aa				1			1
aab				2			0
aaba				3			1
aabaa				4			2
aabaaf				5			0

```

## KMP实现

有关于KMP得出字符串的前缀表的代码如下：

```C++
// next：前缀表数组
// i：维护的是后缀
// j：维护的是前缀
// 原则：当前后缀不匹配时，前缀指针 j 回退到上一个匹配的位置，在那个位置继续往后匹配

void getNum(int* next,const string& s){
    int j=0;			// 哨兵 j：负责计算并在相应字符串位置放置前缀表的数据
    next[0]=0;			// 初始化前缀表：一开始只有首字母，所以前后缀没有相同的
    
    // 哨兵 i：遍历字符串，判断该位置的后缀与哨兵 j 所维护的前缀是否相等
    for(int i=1;i<s.size();i++){
        // 不相等，则哨兵 j 回退到前一个能够匹配的位置（-1）
        while(j>0 && s[i]!=s[j]){
            j=next[j-1];
        }
        
        // 如果匹配的话，哨兵i 和哨兵 j继续前进
        if(s[i]==s[j]){
            j++;
        }
        
        // 更新前缀表的数值
        next[i]=j;
    }
}
```



## 字符串匹配

利用字符串的前缀表，可以查看另一个字符串中字符的匹配问题

### 重复的子字符串

*原题链接：https://leetcode-cn.com/problems/repeated-substring-pattern/*

```
给定一个非空的字符串，判断它是否可以由它的一个子串重复多次构成。给定的字符串只含有小写英文字母，并且长度不超过10000。

示例 1:

输入: "abab"

输出: True

解释: 可由子字符串 "ab" 重复两次构成。
示例 2:

输入: "aba"

输出: False
示例 3:

输入: "abcabcabcabc"

输出: True

解释: 可由子字符串 "abc" 重复四次构成。 (或者子字符串 "abcabc" 重复两次构成。)

```

*代码实现：*

```C++
class Solution {
public:

    // 获得前缀表
    void getNum(int* next,const string& s){
        int j=0;
        next[0]=0;

        for(int i=1;i<s.size();i++){
            while(j>0 && s[i]!=s[j]){
                j=next[j-1];
            }

            if(s[i]==s[j]){
                j++;
            }

            next[i]=j;
        }
    }


    bool repeatedSubstringPattern(string s) {
        if(s.size()==0) return false;

        int next[s.size()];
        getNum(next,s);
        
        // 打印日志：
        // 例：“a b c a b c a b c a b c”
        // 	   0 0 0 1 2 3 4 5 6 7 8 9
        // for(int i=0;i<s.size();i++){
        //     cout<<next[i]<<" ";
        // }

        // 前缀表最后一个元素不为0（为0说明最后一位前后缀不匹配，则这个字符串的子串不能构成本身）
        // 字符串减去最长前后缀相等字符串，如果能被本身长度整除，说明这个字符串除去最长相等的前后缀字符之后，剩余的字符串就是能够成原字符串的子串
        int n=s.size();
        if(next[n-1] && n%(n-next[n-1])==0) return true;
        return false;
    }
};
```

---

### 实现strStr (  )

*原题链接：https://leetcode-cn.com/problems/implement-strstr/*

```
实现 strStr() 函数。

给你两个字符串 haystack 和 needle ，请你在 haystack 字符串中找出 needle 字符串出现的第一个位置（下标从 0 开始）。如果不存在，则返回  -1 。

 

说明：

当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。

对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与 C 语言的 strstr() 以及 Java 的 indexOf() 定义相符。

 

示例 1：

输入：haystack = "hello", needle = "ll"
输出：2
示例 2：

输入：haystack = "aaaaa", needle = "bba"
输出：-1
示例 3：

输入：haystack = "", needle = ""
输出：0
 

提示：

0 <= haystack.length, needle.length <= 5 * 104
haystack 和 needle 仅由小写英文字符组成

```

*代码实现：*

```C++
class Solution {
public:

    // 获得前缀表
    void getNext(int* next,const string& s){
        int j=0;        // 哨兵 1：遍历以得到前缀表的各个元素
        next[0]=0;      // 初始化前缀表：因为只有首字母，所以为 0

        // 另一个哨兵 i：从 j 的后面开始遍历，比较 i 和 j 所指的值是否相等（比较前后缀）
        for(int i=1;i<s.size();i++){
            // 前后缀不匹配，回退到前一个匹配的位置，获得此位置前缀表的值，直到不匹配时，哨兵 j 回退到前面的那个位置
            while(j>0 && s[i]!=s[j]){
                j=next[j-1];
            }

            // 字符匹配的时候，哨兵往后走
            if(s[i]==s[j]){
                j++;
            }
            // 更新前缀表：由哨兵 j 更新
            next[i]=j;
        }
    }


    // 比较两个字符串
    int strStr(string haystack, string needle) {
        if(needle.size()==0) return 0;

        int next[needle.size()];
        getNext(next,needle);       // 得出前缀表

        // 像获得前缀表一样的方法匹配字符串
        int j=0;
        for(int i=0;i<haystack.size();i++){
            while(j>0 && haystack[i]!=needle[j]){
                j=next[j-1];
            }

            if(haystack[i]==needle[j]){
                j++;
            }
            
            // 找到了匹配的字符串（所有字母都满足），则返回索引
            if(j==needle.size()){
                return (i-needle.size()+1);
            }
        }

        return -1;
    }
};
```

---

