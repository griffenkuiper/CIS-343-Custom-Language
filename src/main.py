import enum
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
            case 'o':
                if self.match("r"):
                    self.tokens.append(Token("OR", "or", None, self.line))
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





# main loop
if __name__ == "__main__":
    user_input = len(sys.argv)

    # use input
    if user_input == 1:
        while True:
            try:
                get_input = input()
                scanner = Scanner(get_input)
                tokens = scanner.scanTokens()
                for token in tokens:
                    print(token)
            except KeyboardInterrupt:
                break

    # use a file
    if user_input == 2:
        file = sys.argv[1]
        with open(file, "r") as f:
            get_input = f.read()

        print(get_input)
        scanner = Scanner(get_input)
        tokens = scanner.scanTokens()
        for token in tokens:
            print(token)

    # too many inputs error
    if user_input > 2:
        print("Error: Only at most 2 arguments are allowed")



