iota_counter = 0

def iota(reset=False) -> int:
    global iota_counter
    if reset:
        iota_counter = 0
    result = iota_counter
    iota_counter += 1
    return result

Token_Open = iota(True)
Token_Close = iota()
Token_Ident = iota()
Token_Literal = iota()

def token_open():
    return (Token_Open,)

def token_close():
    return (Token_Close,)

def token_ident(x):
    return (Token_Ident, x)

def token_literal(x):
    return (Token_Literal, x)

def token_parse(x):
    try:
        return token_literal(int(x))
    except:
        return token_ident(x)

def tokenize(code: str) -> list:
    i = 0
    n = len(code)
    in_word_flag = False
    tokens = []
    word = ''
    while i < n:
        if code[i] == '(':
            tokens.append(token_open())
        elif code[i] == ')':
            if word:
                tokens.append(token_parse(word))
                word = ''
                in_word_flag = False
            tokens.append(token_close())
        elif code[i].isspace() and in_word_flag:
            tokens.append(token_parse(word))
            in_word_flag = False
            word = ''
        elif code[i].isspace() and not in_word_flag:
            ...
        elif code[i] != '(' and code[i] != ')':
            in_word_flag = True
            word += code[i]
        i+=1
    return tokens

def parse_statements(tokens: list) -> list:
    i = 0
    n = len(tokens)
    stack = []
    statements = []
    while i < n:
        if tokens[i][0] == Token_Open:
            stack.append([])
        elif tokens[i][0] == Token_Close:
            l = stack.pop()
            if len(stack) != 0:
                stack[-1].append(l)
            else:
                statements.append(l)
        elif tokens[i][0] == Token_Ident or tokens[i][0] == Token_Literal:
            stack[-1].append(tokens[i])
        else:
            assert False, f"Assert not reached!, Token: {tokens[i]}\n"
        i += 1
    return statements

AST_Func = iota(True)
AST_Func_Body = iota()

def statement_start_of_func(statement):
    return statement[0][0] == Token_Ident and statement[0][1] == 'def'

def statement_end_of_func(statement):
    return statement[0][0] == Token_Ident and statement[0][1] == 'end'

from copy import deepcopy

def parse_ast(statements):
    i = 0
    n = len(statements)
    ast = []
    func = {}
    func_block = []
    in_func_flag = False
    while i < n:
        if statement_start_of_func(statements[i]):
            in_func_flag = True
            func_block = []
        elif statement_end_of_func(statements[i]):
            func['type'] = AST_Func
            func['name'] = statements[i][1][1]
            func['block'] = deepcopy(func_block)
            ast.append(deepcopy(func))
            func = {}
            func_block = []
            in_func_flag = False
        elif in_func_flag:
            func_block.append(statements[i])
        else:
            assert False, f"Assert not reached: {statements[i]}"
        i += 1
    return ast

def apply(f, args):
    if f[0] == Token_Ident:
        if f[1] == 'print':
            print(args[0][1])
            return 0
        elif f[1] == '+':
            print(args[0][1], args[1][1])
            return (Token_Literal, args[0][1] + args[1][1])
        elif f[1] == '*':
            return (Token_Literal, args[0][1] * args[1][1])
    else:
        assert False, "Assert not reached!\n"

def eval(l, env):
    if type(l) == list:
        if l[0][0] == Token_Ident and l[0][1] == 'set':
            env[l[1][1]] = eval(l[2], env)
            print(env)
        return apply(eval(l[0], env), [eval(i, env) for i in l[1:]])

    elif type(l) == tuple:
        if l[0] == Token_Literal:
            return l
        elif l[0] == Token_Ident:
            if l[1] in env:
                return env[l[1]]
            return l
        else:
            assert False, f"Assert not reached!, {l}\n"
    else:
            assert False, f"Assert not reached!, {l}\n"

def run_function(ast, func_name):
    env = {}
    for func in ast:
        print(func['name'])
        if func['name'] == func_name:
            for statement in func['block']:
                eval(statement, env)
            return
    assert False, f'Assert not reached. Function {func_name} not found.'

source_code = ''
with open('test.lsp') as fin:
    source_code = fin.read()

tokens = tokenize(source_code)
statements = parse_statements(tokens)
print(statements)

ast = parse_ast(statements)
print(ast)

run_function(ast, 'main')
