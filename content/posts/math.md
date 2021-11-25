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

# 数学+模拟

## 打乱数组

*原题链接：https://leetcode-cn.com/problems/shuffle-an-array/*

```
给你一个整数数组 nums ，设计算法来打乱一个没有重复元素的数组。

实现 Solution class:

Solution(int[] nums) 使用整数数组 nums 初始化对象
int[] reset() 重设数组到它的初始状态并返回
int[] shuffle() 返回数组随机打乱后的结果
 

示例：

输入
["Solution", "shuffle", "reset", "shuffle"]
[[[1, 2, 3]], [], [], []]
输出
[null, [3, 1, 2], [1, 2, 3], [1, 3, 2]]

解释
Solution solution = new Solution([1, 2, 3]);
solution.shuffle();    // 打乱数组 [1,2,3] 并返回结果。任何 [1,2,3]的排列返回的概率应该相同。例如，返回 [3, 1, 2]
solution.reset();      // 重设数组到它的初始状态 [1, 2, 3] 。返回 [1, 2, 3]
solution.shuffle();    // 随机返回数组 [1, 2, 3] 打乱后的结果。例如，返回 [1, 3, 2]
 

提示：

1 <= nums.length <= 200
-106 <= nums[i] <= 106
nums 中的所有元素都是 唯一的
最多可以调用 5 * 104 次 reset 和 shuffle
```

**模拟：**
这个题目最主要的功能是完成对数组随机排列的实现
要想使数组中每一个元素在其位置出现的概率相同，可以从左往右开始，在每个位置处，用其后的元素（随机选取一个）和该位置元素进行交换
**概率：**

* 第一次在某个位置，在数组中随机选取一个数的概率：1/n
* 在剩下的元素中，选择另一个元素与其交换：（1/n）*（ n - 1 ）*（1/（n - 1））
* 所以概率为 1/n
  而对于第二个位置，我们要考虑这个元素没有出现在之前的选择中，然后是从剩下n-1个元素中随机选择一个，所以任意一个元素出现的概率是 **((n-1)/n) * (1/(n-1)) = 1/n **




```C++
class Solution {
public:
    Solution(vector<int>& nums) {
        this->num = nums;
        original = num;
    }
    
    vector<int> reset() {
        return original;
    }
    
    vector<int> shuffle() {
        for(int i=0;i<num.size();i++) {
            // 从左往右遍历：
            // 当前位置值 与 后面位置的随机位置值交换
            int randNum = i + rand()%(num.size() - i);
            int tmp = num[i];
            num[i] = num[randNum];
            num[randNum] = tmp;
        }
        return num;
    }

private:
    vector<int> num; // 打乱之后的数组
    vector<int> original; // 打乱之前的数组：保存打乱之前的数组
};
```

---

# 字符串 + 模拟

## 从英文重建数字

*原题链接：https://leetcode-cn.com/problems/reconstruct-original-digits-from-english/*

```
给你一个字符串 s ，其中包含字母顺序打乱的用英文单词表示的若干数字（0-9）。按 升序 返回原始的数字。

 

示例 1：

输入：s = "owoztneoer"
输出："012"
示例 2：

输入：s = "fviefuro"
输出："45"
 

提示：

1 <= s.length <= 105
s[i] 为 ["e","g","f","i","h","o","n","s","r","u","t","w","v","x","z"] 这些字符之一
s 保证是一个符合题目要求的字符串

```

**解题思路**
首先想到的是通过一个哈希表将所有的字符放进去，然后根据数字0~9的英文单词遍历哈希表
这样直接的想法看似简单实际颇为复杂：

* 0~9数字单词的字母都不止一个
* 0~9单词中有相同的字母
* 如果单纯遍历哈希表，既要再遍历过程中拼凑单词，又要对使用过的字母进行计数，确实比较复杂

如果遍历整个单词比较麻烦，那只遍历单词中的一个字母呢？靠着一个字母可以单独标志一个单词吗？

```
1 -- one
2 -- two -- w
3 -- three
4 -- four -- u
5 -- five
6 -- six -- x
7 -- seven
8 -- eight -- g
9 -- nine
0 -- zero -- z
```

由以上可以得出，数字0、2、4、6、8，是可以使用唯一的单词进行标志的。那么其他数字呢？由相同的字母就不可以了吗？
其实可以通过已知的数字求出未知的数字

上述中，可以凭着唯一标志的字母得出对应数字的个数
接着可以得到以下列表

```
1 2 4 0 -- o -- 1     
2 3 8 -- t -- 3       
6 7 --s -- 7    
4 5 -- f --5       
5 6 8 9 -- i -- 9
```


*解释：可以由已知的数字2、4、0的个数，根据字母o出现的频率相减得出数字1的个数；可以由已知的数字2、8的个数，根据字母t出现的频率相减得出数字3的个数......以此类推*

这样就可以得到所有数字的个数了

**算法实现：**

* 使用哈希表统计字符串中的字符及其出现次数
* 利用一个数组，下标对应的是0~9数字，下标对应的数组位置存放的是数字出现的频率
* 数组先根据哈希表统计数字单词中可以使用唯一字母标志的数字，之后根据已知的数字求未知的数字

```C++
class Solution {
public:
    string originalDigits(string s) {
        unordered_map<char, int> map;
        for(auto& c: s) {
            map[c]++;
        }

        vector<int> vec(10);
        // 先求唯一字母可以标志的
        vec[0] = map['z'];
        vec[2] = map['w'];
        vec[4] = map['u'];
        vec[6] = map['x'];
        vec[8] = map['g'];

        // 根据已知的求未知的数字
        vec[1] = map['o'] - vec[2] - vec[4] - vec[0];
        vec[3] = map['t'] - vec[2] - vec[8];
        vec[7] = map['s'] - vec[6];
        vec[5] = map['f'] - vec[4];
        vec[9] = map['i'] - vec[5] - vec[6] - vec[8];


        // 转换为字符串
        string res;
        for(int i=0; i<10; i++) {
            for(int j=0; j<vec[i]; j++) {
                res += char(i + '0');
            }
        }
        return res;
    }
};

```

---

# 数学 + 进制

## 可怜的小猪

*原题链接：https://leetcode-cn.com/problems/poor-pigs/submissions/*

```
有 buckets 桶液体，其中 正好 有一桶含有毒药，其余装的都是水。它们从外观看起来都一样。为了弄清楚哪只水桶含有毒药，你可以喂一些猪喝，通过观察猪是否会死进行判断。不幸的是，你只有 minutesToTest 分钟时间来确定哪桶液体是有毒的。

喂猪的规则如下：

选择若干活猪进行喂养
可以允许小猪同时饮用任意数量的桶中的水，并且该过程不需要时间。
小猪喝完水后，必须有 minutesToDie 分钟的冷却时间。在这段时间里，你只能观察，而不允许继续喂猪。
过了 minutesToDie 分钟后，所有喝到毒药的猪都会死去，其他所有猪都会活下来。
重复这一过程，直到时间用完。
给你桶的数目 buckets ，minutesToDie 和 minutesToTest ，返回在规定时间内判断哪个桶有毒所需的 最小 猪数。

 

示例 1：

输入：buckets = 1000, minutesToDie = 15, minutesToTest = 60
输出：5
示例 2：

输入：buckets = 4, minutesToDie = 15, minutesToTest = 15
输出：2
示例 3：

输入：buckets = 4, minutesToDie = 15, minutesToTest = 30
输出：2
 

提示：

1 <= buckets <= 1000
1 <= minutesToDie <= minutesToTest <= 100

```

**联想：**

* 1000瓶水中有若干瓶毒药，需要多少小白鼠才能测得出来？
  *答案：需要10只小白鼠。将1000瓶水利用二进制标号，可以使用`2^10=1024`来表示这1000瓶水，所以二进制数位数一共有10位，让10只小白鼠分别按列喝这标号10位的二进制的1000瓶水，某只小白鼠牺牲说明1000瓶水中毒药的二进制某一位为1（1表示喝了之后会g， 0表示不会）*，依次得出

上面一只小白鼠可以携带的信息：2（非死即活）
这里一只小猪可以携带的信息：5

*原因：*

在测试时间范围内

1. 第一次：喝第一瓶，完
2. 第二次：喝第二瓶，完
3. 第三次：喝第三瓶，完
4. 第四次：喝第四瓶，完
5. 四次喝完都没事：第五瓶是毒药

所以可以携带5种状态信息
**所以60分钟内，每次测试时间为15分钟，一只小猪可以得到5种情况**

结合以上的**联想**，可以得到：
*`5^x=1000*  -->  *log5(1000)=x`*
`x=5`
所以需要5只小猪

**由此可得到：**

`logt(buckets)=result`
`t=testTime/dieTime+1`

```C++
class Solution {
public:
    int poorPigs(int buckets, int minutesToDie, int minutesToTest) {
        int tastTime = minutesToTest / minutesToDie;
        int looks = tastTime + 1;
        // ceil 是向上取整
        return ceil(log(buckets) / log(looks));
    }
};
```

---

