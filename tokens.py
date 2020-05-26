import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR'
}

functions = {
    'sin': 'FUNCTION',
    'cos': 'FUNCTION',
    'tan': 'FUNCTION',
    'sqrt': 'FUNCTION',
    'inttofloat': 'FUNCTION',
    'floattoint': 'FUNCTION'
}

types = {
    'int': 'TYPE',
    'float': 'TYPE',
    'boolean': 'TYPE'
}

tokens = [
             'NAME', 'INTEGER', 'FLOAT', 'BOOLEAN', 'TYPE', 'ARROW',
             'PLUS', 'MINUS', 'EXP', 'TIMES', 'DIVIDE', 'EQUALS',
             'LPAREN', 'RPAREN',
             'FUNCTION', 'USELESSEQ', 'SEMICOLON',
             'RELATION'
         ] + list(reserved.values())

t_ARROW = r'-\>'
t_SEMICOLON = r';|.\Z'
t_PLUS = r'\+'
t_MINUS = r'-'
t_EXP = r'\*\*|\^'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_RELATION = r'\<|\>|==|\<=|\>=|\<\>|\!='


# discard trailing "="

def t_USELESSEQ(t):
    r'=\s*$'
    pass


# match names but check if its not reserved
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'NAME')
    if t.type == 'NAME':
        t.type = functions.get(t.value, 'NAME')
    if t.type == 'NAME':
        t.type = types.get(t.value, 'NAME')
    return t


def t_FLOAT(t):
    r'\d+\.\d*|\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float printer goes brrr")
        t.value = 0.0
    return t


def t_INTEGER(t):
    r'(?<!\.)\d+(?!\.)|^\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %s" % t.value)
        t.value = 0
    # print "parsed number %s" % repr(t.value)
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
