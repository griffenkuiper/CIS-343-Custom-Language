import enum
import os
import sys

class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    keywords = {
        "and": "AND",
        "class": "CLASS",
        "else": "ELSE",
        "false": "FALSE",
        "for": "FOR",
        "fun": "FUN",
        "if": "IF",
        "nil": "NIL",
        "or": "OR",
        "say": "PRINT",
        "return": "RETURN",
        "super": "SUPER",
        "this": "THIS",
        "true": "TRUE",
        "var": "VAR",
        "while": "WHILE"
    }


    def is_at_end(self):
        return self.current >= len(self.source)

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            print(f"Unterminated string on line {self.line}")
            return
        self.advance()
        value = self.source[self.start + 1:self.current - 1]
        self.tokens.append(Token("STRING", value, value, self.line))

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current]
        token_type = self.keywords.get(text, "IDENTIFIER")
        self.tokens.append(Token(token_type, text, None, self.line))

    def isAlpha(self, c):
        return c.isalpha() or c == '_'

    def isAlphaNumeric(self, c):
        return self.isAlpha(c) or self.isDigit(c)

    def isDigit(self, c):
        return c >= '0' and c <= '9'

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()

            while self.isDigit(self.peek()):
                self.advance()

        self.tokens.append(Token("NUMBER", self.source[self.start:self.current], float(self.source[self.start:self.current]), self.line))

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def scanToken(self):
        c = self.advance()

        match c:
            case '(':
                self.tokens.append(Token("LEFT_PAREN", "(", None, self.line))
            case ')': 
                self.tokens.append(Token("RIGHT_PAREN", ")", None, self.line))
            case '{': 
                self.tokens.append(Token("LEFT_BRACE", "{", None, self.line))
            case '}': 
                self.tokens.append(Token("RIGHT_BRACE", "}", None, self.line))
            case ',': 
                self.tokens.append(Token("COMMA", ",", None, self.line))
            case '.': 
                self.tokens.append(Token("DOT", ".", None, self.line))
            case '-': 
                self.tokens.append(Token("MINUS", "-", None, self.line))
            case '+': 
                self.tokens.append(Token("PLUS", "+", None, self.line))
            case ';': 
                self.tokens.append(Token("SEMICOLON", ";", None, self.line))
            case '*': 
                self.tokens.append(Token("STAR", "*", None, self.line))
            case "!":
                if self.match("="):
                    self.tokens.append(Token("BANG_EQUAL", "!=", None, self.line))
                else:
                    self.tokens.append(Token("BANG", "!", None, self.line))
            case "=":
                if self.match("="):
                    self.tokens.append(Token("EQUAL_EQUAL", "==", None, self.line))
                else:
                    self.tokens.append(Token("EQUAL", "=", None, self.line))
            case "<":
                if self.match("="):
                    self.tokens.append(Token("LESS_EQUAL", "<=", None, self.line))
                else:
                    self.tokens.append(Token("LESS", "<", None, self.line))
            case ">":
                if self.match("="):
                    self.tokens.append(Token("GREATER_EQUAL", ">=", None, self.line))
                else:
                    self.tokens.append(Token("GREATER", ">", None, self.line))
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.tokens.append(Token("SLASH", "/", None, self.line))
            case ' ':
                pass
            case '\t':
                pass
            case '\r':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.isDigit(c):
                    self.number()
                elif self.isAlpha(c):
                    self.identifier()
                else:
                    print(f"Unexpected character: {c} at line {self.line}")

    def scanTokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token("EOF", "", None, self.line))
        return self.tokens


class Expression:
    pass

class Binary(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class Literal(Expression):
    def __init__(self, value):
        self.value = value

class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression

class Unary(Expression):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

class Statement:
    pass
class Print_Statement(Statement):
    def __init__(self, expression):
        self.expression = expression
class Expression_Statement(Statement):
    def __init__(self, expression):
        self.expression = expression

class Variable(Expression):
    def __init__(self, name):
        self.name = name

class Assign(Expression):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Variable_Statement(Statement):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

class Block_Statement(Statement):
    def __init__(self, statements):
        self.statements = statements

class ASTprinter:
    def print(self, expression):
        if isinstance(expression, Binary):
            return f"({self.print(expression.left)} {expression.operator} {self.print(expression.right)})"
        elif isinstance(expression, Literal):
            return str(expression.value)
        elif isinstance(expression, Grouping):
            return f"({self.print(expression.expression)})"
        elif isinstance(expression, Unary):
            return f"({expression.operator} {self.print(expression.right)})"
        else:
            return ""

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []

        while not self.is_at_end():
            try:
                statements.append(self.declaration())

            except SyntaxError as error:
                print(f"Parse error: {error}")
                self.synchronize()

        return statements

    def synchronize(self):
        while not self.is_at_end():
            if self.previous().type == "SEMICOLON":
                return
            if self.peek().type in ["CLASS", "FUN", "VAR", "FOR", "IF", "WHILE", "PRINT", "RETURN"]:
                return
            self.advance()

    def assignment(self):
        expr = self.equality()

        if self.match("EQUAL"):
            value = self.assignment()

            if isinstance(expr, Variable):
                return Assign(expr.name, value)

            raise SyntaxError(
                f"Invalid assignment target on line {self.previous().line}"
            )

        return expr
    
    def statement(self):
        if self.match("PRINT"):
            return self.print_statement()

        if self.match("LEFT_BRACE"):
            return Block_Statement(self.block())

        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        if not self.match("SEMICOLON"):
            raise SyntaxError(
                f"Expected ';' after value on line {self.peek().line}"
            )
        return Print_Statement(value)
    
    def declaration(self):
        if self.match("VAR"):
            return self.var_declaration()

        if self.check("RIGHT_BRACE"):
            raise SyntaxError(
                f"Unmatched '}}' on line {self.peek().line}"
            )

        return self.statement()

    def var_declaration(self):
        if not self.check("IDENTIFIER"):
            raise SyntaxError(
                f"Expected variable name on line {self.peek().line}"
            )

        name = self.advance()

        initializer = None

        if self.match("EQUAL"):
            initializer = self.expression()

        if not self.match("SEMICOLON"):
            raise SyntaxError(
                f"Expected ';' after variable declaration on line {self.peek().line}"
            )

        return Variable_Statement(name.lexeme, initializer)

    def block(self):
        statements = []

        while not self.check("RIGHT_BRACE") and not self.is_at_end():
            statements.append(self.declaration())

        if not self.match("RIGHT_BRACE"):
            raise SyntaxError(
                f"Unmatched '{{' on line {self.peek().line}"
            )

        return statements
    def expression_statement(self):
        expr = self.expression()
        if not self.match("SEMICOLON"):
            raise SyntaxError(
                f"Expected ';' after expression on line {self.peek().line}"
            )
        return Expression_Statement(expr)

    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type):
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == "EOF"

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def expression(self):
        return self.assignment()

    def equality(self):
        expr = self.comparison()
        while self.match("BANG_EQUAL", "EQUAL_EQUAL"):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator.lexeme, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match("GREATER", "GREATER_EQUAL", "LESS", "LESS_EQUAL"):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator.lexeme, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match("MINUS", "PLUS"):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator.lexeme, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match("SLASH", "STAR"):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator.lexeme, right)
        return expr

    def unary(self):
        if self.match("BANG", "MINUS"):
            operator = self.previous()
            right = self.unary()
            return Unary(operator.lexeme, right)
        return self.primary()

    def primary(self):
        if self.match("FALSE"):
            return Literal(False)
        if self.match("TRUE"):
            return Literal(True)
        if self.match("NIL"):
            return Literal(None)
        if self.match("NUMBER", "STRING"):
            return Literal(self.previous().literal)
        if self.match("LEFT_PAREN"):
            expr = self.expression()
            if not self.match("RIGHT_PAREN"):
                raise SyntaxError(
                    f"Expected ')' after expression on line {self.peek().line}"
                )
            return Grouping(expr)
        token = self.peek()
        if self.match("IDENTIFIER"):
            return Variable(token.lexeme)
        raise SyntaxError(
            f"Expected an expression on line {token.line}; "
            f"found {token.lexeme or token.type}"
        )


def parse_and_interpret(source):
    statements = Parser(Scanner(source).scanTokens()).parse()
    Interpreter().interpret(statements)


class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        if name in self.values:
            raise RuntimeError(f"Variable '{name}' already declared")
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise RuntimeError(f"Undefined variable '{name}'")

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise RuntimeError(f"Undefined variable '{name}'")
    
class Interpreter:
    def __init__(self):
        self.environment = Environment()
    def interpret(self, statements):
        for statement in statements:
            try:
                self.execute(statement)
            except (RuntimeError, TypeError, ZeroDivisionError) as error:
                print(f"Runtime error: {error}")

    def execute(self, statement):
        if isinstance(statement, Print_Statement):
            value = self.evaluate(statement.expression)
            print(value)

        elif isinstance(statement, Expression_Statement):
            self.evaluate(statement.expression)

        elif isinstance(statement, Variable_Statement):
            value = None

            if statement.initializer is not None:
                value = self.evaluate(statement.initializer)

            self.environment.define(statement.name, value)

        elif isinstance(statement, Block_Statement):
            previous = self.environment

            try:
                self.environment = Environment(previous)
                self.interpret(statement.statements)
            finally:
                self.environment = previous

    def evaluate(self, expression):
        if isinstance(expression, Literal):
            return expression.value
        elif isinstance(expression, Grouping):
            return self.evaluate(expression.expression)
        elif isinstance(expression, Unary):
            right = self.evaluate(expression.right)
            if expression.operator == "-":
                return -right
            elif expression.operator == "!":
                return not right
        elif isinstance(expression, Binary):
            left = self.evaluate(expression.left)
            right = self.evaluate(expression.right)
            if expression.operator == "+":
                return left + right
            elif expression.operator == "-":
                return left - right
            elif expression.operator == "*":
                return left * right
            elif expression.operator == "/":
                return left / right
            elif expression.operator == ">":
                return left > right
            elif expression.operator == ">=":
                return left >= right
            elif expression.operator == "<":
                return left < right
            elif expression.operator == "<=":
                return left <= right
            elif expression.operator == "==":
                return left == right
            elif expression.operator == "!=":
                return left != right
            elif isinstance(expression, Variable):
                return self.environment.get(expression.name)

            elif isinstance(expression, Assign):
                value = self.evaluate(expression.value)
                self.environment.assign(expression.name, value)
                return value
            
    def is_truthy(self, value):
        if value is None:
            return False
        if value is False:
            return False
        return True

# main loop
if __name__ == "__main__":
    user_input = len(sys.argv)

    # use input
    if user_input == 1:
        while True:
            try:
                get_input = input()
                parse_and_interpret(get_input)
            except KeyboardInterrupt:
                break

    # use a file
    if user_input == 2:
        file = sys.argv[1]
        with open(file, "r") as f:
            get_input = f.read()

        parse_and_interpret(get_input)

    # too many inputs error
    if user_input > 2:
        print("Error: Only at most 2 arguments are allowed")


