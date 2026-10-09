from main import Binary, Literal, Grouping, Unary, ASTprinter

printer = ASTprinter()

# Literal expression test
literal_expression = Literal(42)
print(printer.print(literal_expression))

# Binary expression test
binary_expression = Binary(Literal(1), "+", Literal(2))
print(printer.print(binary_expression))

# Grouping expression test
grouping_expression = Grouping(Literal(3))
print(printer.print(grouping_expression))

# Unary expression test
unary_expression = Unary("-", Literal(4))
print(printer.print(unary_expression))

# Combination test 1
combo_expression = Binary(Grouping(Literal(5)), "*", Unary("-", Literal(6)))
print(printer.print(combo_expression))

# Combination test 2
combo_expression2 = Binary(Binary(Unary("-", Literal(7)), "+", Grouping(Literal(8))), "*", Literal(9))
print(printer.print(combo_expression2))

# All Literals (T/F) test
all_literals_tf = Binary(Literal(True), "NOT", Literal(False))
print(printer.print(all_literals_tf))