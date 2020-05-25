import ply.yacc as yacc
import parser
import tokens

if __name__ == '__main__':
    parser = yacc.yacc(module=parser)
    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if not text:
            continue
        ast = parser.parse(text, lexer=tokens.lexer, debug=True)
        # ast.printTree()