'''
@author: badmonkey
@software: PyCharm
@file: scanner.py
@time: 2021/4/7 上午9:50
'''

class State():
    START="start"
    ASSIGN="assign"
    COMMENT="comment"
    NUM="num"
    ID="id"
    CHAR="char"
    RANGE="range"
    DONE="done"

from Scanner.token import *

import sys

HELP = '''
Usage: scanner filename output
Example: scanner demo.txt result.txt
'''

def Scan(scanner):
    state = State.START
    tokenList = list()
    line = 1
    nxt = 0
    length = len(scanner)
    while nxt<length:
        if state == State.START:
            nxtChar = scanner[nxt]
            # print(nxtChar.isalpha())
            while nxt < length and (nxtChar == ' ' or nxtChar == '\n' or nxtChar == '\r' or nxtChar == '\t'):
                if nxtChar == '\n':
                    line += 1
                nxt += 1
                if nxt == length:
                    break
                nxtChar = scanner[nxt]
            if nxt == length:
                break
            if nxtChar.isalpha() or nxtChar == '_':
                state = State.ID
            elif nxtChar.isnumeric():
                state = State.NUM
            else:
                if nxtChar == '.' and scanner[nxt+1] == '.':
                    nxt += 1
                    nxtChar = ".."
                elif nxtChar == ":" and scanner[nxt+1] =='=':
                    nxt +=1
                    nxtChar = ":="
                elif nxtChar == "{":
                    while nxtChar != "}":
                        nxt += 1
                        nxtChar = scanner[nxt]
                    nxt += 1
                    nxtChar = scanner[nxt]
                    state = State.START
                    continue
                # else:
                    # print(nxt,nxtChar,state,"error")
                    # break
                    # pass
                if nxtChar in tokenType.Types:
                    tokenList.append((nxtChar,nxtChar,line))
                    # print(tokenList)
                    nxt += 1
                    state = State.START
                else:
                    print(nxt,nxtChar,state,"error",line,scanner[nxt:])
                    break
                    # pass
                # 赋值，注释之类的
        elif state == State.ID: # id
            currentId = ""
            nxtChar = scanner[nxt]
            while nxt < len(scanner) and (nxtChar.isalpha() or nxtChar.isnumeric() or nxtChar == '_'):
                currentId += nxtChar
                nxt += 1
                if nxt == length:
                    break
                nxtChar = scanner[nxt]
            # 关键字需要单独挑出来
            if currentId.lower() in tokenType.KEYWORDS:
                tokenList.append((currentId.upper(),currentId,line))
            else:
                tokenList.append((tokenType.IDENTIFIERS,currentId,line))
            state = State.START
        elif state == State.NUM:
            currentNum = ""
            nxtChar = scanner[nxt]
            while nxt<len(scanner) and nxtChar.isnumeric():
                currentNum += nxtChar
                nxt += 1
                if nxt == length:
                    break
                nxtChar = scanner[nxt]
            tokenList.append((tokenType.INTC,int(currentNum),line))
            state = State.START
    return tokenList

if __name__ == '__main__':
    scanner = list(open("demo.txt","r").read())
    tokens = Scan(scanner)
    out = open("demo_scan.txt","w")
    for i in tokens:
        out.write(str(i)+"\n")
    out.close()
    # if len(sys.argv) <2:
    #     print(HELP)
    # elif len(sys.argv) ==2:
    #     filename = sys.argv[1]
    #     output = filename.split('.')[0]+"_scan.txt"
    # else:
    #     filename = sys.argv[1]
    #     output = sys.argv[2]
    # try:
    #     scanner = list(open(filename,"r").read())
    #     tokens = Scan(scanner)
    #     out = open(output,"w")
    #     for i in tokens:
    #         out.write(str(i)+"\n")
    #     out.close()
    # except:
    #     print("file not exist or permission denied\n")
    #     exit(1)




