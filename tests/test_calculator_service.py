import unittest

from services.calculator_service import (
    ExpressionError,
    calculate_expression,
)


class CalculatorServiceTestCase(unittest.TestCase):
    """测试计算器核心表达式计算功能。"""

    def test_addition(self):
        self.assertEqual(
            calculate_expression("12+8"),
            20,
        )

    def test_subtraction(self):
        self.assertEqual(
            calculate_expression("10-7"),
            3,
        )

    def test_multiplication(self):
        self.assertEqual(
            calculate_expression("6*8"),
            48,
        )

    def test_division(self):
        self.assertEqual(
            calculate_expression("20/4"),
            5,
        )

    def test_operator_precedence(self):
        self.assertEqual(
            calculate_expression("1+2*3"),
            7,
        )

    def test_parentheses(self):
        self.assertEqual(
            calculate_expression("(1+2)*3"),
            9,
        )

    def test_decimal_numbers(self):
        self.assertEqual(
            calculate_expression("1.5+2.3"),
            3.8,
        )

    def test_unary_negative_number(self):
        self.assertEqual(
            calculate_expression("-5+8"),
            3,
        )

    def test_negative_operand(self):
        self.assertEqual(
            calculate_expression("3*-2"),
            -6,
        )

    def test_unary_positive_number(self):
        self.assertEqual(
            calculate_expression("+5+2"),
            7,
        )

    def test_division_by_zero(self):
        with self.assertRaisesRegex(
            ExpressionError,
            "Division by zero",
        ):
            calculate_expression("10/0")

    def test_invalid_expression(self):
        with self.assertRaisesRegex(
            ExpressionError,
            "Invalid expression",
        ):
            calculate_expression("1++*2")

    def test_empty_expression(self):
        with self.assertRaisesRegex(
            ExpressionError,
            "Expression cannot be empty",
        ):
            calculate_expression("")

    def test_unsupported_power_operator(self):
        with self.assertRaisesRegex(
            ExpressionError,
            "Unsupported operator",
        ):
            calculate_expression("2**3")

    def test_function_call_is_rejected(self):
        with self.assertRaisesRegex(
            ExpressionError,
            "Invalid expression",
        ):
            calculate_expression(
                "__import__('os').system('echo unsafe')"
            )

    def test_boolean_is_rejected(self):
        with self.assertRaisesRegex(
            ExpressionError,
            "Invalid number",
        ):
            calculate_expression("True")


if __name__ == "__main__":
    unittest.main()