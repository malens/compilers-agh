# compilers-agh
Parser/REPL solution for http://orchel.pl/compilers.php for a course at AGH.

# Usage
run main.py
enter commands, available commands:
* math commands (number + number, var + number etc)
* variable assignment (x = value, int x = value)
* lambda function definition (syntax: type funcname var -> var expression (like var + 2 or sin(var)))
* function calculcation (either user defined lambdas, or sin/cos/tan/sqrt)
* for loops (for var = number; comparison (e.g. : var < number); var = expression (e.g. : var = var + 1)) expression (e.g.: anothervar = value)
* while loops (while (comparison) expression)
* type checking (cannot add float to int etc)
known limitations:
  no string support
  lambdas evalute only to expression, you cannot use lambda()()
  functions only take singular arguments

