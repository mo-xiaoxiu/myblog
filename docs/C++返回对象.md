# C++返回对象

## 返回对象的方式

* 当返回同个类型一个变量时，在一个函数中一般直接返回（*注意：不能返回局部变量的引用*）

  ```cpp
  Type func(){
      return Type();
  }
  ```

* 当返回同一类型多个变量时，可以使用`std::array`或者是`std::vector`

  ```cpp
  std::array<std::string, 2> func() {
      std::string str1 = "...";
      std::string str2 = "...";
      return {str1, str2};
  }
  ```

  *注意：使用array一般是在栈上分配内存，而vector一般是在堆上分配内存，注意这里的开销问题*

* 使用**创建结构体**的方式

  ```cpp
  //创建接收返回值的结构体
  struct shareStruct
  {
      std::string str1;
      std::string str2;
  };
  
  //使用时
  shareStruct func() {
      std::string str1 = "...", str2 = "...";
      shareStruct ss;
      ss.str1 = str1;
      ss.str2 = str2;
      return ss;
  }
  ```

* 使用`std::tuple`或者是`std::pair`

  ```cpp
  #include <tuple>
  
  std::pair<std::string, int> func_1() {
  	std::string str = "...";
    	int id = 5;
    	return {str, id};
  }
  
  std::tuple<std::string, std::string, int> func_1(int size) {
  	std::string str1 = "...", str2 = "...";
    	int id = 6;
    	return {str1, str2, id};
  }
  
  //使用时
  std::tuple<std::string, int> tmp = 
  func_1();
  
  auto tmp1 = func_1(2);
  ```

* 可以使用是指针或者引用的参数作为参数传入函数中接收返回值

  ```cpp
  std::string sRef;
  void func(std::string& sRef) {
  	std::string s = "...";
    	sRef = s;
  }
  
  //使用时
  std::string sTest;
  func(sTest);
  ```



