from __future__ import print_function
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def print_indented(self, content, indent=0):
        print(indent * "| " + content)

    @addToClass(AST.Node)
    def print_tree(self, indent=0):
        self.print_indented(self.__class__.__name__, indent)
        for attr in self.__dict__:
            attr = getattr(self, attr)
            print_tree = getattr(attr, 'print_tree', None)
            if callable(print_tree):
                print_tree(indent + 1)
