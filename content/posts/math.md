---
title: "算法数学"
date: 2021-11-01T13:50:16+08:00
draft: true
---

# 数学

## 形成3的最大倍数

*原题链接：https://leetcode-cn.com/problems/largest-multiple-of-three/*

```
给你一个整数数组 digits，你可以通过按任意顺序连接其中某些数字来形成 3 的倍数，请你返回所能得到的最大的 3 的倍数。

由于答案可能不在整数数据类型范围内，请以字符串形式返回答案。

如果无法得到答案，请返回一个空字符串。

 

示例 1：

输入：digits = [8,1,9]
输出："981"
示例 2：

输入：digits = [8,6,7,1,0]
输出："8760"
示例 3：

输入：digits = [1]
输出：""
示例 4：

输入：digits = [0,0,0,0,0,0]
输出："0"
 

提示：

1 <= digits.length <= 10^4
0 <= digits[i] <= 9
返回的结果不应包含不必要的前导零。

```

首先明确：一个数如果是3的倍数，则将它的各位加起来也会是3的倍数

这样看来，题目给出的数组中，所有元素值的总和有可能是3的倍数，有可能不是3的倍数
* 当总和是3的倍数时，直接返回原数组中的元素所组成的最大值的字符串即可
* 当总和不是3的倍数时：当总和与3取模余1时
	* 找到数组中最小的、与3取模余1的一个数，将该数移除考虑范围
	* 如果没有找到这样的数，则找到数组中最小的、与3取模余2的两个数，将这两个数移除考虑范围
	* 如果不存在上面这两种情况的数，只有一个与3取模余2的最小数，那数组总和必然是3的倍数

当数组总和与3取模余2时也是一样的分析：
* 找到数组中最小的、与3取模余1的两个数
* 找到数组中最小的、与3取模余2的一个数

*代码实现：*

```C++
class Solution{
public:
    string largestMultpleOfThree(vector<int>& digits){
        vector<int> count(10),modulo(3);
        int sum=0;
        for(int digit: digits){
            count[digit]++;
            modulo[digit % 3]++;
            sum += digit;
        }
        
        int res=0;int remove_mo=0;
        if(sum % 3 == 1){
            if(modulo[1]>=1){
                res = 1;
                remove_mo = 1;
            }else{
                res = 2;
                remove_mo = 2;
            }
        }
        
        if(sum % 3 == 2){
            if(modulo[2]>=1){
                res = 1;
                remove_mo = 2;
            }else{
                res = 2;
                remove_mo = 1;
            }
        }
        
        string result;
        for(int i=0;i<10;i++){
            for(int j=0;j<count[i];j++){
                if(res && remove_mo == i % 3){
                    res--;
                }else{
                    result += static_cast<char>(i + 48);
                }
            }
        }
        if(result.size() && result.back=='0'){
            res = "0";
        }
        
        reverse(result.begin(),result.end());
        return result;
    }
};
```

*注解版：*

```C++
class Solution {
public:
    string largestMultipleOfThree(vector<int>& digits) {
        // count用于记录数组中元素及其出现的次数，用于拼接返回值
        // modulo用于记录数组中元素与3取模余1、与3取模余2的元素个数，用于删除
        vector<int> count(10),modulo(3);
        // 数组总和
        int sum = 0;
        // 遍历数组：同步这3件事情
        for(int digit: digits){
            count[digit]++;
            sum += digit;
            modulo[digit % 3]++;
        }

        // res用于记录需要删除的元素个数
        // remove_mo用于记录删除的元素是：与3取模余1 or 与3取模余2
        int res=0;int remove_mo=0;
        // 当总和是与3取模余1
        if(sum % 3 == 1){
            // 数组中存在与3取模余1的数，记录
            if(modulo[1]>=1){
                res=1;
                remove_mo=1;
            // 否则，则记录与3取模余2的两个数
            }else{
                res=2;
                remove_mo=2;
            }
        }
        // 分析同上
        if(sum % 3 == 2){
            if(modulo[2]>=1){
                res=1;
                remove_mo=2;
            }else{
                res=2;
                remove_mo=1;
            }
        }

        // 结果字符串
        string result;
        // 从小到大拼接字符串：移除删除的元素
        for(int i=0;i<10;i++){
            for(int j=0;j<count[i];j++){
                if(res && remove_mo==i % 3){
                    res--;
                }else{  // 转化为字符
                    result+=static_cast<char>(i+48);
                }
            }
        }
        // 如果结果字符串都是0，则将结果字符串置为一个0
        if(result.size() && result.back()=='0'){
            result="0";
        }

        // 反转字符串：为了得到最大值
        reverse(result.begin(),result.end());
        return result;
    }
};
```

---

# 模拟

## 检测大写字母

*原题链接：https://leetcode-cn.com/problems/detect-capital/*

```
我们定义，在以下情况时，单词的大写用法是正确的：

全部字母都是大写，比如 "USA" 。
单词中所有字母都不是大写，比如 "leetcode" 。
如果单词不只含有一个字母，只有首字母大写， 比如 "Google" 。
给你一个字符串 word 。如果大写用法正确，返回 true ；否则，返回 false 。

 

示例 1：

输入：word = "USA"
输出：true
示例 2：

输入：word = "FlaG"
输出：false
 

提示：

1 <= word.length <= 100
word 由小写和大写英文字母组成

```

**思路一：**

首先确定一下题目规定的满足条件的几点：

* 字符串字符全部都是小写字母
* 字符串首字母是大写字母，其余后面的字符是小写字母
* 字符串全部都是大写字母

常规的思路是：

遍历字符串，从第一个·字符入手

1. **如果第一个字符为大写字母，需要判断其后的第二个字符**

2. **如果第一个字符为小写字母，需要判断后面所有的字符**

首先看第一种情况：

* 第一个字符为大写字母，第二个字符也为大写字母：后面所有的字符都得是大写字母
* 第一个字符为大写字母，第二个字符为小写字母：后面所有的字符都得是小写字母

再来看看第二种情况：

* 第一个字符为小写字母，后面所有的字符都得是小写字母

**算法实现：**

* 利用`if-else`条件判断语句来判断区分字符串第一个字符为大写字母或者小写字母的两种情况
  * `isupper(word[0])`：条件为真，判断第二个字符的大小写情况
    * `isupper(word[1])`：条件为真，`for`循环遍历后续字符：`if(islower(word[i]))`条件为真则返回假
    * `isupper(word[1])`：条件为假，`for`循环遍历后续字符：`if(isupper(word[i]))`条件为真则返回假
  * `islower(word[0])`：条件为真，`for`循环遍历后续字符：`if(isupper(word[i]))`条件为真则返回假
* 其余情况为真



```C++
class Solution{
public:
    bool detectCapitalUse(string word) {
        bool isWord = true;
        // 判断第一个字符是否为大写：
        // 大写情况：
        if(isupper(word[0])) {
            // 判断第二个字符是否为小写：
            // 大写：
            if(isupper(word[1])) {
                // 后续若出现小写直接返回假
                for(int i=2;i<word.size();i++) {
                    if(islower(word[i])) {
                        isWord = false;
                        break;
                    }
                }
                // 小写：
            }else {
                // 后续若出现大写直接返回假
                for(int i=2;i<word.size();i++) {
                    if(isupper(word[i])) {
                        isWord = false;
                        break;
                    }
                }
            }
            // 小写情况：
        }else if(islower(word[0])) {
            // 后续若出现大写直接返回假
            for(int i=1;i<word.size();i++) {
                if(isupper(word[i])) {
                    isWord = false;
                    break;
                }
            }
        }
        
        return isWord;
    }
};
```

---

*这样重复的出现条件判断语句有些繁琐，有没有可以避重就轻地思路？*

**思路二：**

既然从第一个字符开始判断需要面临多种临界条件，那从第二个字符开始呢，第三个呢，后面的呢？

先试试从第二个字符开始判断：

同样需要判断第二个字符大小写的情况：

* 大写：需要判断字符左右两边的字符大小写情况：

  * 左边也必须是大写：如果左边是小写的话，那相当于小写字符串中间突然出现大写字母，不满足条件
  * 右边也必须是大写：很显然，前两个字符都已经是大写字母了，所以表示这一整个字符串都得是大写字母

* 小写：同样需要判断字符左右两边的字符大小写情况：

  * 左边大写可以吗？

    当然可以，如果是第二个字符的话，那第一个字符当然可以是大写字母

  * 左边小写可以吗？

    当然可以，这样整体就是小写字符串

  * 右边大写可以吗？

    不可以，相当于小写字符串中间突然出现大写字母，不满足条件

  * 右边小写可以吗？

    可以，整体小写字符串

这样看起来似乎条件更多了，我们来考虑一下有没有可以归并的情况：

我们先来看看后续随意一个字符的情况（除了第一个字符之外）：

* 该字符大写：
  * 左边字符必须大写
  * 右边字符必须大写
* 该字符小写：
  * 左边字符必须小写：这是最保险的
  * 右边字符必须小写

这样我们似乎可以将问题简化：遍历字符串的时候只需要判断都为小写或者都为大写既可以了



**算法实现：（以左右两边字符是否为小写来作为判断依据）**

* `for`循环遍历字符串：索引 i 从 1 开始，判断前一个字符（该字符左边的字符）是否为小写

  * `if(isupper(word[i]))`：当前遍历位置字符为大写字母，左右两边字符必须是大写才能满足条件

    * `islower(word[i-1])`：条件为真，直接返回假

    * `islower(word[i+1])`：条件为真，直接返回假，加上防止越界的先决条件`i!=word.size()-1`

      即`if(i!=word.size()-1 && islower(word[i+1]))`

* 其余条件为真



```C++
class Solution {
public:
    bool detectCapitalUse(string word) {
        // 判断遍历位置字符及其左右字符的大小写情况
        for(int i=1;i<word.size();i++) {
            // 如果当前字符为大写
            if(isupper(word[i])) {
                // 左边字符为小写直接返回假
                if(islower(word[i-1])) {
                    return false;
                }
                // 右边字符为小写直接返回假
                if(i!=word.size()-1 && islower(word[i+1])) {
                    return false;
                }
            }
        }
        return true;
    }
};
```

---

