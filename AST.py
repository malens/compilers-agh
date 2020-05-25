import math
import time

import Levenshtein as lev
import tokens


class Node(object):
    pass


names = {}
reserved = tokens.reserved
functions = tokens.functions

f_functions = {
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'sqrt': math.sqrt
}


# Structure

class CodeLine(Node):
    def __init__(self, line, value):
        self.line = line
        self.value = value if value is not None else value

        # print(self.value)


# Control

class If(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction
        self.value = instruction if condition else None


class IfElse(Node):
    def __init__(self, condition, if_instruction, else_instruction):
        self.condition = condition
        self.if_instruction = if_instruction
        self.else_instruction = else_instruction
        self.value = if_instruction if condition else else_instruction


class For(Node):
    def __init__(self, initialassignment, condition, assignment, instruction):
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
        print(condition.value)
        print(condition.value == True)
        while condition.value:
            print(instruction.value)
            instruction.redo()
            print(instruction.value)
            print(condition.value)
            condition.refresh()
            print(condition.value)

            time.sleep(1)


# Operations

class Function(Node):
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg
        self.value = f_functions[func](arg)


class Comparison(Node):
    def __init__(self, lhs, op, rhs):
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
    def __init__(self, name, value):
        self.name = name
        names[name] = value
        # print(names)
        self.value = names[name].value

    def redo(self):
        names[self.name].redo()
        self.value = names[self.name].value


class Number(Node):
    def __init__(self, value):
        self.value = value

    def redo(self):
        return


class Expression(Node):
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self.setval(lhs, op, rhs)

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
        self.value = -value


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
            else:
                similar = list(filter(lambda x: lev.ratio(name, x) > 0.66, list(names.keys())))
                if len(similar) == 1:
                    self.name = similar[0]
                    self.value = names[similar[0]].value
                else:
                    print("Undefined name '%s'" % name)
                    self.name = "UNDEFINED"
                    self.value = 0
    def redo(self):
        self.value = names[self.name].value

class Error(Node):
    def __init__(self):
        pass
