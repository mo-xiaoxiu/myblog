# UML类图

## 基础

![UML](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/UML.drawio.png)

## example

这里以设计模式中的**生成器模式**为例：

![UML_ep](https://myblog-1308923350.cos.ap-guangzhou.myqcloud.com/img/UML_ep.drawio.png)

[图片来源](https://refactoringguru.cn/design-patterns/builder)

* `Builder`：抽象接口类；生成器，包含生成产品的各个步骤

  * 成员函数：
    * `reset()`：(`public`)释放资源便于重新生成对象，以防止在提供一个对象时一个相同的对象在构造（确保只有一个对象）
    * `buildStepA()`：(`public`)生成器中的步骤一
    * `buildStepB()`：(`public`)生成器中的步骤二
    * `buildStepZ()`：(`public`)生成器中的步骤三

* `Concrete Builder1`：具象建造者，**继承于`Builder`**

  * 成员变量：

    * `result`：(`private`)类型为`Product 1`，表示生成的产品为`Product 1`

  * 成员函数：

    * `reset()`：(`public`)同上

      `result = new Product1()`

    * `buildStepA()`：(`public`)具象生成器中的步骤一

    * `buildStepB()`：(`public`)具象生成器中的步骤二

      `result.setFeatureB()`

    * `buildStepZ()`：(`public`)具象生成器中的步骤三

    * `getResult()`：(`pubilc`)类型为`product 1`，表示取出`Product 1`

      `return this->result`

  * `Concrete Builder2`：同上

* `Director`：主管类，负责接收用户委托，指定生成器进行生产，产品由客户自行接收（有些情况下不是必须的）

  * 成员变量：
    * `builder`：(`private`)类型为`Builder`，表示主管有此生成器
  * 成员函数：
    * `Director(builder)`：(`pubilc`)构造函数需要传入生成器作为参数，表示接收用户委托
    * `changeBuilder(builder)`：(`public`)表示根据用户意愿改变生成器，具体实现为重写`builder`中的某些函数
    * `make(type)`：(`public`)根据样式安排生成器制造需要的产品（即按照需求只进行必要的步骤）

* `Client`：客户

  * 可以选择将需求委托给主管类

  * 也可以选择自己找生成器进行制造

    