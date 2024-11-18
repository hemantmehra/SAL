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
            i+=1
        elif code[i] == ')':
            if word:
                tokens.append(token_parse(word))
                word = ''
                in_word_flag = False
            tokens.append(token_close())
            i+=1
        elif code[i] == "'":
            if code[i+1] == "'":
                tokens.append(token_literal(""))
                i += 2
            elif code[i+2] == "'":
                tokens.append(token_literal(code[i+1]))
                i += 3
            elif code[i+3] == "'":
                if code[i+2] == '\\' and code[i+3] == 'n':
                    tokens.append(token_literal('\n'))
                    i += 4
                else:
                    assert False, f"invalid character. {code[i:i+3]}"
            else:
                assert False, f"invalid character. {code[i:i+3]}"
            
        elif code[i].isspace() and in_word_flag:
            tokens.append(token_parse(word))
            in_word_flag = False
            word = ''
            i+=1
        elif code[i].isspace() and not in_word_flag:
            i+=1
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
            func['type'] = AST_Func
            func['args'] = statements[i][2] if len(statements[i]) == 3 else []
            func['name'] = statements[i][1][1]
        elif statement_end_of_func(statements[i]):
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

def apply(f, args, global_env):
    if type(f) == dict:
        return run_function(f, args, global_env)
    elif f[0] == Token_Ident:
        if f[1] == 'print':
            print(args[0][1], end='')
            return 0
        elif f[1] == 'println':
            print(args[0][1])
            return 0
        elif f[1] == '+':
            return (Token_Literal, args[0][1] + args[1][1])
        elif f[1] == '-':
            return (Token_Literal, args[0][1] - args[1][1])
        elif f[1] == '*':
            return (Token_Literal, args[0][1] * args[1][1])
        elif f[1] == '<<':
            return (Token_Literal, args[0][1] << args[1][1])
        elif f[1] == '>>':
            return (Token_Literal, args[0][1] >> args[1][1])
        elif f[1] == '&':
            return (Token_Literal, args[0][1] & args[1][1])
        elif f[1] == '|':
            return (Token_Literal, args[0][1] | args[1][1])
        elif f[1] == 'if':
            test = args[0][1]
            true_val = args[1][1]
            false_val = args[2][1]
            return (Token_Literal, true_val if test else false_val)
        else:
            assert False, f"Assert not reached, unknown func: {f}"
    else:
        assert False, f"Assert not reached, unknown func: {f}"

def eval(l, env, global_env):
    if type(l) == list:
        if l[0][0] == Token_Ident and l[0][1] == 'set':
            k = l[1][1]
            if k in env and type(env[k]) == list:
                index = l[2]
                index = eval(index, env, global_env)[1]
                val = l[3]
                # print(k, index, val)
                env[k][index] = eval(val, env, global_env)
                return
            env[k] = eval(l[2], env, global_env)
            return
        elif l[0][0] == Token_Ident and l[0][1] == 'dec':
            k = l[1][1]
            env[k] = (env[k][0], env[k][1]-1)
            return
        elif l[0][0] == Token_Ident and l[0][1] == 'inc':
            k = l[1][1]
            env[k] = (env[k][0], env[k][1]+1)
            return
        elif l[0][0] == Token_Ident and l[0][1] == 'array':
            env[l[1][1]] = [(Token_Literal, 0)] * eval(l[2], env, global_env)[1]
            return
        elif l[0][0] == Token_Ident and l[0][1] == 'get':
            index = l[2]
            index = eval(index, env, global_env)[1]
            key = l[1][1]
            # print('get>>', key, index)
            return env[key][index]
        elif l[0][0] == Token_Ident:
            func_name = l[0][1]
            if func_name in global_env:
                func = global_env[func_name]
                return apply(func, [eval(i, env, global_env) for i in l[1:]], global_env)

        res = apply(eval(l[0], env, global_env), [eval(i, env, global_env) for i in l[1:]], global_env)
        return res

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

def make_global_env(ast):
    global_env = {}
    for func in ast:
        global_env[func['name']] = func
    return global_env

def find_function(global_env, func_name):
    if func_name in global_env:
        return global_env[func_name]
    assert False, f'Assert not reached. Function {func_name} was not found.'

def bind_args_to_env(func_args, args, env):
    if len(func_args) == len(args):
        for i, j in zip(func_args, args):
            env[i[1]] = j
        return
    assert False, f"Assert not reached. func_args and args are of different length, {func_args}, {args}"

def run_function(func, args, global_env):
    env = {}
    bind_args_to_env(func['args'], args, env)
    i = 0
    label_map = {}
    block = func['block']
    n = len(block)

    while i < n:
        statement = block[i]
        if statement[0][0] == Token_Ident and statement[0][1] == 'label':
            key = statement[1][1]
            label_map[key] = i
            i += 1
        elif statement[0][0] == Token_Ident and statement[0][1] == 'jmp_g':
            key = statement[1][1]
            a = eval(statement[2], env, global_env)
            b = eval(statement[3], env, global_env)
            if a > b:
                i = label_map[key]
            else:
                i += 1
        elif statement[0][0] == Token_Ident and statement[0][1] == 'jmp_l':
            key = statement[1][1]
            a = eval(statement[2], env, global_env)
            b = eval(statement[3], env, global_env)
            if a < b:
                i = label_map[key]
            else:
                i += 1
        elif statement[0][0] == Token_Ident and statement[0][1] == 'return':
            ret = eval(statement[1], env, global_env)
            return ret
        else:
            eval(statement, env, global_env)
            i+=1

source_code = ''
with open('rule110.lsp') as fin:
    source_code = fin.read()

# print(source_code)
tokens = tokenize(source_code)
statements = parse_statements(tokens)
# print(statements)

ast = parse_ast(statements)
# print(ast)

global_env = make_global_env(ast)
# print(global_env.keys())
main_func = find_function(global_env, 'main')
ret_val = run_function(main_func, [], global_env)
# print(ret_val)
