# 语义分析

## 符号表定义

1. 符号的内部结构
	- name 标识符的名字
	- decKind 标识符的类型(变量，类型，过程)
	- typePtr 标识符指向的具体类型(基本类型，结构体类型，数据类型)
2. 符号表
	- 使用list保存符号
	- 结构体的fieldList，过程的paramList均采用符号表
3. scope栈
	- 出现过程声明时，将过程加入到当前符号表中，然后为过程声明单独新建一个符号表，过程的符号表填完后加入scope栈中，同时使当前符号表指向此过程的符号表(为了嵌套声明做准备)，声明结束后，还原符号表指针。

## 变量定义

类型标识符定义和变量表示符定义的产生式结构很相似，过程定义的产生式比较复杂，但是和program部分结构类似，需要先完成program部分。

### 类型标识符定义

```text
TypeDec -> ε
TypeDec -> TypeDeclaration
TypeDeclaration -> TYPE TypeDecList
TypeDecList -> TypeId = TypeName ; TypeDecMore
TypeDecMore -> ε
TypeDecMore -> TypeDecList
```

思路：对每一个TypeId进行查表，检查是否重复定义，Typename结构复杂，且在变量定义和过程参数定义中使用到了，需要封装一下。

```text
TypeName -> BaseType
TypeName -> StructureType
TypeName -> ID
```

如果Typename是ID需要查表，反之直接读取BaseType或者StructureType的信息即可。出现TyDecMore+空跳出类型定义。

BaseType和ArrayType比较简单，RecType比较复杂，但是不能嵌套定义RecType也还好

```text
RecType -> RECORD FieldDecList END
FieldDecList -> BaseType IdList ; FieldDecMore
FieldDecList -> ArrayType IdList ; FieldDecMore
FieldDecMore -> ε
FieldDecMore -> FieldDecList
IdList -> ID IdMore
IdMore -> ε
IdMore -> , IdList
```



### 变量标识符定义

```
VarDec -> ε
VarDec -> VarDeclaration
VarDeclaration -> VAR VarDecList
VarDecList -> TypeName VarIdList ; VarDecMore
VarDecMore -> ε
VarDecMore -> VarDecList
VarIdList -> ID VarIdMore
VarIdMore -> ε
VarIdMore -> , VarIdList
```

处理好TypeName之后，遍历VarIdList(遇到空停止)，将得到的Id依次查表，并加入符号表即可。遇到VarDecMore + 空 跳出变量定义

### 过程定义

```text
ProcDec -> ε
ProcDec -> ProcDeclaration
ProcDeclaration -> PROCEDURE  ProcName ( ParamList ) ;  ProcDecPart  ProcBody  ProcDecMore
ProcDecMore -> ε
ProcDecMore -> ProcDeclaration
```

过程定义较复杂，首先处理procname,处理ID查表即可，paramList有点类似变量定义的结构

```text
ParamList -> ParamDecList
ParamDecList -> Param ParamMore
ParamMore -> ε
ParamMore -> ; ParamDecList
Param -> TypeName FormList
Param -> VAR TypeName FormList
FormList -> ID FidMore
FidMore -> ε
FidMore -> , FormList
```

处理TypeName,然后遍历FormList查表并加入过程符号表(遇到空停止)，遇到ParamMore + 空停止 参数列表部分。

过程定义存在嵌套定义，注意符号表更新和scope栈的维护

```text
ProcDecPart -> DeclarePart
DeclarePart -> TypeDec VarDec ProcDec
```

## 程序体

```text
ProgramBody -> BEGIN StmList END
StmList -> Stm StmMore
StmMore -> ε
StmMore -> ; StmList
Stm -> ConditionalStm
Stm -> LoopStm
Stm -> InputStm
Stm -> OutputStm
Stm -> ReturnStm
Stm -> ID AssCall
```

有必要将程序体部分封装，过程的程序体和主程序的程序体的处理逻辑是一样的。

思路：对每一种stm封装对应的处理逻辑，然后每次读一个stm,直到空为止。最后读到end结束程序体部分

### if 语句

```text
ConditionalStm -> IF RelExp THEN StmList ELSE StmList FI
RelExp -> Exp OtherRelE
OtherRelE -> CmpOp Exp
```

来到了很恶心的一部分，需要处理一下Exp

```text
Exp -> Term OtherTerm
OtherTerm -> ε
OtherTerm -> AddOp Exp
```

停止条件 otherTerm + 空

```text
Term -> Factor OtherFactor
OtherFactor -> ε
OtherFactor -> MultOp Term
```

停止条件 otherFactor + 空

```text
Factor -> ( Exp )
Factor -> INTC
Factor -> Variable
```

遇到INTC 直接返回对应的值和类型就好了，Exp 需要考虑递归的问题，先分析Variable

```text
Variable -> ID VariMore
VariMore -> ε
```

最简单的情况只有一个ID,查表即可。

```text
VariMore -> [ Exp ]
```

数组的时候，需要递归一下Exp,检查下标类型是否合法

```text
VariMore -> . FieldVar
FieldVar -> ID FieldVarMore
FieldVarMore -> ε
```

成员变量，查结构体的fieldList即可，成员是数组的时候，需要递归使用Exp检查数组下标

```text
FieldVarMore -> [ Exp ]
```

综上需要对Exp处理进行封装，同时处理好递归调用的问题。

### while 语句

```text
LoopStm -> WHILE RelExp DO StmList ENDWH
```

同if 语句，处理 RelExp后，处理stmList

### read 语句

```text
InputStm -> READ ( Invar )
Invar -> ID
```

读Id 查表

### write 语句

```text
OutputStm -> WRITE ( Exp )
```

处理Exp

### return 语句

```text
ReturnStm -> RETURN ( Exp )
```

处理Exp

### 赋值语句

```text
Stm -> ID AssCall
AssCall -> AssignmentRest
AssCall -> AssignmentRest
AssignmentRest -> VariMore := Exp
```

stm语句使用 Id 开始时，要么是过程调用，要么是赋值语句，对于赋值语句需要单独处理一下变量的识别，然后处理Exp

### 过程调用

```text
Stm -> ID AssCall
AssCall -> CallStmRest
CallStmRest -> ( ActParamList )
ActParamList -> ε
ActParamList -> Exp ActParamMore
ActParamMore -> ε
ActParamMore -> , ActParamList
```

一连串的Exp处理，直到ActParamMore + 空停止

## 语义错误定义

1. 类型未定义 
	- type t1 = xxx;
2. 成员变量未定义
	- var record integer b;end aRecord; aRecord.c := 1;
3. 重复定义
	- var char a,a;
	- type a = integer; var integer a;
4. 非法的数组定义
	- var array [-1..10] of char a;
	- var array [5..1] of char a;
	- var array [5..5] of char a;
5. 赋值语句类型不匹配
	- var char c; c:= 10;
6. 类型不兼容
	- var array [1..10] of char a;char b; write(a[b]);
7. 变量作为过程被调用
	- var integer a; a(1);
8. 过程参数数量不匹配
9. 过程参数类型不匹配