'''
@author: badmonkey
@software: PyCharm
@file: token.py
@time: 2021/4/7 上午9:52
'''
class tokenType():
    PROGRAM = "PROGRAM"
    TYPE = "TYPE"
    VAR ="VAR"
    PROCEDURE = "PROCEDURE"
    BEGIN = "BEGIN"
    END = "END"
    ARRAY = "ARRAY"
    OF="OF"
    RECORD="RECORD"
    IF="IF"
    THEN="THEN"
    ELSE="ELSE"
    FI="FI"
    WHILE="WHILE"
    DO="DO"
    ENDWH="ENDWH"
    READ="READ"
    WRITE="WRITE"
    RETURN="RETURN"
    INTEGER="INTEGER"
    CHAR="CHAR"
    UNSIGNEDNUMBER="UNSIGNEDNUMBER"
    ADD="+"
    SUB="-"
    MUL="*"
    DIV="/"
    LESS="<"
    EQUAL="="
    LEFT_PARENT="("
    RIGHT_PARENT=")"
    LEFT_BRACKET="{"
    RIGHT_BRACKET="}"
    DOT="."
    SEMICOLON=";"
    EOF="EOF"
    SPACE=" "
    COLON_EQUAL=":="
    LEFT_BRACES="["
    RIGHT_BRACES="]"
    APOSTROPHE="'"
    TWO_DOT=".."
    COMMA=","
    IDENTIFIERS="ID"
    KEYWORDS = ["repeat", "program", "type", "var", "procedure", "begin", "end", "array", "of", "record", "if", "then",
                "else", "fi", "while", "do", "endwh", "read", "write", "return", "integer", "char"]
    Types = ["repeat", "program", "type", "var", "procedure", "begin", "end", "array", "of", "record", "if", "then",
                "else", "fi", "while", "do", "endwh", "read", "write", "return", "integer", "char","unsignednumber",
             "+","-","*","/","<","=","(",")","{","}","[","]",".",";","EOF"," ",":=","'","..",",","ID"]

class Token():
    tokentype = ""
    value = ""
    line = 0
    def __init__(self,tokentype,value,line):
        self.tokentype = tokentype
        self.value = value
        self.line = line



