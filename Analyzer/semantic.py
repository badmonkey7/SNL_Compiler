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
    procedureCallError  = "%s %s can not be called"
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
                    self.symTable = curSymTab
                    break
                else:
                    self.stepInto("ProcName")
                    self.step()
                    procName = self.current.getTokenVal()
                    proc = Symbol(kind="procDec",name=procName)
                    symTable = SymbolTable()
                    symTable.add(proc)
                    procError = False
                    if procName in self.symTable:
                        procError = True
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
                    self.stepInto("ProcDecMore")


    def stmList(self):
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
        pass

    def variable(self):
        pass







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
    print(analyzer.scope)
    # print(analyzer.symTable)

