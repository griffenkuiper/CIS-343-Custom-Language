from main import Scanner, Parser, ASTprinter, parse_and_print
import unittest

def parse_expression(source):
    tokens = Scanner(source).scanTokens()
    expression = Parser(tokens).parse()
    return ASTprinter().print(expression)

class ParserTests(unittest.TestCase):

    def test_number_literal(self):
        self.assertEqual(parse_expression("42"), "42.0")
        print(parse_expression("42"))

    def test_string_literal(self):
        self.assertEqual(parse_expression('"hello"'), "hello")
        print(parse_expression('"hello"'))

    def test_true_literal(self):
        self.assertEqual(parse_expression("true"), "True")
        print(parse_expression("true"))

    def test_false_literal(self):
        self.assertEqual(parse_expression("false"), "False")
        print(parse_expression("false"))

    def test_nil_literal(self):
        self.assertEqual(parse_expression("nil"), "None")
        print(parse_expression("nil"))

    def test_unary_not(self):
        self.assertEqual(parse_expression("!true"), "(! True)")
        print(parse_expression("!true"))

    def test_unary_minus(self):
        self.assertEqual(parse_expression("-5"), "(- 5.0)")
        print(parse_expression("-5"))

    def test_all_binary_operators(self):
        cases = [
            ("1 + 2", "(1.0 + 2.0)"),
            ("1 - 2", "(1.0 - 2.0)"),
            ("2 * 3", "(2.0 * 3.0)"),
            ("6 / 2", "(6.0 / 2.0)"),
            ("1 > 2", "(1.0 > 2.0)"),
            ("1 >= 2", "(1.0 >= 2.0)"),
            ("1 < 2", "(1.0 < 2.0)"),
            ("1 <= 2", "(1.0 <= 2.0)"),
            ("1 == 2", "(1.0 == 2.0)"),
            ("1 != 2", "(1.0 != 2.0)"),
        ]

        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(parse_expression(source), expected)

    def test_multiplication_precedes_addition(self):
        self.assertEqual(
            parse_expression("1 + 2 * 3"),
            "(1.0 + (2.0 * 3.0))"
        )
        print(parse_expression("1 + 2 * 3"))

    def test_comparison_precedes_equality(self):
        self.assertEqual(
            parse_expression("1 < 2 == true"),
            "((1.0 < 2.0) == True)"
        )
        print(parse_expression("1 < 2 == true"))

    def test_left_associativity(self):
        self.assertEqual(
            parse_expression("10 - 3 - 2"),
            "((10.0 - 3.0) - 2.0)"
        )
        print(parse_expression("10 - 3 - 2"))

    def test_right_associativity_of_unary(self):
        self.assertEqual(
            parse_expression("!!true"),
            "(! (! True))"
        )
        print(parse_expression("!!true"))

    def test_mixed_precedence(self):
        self.assertEqual(
            parse_expression("1 + 2 * 3 > 4 == false"),
            "(((1.0 + (2.0 * 3.0)) > 4.0) == False)"
        )
        print(parse_expression("1 + 2 * 3 > 4 == false"))

    def test_unexpected_trailing_token(self):
        with self.assertRaisesRegex(SyntaxError, "Unexpected token"):
            parse_expression("1 2")

    def test_missing_operand(self):
        with self.assertRaisesRegex(SyntaxError, "Expected an expression"):
            parse_expression("1 +")

    def test_missing_closing_parenthesis(self):
        with self.assertRaisesRegex(SyntaxError, "Expected '\\)'"):
            parse_expression("(1 + 2")

    def test_unexpected_closing_parenthesis(self):
        with self.assertRaisesRegex(SyntaxError, "Unexpected token"):
            parse_expression("1)")

    def test_empty_expression(self):
        with self.assertRaisesRegex(SyntaxError, "Expected an expression"):
            parse_expression("")

    def test_operator_without_left_operand(self):
        with self.assertRaisesRegex(SyntaxError, "Expected an expression"):
            parse_expression("* 2")

    def test_consecutive_operators(self):
        with self.assertRaisesRegex(SyntaxError, "Expected an expression"):
            parse_expression("1 + * 2")


if __name__ == "__main__":
    unittest.main()