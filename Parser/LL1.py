'''
@author: badmonkey
@software: PyCharm
@file: LL1.py
@time: 2021/4/14 上午10:34
'''
# 文法
grammar = {
    # 起始符
    "S":"Program",
    # 产生式
    "P":{
        'Program': {0: ['ProgramHead', 'DeclarePart', 'ProgramBody']},
        'ProgramHead': {0: ['PROGRAM', 'ProgramName']},
         'ProgramName': {0: ['ID']},
        'DeclarePart': {0: ['TypeDec', 'VarDec', 'ProcDec']},
         'TypeDec': {0: ['ε'], 1: ['TypeDeclaration']},
        'TypeDeclaration': {0: ['TYPE', 'TypeDecList']},
         'TypeDecList': {0: ['TypeId', '=', 'TypeName', ';', 'TypeDecMore']},
         'TypeDecMore': {0: ['ε'], 1: ['TypeDecList']},
        'TypeId': {0: ['ID']},
         'TypeName': {0: ['BaseType'], 1: ['StructureType'], 2: ['ID']},
        'BaseType': {0: ['INTEGER'], 1: ['CHAR']},
         'StructureType': {0: ['ArrayType'], 1: ['RecType']},
         'ArrayType': {0: ['ARRAY', '[','Low','..','Top', ']', 'OF', 'BaseType']},
        'Low': {0: ['INTC']},
        'Top': {0: ['INTC']},
         'RecType': {0: ['RECORD', 'FieldDecList', 'END']},
         'FieldDecList': {0: ['BaseType', 'IdList', ';', 'FieldDecMore'],
                          1: ['ArrayType', 'IdList', ';', 'FieldDecMore']},
         'FieldDecMore': {0: ['ε'], 1: ['FieldDecList']},
        'IdList': {0: ['ID', 'IdMore']},
         'IdMore': {0: ['ε'], 1: [',', 'IdList']},
        'VarDec': {0: ['ε'], 1: ['VarDeclaration']},
         'VarDeclaration': {0: ['VAR', 'VarDecList']},
        'VarDecList': {0: ['TypeName', 'VarIdList', ';', 'VarDecMore']},
         'VarDecMore': {0: ['ε'], 1: ['VarDecList']},
        'VarIdList': {0: ['ID', 'VarIdMore']},
         'VarIdMore': {0: ['ε'], 1: [',', 'VarIdList']},
        'ProcDec': {0: ['ε'], 1: ['ProcDeclaration']},
         'ProcDeclaration': {
             0: ['PROCEDURE', 'ProcName', '(', 'ParamList', ')', ';', 'ProcDecPart',  'ProcBody',
                 'ProcDecMore']},
        'ProcDecMore': {0: ['ε'], 1: ['ProcDeclaration']},
        'ProcName': {0: ['ID']},
         'ParamList': {0: ['ε'], 1: ['ParamDecList']},
        'ParamDecList': {0: ['Param', 'ParamMore']},
         'ParamMore': {0: ['ε'], 1: [';', 'ParamDecList']},
         'Param': {0: ['TypeName', 'FormList'], 1: ['VAR', 'TypeName', 'FormList']},
        'FormList': {0: ['ID', 'FidMore']},
         'FidMore': {0: ['ε'], 1: [',', 'FormList']},
        'ProcDecPart': {0: ['DeclarePart']},
         'ProcBody': {0: ['ProgramBody']},
        'ProgramBody': {0: ['BEGIN', 'StmList', 'END']},
         'StmList': {0: ['Stm', 'StmMore']},
        'StmMore': {0: ['ε'], 1: [';', 'StmList']},
         'Stm': {0: ['ConditionalStm'], 1: ['LoopStm'], 2: ['InputStm'], 3: ['OutputStm'], 4: ['ReturnStm'],
                 5: ['ID', 'AssCall']},
        'AssCall': {0: ['AssignmentRest'], 1: ['CallStmRest']},
         'AssignmentRest': {0: ['VariMore', ':=', 'Exp']},
         'ConditionalStm': {0: ['IF', 'RelExp', 'THEN', 'StmList', 'ELSE', 'StmList', 'FI']},
         'LoopStm': {0: ['WHILE', 'RelExp', 'DO', 'StmList', 'ENDWH']},
        'InputStm': {0: ['READ', '(', 'Invar', ')']},
         'Invar': {0: ['ID']},
        'OutputStm': {0: ['WRITE', '(', 'Exp', ')']},
         'ReturnStm': {0: ['RETURN', '(', 'Exp', ')']},
        'CallStmRest': {0: ['(', 'ActParamList', ')']},
         'ActParamList': {0: ['ε'], 1: ['Exp', 'ActParamMore']},
        'ActParamMore': {0: ['ε'], 1: [',', 'ActParamList']},
         'RelExp': {0: ['Exp', 'OtherRelE']},
        'OtherRelE': {0: ['CmpOp', 'Exp']},
        'Exp': {0: ['Term', 'OtherTerm']},
         'OtherTerm': {0: ['ε'], 1: ['AddOp', 'Exp']},
        'Term': {0: ['Factor', 'OtherFactor']},
         'OtherFactor': {0: ['ε'], 1: ['MultOp', 'Term']},
         'Factor': {0: ['(', 'Exp', ')'], 1: ['INTC'], 2: ['Variable']},
        'Variable': {0: ['ID', 'VariMore']},
         'VariMore': {0: ['ε'], 1: ['[', 'Exp', ']'], 2: ['.', 'FieldVar']},
        'FieldVar': {0: ['ID', 'FieldVarMore']},
         'FieldVarMore': {0: ['ε'], 1: ['[', 'Exp', ']']},
        'CmpOp': {0: ['<'], 1: ['=']},
        'AddOp': {0: ['+'], 1: ['-']},
         'MultOp': {0: ['*'], 1: ['/']}}
    ,
    # 非终极符
    "VN": ["ActParamList", "ActParamMore", "AddOp", "ArrayType", "AssCall", "AssignmentRest", "BaseType", "CallStmRest", "CmpOp", "ConditionalStm", "DeclarePart", "Exp", "Factor", "FidMore", "FieldDecList", "FieldDecMore", "FieldVar", "FieldVarMore", "FormList", "IdList", "IdMore", "InputStm", "Invar", "LoopStm", "Low", "MultOp", "OtherFactor", "OtherRelE", "OtherTerm", "OutputStm", "Param", "ParamDecList", "ParamList", "ParamMore", "ProcBody", "ProcDec", "ProcDecMore", "ProcDecPart", "ProcDeclaration", "ProcName", "Program", "ProgramBody", "ProgramHead", "ProgramName", "RecType", "RelExp", "ReturnStm", "Stm", "StmList", "StmMore", "StructureType", "Term", "Top", "TypeDec", "TypeDecList", "TypeDecMore", "TypeDeclaration", "TypeId", "TypeName", "VarDec", "VarDecList", "VarDecMore", "VarDeclaration", "VarIdList", "VarIdMore", "VariMore", "Variable"],
    # 终极符
    "VT": ["(", ")", "*", "+", ",", "-", ".", "..", "/", ":=", ";", "<", "=", "ARRAY", "BEGIN", "CHAR", "DO", "ELSE", "END", "ENDWH", "FI", "ID", "IF", "INTC", "INTEGER", "OF", "PROCEDURE", "PROGRAM", "READ", "RECORD", "RETURN", "THEN", "TYPE", "VAR", "WHILE", "WRITE", "[", "]"],
    # 空
    "NN": ["ε"]
}


def firstSet(grammar,leftSymbol):
    '''

    :param grammar:文法规则
    :param leftSymbol:生成式左部符号
    :return: first set
    '''
    result = set()
    # situation one
    if leftSymbol in grammar["VT"] or leftSymbol == 'ε':
        result.add(leftSymbol)
        return result
    else:
        sons = grammar["P"][leftSymbol]
        length = len(sons)
        for i in range(length):
            son = sons[i]
            # print(son)
            # 遍历子分支的所有节点
            for grandSon in son:
                grandSonFrist = firstSet(grammar,grandSon)
                if 'ε' in grandSonFrist:
                    if son[len(son)-1] == grandSon:
                        pass
                    else:
                        grandSonFrist.remove('ε')
                    result = result.union(grandSonFrist)
                else:
                    result = result.union(grandSonFrist)
                    break
    return result

def followSet(grammar):
    '''

    :param gram: 文法规则
    :return: follow set
    '''
    # declare empty set for all VN
    allFollowSet = {}
    for vn in grammar["VN"]:
        allFollowSet[vn] = set()
    # start symbol init with '#'
    allFollowSet[grammar["S"]].add("#")

    done = False
    while not done:
        # print(allFollowSet)
        preStatus = [len(allFollowSet[vn]) for vn in grammar["VN"]]
        # loop all P
        for p in grammar["P"]:
            sons = grammar["P"][p]
            length = len(sons)
            for i in range(length):

                # 每个分支为一个son
                son = sons[i]
                # print(son)
                # 遍历每个son的节点
                sonNum = len(son)
                for j in range(sonNum):
                    grandSon = son[j]
                    # print(j,sonNum)
                    if grandSon not in grammar["VN"]:
                        continue
                    else:
                        if j == sonNum-1:
                            allFollowSet[grandSon]=allFollowSet[grandSon].union(allFollowSet[p])
                        else:
                            k = j+1
                            backSon = son[k]
                            backSonFirst = firstSet(grammar,backSon)
                            while k<sonNum and 'ε' in backSonFirst:
                                backSonFirst.remove('ε')
                                allFollowSet[grandSon] = allFollowSet[grandSon].union(backSonFirst)
                                k += 1
                                if k == sonNum:
                                    allFollowSet[grandSon] =  allFollowSet[grandSon].union(allFollowSet[p])
                                    break
                                backSon = son[k]
                                backSonFirst = firstSet(grammar, backSon)
                            allFollowSet[grandSon]=allFollowSet[grandSon].union(backSonFirst)

        curStatus = [len(allFollowSet[vn]) for vn in grammar["VN"]]
        if curStatus == preStatus:
            done = True
    return allFollowSet


def ll1Table(grammar):
    first = {}
    table = {}
    for vn in grammar["VN"]:
        first[vn] = firstSet(grammar,vn)
        table[vn] = {}
        for vt in grammar["VT"]:
            table[vn][vt] = "error"
    follow = followSet(grammar)
    # loop all P
    for p in grammar["P"]:

        sons = grammar["P"][p]
        sonNum = len(sons)
        for i in range(sonNum):
            son = sons[i]
            # print(son)
            head = son[0]
            if head in grammar["VT"]:
                table[p][head] = son
            # elif
            else:
                possible = set()
                # print(son)
                for element in son:
                    if element in grammar["VN"]:
                        tmp = first[element].copy()
                        if 'ε' in tmp:
                            tmp.remove('ε')
                            possible = possible.union(tmp,follow[p])
                        else:
                            possible = possible.union(tmp)
                            break
                    elif element == 'ε':
                        possible = possible.union(follow[p])
                    elif element in grammar["VT"]:
                        # print(son)
                        possible.add(element)
                        break
                # print(p+":" + str(possible))
                for poss in possible:
                    table[p][poss] = son
    return table


table = ll1Table(grammar)
node_count = (x for x in range(100000))
class AstNode(object):
    """node of ast """
    def __init__(self,tokenType,tokenVal="",father=None):
        self.tokenType = tokenType
        self.tokenVal = tokenVal
        self.father = father
        self.child = []
        self.brother = []
        self.id = next(node_count)

    def getTokenType(self):
        return self.tokenType

    def getTokenVal(self):
        return self.tokenVal

    def getId(self):
        return self.id

    def getFather(self):
        return self.father

    def __repr__(self):
        return "astNode %d %s\n"%(self.id,self.tokenType)

    def insertChild(self,node):
        """ add a ast node to current node"""
        if node and not isinstance(node,AstNode):
            raise ValueError("child node must be an astNode")
        self.child.append(node)
        node.brother = self.child
        node.father = self

    def step(self):
        cur = self
        while cur.id != 0 and cur.brother[::-1].index(cur) == 0:
            cur = cur.father
        if cur.id != 0:
            cur = cur.brother[cur.brother.index(cur)+1]
        return cur

    def __len__(self):
        return len(self.child)

    def dump(self,depth=0):
        tab = '     '*(depth-1)+" |- " if depth>0 else ""
        print("%s%s"%(tab,self.tokenType))
        for child in self.child:
            child.dump(depth+1)

import json
class AstNodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,AstNode):
            return {
                "TokenType":obj.tokenType,
                "child":[{"TokenType": child.tokenType,"child": child.child} for child in obj.child]
            }
        return json.JSONEncoder.default(self,obj)

def AstNodeDecoder(obj):
    if isinstance(obj,dict) and "TokenType" in obj:
        node = AstNode(obj["TokenType"])
        for childNode in obj.get("child"):
            node.insertChild(AstNodeDecoder(childNode))
        return node

    return obj

tokens = open("demo.txt",'r').readlines()



def generateAST(tokens):
    tokenStack = []

    for token in tokens:
        token = eval(token.strip())
        tokenType = token[0]
        tokenStack.append(tokenType)

    stack = [grammar["S"]]
    root = AstNode(grammar["S"])
    current = root

    for token in tokens:
        token = eval(token.strip())
        tokenType = token[0]
        tokenVal = token[-1]
        done = False
        error = False
        while not done:
            top = stack.pop()
            while top == 'ε':
                # print(stack)
                top = stack.pop()
                current.insertChild(AstNode("ε"))
                current = current.step()

            if top == tokenType:
                done = True
                tokenStack.pop(0)
                current = current.step()
                break
            try:
                choice = table[top][tokenType]
            except:
                break
            if choice == "error":
                done = True
                error = True
                break
            else:
                # for
                for i in choice[::-1]:
                    stack.append(i)
                for i in choice:
                    current.insertChild(AstNode(i))
                current = current.child[0]
    return root

root = generateAST(tokens)

root.dump()


# astfile = open("ast.txt","w")
# res = json.dumps(root,cls=AstNodeEncoder)
# json.dump(root,astfile,cls=AstNodeEncoder)
# astfile.close()

# astfile = open("ast.txt","r")
# root2 = json.load(astfile,object_hook=AstNodeDecoder)
# astfile.close()
# root2.dump()

