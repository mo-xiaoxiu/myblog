# vsomeip小记

关于SOME/IP协议的文章网络上已经很多了，在本篇文章不过多赘述。在这里主要是记录下自己在使用vsomeip过程中的一些小注意点，一方面是方便自己后续的查看和追溯，另一方面也是通过写文章这种输出方式达到加深印象的作用。

<br>

首先讲一下vsomeip为何物。vsomeip是一种专为汽车电子网络设计的开源中间件解决方案，基于SOME/IP协议（Scalable service-Oriented MiddlewarE over IP）实现。也是作为汽车SOA（Service-Oriented Architecture）架构的关键组件。

## vsomeip编译与安装

我使用的环境是Ubuntu 24.04.2，运行在VMware虚拟机上，在使用vsomeip之前我们需要先在本地安装一些依赖，包括编译工具：
```shell
sudo apt-get install libboost-system-dev libboost-thread-dev libboost-log-dev

sudo apt-get install asciidoc source-highlight doxygen graphviz

sudo apt-get install gcc g++ make
```

之后可以使用git的方式将源码克隆到本地：

```shell
git clone https://github.com/COVESA/vsomeip.git
```

然后我们就可以进行编译，首先进入到vsomeip文件夹中，然后执行以下指令：

```cpp
mkdir build
    
cd build
    
cmake ..

make
```

安装的话可以通过`make install`（需要root权限），如果有想要自定义的安装路径的话，需要在执行cmake的时候指定安装路径：

```shell
cmake -DCMAKE_INSTALL_PREFIX:PATH=$YOUR_PATH ..
make
sudo make install
```

更详细的编译安装指令可以查看`README.md`。

接下来可以使用examples文件夹下的`hello_world`相关程序来快速开始。

## 快速开始

如果我们成功安装了vsomeip的一些库和头文件，可以在如`/usr/local/lib`下或者自定义的安装路径下看到vsomeip的一系列产物，如`libvsomeip3-sd.so`等。当然，如果你想编译成静态库也是可以的，只需要在vsomeip文件夹下的`CMakeLists.txt`中将`add_library`的`SHARED`改成`STATIC`，但是代价是编译出来的静态库很大，还是考虑使用动态库吧。

我们可以利用vsomeip下的examples文件夹下的程序来验证SOME/IP相关的功能。快速开始的方法可以先进入到`examples`，进入到`hello_world`，再创建一个`build`文件夹，进入到build里边，执行`cmake ..` ，再`make`一下，就可以得到hello_world相关的可执行文件。在执行hello_world相关程序之前，我们需要：

* 修改json配置文件：json配置文件的路径在examples下的hello_world下，名为`helloworld-local.json`

  * 修改内容：将json文件中的`unicast`字段的ip地址改为localhost，即127.0.0.1，方便我们在运行hello_world相关程序的时候使用这个ip作为通信端点
  * 为了方便后续使用，直接将修改之后的json文件复制一份到build文件夹下

* 修改hello_world程序：主要是直接在程序中设置环境变量，方便运行

  * 修改`hello_world_client_main.cpp`：

    ```cpp
    int main(int argc, char **argv)
    {
        (void)argc;
        (void)argv;
    
        //设置环境变量
        setenv("VSOMEIP_APPLICATION_NAME", "hello_world_client", 1);
        setenv("VSOMEIP_CONFIGURATION", "./helloword-local.json", 1);
    
        hello_world_client hw_cl;
        ...
    }
    ```

  * 修改`hello_world_service_main.cpp`:

    ```cpp
    int main(int argc, char **argv)
    {
        (void)argc;
        (void)argv;
    
        setenv("VSOMEIP_APPLICATION_NAME", "hello_world_service", 1);
        setenv("VSOMEIP_CONFIGURATION", "./helloword-local.json", 1);
    
        hello_world_service hw_srv;
        ...
    }
    ```

  * 对于`hello_world_service`来说，我想让他一直运行着，我们可以这样修改：

    ```cpp
    //hello_world_service.hpp
    void stop()
        {
            ...
            // shutdown the application -->将stop给注释掉
            //app_->stop();
        }
    ```

除了以上修改程序和移动json文件的方式外，还可以使用hello_world下面的`README.md`给我们提供的方法，即使用export这种导入环境变量的方式：

```
HOST1:
VSOMEIP_CONFIGURATION=../helloworld-local.json \
VSOMEIP_APPLICATION_NAME=hello_world_service \
./hello_world_service

HOST1:
VSOMEIP_CONFIGURATION=../helloworld-local.json \
VSOMEIP_APPLICATION_NAME=hello_world_client \
./hello_world_client
```

做完以上操作之后（如果像我上面改代码的话，需要重新在build下面make一下），可以分别开启两个终端，分别执行`./hello_world_service`和`./hello_world_client`：

*./hello_world_service*

```shell
zjp@zjp-VMware-Virtual-Platform:~/git_pro/someip/vsomeip/examples/hello_world/build$ ./hello_world_service
2025-03-04 16:50:41.926145 hello_world_service [info] Using configuration file: "./helloworld-local.json".
2025-03-04 16:50:41.926685 hello_world_service [info] Parsed vsomeip configuration in 0ms
2025-03-04 16:50:41.926754 hello_world_service [info] Configuration module loaded.
2025-03-04 16:50:41.926820 hello_world_service [info] Security disabled!
2025-03-04 16:50:41.926851 hello_world_service [info] Initializing vsomeip (3.5.4) application "hello_world_service".
2025-03-04 16:50:41.927727 hello_world_service [info] Instantiating routing manager [Host].
2025-03-04 16:50:41.928534 hello_world_service [info] create_routing_root: Routing root @ /tmp/vsomeip-0
2025-03-04 16:50:41.929534 hello_world_service [info] Application(hello_world_service, 4444) is initialized (11, 100).
2025-03-04 16:50:41.929791 hello_world_service [info] Starting vsomeip application "hello_world_service" (4444) using 2 threads I/O nice 0
2025-03-04 16:50:41.930260 hello_world_service [debug] Thread created. Number of active threads for hello_world_service : 1
2025-03-04 16:50:41.931267 hello_world_service [info] Client [4444] routes unicast:127.0.0.1, netmask:255.255.255.0
2025-03-04 16:50:41.932781 hello_world_service [info] Watchdog is disabled!
2025-03-04 16:50:41.930414 hello_world_service [info] main dispatch thread id from application: 4444 (hello_world_service) is: 7a96b39fd6c0 TID: 22843
2025-03-04 16:50:41.933352 hello_world_service [info] rmi::offer_service added service: 1111 to pending_sd_offers_.size = 1
2025-03-04 16:50:41.933442 hello_world_service [info] routing_manager_stub::on_offer_service: ON_OFFER_SERVICE(4444): [1111.2222:0.0]
2025-03-04 16:50:41.934366 hello_world_service [info] create_local_server: Listening @ /tmp/vsomeip-4444
2025-03-04 16:50:41.935125 hello_world_service [info] OFFER(4444): [1111.2222:0.0] (true)
2025-03-04 16:50:41.934896 hello_world_service [info] io thread id from application: 4444 (hello_world_service) is: 7a96b55b3b80 TID: 22840
2025-03-04 16:50:41.937241 hello_world_service [info] vSomeIP 3.5.4 | (default)
2025-03-04 16:50:41.935243 hello_world_service [info] io thread id from application: 4444 (hello_world_service) is: 7a96b19f96c0 TID: 22847
2025-03-04 16:50:41.937753 hello_world_service [warning] Network interface "lo" state changed: up
2025-03-04 16:50:41.937898 hello_world_service [info] Service Discovery disabled. Using static routing information.
2025-03-04 16:50:41.938316 hello_world_service [info] rmi::start_ip_routing: clear pending_sd_offers_
2025-03-04 16:50:41.938395 hello_world_service [info] SOME/IP routing ready.
2025-03-04 16:50:41.942275 hello_world_service [info] shutdown thread id from application: 4444 (hello_world_service) is: 7a96b31fc6c0 TID: 22844
2025-03-04 16:50:45.577659 hello_world_service [info] Application/Client 5555 is registering.
2025-03-04 16:50:45.579943 hello_world_service [info] emb::find_or_create_local: create_client 5555
2025-03-04 16:50:45.580307 hello_world_service [info] Client [4444] is connecting to [5555] at /tmp/vsomeip-5555 endpoint > 0x7a9698000e50
2025-03-04 16:50:45.587647 hello_world_service [info] REGISTERED_ACK(5555)
2025-03-04 16:50:45.693632 hello_world_service [info] REQUEST(5555): [1111.2222:255.4294967295]
2025-03-04 16:50:45.711093 hello_world_service [info] RELEASE(5555): [1111.2222]
2025-03-04 16:50:45.712754 hello_world_service [info] Application/Client 5555 is deregistering.
2025-03-04 16:50:45.714780 hello_world_service [info] emb::remove_local: client 5555
2025-03-04 16:50:45.719187 hello_world_service [info] cei::shutdown_and_close_socket_unlocked: not recreating socket  endpoint > 0x7a9698000e50 socket state > 0
2025-03-04 16:50:45.719379 hello_world_service [info] local_uds_client_endpoint_impl::receive_cbk Error: Operation canceled
2025-03-04 16:50:45.719560 hello_world_service [info] Client [4444] is closing connection to [5555] endpoint > 0x7a9698000e50
2025-03-04 16:50:51.951734 hello_world_service [info] vSomeIP 3.5.4 | (default)
```

*hello_world_client*

```shell
zjp@zjp-VMware-Virtual-Platform:~/git_pro/someip/vsomeip/examples/hello_world/build$ ./hello_world_client
2025-03-04 16:52:37.340813 hello_world_client [info] Using configuration file: "./helloworld-local.json".
2025-03-04 16:52:37.341289 hello_world_client [info] Parsed vsomeip configuration in 0ms
2025-03-04 16:52:37.341356 hello_world_client [info] Configuration module loaded.
2025-03-04 16:52:37.341422 hello_world_client [info] Security disabled!
2025-03-04 16:52:37.341450 hello_world_client [info] Initializing vsomeip (3.5.4) application "hello_world_client".
2025-03-04 16:52:37.341487 hello_world_client [info] Instantiating routing manager [Proxy].
2025-03-04 16:52:37.341711 hello_world_client [info] Client [5555] is connecting to [0] at /tmp/vsomeip-0 endpoint > 0x5c9bbd495a80
2025-03-04 16:52:37.341790 hello_world_client [info] Application(hello_world_client, 5555) is initialized (11, 100).
2025-03-04 16:52:37.341981 hello_world_client [info] Starting vsomeip application "hello_world_client" (5555) using 2 threads I/O nice 0
2025-03-04 16:52:37.342742 hello_world_client [debug] Thread created. Number of active threads for hello_world_client : 1
2025-03-04 16:52:37.343048 hello_world_client [info] main dispatch thread id from application: 5555 (hello_world_client) is: 7327027ff6c0 TID: 23086
2025-03-04 16:52:37.344029 hello_world_client [info] io thread id from application: 5555 (hello_world_client) is: 7327032feb80 TID: 23085
2025-03-04 16:52:37.344160 hello_world_client [info] assign_client: (5555:hello_world_client)
2025-03-04 16:52:37.344206 hello_world_client [debug] rmc::assign_client: state_ change 1 -> 3
2025-03-04 16:52:37.345818 hello_world_client [info] shutdown thread id from application: 5555 (hello_world_client) is: 732701ffe6c0 TID: 23087
2025-03-04 16:52:37.346316 hello_world_client [info] io thread id from application: 5555 (hello_world_client) is: 7327017fd6c0 TID: 23088
2025-03-04 16:52:37.352238 hello_world_client [debug] rmc::on_client_assign_ack: state_ change 3 -> 4
2025-03-04 16:52:37.353493 hello_world_client [info] create_local_server: Listening @ /tmp/vsomeip-5555
2025-03-04 16:52:37.353713 hello_world_client [info] Client 5555 (hello_world_client) successfully connected to routing  ~> registering..
2025-03-04 16:52:37.353812 hello_world_client [info] Client 5555 Registering to routing manager @ vsomeip-0
2025-03-04 16:52:37.353898 hello_world_client [debug] rmc::register_application: state_ change 4 -> 2
2025-03-04 16:52:37.362533 hello_world_client [info] Application/Client 5555 (hello_world_client) is registered.
2025-03-04 16:52:37.364639 hello_world_client [debug] rmc::on_routing_info: state_ change 0 -> 0
2025-03-04 16:52:37.481594 hello_world_client [info] ON_AVAILABLE(5555): [1111.2222:0.0]
Sending: World
2025-03-04 16:52:37.482568 hello_world_client [info] emb::find_or_create_local: create_client 4444
2025-03-04 16:52:37.482981 hello_world_client [info] Client [5555] is connecting to [4444] at /tmp/vsomeip-4444 endpoint > 0x7326fc0015b0
Received: Hello World
2025-03-04 16:52:37.490329 hello_world_client [info] Stopping vsomeip application "hello_world_client" (5555).
2025-03-04 16:52:37.496884 hello_world_client [info] Application/Client 5555 (hello_world_client) is deregistered.
2025-03-04 16:52:37.498031 hello_world_client [debug] rmc::on_routing_info: state_ change 0 -> 1
2025-03-04 16:52:37.498534 hello_world_client [info] cei::shutdown_and_close_socket_unlocked: not recreating socket  endpoint > 0x5c9bbd495a80 socket state > 0
2025-03-04 16:52:37.499550 hello_world_client [info] emb::remove_local: client 4444
2025-03-04 16:52:37.500030 hello_world_client [info] cei::shutdown_and_close_socket_unlocked: not recreating socket  endpoint > 0x7326fc0015b0 socket state > 0
2025-03-04 16:52:37.500602 hello_world_client [info] local_uds_client_endpoint_impl::receive_cbk Error: Operation canceled
2025-03-04 16:52:37.499035 hello_world_client [info] local_uds_client_endpoint_impl::receive_cbk Error: Operation canceled
2025-03-04 16:52:37.500913 hello_world_client [info] Client [5555] is closing connection to [4444] endpoint > 0x7326fc0015b0
2025-03-04 16:52:37.498578 hello_world_client [warning] BLOCKING CALL MESSAGE(5555): [1111.2222.3333:0001]
2025-03-04 16:52:38.498092 hello_world_client [debug] Thread destroyed. Number of active threads for hello_world_client : 0
2025-03-04 16:52:38.498584 hello_world_client [info] Detached thread with id: 7327027ff6c0 exited successfully; Number of threads still active : 0
```

## offer和subscribe、request和response

以上只是在本地通信的小demo。如果想要进一步验证SOME/IP的offer和subscribe的简单过程，可以在`examples`下面查看`notify_sample.cpp`和`subscribe_sample.cpp`，如果想要运行下试试可以到`vsomeip`文件夹下面的`build`的`examples`下面，直接`make`一下就可以生成可执行文件了

同样的，需要修改对应的json配置文件：

* 我这边选择的方式还是在示例程序中通过`setenv`设置环境变量，避免每次重复设置
* 修改json配置文件：
  * json文件路径：vsomeip文件夹下`config`下，`vsomeip-local.json`
  * 由于我这边想要跨主机通信，索性再开了个虚拟机，将两个虚拟机都设置成桥接模式，连接到我的WLAN上，这样相当于我的windows、虚拟机1和虚拟机2都在同一个网段，并各自分配有一个IP地址，其实也可以直接将虚拟机1和虚拟机2桥接起来，不用经过WLAN等其他物理网卡，这样可以给虚拟机1和虚拟机2各自分配一个本地的ip地址，等后续有空我更新文章的时候整一下，并抓取数据包在后续介绍；所以现在我需要在两台虚拟机上都布置一下vsomeip的环境，并修改对应的json配置文件。在虚拟机1上，将`vsomeip-local.json`的`unicast`字段的ip地址改为虚拟机1的`ens33`（取决于桥接的虚拟网卡）IP地址；虚拟机2同理

接着同样开启两个终端分别执行`notify_sample`和`subscribe_sample`

`request`和`response`的操作方式也是一样。

---



> 世界上没有一条道路是重复的，也没有一个人生是能够替代的。
>
> <p align="right">--余华《活着》</p>