'''
@author: badmonkey
@software: PyCharm
@file: semantic.py
@time: 2021/4/18 下午6:47
'''
from Parser.AST import *
from Parser.LL1 import *
from Scanner.scanner import *
from Analyzer.symbol import *

class myState():
    START="start"
    TYPEDEC="typedec"
    VARDEC = "vardec"
    PRODEC = "prodec"
    DONE="done"

class semanticError(object):
    duplicateDefine = "duplicate defined variable\n"
    unDefined = "undefined variable\n"
    arrayOut = "index out of array bound\n"
    invalidMember = "invalid member access\n"
    assignmentTypeError = "invalid assginment;variable type do not match\n"
    assignmentVariableError = "invalid assignment; the left side of the assginment is not variable\n"
    paramTypeError = "procedure praam type do not match\n"
    paramNumError = "procedure param number do not match\n"
    procedureCallError  = "variable can not be called\n"
    boolError = "conditon must be an boolean value\n"
    typeMatchError = "variable type do not match expect %s got %s\n"
    arrayDefineError = "invalid array define"
    typeKindMatchError = "type kind do not match expect %s got %s"


class Analyzer(object):

    def __init__(self,tokens,root):
        self.index = 0
        self.tokens = tokens
        self.root = root
        self.symTable = SymbolTable()
        self.state = myState.START
        self.current = root
        self.error = False
        self.scope = [self.symTable]
        self.errorMessage = ""
        self.currentVarType = ""
        self.currentVarKind = ""
        self.currentExp = ""
        self.currentVarValue = ""
        self.currentVar = None

    def __len__(self):
        return len(self.symTable)

    def __repr__(self):
        print(self.symTable)
        return ""

    def updateIndex(self):
        if self.current.getTokenVal() != 'ε' and self.current.getTokenVal():
            self.index += 1
            # print(self.index,self.tokens[self.index-1][0],self.current.getTokenVal())

    def step(self):
        if self.current.isEmpty():
            self.current = self.current.step()
        else:
            self.current = self.current.firstChild()

    def preToken(self):
        if self.index - 2 >0 :
            return self.tokens[self.index-2]
        else:
            return None

    def nextToken(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return None
    def currentToken(self):
        if self.index - 1 > 0:
            return self.tokens[self.index-1]
        else:
            return None

    def procDec(self):
        sym = Symbol(kind="procDec")
        paramList = SymbolTable()
        self.step()
        while not self.current.isTokenType("ProcBody"):
            self.updateIndex()
            if self.current.isTokenType("ID"):
                if self.current.father.isTokenType("ProcName"):
                    name = self.current.getTokenVal()
                    if name in self.symTable:
                        self.error = True
                        self.errorMessage = semanticError.duplicateDefine
                        return
                    else:
                        sym.name = name
                elif self.current.father.isTokenType("FormList"):
                    typeName = self.tokens[self.index-2][0]
                    if typeName == "INTEGER" or typeName == "CHAR":
                        param = Symbol()
                        param.name = self.current.getTokenVal()
                        param.kind = "varDec"
                        param.type = typeName
                        paramList.add(param)
            elif  self.current.isTokenType(")") and self.tokens[self.index][0] == ';':
                sym.param = paramList
                sym.level = len(self.symTable)
                self.symTable.add(sym)
                self.scope.append(SymbolTable())
                self.symTable = self.scope[-1]
                # 函数 的参数也是符号信息
                for i in paramList:
                    self.symTable.add(i)

            elif self.current.isTokenType("TypeDecList"):
                # 这里有递归的过程定义部分
                self.typeDec()
                if self.error:
                    return
            elif self.current.isTokenType("VarDecList"):
                self.varDec()
                if self.error:
                    return
            elif self.current.isTokenType("ProcDeclaration"):
                self.procDec()
                if self.error:
                    return
            self.step()
        self.updateIndex()
    def varDec(self):
        sym = Symbol(kind="varDec")
        self.step()
        idType = ""
        while not self.current.isTokenVal(';'):
            self.updateIndex()

            if self.current.isTokenType("ID"):
                if self.current.father.isTokenType("VarIdList"):
                    sym.name = self.current.getTokenVal()
                    # print(sym)
                    self.symTable.add(sym)
                    sym = Symbol(kind="varDec",type=idType)
                elif self.current.father.isTokenType("TypeName"):
                    currentId = self.current.getTokenVal()
                    if currentId in self.symTable:
                        sym.type = self.symTable.get(currentId).type
                    else:
                        # print("error in line %s  " % (tokens[self.index][2]) + currentId + "未定义\n", )
                        self.errorMessage = semanticError.unDefined
                        self.error = True
                        return
            elif self.current.isTokenType("INTEGER") and self.tokens[self.index][0] == "ID":
                # print(self.tokens[self.index-2])
                idType = self.current.getTokenType()
                sym.type = idType
            elif self.current.isTokenType("CHAR") and self.tokens[self.index][0] == "ID":
                idType =  self.current.getTokenType()
                sym.type = idType
                # root = root.firstChild()
            elif self.current.isTokenType("ArrayType"):
                # 数组类型
                array = ArrayType()
                self.step()
                while not self.current.isTokenType("INTEGER") and not self.current.isTokenType("CHAR"):
                    self.updateIndex()
                    if self.current.isTokenType("INTC"):
                        if self.current.father.isTokenType("Low"):
                            low = int(self.current.getTokenVal())
                            # print("low :",low)
                            if low < 0:
                                self.error = True
                                self.errorMessage = semanticError.arrayDefineError
                                # print("数组下界小于零")
                                return
                            else:
                                array.low = low
                        elif self.current.father.isTokenType("Top"):
                            top = int(self.current.getTokenVal())
                            # print("top:",top)
                            if top <= array.low:
                                self.error = True
                                self.errorMessage = semanticError.arrayDefineError
                                # print("数组上界小于下界")
                                return
                            else:
                                array.top = top
                    self.step()
                self.updateIndex()
                array.element = self.current.getTokenType()
                sym.type = array
            elif self.current.isTokenType("RecType"):
                # 结构体
                record = RecordType()
                fieldList = FieldList()
                self.step()
                # end of record
                while not self.current.isTokenType("END"):
                    # basetype declare
                    self.updateIndex()
                    #
                    if self.current.isTokenType("BaseType") and self.current.father.isTokenType("FieldDecList"):
                        baseType = ""
                        self.step()
                        while not self.current.isTokenType(";"):

                            self.updateIndex()
                            if self.current.isTokenType("INTEGER"):
                                baseType = "INTEGER"
                            elif self.current.isTokenType("CHAR"):
                                baseType = "CHAR"
                            elif self.current.isTokenType("ID"):
                                field = Field()
                                field.type = baseType
                                field.name = self.current.getTokenVal()
                                if field.name not in fieldList:
                                    fieldList.append(field)
                                else:
                                    self.error = True
                                    self.errorMessage = semanticError.duplicateDefine
                                    # print("结构体内部出现重复定义")
                                    return
                            self.step()
                        self.updateIndex()
                    elif self.current.isTokenType("ArrayType") and self.current.father.isTokenType("FieldDecList"):
                        array = ArrayType()
                        self.step()
                        while not self.current.isTokenType("INTEGER") and not self.current.isTokenType("CHAR"):
                            self.updateIndex()
                            if self.current.isTokenType("INTC"):
                                if self.current.father.isTokenType("Low"):
                                    low = int(self.current.getTokenVal())
                                    # print("low :",low)
                                    if low < 0:
                                        self.error = True
                                        self.errorMessage = semanticError.arrayDefineError
                                        # print("数组下界小于零")
                                        return
                                    else:
                                        array.low = low
                                elif self.current.father.isTokenType("Top"):
                                    top = int(self.current.getTokenVal())
                                    # print("top:",top)
                                    if top <= array.low:
                                        self.error = True
                                        self.errorMessage = semanticError.arrayDefineError
                                        # print("数组上界小于下界")
                                        return
                                    else:
                                        array.top = top
                            self.step()
                        array.element = self.current.getTokenType()
                        arrayType = array
                        self.updateIndex()
                        # arraylist
                        self.step()
                        while not self.current.isTokenType(";"):

                            self.updateIndex()
                            if self.current.isTokenType("ID"):
                                field = Field()
                                field.type = arrayType
                                field.name = self.current.getTokenVal()
                                if field.name not in fieldList:
                                    fieldList.append(field)
                                else:
                                    self.error = True
                                    self.errorMessage = semanticError.duplicateDefine
                                    # print("结构体内部出现重复定义")
                                    return
                            self.step()
                        self.updateIndex()
                    self.step()
                self.updateIndex()
                # pass
                record.fieldList = fieldList
                sym.type = record
            self.step()
        self.updateIndex()
        # if self.current.isTokenVal(";") and not self.error:
        #     self.symTable.add(sym)
        #     self.current = self.current.step()
        #     self.index += 1
    def typeDec(self):
        sym = Symbol(kind="typeDec")
        self.step()
        while not self.current.isTokenVal(';'):
            self.updateIndex()

            if self.current.isTokenType("ID"):
                if self.current.father.isTokenType("TypeId"):
                    sym.name = self.current.getTokenVal()
                elif self.current.father.isTokenType("TypeName"):
                    currentId = self.current.getTokenVal()
                    if currentId in self.symTable:
                        sym.type = self.symTable.get(currentId).type
                    else:
                        # print("error in line %s  "%(tokens[self.index][2])+currentId+"未定义\n",)
                        self.error = True
                        self.errorMessage = semanticError.unDefined
                        return
            elif self.current.isTokenType("INTEGER") and self.tokens[self.index-2][0] == "=" :
                # print(self.tokens[self.index-2])
                sym.type = self.current.getTokenType()
            elif self.current.isTokenType("CHAR")  and self.tokens[self.index-2][0] == "=" :
                sym.type = self.current.getTokenType()
                # root = root.firstChild()
            elif self.current.isTokenType("ArrayType"):
                # 数组类型
                array = ArrayType()
                self.step()
                while not self.current.isTokenType("INTEGER") and not self.current.isTokenType("CHAR"):
                    self.updateIndex()
                    if self.current.isTokenType("INTC"):
                        if self.current.father.isTokenType("Low"):
                            low = int(self.current.getTokenVal())
                            # print("low :",low)
                            if low<0:
                                self.error = True
                                self.errorMessage = semanticError.arrayDefineError
                                # print("数组下界小于零")
                                return
                            else:
                                array.low = low
                        elif self.current.father.isTokenType("Top"):
                            top = int(self.current.getTokenVal())
                            # print("top:",top)
                            if top <= array.low:
                                self.error = True
                                self.errorMessage = semanticError.arrayDefineError

                                # print("数组上界小于下界")
                                return
                            else:
                                array.top = top
                    self.step()
                self.updateIndex()
                array.element = self.current.getTokenType()
                sym.type = array
            elif self.current.isTokenType("RecType"):
                # 结构体
                record = RecordType()
                fieldList = FieldList()
                self.step()
                # end of record
                while not self.current.isTokenType("END"):
                    # basetype declare
                    self.updateIndex()
                    #
                    if self.current.isTokenType("BaseType") and self.current.father.isTokenType("FieldDecList"):
                        baseType = ""
                        self.step()
                        while not self.current.isTokenType(";"):

                            self.updateIndex()
                            if self.current.isTokenType("INTEGER"):
                                baseType = "INTEGER"
                            elif self.current.isTokenType("CHAR"):
                                baseType = "CHAR"
                            elif self.current.isTokenType("ID"):
                                field = Field()
                                field.type = baseType
                                field.name = self.current.getTokenVal()
                                if field.name not in fieldList:
                                    fieldList.append(field)
                                else:
                                    self.error = True
                                    self.errorMessage = semanticError.duplicateDefine
                                    # print("结构体内部出现重复定义")
                                    return
                            self.step()
                        self.updateIndex()
                    elif self.current.isTokenType("ArrayType") and self.current.father.isTokenType("FieldDecList"):
                        array = ArrayType()
                        self.step()
                        while not self.current.isTokenType("INTEGER") and not self.current.isTokenType("CHAR"):
                            self.updateIndex()
                            if self.current.isTokenType("INTC"):
                                if self.current.father.isTokenType("Low"):
                                    low = int(self.current.getTokenVal())
                                    # print("low :",low)
                                    if low < 0:
                                        self.error = True
                                        self.errorMessage = semanticError.arrayDefineError
                                        # print("数组下界小于零")
                                        return
                                    else:
                                        array.low = low
                                elif self.current.father.isTokenType("Top"):
                                    top = int(self.current.getTokenVal())
                                    # print("top:",top)
                                    if top <= array.low:
                                        self.error = True
                                        self.errorMessage = semanticError.arrayDefineError
                                        # print("数组上界小于下界")
                                        return
                                    else:
                                        array.top = top
                            self.step()
                        array.element = self.current.getTokenType()
                        arrayType = array
                        self.updateIndex()
                        # arraylist
                        self.step()
                        while not self.current.isTokenType(";"):

                            self.updateIndex()
                            if self.current.isTokenType("ID"):
                                field = Field()
                                field.type = arrayType
                                field.name = self.current.getTokenVal()
                                if field.name not in fieldList:
                                    fieldList.append(field)
                                else:
                                    self.error = True
                                    self.errorMessage = semanticError.duplicateDefine
                                    # print("结构体内部出现重复定义")
                                    return
                            self.step()
                        self.updateIndex()
                    self.step()
                self.updateIndex()
                # pass
                record.fieldList = fieldList
                sym.type = record
            self.step()

        if self.current.isTokenVal(";") and not self.error:
            self.symTable.add(sym)
            self.current = self.current.step()
            self.index += 1

    def loopStm(self):
        """
        循环语句
        :return:
        """
        # self.step()
        # while self.current.isTokenType("THEN"):
        #     self.updateIndex()
        #     if self.current.isTokenType("Cmpop"):

        pass
    def ifStm(self):
        """
        if 语句
        :return:
        """
        pass
    def assignStm(self):
        """
        赋值语句
        :return:
        """
        pass
    def callStm(self):
        """
        过程调用
        :return:
        """
    def variable(self):
        """

        :return: varType(integer or char),value, symPtr(use to update value)
        """
        # self.step()
        sym = Symbol()
        # varType = ""
        while True:
            # self.updateIndex()
            if self.current.isTokenType("ID"):
                currentId = self.current.getTokenVal()
                if self.current.father.isTokenType("Stm"):
                    for symTable in self.scope[::-1]:
                        if currentId in symTable:
                            sym = symTable.get(currentId)
                            if sym.kind != "varDec":
                                self.error = True
                                self.errorMessage = semanticError.typeKindMatchError % (sym.kind, "varDec")
                                return
                            self.currentVarType = sym.type.kind
                            self.currentVarKind = sym.kind
                            self.currentVarValue = sym.value
                            break
                    if sym.kind == None:
                        self.error = True
                        self.errorMessage = semanticError.unDefined
                        return
                elif self.current.father.isTokenType("FieldVar"):
                    # print(self.currentVariType)
                    if self.currentVarType != "recordType":
                        self.error = True
                        self.errorMessage = semanticError.typeMatchError%("recordType",self.currentVarType)
                        return
                    else:
                        # print(sym.type.fieldList,currentId)
                        if currentId not in sym.type.fieldList:
                            self.error = True
                            self.errorMessage = semanticError.unDefined
                            return
                        else:
                            sym = sym.type.fieldList.get(currentId)
                elif self.current.father.isTokenType("Variable"):
                    pass


            elif self.current.isTokenType("Exp") and self.preToken() == "[" and self.nextToken() == "]":
                # value = self.exp()
                if self.currentVarType != "arrayType":
                    self.error = True
                    self.errorMessage = semanticError.typeKindMatchError%("arrayType",self.currentVarType)
                else:
                    expType,expValue = self.exp()
                    if expType != "INTC":
                        self.error = True
                        self.errorMessage = semanticError.typeMatchError%("INTC",expType)
                        return
                    # ok
            elif self.current.isTokenType("ε"):
                break
            # elif self.
            self.step()
            self.updateIndex()
        if self.currentVarType == "arrayType":
            return (sym,sym.type.element,sym.kind)
        else:
            return (sym,sym.type,None)
        # self.currentVar = sym
        # self.currentVarType = sym.type
        # self.currentVarKind = sym.kind

    def exp(self):
        """
        只做了静态语义分析，只需要知道exp的类型即可，value为动态语义分析保留
        :return: INTC value ()
        """
        # print(self.currentToken())
        self.step()

        while True:
            self.updateIndex()
            if self.current.isTokenType("ε") and self.current.father.isTokenType("OtherTerm"):
                break
            elif self.current.isTokenType("Variable"):
                var,varType,_ = self.variable()
                # print(varType)
                if varType != "INTEGER":
                    self.error = True
                    self.errorMessage = semanticError.typeMatchError%("INTEGER",varType)
                    return None,None
            # elif self.current.isTokenType("INTC"):
            self.step()

        return "INTC",None

    def printError(self):
        print("Error in line: %d\tDetail: %s %s %s\n"%(self.tokens[self.index-1][-1],self.tokens[self.index-1][0],self.tokens[self.index-1][1],self.errorMessage))


    def analyze(self):
        self.current = self.root.firstChild()
        while self.current.getId() != 0:
            self.updateIndex()
            if self.current.isTokenType("TypeDecList"):
                self.typeDec()
                if self.error:
                    break
            elif self.current.isTokenType("VarDecList"):
                self.varDec()
                if self.error:
                    break
            elif self.current.isTokenType("ProcDeclaration"):
                # scope 栈 需要更新
                self.procDec()
                if self.error:
                    break
            elif self.current.isTokenType("LoopStm"):
                self.loopStm()
                if self.error:
                    break
            elif self.current.isTokenType("ConditionalStm"):
                self.ifStm()
                if self.error:
                    break
            elif self.current.isTokenType("AssignmentRest"):
                self.assignStm()
                if self.error:
                    break
            elif self.current.isTokenType("CallStmRest"):
                if self.error:
                    break
            elif self.current.isTokenType("ID") and self.current.father.isTokenType("Stm"):
                if self.tokens[self.index][0] == "(":
                    # procedure call
                    pass
                else:
                    # variable assginment
                    var,varType,varKind= self.variable()
                    # print(self.currentToken())
                    expType,_ = self.exp()

                    # print(self.currentToken())
                    print(varType,expType)
                    # print(self.currentVar)
                if self.error:
                    break

            self.step()
        if self.error:
            self.printError()





if __name__ == '__main__':
    scanner = list(open("source.txt","r").read())
    tokens = Scan(scanner)
    out = open("demo.txt","w")
    for i in tokens:
        out.write(str(i)+"\n")
    out.close()
    tokens = open("demo.txt",'r').readlines()

    index = 0
    root = generateAST(tokens)
    tokens = [eval(token) for token in tokens]
    astfile = open("ast.txt","w")
    root.dump(file=astfile)
    astfile.close()
    analyzer = Analyzer(tokens,root)
    analyzer.analyze()
    # print(analyzer.scope[0])
    # print(analyzer.symTable)

