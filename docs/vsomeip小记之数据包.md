# vsomeip小记：Service discovery

上一篇文章介绍了vsomeip的快速开始的一些基本操作，接下来我们可以看下具体各个报文是怎么发送和接收的。先说一下SOME/IP-SD报文，即服务发现报文。

## offer

SOME/IP通信过程中，分为服务端和客户端，各端之间通信的数据我们抽象为服务。举个例子，设备节点1现在能给整车某个局域网内提供定位数据，于是设备节点1将定位数据抽象为一种服务，并给它定了服务id，设备节点1在满足某种条件（比如说定上位）之后开始向这个局域网内发送通知消息，告诉局域网内的其他节点：“我有定位数据，谁要？”，这种通知方式就叫做offer。但是offer本身不包含服务的数据，比如在这个例子中，offer是不包含定位数据的，它只是一个通知，是为了其他节点能发现它提供了这个服务（如果其他节点关注这个服务的话），比如设备节点2，在这个局域网内收到了设备节点1发的offer报文，它就知道：“原来是你有这个数据，好好好！”。

那发送offer报文需要遵循什么样的数据格式呢？这块我们可以看AUTOSAR的规范，在此不做赘述。我们可以从下面的报文截图看到`notify_sample`发出的offer报文内容：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20250304190428.png)

* SOME/IP部分
  * Service ID：0xffff 固定值
  * Method ID：0x8100固定值
* SOME/IP Service Discovery部分
  * Flags
    * Reboot：会话ID是否需要回滚。可以理解为每次接发数据都是一次会话。
    * Unicast：支持单播，和本身这个报文是不是单播没有关系
  * Entries Array
    * Service ID 0x1234：每个服务对应的标识符
    * Instance ID 0x5678：每个服务对应的通信实例，概念类似于对象
    * Type 0x01：表示offer服务或停止offer服务，停止offer服务就是告诉这个局域网内的其他节点“我这没有xxx数据了哈”；怎么区分是offer还是停止offer呢？看下面的ttl就知道了
    * Index 1：表示该offer服务的第几个option数组；option数组里边包含了描述这个服务相关的一些信息，包括提供服务对应的通信端点信息，如ip地址和端口等；这里表示第一个option
    * Index 2：和Index 1一样，这里表示是第二个option数组
    * Number of Opts 1：0x1表示第一个option数组里边有多少option，这里说明的是第一个option数组里边只有一个option
    * Number of Opts 2：0x0表示第二个option数组里边没有option
    * Major Version：主版本号
    * TTL：对应上面所说的ttl，0就是停止offer报文，不为0就是offer报文，也表示报文在网络中的转发次数
    * Minor Version：次版本号
  * Options Array：前面的option数组里边的具体内容，这里表示提供服务的通信实例的IP地址和端口号，以及服务的通信是UDP通信方式等

注意，offer报文和停止offer报文（stopoffer报文）本身是UDP的。

<br>

offer报文的格式内容有了，那应该按照遵循什么样的规则发送呢？这里offer报文作为服务端提供服务，在发送时需要遵循三个阶段发送：

* 初始阶段：顾名思义，服务在初始化阶段，此时如果收到别的节点查找服务的通知（这个在后面会有，叫做find）是不理会的。就像饭店在准备开门但是还没开门的时间段。在初始阶段结束后，服务端会发送一帧offer
* 重复阶段：此时饭店正式开张，需要不断向外宣告本店已开张的消息，此时会以2的n次幂乘以重复阶段基准时间的时间间隔发送offer，一般是总共发3~4次，看具体需要配置，然后进入下一阶段，即主阶段；在重复阶段如果收到别的节点发送的find是需要回复的，就是要回复一帧单播的offer，之后立刻进入主阶段，回复的时延是可配置的；如果收到的是订阅报文，就是相当于人家知道你开张了直接来向你点餐，那么我们也需要回复一个单播的订阅ack作为响应；订阅报文后面会说
* 主阶段：经过重复阶段之后饭店也就进入正常运营阶段，需要周期性的宣告饭店开张，以防后面来的客户不知道这回事；需要注意，一般情况下，重复阶段报文发完了之后是要经过一个完整的offer周期的（这里的offer周期指的是主阶段发送offer的周期）再进入主阶段的，但对于vsomeip来说有一种情况例外，就是如果识别到重复阶段的最后一帧报文发送的时间间隔是要小于在主阶段周期的一半的话，就直接进入主阶段；怎么理解呢？看下面这张图就可以很好的理解。

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20250305144409.png)

这是正常情况下：初始阶段完了之后进入重复阶段，假设重复阶段的最后一帧报文发送的时间间隔小于在主阶段周期的一半，则直接进入主阶段，后面是等待一个主阶段offer周期之后发的offer报文。

对于主阶段的offer周期比重复阶段最后一帧时间间隔的一半要短的情况，这样处理可以缩短进入主阶段的时间。

否则要多等一个主阶段offer周期才真正进入主阶段，如下：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20250305144517.png)

给大家看下按照autorsar规范的正常报文：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/image-20250304231919315.png)

<br>

主阶段收到find或者订阅报文的回复情况和重复阶段一样。

<br>

## find

有服务端的三阶段，那作为获取服务的客户端也应有这三个阶段：

* 初始阶段：在这个阶段如果收到服务端的offer，则直接进入主阶段；否则超时就发送一帧find报文进入重复阶段
* 重复阶段：发送的规律和offer的重复阶段是一样的，就是2的n次幂间隔发送，n也是可配置的；如果在这个阶段收到offer或者stopoffer报文，直接进入主阶段；否则超时了也进入主阶段
* 主阶段：注意，这个阶段不会周期报文的，如果没有收到服务端发送offer或stopoffer，是不会发送订阅或取消订阅的，只有收到服务端发送的offer或者stopoffer才会对应发送订阅或者取消订阅的

find报文也是基于UDP的。

我们来看下find报文的内容：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20250305114224.png)

大家可以对照着前面的关键字段看一下，区别在于Type字段是0x00，表示是find报文类型。可以看到发送的周期遵循的规则和我们上面说的一致，主阶段是不会周期发送find报文的。

<br>

## subscribe/subscribeAck

订阅和订阅响应ack前面提到过，是在客户端收到服务端发送的offer报文后，知道对方提供了本端关注的服务，向服务端发送订阅表示后续要服务端遵循一定的规则向客户端发送服务数据。

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20250305115654.png)

下面说一下值得关注的点：

* Type：0x06表示订阅或停止订阅，区分订阅和停止订阅还是在下面ttl这个字段，ttl不为0就是订阅，否则就是停止订阅
* 订阅报文订阅的单元是事件组，一个事件组可以包含多个事件，每一个事件对应这一种具体的服务数据；打个比方，服务端提供定位数据这项服务，但是定位数据分为多种，比如经度纬度等等，服务端就可以把经度纬度等具体的定位数据抽象为一个事件，并且给他定义行为（这个涉及到SOME/IP服务的通信方式，这里简单说明下，就是获取服务数据的方式，比如get的方式获取，还是set的方式设置，是要求客户端发送请求之后服务端需要立刻响应，还是服务端不需要等等）

接下来看下subscribeack报文，subscribeAck报文的Type是0x07：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20250305125425.png)

<br>

## vsomeip service discovery的问题

不知道有没有小伙伴在一开始试验`notify_sample`的时候，抓取的数据包是这样的：

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20250305130917.png)

前提：配置重复阶段的基准周期是200ms，重复阶段最大重复次数是3，主阶段offer周期是2s

问题：第一帧是初始阶段完成之后的offer，后面间隔200ms、400ms、800ms、1.6s的offer分别是重复阶段2的0次方 * 200ms、2的1次方 * 200ms、2的2次方 * 200ms、2的3次方乘以200ms，这里重复阶段最后一帧时间间隔是1.6s，主阶段offer周期的一半是1s，1 < 1.6按道理说是直接进入主阶段，后面都是以主阶段offer周期来发送offer，可是按照上面报文情况进入主阶段后，间隔了大约2s9的时间才发出offer。这是为何？

这里就要看下vsomeip是如何在重复阶段处理完成后进入主阶段的：

```cpp
//vsomeip/implementation/service_discovery/src/service_discovery_impl.cpp
void
service_discovery_impl::start() {
   ...
    start_main_phase_timer();
    start_offer_debounce_timer(true);
    start_find_debounce_timer(true);
    start_ttl_timer();
}
```

这里可以看到，在开启service discovery组件（后面称sd组件）的start里边，有个`start_main_phase_timer()`：

```cpp
//vsomeip/implementation/service_discovery/src/service_discovery_impl.cpp
void
service_discovery_impl::start_main_phase_timer() {
    std::lock_guard<std::mutex> its_lock(main_phase_timer_mutex_);
    boost::system::error_code ec;
    main_phase_timer_.expires_from_now(cyclic_offer_delay_, ec);
    if (ec) {
        VSOMEIP_ERROR<< "service_discovery_impl::start_main_phase_timer "
        "setting expiry time of timer failed: " << ec.message();
    }
    main_phase_timer_.async_wait(
            std::bind(&service_discovery_impl::on_main_phase_timer_expired,
                    this, std::placeholders::_1));
}

void
service_discovery_impl::on_main_phase_timer_expired(
        const boost::system::error_code &_error) {
    if (_error) {
        return;
    }
    send(true);
    start_main_phase_timer();
}
```

显然，`start_main_phase_timer()`的做法就是根据json配置文件里边的`cyclic_offer_delay_`，就是主阶段offer周期，不断定时地发送offer。具体一开始就把主阶段定时器开起来后有没有发送offer，其实还和是否真正进入主阶段有关，有个标志位是用来标识是否进入主阶段的，之后进入主阶段才会真正发送主阶段的offer报文。我们可以看下接下来开启的`start_offer_debounce_timer`这部分：

```cpp
//vsomeip/implementation/service_discovery/src/service_discovery_impl.cpp
void
service_discovery_impl::start_offer_debounce_timer(bool _first_start) {
    std::lock_guard<std::mutex> its_lock(offer_debounce_timer_mutex_);
    boost::system::error_code ec;
    if (_first_start) {
        offer_debounce_timer_.expires_from_now(initial_delay_, ec);
    } else {
        offer_debounce_timer_.expires_from_now(offer_debounce_time_, ec);
    }
    if (ec) {
        VSOMEIP_ERROR<< "service_discovery_impl::start_offer_debounce_timer "
        "setting expiry time of timer failed: " << ec.message();
    }
    offer_debounce_timer_.async_wait(
            std::bind(&service_discovery_impl::on_offer_debounce_timer_expired,
                      this, std::placeholders::_1));
}

void
service_discovery_impl::on_offer_debounce_timer_expired(
        const boost::system::error_code &_error) {
    if(_error) { // timer was canceled
        return;
    }

    // Copy the accumulated offers of the initial wait phase
    services_t repetition_phase_offers;
    bool new_offers(false);
    {
        std::vector<services_t::iterator> non_someip_services;
        std::lock_guard<std::mutex> its_lock(collected_offers_mutex_);
        if (collected_offers_.size()) {
            if (is_diagnosis_) {
                for (services_t::iterator its_service = collected_offers_.begin();
                        its_service != collected_offers_.end(); its_service++) {
                    for (const auto& its_instance : its_service->second) {
                        if (!configuration_->is_someip(
                                its_service->first, its_instance.first)) {
                            non_someip_services.push_back(its_service);
                        }
                    }
                }
                for (auto its_service : non_someip_services) {
                    repetition_phase_offers.insert(*its_service);
                    collected_offers_.erase(its_service);
                }
            } else {
                repetition_phase_offers = collected_offers_;
                collected_offers_.clear();
            }

            new_offers = true;
        }
    }

    if (!new_offers) {
        start_offer_debounce_timer(false);
        return;
    }

    // Sent out offers for the first time as initial wait phase ended
    std::vector<std::shared_ptr<message_impl>> its_messages;
    auto its_message = std::make_shared<message_impl>();
    its_messages.push_back(its_message);
    insert_offer_entries(its_messages, repetition_phase_offers, true);

    // Serialize and send
    send(its_messages);

    std::chrono::milliseconds its_delay(0);
    std::uint8_t its_repetitions(0);
    if (repetitions_max_) {
        // Start timer for repetition phase the first time
        // with 2^0 * repetitions_base_delay
        its_delay = repetitions_base_delay_;
        its_repetitions = 1;
    } else {
        // If repetitions_max is set to zero repetition phase is skipped,
        // therefore wait one cyclic offer delay before entering main phase
        its_delay = cyclic_offer_delay_;
        its_repetitions = 0;
    }

    auto its_timer = std::make_shared<boost::asio::steady_timer>(host_->get_io());

    {
        std::lock_guard<std::mutex> its_lock(repetition_phase_timers_mutex_);
        repetition_phase_timers_[its_timer] = repetition_phase_offers;
    }

    boost::system::error_code ec;
    its_timer->expires_from_now(its_delay, ec);
    if (ec) {
        VSOMEIP_ERROR<< "service_discovery_impl::on_offer_debounce_timer_expired "
        "setting expiry time of timer failed: " << ec.message();
    }
    its_timer->async_wait(
            std::bind(
                    &service_discovery_impl::on_repetition_phase_timer_expired,
                    this, std::placeholders::_1, its_timer, its_repetitions,
                    its_delay.count()));
    start_offer_debounce_timer(false);
}
```

`start_offer_debounce_timer`的处理是主要是对于初始阶段的offer：

* 如果是第一次运行，则表示是初始阶段，需要等待配置在json文件指定的初始延时之后才开始；这个延时配置是取的json配置文件中`initial_min`和`initial_max`之间的随机值
* 等初始阶段延时一到，就进入绑定的回调：所有的offer都是先添加到`collected_offers_`里边的，在处理offer的时候会把里边的内容倒换到另一个容器里边，这个动作也表示有新的offer需要处理；对于新的offer，就直接发送，因为进入到这个动作的时候已经等待初始阶段延时了
* 发送完成后就进入重复阶段了：进行一系列处理之后再次开启`start_offer_debounce_timer`，定时器超时进入回调，判断此时不是新的offer，所以直接返回了

至此，`start_offer_debounce_timer`的使命基本完成。本质上就是周期检测有没有新的offer被添加进来，有的话就进行初始阶段的处理，发送offer。

```cpp
void
service_discovery_impl::on_repetition_phase_timer_expired(
        const boost::system::error_code &_error,
        const std::shared_ptr<boost::asio::steady_timer>& _timer,
        std::uint8_t _repetition, std::uint32_t _last_delay) {
    if (_error) {
        return;
    }
    if (_repetition == 0) {
        std::lock_guard<std::mutex> its_lock(repetition_phase_timers_mutex_);
        // We waited one cyclic offer delay, the offers can now be sent in the
        // main phase and the timer can be deleted
        move_offers_into_main_phase(_timer);
    } else {
        std::lock_guard<std::mutex> its_lock(repetition_phase_timers_mutex_);
        auto its_timer_pair = repetition_phase_timers_.find(_timer);
        if (its_timer_pair != repetition_phase_timers_.end()) {
            std::chrono::milliseconds new_delay(0);
            std::uint8_t repetition(0);
            bool move_to_main(false);
            if (_repetition <= repetitions_max_) {
                // Sent offers, double time to wait and start timer again.
                VSOMEIP_INFO << "service_discovery_impl::on_repetition_phase_timer_expired "
                        "repetition: " << static_cast<int>(_repetition);
                new_delay = std::chrono::milliseconds(_last_delay * 2);
                repetition = ++_repetition;
            } else {
                // Repetition phase is now over we have to sleep one cyclic
                // offer delay before it's allowed to sent the offer again.
                // If the last offer was sent shorter than half the
                // configured cyclic_offer_delay_ago the offers are directly
                // moved into the mainphase to avoid potentially sleeping twice
                // the cyclic offer delay before moving the offers in to main
                // phase
                if (last_offer_shorter_half_offer_delay_ago()) {
                    move_to_main = true;
                } else {
                    VSOMEIP_INFO << "service_discovery_impl::on_repetition_phase_timer_expired "
                            "repetition phase is over, waiting one cyclic offer delay";
                    new_delay = cyclic_offer_delay_;
                    repetition = 0;
                }
            }
            std::vector<std::shared_ptr<message_impl>> its_messages;
            auto its_message = std::make_shared<message_impl>();
            its_messages.push_back(its_message);
            insert_offer_entries(its_messages, its_timer_pair->second, true);

            // Serialize and send
            send(its_messages);
            if (move_to_main) {
                move_offers_into_main_phase(_timer);
                return;
            }
            boost::system::error_code ec;
            its_timer_pair->first->expires_from_now(new_delay, ec);
            if (ec) {
                VSOMEIP_ERROR <<
                "service_discovery_impl::on_repetition_phase_timer_expired "
                "setting expiry time of timer failed: " << ec.message();
            }
            its_timer_pair->first->async_wait(
                    std::bind(
                            &service_discovery_impl::on_repetition_phase_timer_expired,
                            this, std::placeholders::_1, its_timer_pair->first,
                            repetition, new_delay.count()));
        }
    }
}
```

`on_repetition_phase_timer_expired`顾名思义就是重复阶段的处理：

* 找到对应offer的重复阶段定时器，判断此时的重复次数有没有超过配置的值；没有的话继续发送offer，延迟2的n次幂 * 重复阶段基准周期，开启定时器继续重复阶段
* 如果是重复阶段的最后一次了，则判断重复阶段最后一帧的间隔时长是否要小于主阶段offer周期的一半，如果是则直接进入主阶段，否则就等一个主阶段offer周期
* 下次进入`on_repetition_phase_timer_expired`的时候由于不再是重复阶段了，所以直接进入主阶段

进入主阶段的操作其实就是把对应offer的重复阶段定时器给删除了，然后把对应的offer实例标记为已经进入主阶段。这里就是我上面说的进入主阶段的标志位。

```cpp
void
service_discovery_impl::move_offers_into_main_phase(
        const std::shared_ptr<boost::asio::steady_timer> &_timer) {
    // HINT: make sure to lock the repetition_phase_timers_mutex_ before calling
    // this function set flag on all serviceinfos bound to this timer that they
    // will be included in the cyclic offers from now on
    const auto its_timer = repetition_phase_timers_.find(_timer);
    if (its_timer != repetition_phase_timers_.end()) {
        for (const auto& its_service : its_timer->second) {
            for (const auto& its_instance : its_service.second) {
                its_instance.second->set_is_in_mainphase(true);
            }
        }
        repetition_phase_timers_.erase(_timer);
    }
}
```

综上，进入主阶段发送offer报文的实际控制只有在一开始sd组件`start`的时候，那么我们从抓取的数据包看，第一帧offer开始，主阶段的定时器就已经打开了。我们可以大致算一下从第一帧开始到重复阶段结束后，过了几个offer周期：

200 + 400 + 800 + 1600 + 100 = 3100 ms

重复阶段的间隔时间加上初始阶段所花时间，我们把初始阶段所花时间大致算是100ms的话，就过了3100ms，主阶段offer周期是2000ms，那就是过了一个主阶段offer周期，此时还有3100ms - 2000ms = 1100ms才走完重复阶段。

且重复阶段的最后一帧时间间隔是1600ms，大于主阶段offer周期的一半1000ms，所以从vsomeip的处理角度出发，它需要在重复阶段结束后再过2000ms，才能真正进入主阶段。所以在过完重复阶段后，又延迟了2000ms才把对应offer的进入主阶段的标志位置上。

主阶段定时器在走完第一个offer周期后，发现标志位还不在主阶段，此时还在重复阶段，所以又继续等待2000ms。等过了2000ms后，重复阶段早就过了，且过了重复阶段大约900ms（计算：2000ms - 1100ms = 900ms）。但此时判断标志位还不在主阶段，所以又等待2000ms。等再过了2000ms，发现标志位就是主阶段了，因为在主阶段定时器第二次判断的时候，再过1100ms主阶段标志位就置上了，这个时候才真正发送offer报文。

<br>

所以在发完重复阶段最后一帧offer之后，需要再等待大约2900ms才会发送offer报文，而进入主阶段的时间实际上在重复阶段结束后延迟一个主阶段offer周期，也就是2000ms的时候就已经到达了。

![](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/20250306102903.png)

<br>

这个就是问题的全部分析过程了。接下来就是如何修改的问题。其实也比较简单，但是文章就先写到这吧。

<br>

>所以，以后你看到谁被按在哪个角色里，无论你喜不喜欢那个角色，无论那个角色多讨人厌多脏，你还是要看到按在他身上的那个命运的手指头，说不定命运的手指头一松，他就马上脱离那个角色了。
>
><p align="right">蔡崇达《命运》</p>
