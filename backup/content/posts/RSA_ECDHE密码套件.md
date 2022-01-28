---
title: "RSA_ECDHE密码套件"
date: 2021-09-23T10:05:27+08:00
draft: true
---

# 补充：密码套件

在文章[RSA_TCP三次握手](https://myblog-gamma-olive.vercel.app/posts/rsa_tcp%E4%B8%89%E6%AC%A1%E6%8F%A1%E6%89%8B/ "RSA_TCP三次握手 // ZJP")以及[HTTPS_ECDHE握手解析](https://myblog-gamma-olive.vercel.app/posts/https_ecdhe%E6%8F%A1%E6%89%8B%E8%A7%A3%E6%9E%90/ "HTTPS_ECDHE握手解析 // ZJP")中，总结到一个地方：

* TLS握手的时候，客户端发送的**`Client Hello`**消息中有可供选择的密码套件列表以及服务端选择的密码套件
* *问题：密码套件是什么样子的？是由什么组成的？*

## RSA算法

首先来看看RSA算法中握手过程的密码套件：

在TLS第二次握手中，服务端确认的密码套件：“Cipher Suite: TLS_RSA_WITH_AES_128_GCM_SHA256”

*基本的形式：* **密钥交换算法 + 签名算法 + 对称加密算法 + 摘要算法**

一般**WITH**前面有两个单词，**第一个单词是约定密钥交换算法，第二个单词是约定的证书验证算法**

```
Cipher Suite: TLS_RSA_WITH_AES_128_GCM_SHA256
```

*(TLS不算)*

* WITH前面只有一个单词`RSA`：**握手时的密钥交换算法和签名算法都是RSA**
* **握手后通信使用`AES`对称算法，密钥长度128位，分组模式是GCM**
* **摘要算法：SHA384 用于消息认证和产生随机数**

---

## ECDHE算法

再来看看ECDHE算法握手过程的密码套件

在服务端确认的的信息中，选择的密码套件：“Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384”

```
Cipher Suite: TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
```

* **密钥交换算法**：ECDHE
* **签名算法**：RSA
* **握手后通信的对称加密算法**：AES；密钥长度：256；分组模式：GCM
* **摘要算法**：SHA384

---

## 总结

**基本形式：**

* 密钥交换算法
* 签名算法
* “WITH”
* 握手后通信的对称加密算法；密钥长度；分组模式
* 摘要算法



