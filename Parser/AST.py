'''
@author: badmonkey
@software: PyCharm
@file: AST.py
@time: 2021/4/18 下午6:15
'''
import json
import sys

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

    def isTokenType(self,tokenType):
        return self.tokenType == tokenType

    def getTokenType(self):
        return self.tokenType

    def getTokenVal(self):
        return self.tokenVal

    def isTokenVal(self,tokenVal):
        return self.tokenVal == tokenVal

    def getId(self):
        return self.id

    def getFather(self):
        return self.father

    def isEmpty(self):
        return len(self.child) == 0

    def firstChild(self):
        if self.isEmpty():
            raise ValueError("node has no child\n")
        else:
            return self.child[0]

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

    def dump(self,depth=0,file=sys.stdout):
        tab = '     '*(depth-1)+" |- " if depth>0 else ""
        print("%s%s  %s"%(tab,self.tokenType,self.tokenVal),file=file)
        for child in self.child:
            child.dump(depth+1,file=file)




class AstNodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,AstNode):
            return {
                "TokenType":obj.tokenType,
                "child":[{"TokenType": child.tokenType,"child": child.child} for child in obj.child]
            }
        return json.JSONEncoder.default(self,obj)

# def AstNodeDecoder(obj):
#     if isinstance(obj,dict) and "TokenType" in obj:
#         node = AstNode(obj["TokenType"])
#         for childNode in obj.get("child"):
#             node.insertChild(AstNodeDecoder(childNode))
#         return node
#
#     return obj

class AstNodeDecoder(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self,obj):
        if isinstance(obj, dict) and "TokenType" in obj:
            node = AstNode(obj["TokenType"])
            for childNode in obj.get("child"):
                node.insertChild(AstNodeDecoder.object_hook(self,childNode))
            return node

        return obj



# astfile = open("ast.txt","w")
# res = json.dumps(root,cls=AstNodeEncoder)
# json.dump(root,astfile,cls=AstNodeEncoder)
# astfile.close()

# astfile = open("ast.txt","r")
# root2 = json.load(astfile,cls=AstNodeDecoder)
# astfile.close()
# root2.dump()

# json.load()
