from main import Scanner

def test_num():
    scanner = Scanner("123")
    tokens = scanner.scanTokens()
    assert tokens[0].type == "NUMBER" and tokens[0].lexeme == "123"

def test_nums():
    scanner = Scanner("123 456")
    tokens = scanner.scanTokens()
    assert tokens[0].type == "NUMBER" and tokens[0].lexeme == "123"
    assert tokens[1].type == "NUMBER" and tokens[1].lexeme == "456"

def test_floats():
    scanner = Scanner("123.45 678.90 59.99 0.002")
    tokens = scanner.scanTokens()
    assert tokens[0].type == "NUMBER" and tokens[0].lexeme == "123.45"
    assert tokens[1].type == "NUMBER" and tokens[1].lexeme == "678.90"
    assert tokens[2].type == "NUMBER" and tokens[2].lexeme == "59.99"
    assert tokens[3].type == "NUMBER" and tokens[3].lexeme == "0.002"

def test_strings():
    scanner = Scanner('"hello" "world"')
    tokens = scanner.scanTokens()
    assert tokens[0].type == "STRING" and tokens[0].lexeme == "hello"
    assert tokens[1].type == "STRING" and tokens[1].lexeme == "world"

def test_empty_string():
    scanner = Scanner('""')
    tokens = scanner.scanTokens()
    assert tokens[0].type == "STRING" and tokens[0].lexeme == ""

def test_keywords():
    scanner = Scanner("and class else false for fun if nil or say return super this true var while")
    tokens = scanner.scanTokens()
    assert tokens[0].type == "AND"
    assert tokens[1].type == "CLASS"
    assert tokens[2].type == "ELSE"
    assert tokens[3].type == "FALSE"
    assert tokens[4].type == "FOR"
    assert tokens[5].type == "FUN"
    assert tokens[6].type == "IF"
    assert tokens[7].type == "NIL"
    assert tokens[8].type == "OR"
    assert tokens[9].type == "PRINT"
    assert tokens[10].type == "RETURN"
    assert tokens[11].type == "SUPER"
    assert tokens[12].type == "THIS"
    assert tokens[13].type == "TRUE"
    assert tokens[14].type == "VAR"
    assert tokens[15].type == "WHILE"

def test_identifiers():
    scanner = Scanner("this_identifier anotherIdentifier _privateVar")
    tokens = scanner.scanTokens()
    assert tokens[0].type == "IDENTIFIER" and tokens[0].lexeme == "this_identifier"
    assert tokens[1].type == "IDENTIFIER" and tokens[1].lexeme == "anotherIdentifier"
    assert tokens[2].type == "IDENTIFIER" and tokens[2].lexeme == "_privateVar"


def test_unexpected_character():
    scanner = Scanner("@")
    tokens = scanner.scanTokens()
    assert tokens[0].lexeme != "@"

def test_unterminated_string():
    scanner = Scanner('"unterminated')
    tokens = scanner.scanTokens()
    assert tokens[0].lexeme != '"unterminated'

# This test requires the lab1-testingText file (this is used to test scanning input from a file)
def test_file_input():
    with open("lab1-testingText", "r") as f:
        get_input = f.read()
    scanner = Scanner(get_input)
    tokens = scanner.scanTokens()
    assert tokens[0].type == "NUMBER"
    assert tokens[1].type == "NUMBER"
    assert tokens[2].type == "NUMBER"
    assert tokens[3].type == "STRING"
    assert tokens[4].type == "STRING"
    assert tokens[5].type == "PRINT"
    assert tokens[6].type == "IF"
    assert tokens[7].type == "ELSE"
    assert tokens[8].type == "IDENTIFIER"








if __name__ == "__main__":
    test_num()
    test_nums()
    test_floats()
    test_strings()
    test_keywords()
    test_identifiers()
    test_unexpected_character()
    test_unterminated_string()
    test_empty_string()
    test_file_input()
    