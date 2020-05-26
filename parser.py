import tokens
import AST

import ply.yacc as yacc

tokens = tokens.tokens

# Parsing rules

precedence = (
    ('left', 'SEMICOLON'),
    ('right', 'ELSE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'EXP'),
    ('right', 'UMINUS'),
    ('right', 'FUNCTION')
)


def p_codeline(p):
    """codeline : statement
                | statement SEMICOLON codeline %prec SEMICOLON
                | statement SEMICOLON
    """
    p[0] = AST.CodeLine(p[1])
    pass


def p_statement_assign(p):
    'assignment : NAME EQUALS expression'
    p[0] = AST.Assignment(p[1], p[3])


def p_statement(p):
    """statement : expression
                 | comparison
                 | assignment
    """
    p[0] = p[1]


# def p_expression_binop(p):
#     """
#     expression : expression expression PLUS
#                | expression expression MINUS
#                | expression expression TIMES
#                | expression expression DIVIDE
#                | expression expression EXP
#     """
#     if p[3] == '+':
#         p[0] = p[1] + p[2]
#     elif p[3] == '-':
#         p[0] = p[1] - p[2]
#     elif p[3] == '*':
#         p[0] = p[1] * p[2]
#     elif p[3] == '/':
#         p[0] = p[1] / p[2]
#     elif p[3] == '**' or p[3] == '^':
#         p[0] = p[1] ** p[2]
#

def p_statement_ifelse(p):
    """
    statement : IF LPAREN comparison RPAREN statement ELSE statement %prec ELSE
    """
    p[0] = AST.IfElse(p[3], p[5], p[7])


def p_statement_if(p):
    """
    statement : IF LPAREN comparison RPAREN statement
    """
    p[0] = AST.If(p[3], p[5])


def p_statement_while(p):
    """
    statement : WHILE LPAREN comparison RPAREN statement
    """
    p[0] = AST.While(p[3], p[5])

def p_statement_for(p):
    """
    statement : FOR LPAREN assignment SEMICOLON comparison SEMICOLON assignment RPAREN statement
    """
    p[0] = AST.For(p[3], p[5], p[7], p[9])


def p_comparison(p):
    """
    comparison : expression RELATION expression
    """
    p[0] = AST.Comparison(p[1], p[2], p[3])


def p_expression_binop(p):
    """
    expression : expression PLUS expression
              | expression MINUS expression
              | expression TIMES expression
              | expression DIVIDE expression
              | expression EXP expression
    """
    p[0] = AST.Expression(p[1], p[2], p[3])


def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = AST.MinusOperator(p[1])


def p_expression_function(p):
    'expression : FUNCTION expression %prec FUNCTION'
    p[0] = AST.Function(p[1], p[2])


def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]


def p_expression_number(p):
    """expression : FLOAT
                  | INTEGER
                  | BOOLEAN
    """
    p[0] = AST.Number(p[1])


def p_expression_name(p):
    'expression : NAME'
    p[0] = AST.Name(p[1])

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")




parser = yacc.yacc()


