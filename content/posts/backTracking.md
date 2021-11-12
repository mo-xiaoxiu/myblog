---
title: "回溯算法"
date: 2021-11-12T14:09:58+08:00
draft: true
---

# 回溯

可以将问题的暴力解法抽象成一颗 N 叉树，递归遍历所有可能的方法

回溯，顾名思义，必定有回的步骤，这就相当于在树的某个节点以某个孩子节点为路径递归遍历下去，当触及到该路径的叶子节点时，一层一层回到当前节点的过程

## 电话号码的字母组合

*原题链接：https://leetcode-cn.com/problems/letter-combinations-of-a-phone-number/*

```
给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。答案可以按 任意顺序 返回。

给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。



 

示例 1：

输入：digits = "23"
输出：["ad","ae","af","bd","be","bf","cd","ce","cf"]
示例 2：

输入：digits = ""
输出：[]
示例 3：

输入：digits = "2"
输出：["a","b","c"]
 

提示：

0 <= digits.length <= 4
digits[i] 是范围 ['2', '9'] 的一个数字。


```

### 回溯算法过程

#### 递归函数的参数和返回值

* 参数：目标值
* 返回值：由于回溯需要遍历一整棵树所以不需要返回值，只需要设置存放结果的全局变量即可

#### 递归终止条件

当字母组合元素个数到达“按键”字符串组合的数量时，满足条件，将组合放入结果并返回

#### 单层递归逻辑

* 先将每个按键数字对应的几个字母的字符串用数组映射出来
* 将按键数字转化为对应的字母字符串，对于同一树枝，每次遍历都从字母字符串的第一个字母开始，这就要求递归遍历的时候，索取按键字符串中的数字位置要不断+1；对于同一树层，每次遍历去下一个数字
* 回溯：将字母放入临时字符串中，在下一次递归时判断是否满足条件；回到当前节点时，将该字母取出，放入下一个按键字母

## 完整代码实现：

```C++
class Solution {
private:
    // 将电话号码连键化成数组（数组下标即为按键号码）
    const string letterMap[10]={
        "", // 0
        "", // 1
        "abc", // 2
        "def", // 3
        "ghi", // 4
        "jkl", // 6
        "mno", // 7
        "pqrs", // 8
        "tuv", // 9
        "wxyz", // 9
    };

    vector<string>res;  // 创建全局变量数组存放所有结果
    string s;           // 创建全局变量字符串存放遍历到的字符，作为一组组合

public:
    // 回溯函数：
    // 传入参数：目标值（所输入的数字），遍历深度
    void backtracking(const string& digits,int index){
        // 终止条件： 当遍历深度与所要求的（输入数字）长度相同时，得到一组结果，放入结果数组中，并返回
        if(index==digits.size()){
            res.push_back(s);
            return;
        }

        // 将输入数字组合的每个字符转换成对应的数字
        int dig=digits[index]-'0';
        // 输入数字对应的按键，将其字符串放入临时变量中
        string letters=letterMap[dig];
        // 单层逻辑： 横向遍历放入临时对象的字符串，进行组合
        for(int i=0;i<letters.size();i++){
            // 先将临时对象中第一个字符放入组合中，开始回溯所有可能
            s.push_back(letters[i]);
            backtracking(digits,index+1);
            s.pop_back();
        }
    }

    vector<string> letterCombinations(string digits) {
        if(digits.size()==0) return res;

        backtracking(digits,0);

        return res;
    }
};
```

---

