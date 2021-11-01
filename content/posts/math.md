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

