'''
@author: badmonkey
@software: PyCharm
@file: symbol.py
@time: 2021/4/18 下午6:48
'''
class Symbol(object):
    """
    三种类型的标识符，var,type,procedure
    var -> (name,kind,type,access,level,off,value)
    type -> (name,kind,type)
    procedure -> (name,kind,type,level,off,param,Class,code,size,forward)
    """
    def __init__(self,name=None,kind=None,type=None,value=None,access=None,level=None,offset=None,param=None,Class=None,code=None,Size=None,forward=None):
        self.name = name
        self.decKind = kind
        self.typePtr = type
        self.value = value
        self.access = access
        self.level = level
        self.offset = offset
        self.param = param
        self.Class = Class
        self.code = code
        self.Size = Size
        self.forward = forward

    def __repr__(self):
        return "%s %s %s "%(self.name,self.decKind,self.typePtr)

class SymbolTable(object):
    def __init__(self):
        self.table = []

    def add(self,symbol):
        self.table.append(symbol)

    def __contains__(self, item):
        for sym in self.table:
            if item == sym.name:
                return True
        return False

    def pop(self):
        self.table.pop()

    def remove(self,name):
        length = len(self.table)
        for i in range(length):
            if self.table[i].name == name:
                self.table.pop(i)
                break

    def top(self):
        return self.table[-1]

    def get(self,name):
        length = len(self.table)
        for i in range(length):
            if self.table[i].name == name:
                return self.table[i]
        return None

    def __repr__(self):
        return "\n".join([str(i) for i in self.table])

    def __len__(self):
        return len(self.table)

    def __getitem__(self, item):
        return self.table[item]



class BaseType(object):
    def __init__(self,sz=1,kind=None):
        self.sz = sz
        self.type = kind

    def __repr__(self):
        return self.type

class ArrayType(object):
    def __init__(self,sz=None,low=None,top=None,element=None):
        self.sz = sz
        self.type = "arrayType"
        self.low = low
        self.top = top
        self.element = element
    def __repr__(self):
        return "array[%d .. %d] of %s"%(self.low,self.top,self.element)

class RecordType(object):
    def __init__(self,sz=None,fieldList=None):
        self.type = "recordType"
        self.sz = sz
        self.fieldList = fieldList

    def __repr__(self):
        return "record %s"%(self.fieldList)




