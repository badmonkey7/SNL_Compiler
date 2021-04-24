# SNL_Compiler

## 编译前端

- [x] **词法分析**
	- [x] 输出 token序列
- [ ] **语法分析**
	- [x] LL1文法
		- [x] 产生first集
		- [x] 产生follow集
		- [x] 建立LL1表
		- [x] 建立语法树
	- [ ] 递归下降

- [ ] **语义分析**
	- [x] scope栈，符号表构建
	- [x] 类型，标识符内部表示
	- [x] 标识符重复定义
	- [x] 标识符未声明
	- [x] 标识符类型不匹配(如变量标识符作为过程标识符使用)
	- [ ] 数组下标越界
	- [x] 表达式运算语句，数组下标变量类型不匹配
	- [x] 过程调用，参数数量不匹配
	- [x] 过程调用，参数类型不匹配
	- [x] if，while条件语句不是bool类型

## 效果展示

语法树

![ast](Parser/ast.png)

符号表

![symbolTable](Analyzer/symTable.png)

## 参考链接

`snl semantic errors`

https://github.com/Yesterday17/SNLCompiler

`structrue of ast`

https://blog.csdn.net/xuelians/article/details/79999284

`structrue of ll1 grammar`

https://tech.viewv.top/2019/10/31/%E7%BC%96%E8%AF%91%E5%8E%9F%E7%90%86%E8%AF%8D%E6%B3%95%E5%88%86%E6%9E%90%E4%B8%8ELL1%E6%96%87%E6%B3%95python%E7%AE%80%E5%8D%95%E5%AE%9E%E7%8E%B0%E4%B8%8E%E6%84%9F%E6%83%B3.html#%E5%AE%8C%E6%95%B4%E7%A8%8B%E5%BA%8F

`display ast`

https://graphviz.org/