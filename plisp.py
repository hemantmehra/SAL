from enum import Enum

class Token(Enum):
    Op = 1
    PFunc = 2
    Lit = 3

def _Op(val):
    return (Token.Op, val)

def _PFunc(val):
    return (Token.PFunc, val)

def _Lit(val):
    return (Token.Lit, val)

def apply(f, args):
    if f[0] == Token.Op:
        if f[1] == '+':
            return sum([i[1] for i in args])
        else:
            assert False, "Assert not reached!\n"
    else:
        assert False, "Assert not reached!\n"

def eval(l):
    if type(l) == list:
        # print(l[0])
        return apply(eval(l[0]), [eval(i) for i in l[1:]])
    
    elif type(l) == tuple:
        if l[0] == Token.Op:
            return l
        elif l[0] == Token.Lit:
            return l
        else:
            assert False, "Assert not reached!\n"
    else:
            assert False, "Assert not reached!\n"

TokenType = Enum('TokenType', [
    'Open',
    'Close',
    'Symbol',
    'Literal'
])

def tokenize(code: str) -> list:
    i = 0
    n = len(code)
    in_word_flag = False
    tokens = []
    word = ''
    while i < n:
        if code[i] == '(':
            tokens.append(TokenType.Open)
        elif code[i] == ')':
            if word:
                tokens.append((TokenType.Symbol, word))
                word = ''
                in_word_flag = False
            tokens.append(TokenType.Close)
        elif code[i].isspace() and in_word_flag:
            tokens.append((TokenType.Symbol, word))
            in_word_flag = False
            word = ''
        elif code[i].isspace() and not in_word_flag:
            ...
        elif code[i].isalnum():
            in_word_flag = True
            word += code[i]
        i+=1
    return tokens

def parse(tokens: list) -> list:
    i = 0
    n = len(tokens)
    stack = []
    ast = []
    while i < n:
        if tokens[i] == TokenType.Open:
            stack.append([])
        elif (tokens[i]) == TokenType.Close:
            l = stack.pop()
            if len(stack) != 0:
                stack[-1].append(l)
            else:
                ast.append(l)
        elif type(tokens[i]) == tuple and (tokens[i][0]) == TokenType.Symbol:
            stack[-1].append(tokens[i])
        else:
            assert False, "Assert not reached!\n"
        i += 1
    return ast

with open('test.lsp') as fin:
    source_code = fin.read()

    tokens = tokenize(source_code)
    # for i in tokens:
    #     print(i)
    ast = parse(tokens)
    for i in ast:
        print(i)
