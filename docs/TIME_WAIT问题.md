# TIME_WAIT问题汇总

## TIME_WAIT
![TIME_WAIT](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/TIME_WAIT.drawio.png)

* 主动关闭方才有TIME_WAIT状态
* MSL 指的是 TCP 协议中任何报文在网络上最大的生存时间，任何超过这个时间的数据都将被丢弃
* MSL 是由网络层的 IP 包中的 TTL 来保证的，TTL 是 IP 头部的一个字段，用于设置一个数据报可经过的路由器的数量上限。报文每经过一次路由器的转发，IP 头部的 TTL 字段就会减 1，减到 0 时报文就被丢弃
    * MSL 的单位是时间，而 TTL 是经过路由跳数
    * MSL 应该要大于等于 TTL 消耗为 0 的时间，以确保报文已被自然消亡


## TIME_WAIT时间过短或者没有
* 防止历史连接的数据被相同四元组连接错误接收

![TIME_WAIT_toShort_1](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/TIME_WAIT_ToShort.drawio.png)

* 保证被动关闭一方能被正常关闭

![TIME_WAIT_toShort_2](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/TIME_WAIT_ToShort_2.drawio.png)

## TIME_WAIT时间过长
* 内存资源有限，占用内存资源
* 长时间占用端口号，消耗资源

## 既然打开 net.ipv4.tcp_tw_reuse 参数可以快速复用处于 TIME_WAIT 状态的 TCP 连接，那为什么 Linux 默认是关闭状态呢？

### 何为tcp_tw_reuse
用于快速回收tcp连接的Linux参数选项。如果开启此选项，客户端在发起`connect()`调用的时候，内核会随机找一个TIME_WAIT状态时间超过**1秒**的连接作为新的连接。**只适用于发起连接的一方**

### 何为tcp_tw_recycle
**快速回收处于TIME_WAIT状态的连接，此参数在NAT网络下是不安全的**

#### NAT下的tcp_tw_recycle
使得`tcp_tw_reuse`和`tcp_tw_recycle`生效的前提条件：

打开TCP时间戳 --> `tcp_timestamps = 1`

**同时开启`tcp_tw_recycle`和`tcp_timestamps`，会开启per_host的PAWS机制**


```markdown title="PAWS"
**PAWS机制：**

* 作用：防止TCP包中的序列号回绕

    * TCP序列号是有限的，**一共32bit，所以上限是4GB；递增，溢出之后回绕到0再次递增...**
    * 问题就是延迟的数据包中而重传的序列号和发生回绕的序列号相同的话，就会造成传输错误

* PAWS机制如何解决：

    * TCP包上带上时间戳，双方维护一次最近的的时间戳，每收到一个数据包都会跟最近的时间戳作比较。**如果时间戳不是递增的则会丢弃这个数据包**

* per_host的PAWS机制(同时开启recycle和timestamps)

    * per_host是对**对端IP做PAWS检查**，而非对`IP + port`四元组做PAWS检查。
```


若客户端使用NAT网络环境，则客户端的每一台机器在通过NAT网关之后都会是**相同的IP地址**

**“当客户端 A 通过 NAT 网关和服务器建立 TCP 连接，然后服务器主动关闭并且快速回收 TIME-WAIT 状态的连接后，客户端 B 也通过 NAT 网关和服务器建立 TCP 连接，注意客户端 A  和 客户端 B 因为经过相同的 NAT 网关，所以是用相同的 IP 地址与服务端建立 TCP 连接，如果客户端 B 的 timestamp 比 客户端 A 的 timestamp 小，那么由于服务端的 per-host 的 PAWS 机制的作用，服务端就会丢弃客户端主机 B 发来的 SYN 包”** ------摘自公众号小林coding文章


### 为何tcp_tw_reuse默认关闭

#### RST报文时间戳即使过期仍可接受

```cpp title="验证接收到的 TCP 报文是否合格的函数"
static bool tcp_validate_incoming(struct sock *sk, struct sk_buff *skb, const struct tcphdr *th, int syn_inerr)
{
    struct tcp_sock *tp = tcp_sk(sk);

    /* RFC1323: H1. Apply PAWS check first. */
    if (tcp_fast_parse_options(sock_net(sk), skb, th, tp) &&
        tp->rx_opt.saw_tstamp &&
        tcp_paws_discard(sk, skb)) { //tcp_paws_discard返回true，则说明是历史报文
        if (!th->rst) { //在丢弃之前会判断是否为RST报文
            ....
            goto discard;
        }
        /* Reset is accepted even if it did not pass PAWS. */
    }
```

**“快速复用 TIME_WAIT 状态的端口，导致新连接可能被回绕序列号的 RST 报文断开了，而如果不跳过 TIME_WAIT 状态，而是停留 2MSL 时长，那么这个 RST 报文就不会出现下一个新的连接“** ------摘自公众号小林coding文章

#### 被动关闭连接一方不能正常关闭连接

如果开启`tcp_tw_reuse`快速复用连接，如果之前第四次挥手的ACK报文丢失，则服务端（被动关闭）重传的时候客户端（主动关闭）已经是复用连接的状态，所以回复RST报文导致服务端异常关闭





*更新中......*

