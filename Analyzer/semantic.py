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
    duplicateDefine = "duplicate defined variable"
    unDefined = "undefined variable"
    arrayOut = "index out of array bound"
    invalidMember = "invalid member access"
    assignmentTypeError = "invalid assginment;variable type do not match"
    assignmentVariableError = "invalid assignment; the left side of the assginment is not variable"
    paramTypeError = "procedure param type do not match"
    paramNumError = "procedure param number do not match expect %d params got %d params"
    procedureCallError  = "variable can not be called"
    boolError = "conditon must be an boolean value"
    typeMatchError = "variable type do not match expect %s got %s"
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
        self.printerror = True
        self.symLevel = 0

    def __len__(self):
        return len(self.symTable)

    def __repr__(self):
        print(self.symTable)
        return ""

    def updateIndex(self):
        if self.current.getTokenVal() != 'ε' and (self.current.getTokenVal() or self.current.getTokenVal() == 0) :
            self.index += 1
            # print(self.index,self.tokens[self.index-1][0],self.current.getTokenVal())

    def step(self):
        if self.current.isEmpty():
            self.current = self.current.step()
        else:
            self.current = self.current.firstChild()

    def preToken(self):
        if self.index - 2 >0 :
            return self.tokens[self.index-2][1]
        else:
            return None

    def nextToken(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index][1]
        else:
            return None
    def currentToken(self):
        if self.index - 1 > 0:
            return self.tokens[self.index-1][1]
        else:
            return None

    def procDec(self):
        # print(self.symTable)
        sym = Symbol(kind="procDec")
        paramList = SymbolTable()
        self.step()
        while not self.current.isTokenType("ProcBody"):
            # print(self.current.father.father)
            self.updateIndex()
            if self.current.isTokenType("ID"):
                if self.current.father.isTokenType("ProcName"):
                    name = self.current.getTokenVal()
                    # print("debug",name)
                    if name in self.symTable:
                        self.error = True
                        self.errorMessage = semanticError.duplicateDefine
                        self.printError()
                        # return
                    else:
                        sym.name = name
            # elif self.
            elif self.current.father.father.isTokenType("TypeName"):
                typeName = self.current.getTokenType()
                # print("*********",self.symTable)
                # if typeName == "INTEGER" or typeName == "CHAR":
                self.step()
                while True:
                    self.updateIndex()
                    if self.current.isTokenType("ε") and self.current.father.isTokenType("FidMore"):
                        break
                    elif self.current.isTokenType("ID"):
                        param = Symbol()
                        param.name = self.current.getTokenVal()
                        param.kind = "varDec"
                        param.type = typeName
                        if param.name not in self.symTable:
                            paramList.add(param)
                        else:
                            self.error = True
                            self.errorMessage = semanticError.duplicateDefine
                            self.printError(sym)
                    self.step()

            elif  self.current.isTokenType(")") and self.tokens[self.index][0] == ';':
                sym.param = paramList
                sym.level = self.symLevel
                # print("ddd",paramList)
                if sym.name != None:
                    self.symTable.add(sym)
                    self.scope.append(SymbolTable())
                    self.symTable = self.scope[-1]
                    self.symTable.add(sym)
                    # 函数 的参数也是符号信息
                    for i in paramList:
                        self.symTable.add(i)
                    # print("ddd",self.symTable)
                # self.symTable =self.scope[0]

            elif self.current.isTokenType("TypeDecList"):
                # 这里有递归的过程定义部分
                # print(self.symTable)
                self.typeDec()
                # if self.error:
                #     return
            elif self.current.isTokenType("VarDecList"):
                # print("debug",self.symTable)
                self.varDec()
                # if self.error:
                #     return
            elif self.current.isTokenType("ProcDeclaration"):
                self.symLevel += 1

                self.procDec()
                # if self.error:
                #     return
            self.step()
        self.updateIndex()
        self.symTable = self.scope[0]
    def varDec(self):
        # print("sym:",self.symTable)
        sym = Symbol(kind="varDec")
        self.step()
        idType = ""
        while True:
            self.updateIndex()

            if self.current.isTokenType("ID"):
                if self.current.father.isTokenType("VarIdList"):
                    sym.name = self.current.getTokenVal()
                    # print(sym)
                    if sym.name in self.symTable:
                        self.error = True
                        self.errorMessage = semanticError.duplicateDefine
                        self.printError()
                    else:
                        self.symTable.add(sym)
                    sym = Symbol(kind="varDec",type=idType)
            elif self.current.father.father.isTokenType("TypeName"):
                idType = self.current.getTokenVal()
                # if currentId in self.symTable:
                #     sym.type = self.symTable.get(currentId).type
                # else:
                #     # print("error in line %s  " % (tokens[self.index][2]) + currentId + "未定义\n", )
                #     self.errorMessage = semanticError.unDefined
                #     self.error = True
                #     self.printError()
                self.step()
                while True:
                    self.updateIndex()
                    if self.current.isTokenType("ε") and self.current.father.isTokenType("VarIdMore"):
                        break
                    elif self.current.isTokenType("ID"):
                        sym = Symbol()
                        sym.name = self.current.getTokenVal()
                        sym.kind = "varDec"
                        sym.type = idType
                        # print("cuurent ",sym)
                        if sym.name not in self.symTable:
                            self.symTable.add(sym)
                        else:
                            self.error = True
                            self.errorMessage = semanticError.duplicateDefine
                            self.printError(sym)
                    self.step()

            elif self.current.isTokenType("ε") and self.current.father.isTokenType("VarDecMore"):
                break
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
                            # print()
                            # print("low :",self.current.getTokenVal())
                            if low < 0:
                                self.error = True
                                self.errorMessage = semanticError.arrayDefineError
                                self.printError()
                                # print("数组下界小于零")
                                # return
                            else:
                                array.low = low
                        elif self.current.father.isTokenType("Top"):
                            top = int(self.current.getTokenVal())
                            # print("top:",top)
                            if top <= array.low:
                                self.error = True
                                self.errorMessage = semanticError.arrayDefineError
                                self.printError()
                                # print("数组上界小于下界")
                                # return
                            else:
                                array.top = top
                    self.step()
                self.updateIndex()
                array.element = self.current.getTokenType()
                self.step()
                while not self.current.isTokenType(";"):
                    self.updateIndex()
                    if self.current.isTokenType("ID"):
                        tmpSym = Symbol(kind="varDec")
                        tmpSym.name = self.current.getTokenVal()
                        tmpSym.type = array
                        # print(self.errorMessage)
                        # print("debug:",array)
                        if tmpSym.name not in self.symTable and self.errorMessage != semanticError.arrayDefineError:
                            self.symTable.add(tmpSym)
                    self.step()
                self.updateIndex()
                # sym.type = array
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
                                    self.printError()
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
                                    # print("low :",self.current.getTokenVal())
                                    if low < 0:
                                        self.error = True
                                        self.errorMessage = semanticError.arrayDefineError
                                        self.printError()
                                        # print("数组下界小于零")
                                        # return
                                    else:
                                        array.low = low
                                elif self.current.father.isTokenType("Top"):
                                    top = int(self.current.getTokenVal())
                                    # print("top:",top)
                                    if top <= array.low:
                                        self.error = True
                                        self.errorMessage = semanticError.arrayDefineError
                                        self.printError()
                                        # print("数组上界小于下界")
                                        # return
                                    else:
                                        array.top = top
                            self.step()
                        # self.updateIndex()
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
                                    self.printError()
                                    # print("结构体内部出现重复定义")
                                    # return
                            self.step()
                        self.updateIndex()
                    self.step()
                self.updateIndex()
                # pass
                record.fieldList = fieldList
                self.step()
                while not self.current.isTokenType(";"):
                    self.updateIndex()
                    if self.current.isTokenType("ID"):
                        tmpSym = Symbol(kind="varDec")
                        tmpSym.name = self.current.getTokenVal()
                        tmpSym.type = record
                        if tmpSym.name not in self.symTable:
                            self.symTable.add(tmpSym)
                    self.step()
                self.updateIndex()
                # sym.type = record
            self.step()
        self.updateIndex()
        # if self.current.isTokenVal(";") and not self.error:
        #     self.symTable.add(sym)
        #     self.current = self.current.step()
        #     self.index += 1
    def typeDec(self):
        sym = Symbol(kind="typeDec")
        self.step()
        while True:
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
                        self.printError()
                        # return
            elif self.current.isTokenType("ε") and self.current.father.isTokenType("TypeDecMore"):
                break
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
                                self.printError()
                                # print("数组下界小于零")
                                # return
                            else:
                                array.low = low
                        elif self.current.father.isTokenType("Top"):
                            top = int(self.current.getTokenVal())
                            # print("top:",top)
                            if top <= array.low:
                                self.error = True
                                self.errorMessage = semanticError.arrayDefineError
                                self.printError()
                                # print("数组上界小于下界")
                                # return
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
                                    self.printError()
                                    # print("结构体内部出现重复定义")
                                    # return
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
                                        self.printError()
                                        # print("数组下界小于零")
                                        # return
                                    else:
                                        array.low = low
                                elif self.current.father.isTokenType("Top"):
                                    top = int(self.current.getTokenVal())
                                    # print("top:",top)
                                    if top <= array.low:
                                        self.error = True
                                        self.errorMessage = semanticError.arrayDefineError
                                        self.printError()
                                        # print("数组上界小于下界")
                                        # return
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
                                    self.printError()
                                    # print("结构体内部出现重复定义")
                                    # return
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

    def assignCheck(self,left,right):
        if left == "CHAR":
            return left == right
        elif left == "INTEGER":
            return right == "INTEGER" or right == "INTC"
        else:
            return left == right

    def condationExp(self):
        """
        relexp
        :return:
        """
        left,_ = self.exp()
        if self.errorMessage == semanticError.unDefined:
            self.printerror = False
        right,_ = self.exp()
        if self.errorMessage == semanticError.unDefined:
            self.printerror = False
        if not self.assignCheck(left,right):
            self.error = True
            self.errorMessage = semanticError.typeMatchError % (left, right)
            self.printError()
        self.printerror = True
        # return
        # pass
    def callStm(self):
        """
        过程调用
        :return:
        """
        procSym = None
        paramList = None
        recivedParam = []
        while True:
            if self.current.isTokenType("ε"):
                if self.current.father.isTokenType("ActParamMore") or self.current.father.isTokenType("ActParamList"):
                    break
            elif self.current.isTokenType("ID") and self.current.father.isTokenType("Stm"):
                currentId = self.current.getTokenVal()
                for symTable in self.scope[::-1]:
                    if currentId in symTable:
                        procSym = symTable.get(currentId)
                        # print("procCall",procSym)
                        if procSym.kind != "procDec":
                            # procSym = None
                            self.error = True
                            self.errorMessage = semanticError.procedureCallError
                            self.printError()
                            self.printerror = False
                        else:
                            paramList = procSym.param
                if procSym == None:
                    self.error = True
                    self.errorMessage = semanticError.unDefined
                    self.printError()
                    self.printerror = False
            elif self.current.isTokenType("Exp") and self.current.father.isTokenType("ActParamList"):
                expType,_ = self.exp()
                # print(expType)
                recivedParam.append(expType)
            else:
                pass
            self.step()
            self.updateIndex()
        # if self.errorMessage != semanticError.unDefined or not self.error:
        #     self.printerror = True
        # print(procSym)
        # print(recivedParam)
        # print(procSym)
        if procSym != None and procSym.kind == "procDec":
            if len(recivedParam) != len(paramList):
                self.error = True
                self.errorMessage = semanticError.paramNumError%(len(paramList),len(recivedParam))
                self.printError(procSym)
            else:
                for idx in range(len(paramList)):
                    expectType = paramList[index].type
                    gotType = recivedParam[index]
                    # print(gotType)
                    if not self.assignCheck(expectType,gotType):
                        self.error = True
                        self.errorMessage = semanticError.typeMatchError%(expectType,gotType)
                        self.printError()
            self.printerror = True


    def variable(self):
        """

        :return: varType(integer or char),value, symPtr(use to update value)
        """
        # self.step()
        sym = Symbol()

        invalid = (None,None,None)
        currentVarType = None
        currentSym = None
        # print(self.current.getTokenVal())

        while True:
            # self.updateIndex()
            # print("token: ",self.current.getTokenVal())
            if self.current.isTokenType("ID"):

                currentId = self.current.getTokenVal()
                # print("xx",currentId)
                if self.current.father.isTokenType("Stm") or self.current.father.isTokenType("Variable"):
                    for symTable in self.scope[::-1]:
                        if currentId in symTable:
                            sym = symTable.get(currentId)
                            if currentSym == None:
                                currentSym = sym
                            if sym.kind != "varDec":
                                self.error = True
                                self.errorMessage = semanticError.typeKindMatchError % ("varDec",sym.kind)
                                self.printError()
                                self.printerror = False
                                # return invalid
                            try:
                                currentVarType = sym.type.kind
                            except:
                                currentVarType = sym.type
                            currentVarKind = sym.kind
                            currentVarValue = sym.value
                            break
                    # print(currentSym,currentId)
                    if currentSym == None:
                        # print("undefined")
                        self.error = True
                        self.errorMessage = semanticError.unDefined
                        # print(currentId,self.currentToken(),self.current.getTokenType())
                        self.printError()
                        self.printerror = False
                        break
                        # return invalid
                elif self.current.father.isTokenType("FieldVar"):
                    # print(self.currentVariType)
                    if currentVarType != "recordType":
                        self.error = True
                        self.errorMessage = semanticError.typeMatchError%("recordType",currentVarType)
                        self.printError()
                        # return invalid
                    else:
                        # print(sym.type.fieldList,currentId)
                        if currentId not in sym.type.fieldList:
                            self.error = True
                            self.errorMessage = semanticError.unDefined
                            self.printError()
                            # return invalid
                        else:

                            sym = sym.type.fieldList.get(currentId)
                            # print(sym,self.nextToken())
                            if self.nextToken() != ".":
                                currentSym = sym
                            # print(sym.type)
                            # print(sym, self.nextToken(),currentSym)
                            if sym.type in ["INTEGER","CHAR"]:
                                currentVarType = sym.type
                            else:
                                currentVarType = sym.type.kind


            elif self.current.isTokenType("Exp") and self.currentToken() == "[":
                if currentVarType != "arrayType":
                    self.error = True
                    self.errorMessage = semanticError.typeKindMatchError%("arrayType",currentVarType)
                else:
                    expType,expValue = self.exp()
                    # print(expType)
                    if expType != "INTC":
                        self.error = True
                        self.errorMessage = semanticError.typeMatchError%("INTC",expType)
                        self.printError()
                    else:
                        return (currentSym, currentSym.type.element, None)
                        # return invalid
                    # ok
            elif self.current.isTokenType("ε") and self.current.father.isTokenType("OtherTerm"):
                break
            # else:
            #     pass
            self.step()
            self.updateIndex()
        # print(currentSym)
        if currentSym:
            return (currentSym,currentSym.type,None)
        else:
            return invalid

    def exp(self):
        """
        只做了静态语义分析，只需要知道exp的类型即可，value为动态语义分析保留
        :return: INTC value ()
        """
        # print(self.currentToken())
        self.step()

        while True:
            self.updateIndex()
            if (self.current.isTokenType("ε") or self.current.isTokenType(")")) and self.current.father.isTokenType("OtherTerm"):
                break
            elif self.current.isTokenType("Variable"):
                var,varType,_ = self.variable()
                # print(var.name)
                # print(var,varType)
                if varType != "INTEGER":
                    return varType,None
            elif self.current.isTokenType("Exp"):
                expType,_ = self.exp()
                # print(expType)
                if expType != "INTC":
                    self.error = True
                    self.errorMessage = semanticError.typeMatchError%("INTC",expType)
                    self.printError()
                    self.printerror = False
                    return expType,None
            elif self.current.isTokenType("INTC"):
                break
            # elif self.current.isTokenType("StmMore"):
            #     break

            # elif self.current.isTokenType("INTC"):
            self.step()
        # self.updateIndex()
        self.printerror = True
        return "INTC",None

    def printError(self,var=None):
        # if self.errorMessage == semanticError.unDefined:
        if self.printerror:
            if var != None:
                print("Error in line: %d\tDetail: %s %s %s"%(self.tokens[self.index-1][-1],var.kind,var.name,self.errorMessage))
            else:
                print("Error in line: %d\tDetail: %s %s %s"%(self.tokens[self.index-1][-1],self.tokens[self.index-1][0],self.currentToken(),self.errorMessage))

    def inputStm(self):
        self.step()
        while True:
            self.updateIndex()
            if self.current.isTokenType("ID"):
                currentId = self.current.getTokenVal()
                for symTable in self.scope:
                    if currentId in symTable:
                        return
                self.error = True
                self.errorMessage = semanticError.unDefined
                self.printError()
                break
            self.step()
        self.updateIndex()

    def outputStm(self):
        self.step()
        while True:
            self.updateIndex()
            # if self.current.isTokenType("ε") and self.current.father.isTokenType("OtherTerm"):
            if self.current.isTokenType("ε") and self.nextToken() == ")":
                # print("debug",self.currentToken(),self.preToken())
                break
            elif self.current.isTokenType("Exp"):
                self.exp()
            self.step()
        self.updateIndex()

    def returnStm(self):
        self.step()
        while True:
            self.updateIndex()
            if self.current.isTokenType("ε") and self.current.father.isTokenType("OtherTerm"):
                break
            elif self.current.isTokenType("Exp"):
                self.exp()
            self.step()
            # self.updateIndex()
        self.updateIndex()

    def analyze(self):
        self.current = self.root.firstChild()
        while self.current.getId() != 0:
            # print(self.currentToken(),self.current.getTokenVal())
            self.updateIndex()
            if self.current.isTokenType("TypeDecList"):
                self.typeDec()
            elif self.current.isTokenType("VarDecList"):
                self.varDec()
                # print(self.symTable)
            elif self.current.isTokenType("ProcDeclaration"):
                # scope 栈 需要更新
                # print("before",self.symTable)
                self.procDec()
                # print("after",self.symTable)
            elif self.current.isTokenType("LoopStm"):
                self.condationExp()
            elif self.current.isTokenType("ConditionalStm"):
                self.condationExp()
            elif self.current.isTokenType("InputStm"):
                # self.assignStm()
                self.inputStm()
                # pass
            elif self.current.isTokenType("OutputStm"):
                self.outputStm()
                # pass
            elif self.current.isTokenType("ReturnStm"):
                self.returnStm()
                # pass
            elif self.current.isTokenType("ID") and self.current.father.isTokenType("Stm"):
                print("xx",self.currentToken())
                if self.nextToken() == "(":
                    self.callStm()
                else:

                    var,varType,varKind= self.variable()
                    # print(var)
                    # print(self.currentToken())
                    if self.errorMessage == semanticError.unDefined:
                        self.printerror = False
                    # print(self.errorMessage)
                    expType,_ = self.exp()
                    # print(expType)
                    if not self.assignCheck(varType,expType):
                        # print("type do not match",self.currentToken())
                        self.error = True
                        self.errorMessage = semanticError.typeMatchError%(varType,expType)
                        self.printError(var)
                    self.printerror = True
                    self.errorMessage = ""

            self.step()
        # if self.error:
        #     self.printError()





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
    print("*"*100)
    print(analyzer.scope)
    # print(analyzer.symTable)

