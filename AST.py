import math
from enum import Enum

import Levenshtein as lev
import tokens


class Node(object):
    pass


names = {}

lambdas = {}

reserved = tokens.reserved
functions = tokens.functions


class Type(Enum):
    int = 'int'
    float = 'float'
    boolean = 'boolean'


# types = {
#     'int': 'int',
#     'float': 'float',
#     'boolean': 'boolean'
# }

f_functions = {
    'sin': (math.sin, Type.float.value),
    'cos': (math.cos, Type.float.value),
    'tan': (math.tan, Type.float.value),
    'sqrt': (math.sqrt, Type.float.value),
    'inttofloat': (lambda x: float(x), Type.float.value),
    'floattoint': (lambda x: int(x), Type.int.value)
}


# Structure

class CodeLine(Node):
    def __init__(self, line):
        self.line = line
        self.value = line.value if line is not None else None
        print(self.value)


# Control

class If(Node):
    def __init__(self, condition, instruction):
        if condition.type != Type.boolean.value:
            raise Exception('invalid type for if expression')
        self.condition = condition
        self.instruction = instruction
        self.value = instruction if condition else None


class IfElse(Node):
    def __init__(self, condition, if_instruction, else_instruction):
        if condition.type != Type.boolean.value:
            raise Exception('invalid type for if expression')
        self.condition = condition
        self.if_instruction = if_instruction
        self.else_instruction = else_instruction
        self.value = if_instruction if condition else else_instruction


class For(Node):
    def __init__(self, initialassignment, condition, assignment, instruction):
        if condition.type != Type.boolean.value:
            raise Exception('invalid type for if expression')
        self.value = None
        while condition.value:
            instruction.redo()
            assignment.redo()
            condition.refresh()


class While(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction
        self.value = None
        while condition.value:
            instruction.redo()
            condition.refresh()


# Operations

class Function(Node):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

        if hasattr(arg, "value"):
            print(arg.value)
            self.value = f_functions[func][0](arg.value)
        self.type = f_functions[func][1]

    def redo(self):
        self.value = f_functions[self.func][0](self.arg.value)



class Comparison(Node):
    def __init__(self, lhs, op, rhs):
        self.type = Type.boolean.value
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self.setval(lhs, op, rhs)

    def setval(self, lhs, op, rhs):
        if op == '==':
            self.value = lhs.value == rhs.value
        elif op == '<':
            self.value = lhs.value < rhs.value
        elif op == '<=':
            self.value = lhs.value <= rhs.value
        elif op == '>':
            self.value = lhs.value > rhs.value
        elif op == '>=':
            self.value = lhs.value >= rhs.value
        elif op == '<>':
            self.value = lhs.value != rhs.value
        elif op == '!=':
            self.value = lhs.value != rhs.value

    def refresh(self):
        if hasattr(self.lhs, 'name'):
            self.lhs = names[self.lhs.name]
        if hasattr(self.rhs, 'name'):
            self.rhs = names[self.rhs.name]
        self.setval(self.lhs, self.op, self.rhs)


class Assignment(Node):
    def __init__(self, name, value, type=None):
        if type is not None:
            if value.type != type:
                raise Exception('type doesnt match assignment')
            elif name in names:
                if names[name].type != type:
                    raise Exception('type doesnt match existing')

        self.name = name
        names[name] = value
        # print(names)
        self.value = names[name].value

    def redo(self):
        names[self.name].redo()
        self.value = names[self.name].value


class Number(Node):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def redo(self):
        return


class Lambda(Node):
    def __init__(self, name, var, expr, type):
        self.var = var
        self.expr = expr
        self.name = name
        self.type = type
        self.value = None
        f_functions[name] = (lambda x: self.apply(x), type)
        lambdas[name] = self
        tokens.functions[name] = 'FUNCTION'

    def apply(self, name):
        self.expr.lhs = Number(name, Type.int.value)
        self.expr.arg = Number(name, Type.int.value)
        self.expr.value = name
        self.expr.redo()
        self.value = self.expr.value
        return self.value

    def redo(self):
        self.apply(self.value)


class Expression(Node):
    def __init__(self, lhs, op, rhs):
        if lhs.type == "special":
            self.value = 0
            self.type = rhs.type
        else:
            if lhs.type != rhs.type:
                print(lhs.type, rhs.type)
                raise Exception('mismatched types in expression')
            else:
                self.type = rhs.type
            self.setval(lhs, op, rhs)
        self.lhs = lhs
        self.op = op
        self.rhs = rhs


    def setval(self, lhs, op, rhs):
        if op == '+':
            self.value = lhs.value + rhs.value
        elif op == '-':
            self.value = lhs.value - rhs.value
        elif op == '*':
            self.value = lhs.value * rhs.value
        elif op == '/':
            self.value = lhs.value / rhs.value
        elif op == '**' or op == '^':
            self.value = lhs.value ** rhs.value

    def redo(self):
        self.lhs.redo()
        self.rhs.redo()
        self.setval(self.lhs, self.op, self.rhs)


class MinusOperator(Node):
    def __init__(self, value):
        self.value = -value.value
        self.type = value.type


# Terminals

class Integer(Node):
    def __init__(self, val):
        self.value = val


class Float(Node):
    def __init__(self, val):
        self.value = val


class Name(Node):
    def __init__(self, name):
        if name not in reserved and name not in functions:
            if name in names:
                self.value = names[name].value
                self.name = name
                self.type = names[name].type
            else:
                similar = list(filter(lambda x: lev.ratio(name, x) > 0.66, list(names.keys())))
                if len(similar) == 1:
                    self.name = similar[0]
                    self.value = names[similar[0]].value
                    self.type = names[similar[0]].type
                else:
                    self.name = name
                    self.type = "special"
                    self.value = 0
                    names[name] = Number(0, Type.int.value)
                    # else:
                    #     print("Undefined name '%s'" % name)
                    #     self.name = "UNDEFINED"
                    #     self.value = 0
                    #     self.type = "UNDEFINED"

    def redo(self):
        self.value = names[self.name].value


class Error(Node):
    def __init__(self):
        pass
