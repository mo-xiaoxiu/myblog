---
title: "哈希表知识点"
date: 2021-10-03T16:01:40+08:00
draft: true
---

# 哈希表与其他方法的组合

## 哈希+数组

### 有效的字母异位词

*原题链接：https://leetcode-cn.com/problems/valid-anagram/*

```
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

注意：若 s 和 t 中每个字符出现的次数都相同，则称 s 和 t 互为字母异位词。

 

示例 1:

输入: s = "anagram", t = "nagaram"
输出: true
示例 2:

输入: s = "rat", t = "car"
输出: false
 

提示:

1 <= s.length, t.length <= 5 * 104
s 和 t 仅包含小写字母


```

*代码实现：*

```C++
class Solution {
public:
    bool isAnagram(string s, string t) {
        int array[26]={0};				// 创建一个26个字母数量的数组作为哈希表
        for(int i=0;i<s.size();i++){	 // 将字符串s放入哈希表，记录字符串s中每个字符以及其出现的次数
            array[s[i]-'a']++;
        }

        for(int i=0;i<t.size();i++){	// 遍历字符串t开始对比，如果遍历到字符有出现在哈希数组中，说明字符存在，则哈希数组相应字符出现次数-1
            array[t[i]-'a']--;
        }

        for(int i=0;i<26;i++){			// 最后检查哈希数组中是否还有剩余，有剩余说明字符串s中存在字符串t没有的字符，则不是异位词；
            if(array[i]!=0) return false;
        }
        return true;					// 没有剩余就是异位词
    }
};
```

---

### 赎金信

*原题链接：https://leetcode-cn.com/problems/ransom-note/*

```
给定一个赎金信 (ransom) 字符串和一个杂志(magazine)字符串，判断第一个字符串 ransom 能不能由第二个字符串 magazines 里面的字符构成。如果可以构成，返回 true ；否则返回 false。

(题目说明：为了不暴露赎金信字迹，要从杂志上搜索各个需要的字母，组成单词来表达意思。杂志字符串中的每个字符只能在赎金信字符串中使用一次。)

 

示例 1：

输入：ransomNote = "a", magazine = "b"
输出：false
示例 2：

输入：ransomNote = "aa", magazine = "ab"
输出：false
示例 3：

输入：ransomNote = "aa", magazine = "aab"
输出：true


```

*代码实现：*

```C++
class Solution {
public:
    bool canConstruct(string ransomNote, string magazine) {
        int note[26]={0};					// 创建一个26个字母为数据量的哈希表
        for(int i=0;i<magazine.size();i++){   // 将字符串magazine中的字符放入哈希数组中
            note[magazine[i]-'a']++;
        }
        for(int i=0;i<ransomNote.size();i++){ // 遍历字符串ransomNote，对比哈希数组
            note[ransomNote[i]-'a']--;
            if(note[ransomNote[i]-'a']<0) return false;	// 如果哈希数组中某个位置的元素小于0，说明ransomNote中该字符的出现次数超过了magazine中的了，说明不满足题意，返回假
        }
        return true;
    }
};
```

---

## 哈希表

### 字母异位词分组

*原题链接：https://leetcode-cn.com/problems/group-anagrams/*

```
给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。

字母异位词 是由重新排列源单词的字母得到的一个新单词，所有源单词中的字母都恰好只用一次。

 

示例 1:

输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
示例 2:

输入: strs = [""]
输出: [[""]]
示例 3:

输入: strs = ["a"]
输出: [["a"]]
 

提示：

1 <= strs.length <= 104
0 <= strs[i].length <= 100
strs[i] 仅包含小写字母


```

*代码实现：*

```C++
// 这里用数组的排序加上哈希表的方法
class Solution {
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        vector<vector<string>> res;				// 结果数组
        unordered_map<string,vector<string>>map; // 哈希表

        for(string& str:strs){					// 以每个字符串排序后的样子作为哈希表的key值
            string tmp=str;						// 每个原字符串作为哈希表的value值
            sort(tmp.begin(),tmp.end());		 // 所以需要创建临时字符串保存原子串，作为value值
            map[tmp].emplace_back(str);
        }

        for(auto it=map.begin();it!=map.end();it++){	// 遍历哈希表，将其中的数据放入结果数组并返回
            res.emplace_back(it->second);
        }
        return res;
    }
};
```



## 重复的DNA序列

*原题链接：https://leetcode-cn.com/problems/repeated-dna-sequences/*

```
所有 DNA 都由一系列缩写为 'A'，'C'，'G' 和 'T' 的核苷酸组成，例如："ACGAATTCCG"。在研究 DNA 时，识别 DNA 中的重复序列有时会对研究非常有帮助。

编写一个函数来找出所有目标子串，目标子串的长度为 10，且在 DNA 字符串 s 中出现次数超过一次。

 

示例 1：

输入：s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
输出：["AAAAACCCCC","CCCCCAAAAA"]
示例 2：

输入：s = "AAAAAAAAAAAAA"
输出：["AAAAAAAAAA"]
 

提示：

0 <= s.length <= 105
s[i] 为 'A'、'C'、'G' 或 'T'
```

*代码实现：*

```C++
class Solution{
    public:
    	vector<string> findRepeatedDnaSequences(string s) {
            vector<string> res;
            // key：子串	value：子串出现次数
            unordered_map<string,int>count;	// 用哈希表放置子串，作为计数
            
            int n=s.size();
            for(int i=0;i<=n-10;i++){
                string str=s.substr(i,L);
                if(++count[str]==2) res.push_back(str);
            }
            
            return res;
        }
};
```



---



## 滑动窗口 + 哈希表

### 找到字符串中所有字母异位词

*原题链接：https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/*

```
给定两个字符串 s 和 p，找到 s 中所有 p 的 异位词 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。

异位词 指字母相同，但排列不同的字符串。

 

示例 1:

输入: s = "cbaebabacd", p = "abc"
输出: [0,6]
解释:
起始索引等于 0 的子串是 "cba", 它是 "abc" 的异位词。
起始索引等于 6 的子串是 "bac", 它是 "abc" 的异位词。
 示例 2:

输入: s = "abab", p = "ab"
输出: [0,1,2]
解释:
起始索引等于 0 的子串是 "ab", 它是 "ab" 的异位词。
起始索引等于 1 的子串是 "ba", 它是 "ab" 的异位词。
起始索引等于 2 的子串是 "ab", 它是 "ab" 的异位词。
 

提示:

1 <= s.length, p.length <= 3 * 104
s 和 p 仅包含小写字母


```

*代码实现：*

```C++
class Solution {
public:
    vector<int> findAnagrams(string s, string p) {
        // 结果数组，存放满足要求的子串下标
        vector<int>res;

        int sn=s.size(),pn=p.size();
        if(sn<pn) return res;
        // 一个数组存放 s 字符串滑动窗口的字符及其出现次数
        // 一个数组存放 p 字符串的字符及其出现次数
        vector<int>st(26,0);vector<int>win(26,0);


        // 将 p 字符串的字符及其出现次数放入st数组中
        for(int i=0;i<pn;i++){
            st[p[i]-'a']++;
        }

        // 滑动窗口：
        // 快指针往右遍历，将窗口中的元素放入win哈希数组
        // 窗口长度超过字符串p的长度，则收缩窗口：左指针右移，去除win哈希数组对应的值
        int slow=0,fast=0;
        for(;fast<sn;fast++){
            win[s[fast]-'a']++;
            if(fast>=pn){
                win[s[slow++]-'a']--;
            }

            // 实时对比两个哈希数组是否相等（vector容器提供“==”的比较操作），如果相等则将窗口左指针维护的位置放入结果数组中，此时找到一个满足条件的索引
            if(win==st){
                res.push_back(slow);
            }
        }

        return res;
    }
};
```



## 重复的DNA序列

*原题链接：https://leetcode-cn.com/problems/repeated-dna-sequences/*

```
所有 DNA 都由一系列缩写为 'A'，'C'，'G' 和 'T' 的核苷酸组成，例如："ACGAATTCCG"。在研究 DNA 时，识别 DNA 中的重复序列有时会对研究非常有帮助。

编写一个函数来找出所有目标子串，目标子串的长度为 10，且在 DNA 字符串 s 中出现次数超过一次。

 

示例 1：

输入：s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
输出：["AAAAACCCCC","CCCCCAAAAA"]
示例 2：

输入：s = "AAAAAAAAAAAAA"
输出：["AAAAAAAAAA"]
 

提示：

0 <= s.length <= 105
s[i] 为 'A'、'C'、'G' 或 'T'

```

*代码实现：*

```C++
class Solution{
    public:
    	const int L=10;
    	unordered_map<char,int>map={{'A',0},{'C',1},{'G',2},{'T',3}};	// 将字符串中出现的字母转换成比特位
    
    	vector<string> findRepeatedDnaSequences(string s) {
			vector<string> res;	// 结果数组
            if(s.size()<=10) return res;	// 如果字符串的长度比10还小，则直接返回
            
            // x：用来表示滑动窗口的值（int：32bit  限定其最低位的10位作为字符串的滑动窗口）
            int x=0;
            // 先将开头的10个字符放入滑动窗口
            for(int i=0;i<L-1;i++){
                x=(x<<2) | (map[s[i]]);
            }
            
            // 后续加入字母，窗口长度不满足，缩小窗口
            // 哈希表计数：以滑动窗口中的值作为key（可以避免用字母直接表示滑动窗口而在放入哈希表检查时需要大量空间的情况），以子串出现次数作为value
            unorderde_map<int,int>count;
            for(int i=0;i<s.size()-L+1;i++){
                x=((x<<2) | (map[s[i+L-1]])) & (1<<2*L-1);
                if(++count[x]==2){
                    res.push_back(s.substr(i,L));
                }
            }
            
            return res;
        }
};
```



---

## unordered_set + 数组

### 两个数组的交集

*原题链接：https://leetcode-cn.com/problems/intersection-of-two-arrays/*

```
给定两个数组，编写一个函数来计算它们的交集。

 

示例 1：

输入：nums1 = [1,2,2,1], nums2 = [2,2]
输出：[2]
示例 2：

输入：nums1 = [4,9,5], nums2 = [9,4,9,8,4]
输出：[9,4]
 

说明：

输出结果中的每个元素一定是唯一的。	// 结果使用set的原因
我们可以不考虑输出结果的顺序。

```

*代码实现：*

```C++
// hashSet特点：key值不允许重复
class Solution {
public:
    vector<int> intersection(vector<int>& nums1, vector<int>& nums2) {
        unordered_set<int>res;		// 结果要求不重复，所以使用hashSet
        unordered_set<int>nums1_set(nums1.begin(),nums1.end());	// 将其中一个数组的值放入set中

        // 遍历另一个数组的时候查询set，由于set中的值是唯一的，所以不会重复查到多个值
        // 再将满足条件的结果放入结果的set中，防止其重复
        for(int num:nums2){
            if(nums1_set.find(num)!=nums1_set.end()){
                res.insert(num);
            }
        }

        // 题目要求返回数组类型，所以将结果放入vector
        return vector<int>(res.begin(),res.end());
    }
};
```

---

## 模拟运算 + 哈希表

### 快乐数

*原题链接：https://leetcode-cn.com/problems/happy-number/*

```
编写一个算法来判断一个数 n 是不是快乐数。

「快乐数」定义为：

对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和。
然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。
如果 可以变为  1，那么这个数就是快乐数。
如果 n 是快乐数就返回 true ；不是，则返回 false 。

 

示例 1：

输入：19
输出：true
解释：
12 + 92 = 82
82 + 22 = 68
62 + 82 = 100
12 + 02 + 02 = 1
示例 2：

输入：n = 2
输出：false

```

*代码实现：*

```C++
class Solution {
public:
    // 判断是否为快乐数的函数
    int getSum(int n){
        int sum=0;
        while(n){
            // 取余操作：取不同的位数
            sum+=(n%10)*(n%10);
            n/=10;
        }
        return sum;
    }

    bool isHappy(int n) {
        unordered_set<int>set;	// 创建set来存放每次计算的位数总和（是否为快乐数的数）
        
        while(1){
            int sum=getSum(n);
            if(sum==1){
                return true;	// 满足条件，返回真
            }else if(set.find(sum)!=set.end()){	// 在哈希set中找得到说明接下来的操作会出现循环，所以直接返回假
                return false;
            }else{				// 既不满足条件，在哈希set中又找不到，所以将该数放入set中
                set.insert(sum);
            }
            n=sum;
        }
    }
};
```

---

### 分数到小数

*原题链接：https://leetcode-cn.com/problems/fraction-to-recurring-decimal/*

```
给定两个整数，分别表示分数的分子 numerator 和分母 denominator，以 字符串形式返回小数 。

如果小数部分为循环小数，则将循环的部分括在括号内。

如果存在多个答案，只需返回 任意一个 。

对于所有给定的输入，保证 答案字符串的长度小于 104 。

 

示例 1：

输入：numerator = 1, denominator = 2
输出："0.5"
示例 2：

输入：numerator = 2, denominator = 1
输出："2"
示例 3：

输入：numerator = 2, denominator = 3
输出："0.(6)"
示例 4：

输入：numerator = 4, denominator = 333
输出："0.(012)"
示例 5：

输入：numerator = 1, denominator = 5
输出："0.2"

```

*代码实现：*

```C++
class Solution {
public:
    string fractionToDecimal(int numerator, int denominator) {
        // 取余数数据量比较大，改用long类型
        long num=numerator,den=denominator;
        if(num*den==0) return "0";
        
        string res;     // 结果字符串
        if(num*den<0) res+='-';     // 判断两个数当中有没有负数

        num=abs(num);den=abs(den);  // 取绝对值操作

        res+=to_string(num/den);    // 先将取整的数放进结果

        if(num%den)                 // 如果有余数，追加小数点
        res+='.';

        long a=num%den;             // 取余
        long index=0;
        string s;                   // 临时字符串
        unordered_map<int,int>map;  // 哈希表
        while(a && !map.count(a)){  // 循环条件：余数一直存在 && 有余数重复出现
            // 模拟运算过程
            map[a]=index++;
            a*=10;
            s.push_back((a/den+'0'));
            a%=den;
        }

        if(a!=0){                   // 此条件存在（出循环后，余数部分有循环出现）
            res+=s.substr(0,map[a])+"("+s.substr(map[a])+")";
        }else{					  // 此条件若不存在，说明出循环后，余数有限，直接追加在结果字符串后面
            res+=s;
        }

        return res;
    }
};
```

---

### 两数之和

*原题链接：https://leetcode-cn.com/problems/two-sum/*

```
给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。

你可以按任意顺序返回答案。

 

示例 1：

输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
示例 2：

输入：nums = [3,2,4], target = 6
输出：[1,2]
示例 3：

输入：nums = [3,3], target = 6
输出：[0,1]
 

提示：

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
只会存在一个有效答案
进阶：你可以想出一个时间复杂度小于 O(n2) 的算法吗？

```

*代码实现（哈希表）：*

```C++
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int,int>map;			// 创建一个哈希表存放nums数组的值以及每个数的出现次数
        for(int i=0;i<nums.size();i++){		// 遍历数组中添加
            auto it=map.find(target-nums[i]);	// 先在哈希表中找target-当前元素值有没有出现
            if(it!=map.end()){					// 如果出现了，说明找到了满足的元素，返回该元素的值及其下标
                return {it->second,i};
            }else{								// 没出现，则把该元素及其下标以键值对的形式放入哈希表中
                map.insert(pair<int,int>(nums[i],i));
            }
        }
        return {};
    }
}
```

---

## 哈希表处理众数

*原题链接：https://leetcode-cn.com/problems/majority-element-ii/*

```
给定一个大小为 n 的整数数组，找出其中所有出现超过 ⌊ n/3 ⌋ 次的元素。

 

 

示例 1：

输入：[3,2,3]
输出：[3]
示例 2：

输入：nums = [1]
输出：[1]
示例 3：

输入：[1,1,1,3,3,2,2,2]
输出：[1,2]
 

提示：

1 <= nums.length <= 5 * 104
-109 <= nums[i] <= 109
 

进阶：尝试设计时间复杂度为 O(n)、空间复杂度为 O(1)的算法解决此问题。

```

* 创建一个哈希表和一个结果数组
* 遍历数组将数组中的元素放入哈希表
* 遍历哈希表，如果该元素在哈希表中出现的次数大于数组长度的1/3，则将该元素放入结果数组

*代码实现：*

```C++
class Solution {
public:
    vector<int> majorityElement(vector<int>& nums) {
        vector<int> res;
        unordered_map<int,int> map;

        for(int num:nums){
            map[num]++;
        }

        for(auto it=map.begin();it!=map.end();it++){
            if((*it).second>(nums.size()/3)){
                res.push_back((*it).first);
            }
        }
        return res;
    }
};
```

*进阶做法：摩尔投票法*

---



