# GIt

## Git相关的配置文件：

1. `Git\etc\config`：安装目录下的`gitconfig --system系统级的`
2. `C:\Users\Admin\用户\.gitconfig`：只适合于当前登录用户的配置 `--global`

命令行查看：

```git
git config --system --list
git config --global --list
```



### 设置用户名和邮箱

```git
git config --global user.name "yourusername"
git config --global user.email "youremail.com"
```

## Git基本理论

三个区域：

* 工作区
* 暂存区
* 仓库

还有一个远程仓库，可以使用国内的`gitee`或者世界上最大的同性交友平台`github`搭建

## Git常见命令

* 查看当前git状态：

```git
git status
```

* 初始化仓库：

```git
git init
```

* 或者从远程克隆到本地：

```git
git clone [url]
```

* 添加修改的文件或者新增的文件到暂存区：

```git
git add [filename]
```

**注意：仓库中的`.gitignore`文件可以声明忽略添加提交哪些文件，作用是防止每次提交都需要提交所有文件，造成时间浪费；开发过程中也可以避免一些不必要的文件提交**

* 将暂存区的文件提交到本地仓库：

```git
git commit -m "[message]"
```

* 可以将“添加代码到暂存区”与“提交到本地仓库”结合成一条命令：

```git
git commit -ma "[message]"
```

-a：表示add

* 将本地仓库推到远程仓库：

```git
git push
```

* 从远程仓库将仓库的变化拉取到本地仓库：

```git
git pull
```







## Git分支

* 新建一个分支，但是此时位置还是在当前分支，而不是在新建的分支：

  ```git
  git branch [branchname]
  ```

* 切换到（新建的）分支：

  ```git
  git checkout [branchname]
  ```

* 在当前分支工作想切换到另外一个分支，需要暂时将当前分支modify状态保存起来：

  ```git
  git stash
  ```

  然后切换到另一个分支工作，工作完成之后想要重新加载之前分支的状态：

  ```git
  git stash pop
  ```

* 删除一个分支：

  ```git
  git branch -d [branchname]
  ```



### 分支冲突

需要在版本之间协商一个写法，作为最后确认的版本，将冲突的文件（此时冲突的文件被标记为“冲突”）修改完成之后重新提交：

```git
git add .
```

表示将所有文件（包括修改的文件）添加到暂存区（此时修改的文件就被标记为“冲突已解决”），之后：

```git
git commit -m "[message]"
```





# Git实践

