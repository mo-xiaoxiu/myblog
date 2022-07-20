# Lambda

本质是匿名函数，类似于仿函数的功能

## example

* 写一个叠加整数的类
* 每次叠加一个
* 分别使用类的成员函数和仿函数实现

```cpp title="test.cpp"
#include <iostream>

//add num
class AddNum{
	public:
		AddNum(int x): m_num(0){
			this->m_num += x;
		}
		int getNum();

		//仿函数
		int operator()(int x) {
			return m_num + x;
		}
	private:
		int m_num;
};

//成员函数
int AddNum::getNum(){
	return m_num;
}

```

main函数中：

```cpp
int main() {
	int x = 10;
	AddNum a(x);
    //memeber
	std::cout<<"AddNum: "<<a.getNum()<<std::endl;

	//functor
	std::cout<<"AddNum operator: "<<a(x)<<std::endl;
    
	return 0;
}
```

执行结果：

```
AddNum: 10
AddNum operator: 20
```

**使用lambda完成这个功能：**

```cpp title="tesi.cpp"
#include <iostream>

//add num
class AddNum{
	public:
		AddNum(int x): m_num(0){
			this->m_num += x;
		}
		int getNum();

		//functor
		int operator()(int x) {
			return m_num + x;
		}
	private:
		int m_num;
};

int AddNum::getNum(){
	return m_num;
}

int main() {
	int x = 10;
	AddNum a(x);
	std::cout<<"AddNum: "<<a.getNum()<<std::endl;

	//functor
	std::cout<<"AddNum operator: "<<a(x)<<std::endl;

	//lambda
	auto lambda_addnum = [lambda_x = 10](int x){return x + lambda_x;};
	std::cout<<"lambda: "<< lambda_addnum(10) <<std::endl;
	return 0;
}
```

执行结果：

```
AddNum: 10
AddNum operator: 20
lambda: 20
```

