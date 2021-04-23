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
    duplicateDefine = "duplicate defined"
    unDefinedVar = "undefined variable"
    unDefinedType = "undefined type"
    undefinedField = "undefined field"
    invalidAssignLeft = "invalid assignment %s is not variable"
    invalidAssignRight = "invalid assignment %s is not %s type"
    # arrayOut = "index out of array bound"
    # invalidMember = "invalid member access"
    # assignmentTypeError = "invalid assginment variable type do not match"
    # assignmentVariableError = "invalid assignment; the left side of the assginment is not variable"
    paramTypeError = "procedure param type do not match expect %s got %s"
    paramNumError = "procedure param number do not match expect %d params got %d params"
    procedureCallError  = "can not be called"
    boolError = "conditon must be an boolean value"
    typeMatchError = "Uncompatable type  expect %s got %s"
    arrayDefineError = "invalid array define"
    kindMatchError = "unexpect type expect %s got %s"


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
        self.errorLine = 0

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
        self.updateIndex()
    def stepInto(self,tokenType):
        while not self.current.isTokenType(tokenType):
            self.step()

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
    def currenLine(self):
        if self.index - 1 > 0:
            return self.tokens[self.index-1][-1]
        else:
            return None
    def currentToken(self):
        if self.index - 1 > 0:
            return self.tokens[self.index-1][1]
        else:
            return None

    def printError(self,var=None):
        if not self.printerror and self.tokens[self.index-1][-1] == self.errorLine:
            pass
        else:
            if var != None:
                print("Error in line: %d\tDetail: %s %s %s"%(self.tokens[self.index-1][-1],var.decKind,var.name,self.errorMessage))
            else:
                print("Error in line: %d\tDetail: %s %s %s"%(self.tokens[self.index-1][-1],self.tokens[self.index-1][0],self.currentToken(),self.errorMessage))

    def assignTypeCheck(self,leftType,rightType):
        if leftType == "INTEGER":
            return rightType == "INTEGER" or rightType == "INTC"
        else:
            return leftType == rightType


    def analyze(self):
        self.current = self.root.firstChild()
        self.programHead()
        self.declarePart()
        self.programBody()

    def programHead(self):
        self.stepInto("ProgramName")
        self.stepInto("ID")



    def declarePart(self):
        self.stepInto("DeclarePart")
        self.typeDec()
        self.varDec()
        self.procDec()
        pass

    def programBody(self):
        self.stepInto("BEGIN")
        self.stmList()
        self.stepInto("END")
        # pass

    def typeDec(self):
        self.stepInto("TypeDec")
        self.step()
        if self.current.isTokenType("ε"):
            # 没有类型定义部分
            return
        else:
            self.stepInto("TypeDecList")
            while True:
                if self.current.isTokenType("TypeDecMore") and self.current.firstChild().isTokenType("ε"):
                    break
                else:
                    self.stepInto("TypeId")
                    self.stepInto("ID")
                    sym = Symbol(kind="typeDec",name=self.current.getTokenVal())
                    # self.stepInto("=")
                    typeName = self.typeName()
                    if typeName != None:
                        sym.typePtr = typeName
                        if sym.name not in self.symTable:
                            self.symTable.add(sym)
                        else:
                            self.error = True
                            self.errorMessage = semanticError.duplicateDefine%(sym.name)
                            self.printError()
                    else:
                        pass
                    self.stepInto("TypeDecMore")
                # self.step()



        # type = self.typeName()
        # print("debug",type.type)

        pass

    def varDec(self):
        self.stepInto("VarDec")
        self.step()
        if self.current.isTokenType("ε"):
            return
        else:
            self.stepInto("VarDecList")
            while True:
                if self.current.isTokenType("VarDecMore") and self.current.firstChild().isTokenType("ε"):
                    break
                else:
                    # pass
                    typeName = self.typeName()
                    self.stepInto("VarIdList")
                    while True:
                        if self.current.isTokenType("VarIdMore") and self.current.firstChild().isTokenType("ε"):
                            break
                        else:
                            sym = Symbol(kind="varDec",type=typeName)
                            self.stepInto("ID")
                            sym.name = self.current.getTokenVal()
                            if sym.name in self.symTable:
                                # 重复定义
                                self.error = True
                                self.errorMessage = semanticError.duplicateDefine
                                self.printError()
                            else:
                                self.symTable.add(sym)

                            self.stepInto("VarIdMore")
                    self.stepInto("VarDecMore")
        # pass

    def procDec(self):
        curSymTab = self.symTable
        self.stepInto("ProcDec")
        self.step()
        if self.current.isTokenType("ε"):
            return
        else:
            while True:
                if self.current.isTokenType("ProcDecMore") and self.current.firstChild().isTokenType("ε"):
                    # self.symTable = curSymTab
                    break
                else:
                    self.stepInto("ProcName")
                    self.step()
                    procName = self.current.getTokenVal()
                    proc = Symbol(kind="procDec",name=procName,param=SymbolTable())
                    symTable = SymbolTable()
                    symTable.add(proc)
                    procError = False
                    if procName in self.symTable:
                        procError = True
                        self.error = True
                        self.errorMessage = semanticError.duplicateDefine
                        self.printError()
                    else:
                        self.symTable.add(proc)
                        self.scope.append(symTable)
                        self.symTable = self.scope[-1]
                    self.stepInto("ParamList")
                    self.step()
                    if self.current.isTokenType("ε"):
                        pass
                    else:
                        while True:
                            if self.current.isTokenType("ParamMore") and self.current.firstChild().isTokenType("ε"):
                                break
                            else:
                                self.stepInto("Param")
                                typeName = self.typeName()
                                self.stepInto("FormList")
                                while True:
                                    if self.current.isTokenType("FidMore") and self.current.firstChild().isTokenType("ε"):
                                        break
                                    else:
                                        self.stepInto("ID")
                                        param = Symbol(kind="varDec",name=self.current.getTokenVal(),type=typeName)
                                        proc.param.add(param)
                                        if not procError:
                                            if param.name not in self.symTable:
                                                self.symTable.add(param)
                                            else:
                                                # 参数重名
                                                self.error = True
                                                self.errorMessage = semanticError.duplicateDefine
                                                self.printError()
                                        self.stepInto("FidMore")
                                self.stepInto("ParamMore")
                    self.stepInto("ProcDecPart")
                    self.declarePart()
                    self.stepInto("ProcBody")
                    self.programBody()
                    self.symTable = curSymTab
                    self.stepInto("ProcDecMore")


    def stmList(self):
        self.stepInto("Stm")
        while True:
            if self.current.isTokenType("StmMore") and self.current.firstChild().isTokenType("ε"):
                break
            else:
                self.stepInto("Stm")
                # print("debug",self.current.getTokenType())
                curStm = self.current.firstChild().getTokenType()
                # if curStm == ";":

                if curStm == "ConditionalStm":
                    self.conditionalStm()
                elif curStm == "LoopStm":
                    self.loopStm()
                elif curStm == "InputStm":
                    self.inputStm()
                elif curStm == "OutputStm":
                    self.outputStm()
                elif curStm == "ReturnStm":
                    self.returnStm()
                elif curStm == "ID":
                    # ID
                    self.stepInto("ID")
                    idName = self.current.getTokenVal()
                    self.stepInto("AssCall")
                    self.step()
                    decision = self.current.getTokenType()
                    varError = True
                    var = None
                    for symTable in self.scope[::-1]:
                        if idName in symTable:
                            varError = False
                            var = symTable.get(idName)
                    if varError:
                        self.error = True
                        self.errorMessage = semanticError.unDefinedVar
                        self.printError()
                    if decision == "AssignmentRest":
                        # 赋值语句
                        varType = None
                        self.stepInto("VariMore")
                        self.step()
                        choice = self.current.getTokenType()
                        # print("!!!!!",choice)
                        if choice == "ε":
                            if not varError:
                                varType = var.typePtr.type
                                # print("!!!",varType)
                            # pass
                        elif choice == "[":
                            indType,indVal = self.expresion()
                            if indType not in ["INTEGER","INTC"]:
                                self.error = True
                                self.errorMessage = semanticError.typeMatchError%("INTC",indType)
                                self.printError()
                            else:
                                varType = var.typePtr.element.type
                        elif choice == ".":
                            self.stepInto("FieldVar")
                            self.stepInto("ID")
                            fieldName = self.current.getTokenVal()
                            if var.typePtr.type != "recordType":
                                # 访问非结构体变量
                                self.error = True
                                self.errorMessage = semanticError.typeMatchError % ("recordType", var.typePtr.type)
                                self.printError(var)
                            else:
                                # 成员变量未定义
                                if fieldName not in var.typePtr.fieldList:
                                    self.error = True
                                    self.errorMessage = semanticError.undefinedField
                                    self.printError()
                                else:
                                    #
                                    field = var.typePtr.fieldList.get(fieldName)
                                    self.stepInto("FieldVarMore")
                                    self.step()
                                    if self.current.isTokenType("ε"):
                                        varType = field.typePtr.type
                                        # print("!!!",varType)
                                        pass
                                    elif self.current.isTokenType("["):
                                        indType, indVal = self.expresion()
                                        if indType not in ["INTEGER", "INTC"]:
                                            self.error = True
                                            self.errorMessage = semanticError.typeMatchError % ("INTC", indType)
                                            self.printError()
                                        else:
                                            varType = field.typePtr.element.type
                        self.stepInto(":=")
                        rightType,rigthVal = self.expresion()
                        # print("debug",var,varType,rightType)
                        if varType and not varError:
                            if not self.assignTypeCheck(varType,rightType):
                                self.error = True
                                self.errorMessage = semanticError.typeMatchError%(varType,rightType)
                                self.printError()

                        # varType = var.

                        # pass
                    elif decision == "CallStmRest":
                        # 过程调用
                        self.stepInto("ActParamList")
                        actParamList = []
                        while True:
                            if self.current.isTokenType("ActParamMore") and self.current.firstChild().isTokenType("ε"):
                                break
                            elif self.current.isTokenType("ActParamList") and self.current.firstChild().isTokenType("ε"):
                                break
                            else:
                                expType,expVal = self.expresion()
                                actParamList.append(expType)
                                self.stepInto("ActParamMore")
                        actParamLen = len(actParamList)
                        paramList = SymbolTable()
                        if not varError:
                            # 标识符存在
                            # print(var)
                            if var.decKind != "procDec":
                                # print("debug",var)
                                # 非过程标识符
                                self.error = True
                                self.errorMessage = semanticError.procedureCallError
                                self.printError(var)
                            else:
                                # 过程标识符存在
                                # print(var.)
                                paramList = var.param
                                paramLen = len(paramList)
                                if paramLen != actParamLen:
                                    # num invalid
                                    self.error = True
                                    self.errorMessage = semanticError.paramNumError%(paramLen,actParamLen)
                                    self.printError(var)
                                else:
                                    # param type do not match
                                    for i in range(paramLen):
                                        expect = paramList[i].typePtr.type
                                        got = actParamList[i]
                                        if not self.assignTypeCheck(expect,got):
                                            self.error = True
                                            self.errorMessage = semanticError.typeMatchError%(expect,got)
                                            self.printError()
                # print(self.currenLine())
                self.stepInto("StmMore")

        pass
    def typeName(self):
        self.stepInto("TypeName")
        # self
        """
        三种情况 ID BaseType StructureType
        """
        choice  = self.current.firstChild().getTokenType()
        self.stepInto(choice)
        if choice == "ID":
            idName = self.current.getTokenVal()
            if idName in self.symTable:
                sym = self.symTable.get(idName)
                return sym.typePtr
            else:
                # 未定义 type
                self.error = True
                self.errorMessage = semanticError.unDefinedType
                self.printError()
                self.printerror = False
                return None
            # pass
        elif choice == "BaseType":
            return self.baseType()
            # pass
        elif choice == "StructureType":
            """
            两种情况 ArrayType 或者  RecType
            """
            structType = self.current.firstChild().getTokenType()
            self.stepInto(structType)
            if structType == "ArrayType":
                return self.arrayType()
                # pass
            elif structType == "RecType":
                fieldList = SymbolTable()
                self.stepInto("RECORD")
                while True:
                    if self.current.isTokenType("FieldDecMore") and self.current.firstChild().isTokenType("ε"):
                        break
                    else:
                        self.stepInto("FieldDecList")
                        fieldTypeKind = self.current.firstChild().getTokenType()
                        fieldType = None
                        if fieldTypeKind == "BaseType":
                             fieldType = self.baseType()
                        elif fieldTypeKind == "ArrayType":
                            fieldType = self.arrayType()
                        while True:
                            if self.current.isTokenType("IdMore") and self.current.firstChild().isTokenType("ε"):
                                break
                            else:
                                self.stepInto("IdList")
                                self.stepInto("ID")
                                sym = Symbol(kind="varDec",type=fieldType,name=self.current.getTokenVal())
                                if sym.name in fieldList:
                                    # 成员变量重复定义
                                    self.error = True
                                    self.errorMessage = semanticError.duplicateDefine%(sym.name)
                                    self.printError(sym)
                                else:
                                    fieldList.add(sym)
                                self.stepInto("IdMore")
                        self.stepInto("FieldDecMore")
                        # print("debug", self.current)

                    # self.step()
                self.stepInto("END")
                recType = RecordType(fieldList=fieldList)
                return recType
    def arrayType(self):
        self.stepInto("ArrayType")
        self.stepInto("Low")
        self.stepInto("INTC")
        low = self.current.getTokenVal()
        self.stepInto("Top")
        self.stepInto("INTC")
        top = self.current.getTokenVal()
        self.stepInto("BaseType")
        self.step()
        bType = BaseType(kind=self.current.getTokenType())
        typePtr = ArrayType(sz=top - low, low=low, top=top, element=bType)
        if low < 0 or (low >= top):
            # 非法数组定义
            self.error = True
            self.errorMessage = semanticError.arrayDefineError
            self.printError()
            return None
        else:
            return typePtr
    def baseType(self):
        self.stepInto("BaseType")
        self.step()
        typePtr = BaseType(kind=self.current.getTokenType())
        return typePtr
    def expresion(self):
        """

        :return: 类型 和 数值
        """
        self.stepInto("Exp")
        leftType,leftVal = self.term()
        self.stepInto("OtherTerm")
        expError = False
        while True:
            if self.current.isTokenType("OtherTerm") and self.current.firstChild().isTokenType("ε"):
                break
            else:
                self.stepInto("Exp")
                rightType,rightVal = self.expresion()
                if not self.assignTypeCheck(leftType,rightType):
                    expError = True
                    self.error = True
                    self.errorMessage = semanticError.typeMatchError%(leftType,rightType)
                    self.printError()
                self.stepInto("OtherTerm")
        if expError:
            leftType,leftVal = None,None
        return leftType,leftVal
        # pass
    def term(self):
        self.stepInto("Term")
        leftType,leftVal = self.factor()
        self.stepInto("OtherFactor")
        termError = False
        while True:
            if self.current.isTokenType("OtherFactor") and self.current.firstChild().isTokenType("ε"):
                break
            else:
                self.stepInto("Term")
                rightType,rightVal = self.factor()
                if not self.assignTypeCheck(leftType,rightType):
                    termError = True
                    self.error = True
                    self.errorMessage = semanticError.typeMatchError%(leftType,rightType)
                    self.printError()
                self.stepInto("OtherFactor")
        if termError:
            leftType,leftVal = (None,None)
        return leftType,leftVal
    def factor(self):
        self.stepInto("Factor")
        self.step()
        choice = self.current.getTokenType()
        if choice == "(":
            return self.expresion()
        elif choice == "INTC":
            return "INTC",self.current.getTokenVal()
        elif choice == "Variable":
            return self.variable()
    def variable(self):
        """

        :return: 类型和数值
        """
        self.stepInto("Variable")
        self.stepInto("ID")
        varName = self.current.getTokenVal()
        var = None
        varError = False
        for symTable in self.scope[::-1]:
            if varName in symTable:
                var = symTable.get(varName)
        if var == None:
            varError = True
            self.error = True
            self.errorMessage = semanticError.unDefinedVar
            self.printError()
        self.stepInto("VariMore")
        self.step()
        choice = self.current.getTokenType()
        if choice == "ε":
            if varError:
                return None,None
            else:
                # 可能会返回 数组 和 结构ti类型
                return var.typePtr.type,var.value
        elif choice == "[":
            return self.expresion()
        elif choice == ".":
            self.stepInto("FieldVar")
            self.stepInto("ID")
            fieldName = self.current.getTokenVal()
            if var.typePtr.type != "recordType":
                # 访问非结构体变量
                self.error = True
                self.errorMessage = semanticError.typeMatchError%("recordType",var.typePtr.type)
                self.printError(var)
            else:
                # 成员变量未定义
                if fieldName not in var.typePtr.fieldList:
                    self.error = True
                    self.errorMessage = semanticError.undefinedField
                    self.printError()
                    self.stepInto("FieldVarMore")
                    self.step()
                    if self.current.isTokenType("ε"):
                        return None,None
                    elif self.current.isTokenType("["):
                        self.expresion()
                        return None,None
                else:
                    #
                    field = var.typePtr.fieldList.get(fieldName)
                    self.stepInto("FieldVarMore")
                    self.step()
                    if self.current.isTokenType("ε"):
                        return field.typePtr.type,field.value
                    elif self.current.isTokenType("["):
                        indexType,indexVal =  self.expresion()
                        if indexType not in ["INTEGER","INTC"]:
                            self.error = True
                            self.errorMessage = semanticError.typeMatchError%("INTC",indexType)
                            self.printError()
                            return None,None
                        else:
                            return field.typePtr.element.type,None




            # if fieldName not in var
        # pass
    def conditionalStm(self):
        self.stepInto("IF")
        condition = self.relExp()
        # bool 值判定 ？？什么意思
        self.stepInto("THEN")
        self.stmList()
        self.stepInto("ELSE")
        self.stmList()
        self.stepInto("FI")
        # pass
    def loopStm(self):
        self.stepInto("WHILE")
        condition = self.relExp()
        self.stepInto("DO")
        self.stmList()
        self.stepInto("ENDWH")
        pass
    def inputStm(self):
        self.stepInto("InputStm")
        self.stepInto("READ")
        self.stepInto("Invar")
        self.stepInto("ID")
        idName = self.current.getTokenVal()
        if idName not in self.symTable:
            self.error = True
            self.errorMessage = semanticError.unDefinedVar
            self.printError()
        # pass
    def outputStm(self):
        self.stepInto("OutputStm")
        self.stepInto("WRITE")
        self.expresion()
        # pass
    def returnStm(self):
        self.stepInto("ReturnStm")
        self.stepInto("RETURN")
        self.expresion()
        # pass
    def relExp(self):
        """

        :return: 返回是否是bool值
        """
        self.stepInto("RelExp")
        leftType,leftVal = self.expresion()
        self.stepInto("CmpOp")
        rightType,leftVal = self.expresion()
        if not self.assignTypeCheck(leftType,rightType):
            expError = True
            self.error = True
            self.errorMessage = semanticError.typeMatchError % (leftType, rightType)
            self.printError()
            return False
        else:
            return True







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
    # print("*"*100)
    # print(analyzer.scope)
    # print(analyzer.symTable)

