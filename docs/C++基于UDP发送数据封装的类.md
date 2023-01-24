# C++基于UDP发送数据封装的类

前段时间工作过程中，前期讨论阶段需要将程序中获取的数据发送通过udp协议发送出去，但是由于条件不符讨论过程中不需要了，但我个人认为很有封装的意义。在这里基于项目背景浅浅实现一下吧。

* 发送数据名称：SSR
* 用户只需要自定义发送数据的协议即可（封装格式）

```cpp title="UdpSendSsr.h"
#ifndef _UDPSENDSSR_H_
#define _UDPSENDSSR_H_

#include <iostream>
#include <string>
#include <sys/types.h>
#include <arpa/inet.h>
#include <functional>


class UdpSendSsr{
public:
	UdpSendSsr() = delete;
	UdpSendSsr(std::string ip, int port):
			ip(ip), port(port){}
	~UdpSendSsr(){}

	void initUdpService();
	void startUdpService();

	void sendData(std::string &data);

public:
	uint8_t funcFlag = 0;
	std::function<std::string(std::string&, int)> handler;

private:
	std::string ip;
	int port = 0;
	int sockfd = 0;

	uint8_t startFlag = 0;
	struct sockaddr_in peer;
};


#endif /* _UDPSENDSSR_H_ */

```

```cpp title="UdpSendSsr.cpp"
#include "UdpSendSsr.h"
#include "UserProto.h"
#include <cstring>

void UdpSendSsr::initUdpService(){
	sockfd = socket(AF_INET, SOCK_DGRAM, 0);
	if(!sockfd){
		std::cerr << "create socket failed." << std::endl;
		return;
	}
	std::cout << "create socket succ." << std::endl;

	UserProto up;
	handler = up;
	this->funcFlag = 1;
}

void UdpSendSsr::startUdpService(){
	memset(&peer, 0, sizeof(peer));

	peer.sin_family = AF_INET;
	peer.sin_port = htons(port);
	peer.sin_addr.s_addr = inet_addr(ip.c_str());
}

void UdpSendSsr::sendData(std::string &data){
	if(!data.length()){
		std::cout << "data is nullotr." << std::endl;
		return;
	}
	
	if(funcFlag){
		std::string buf = handler(data, 1);
		sendto(sockfd, buf.c_str(), buf.size(), 0, 
				(struct sockaddr*)&peer, sizeof(peer));
		std::cout << "send ssr data over." << std::endl;
	}
}

```

以上的`UserProto`类实例化对象就是用户自动的协议类：

```cpp title="UserProto.h"
#ifndef _USERPROTO_H_
#define _USERPROTO_H_
#include <string>
#include <iostream>

class UserProto{
public:
    std::string operator()(std::string& data, int index);
};

#endif /* _USERPROTO_H_ */
```

```cpp title="UserProto.cpp"
#include "UserProto.h"

std::string UserProto::operator()(std::string& data, int index){
    std::string buf = "";
    if(!data.length()){
        std::cout << "exit" << std::endl;
        return buf;
    }
    uint8_t interfaceId = 0;
    switch(index){
        case 1:
            interfaceId = 1;
            buf.append((char*)&interfaceId, sizeof(uint8_t));
            buf.append(data);
        break;
        default:
        break;
    }
    
    std::cout << "pack data over" << std::endl;
    return buf;
}
```

