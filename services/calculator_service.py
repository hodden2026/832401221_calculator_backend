import ast
import math
import operator


class ExpressionError(Exception):
    """表示数学表达式不合法或无法计算。"""


MAX_EXPRESSION_LENGTH = 200
MAX_AST_NODES = 100


BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def calculate_expression(expression):
    """安全地解析并计算数学表达式。"""

    if not isinstance(expression, str):
        raise ExpressionError(
            "Expression must be a string"
        )

    expression = expression.strip()

    if not expression:
        raise ExpressionError(
            "Expression cannot be empty"
        )

    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ExpressionError(
            "Expression is too long"
        )

    try:
        tree = ast.parse(
            expression,
            mode="eval",
        )

    except SyntaxError as exc:
        raise ExpressionError(
            "Invalid expression"
        ) from exc


    node_count = sum(
        1 for _ in ast.walk(tree)
    )

    if node_count > MAX_AST_NODES:
        raise ExpressionError(
            "Expression is too complex"
        )


    try:
        result = _evaluate_node(
            tree.body
        )

    except ZeroDivisionError as exc:
        raise ExpressionError(
            "Division by zero"
        ) from exc

    except (
        OverflowError,
        ValueError,
    ) as exc:
        raise ExpressionError(
            "Calculation error"
        ) from exc


    return _normalize_result(result)


def _evaluate_node(node):
    """递归计算允许的 AST 节点。"""

    if isinstance(
        node,
        ast.Constant,
    ):

        if isinstance(
            node.value,
            bool,
        ):
            raise ExpressionError(
                "Invalid number"
            )


        if isinstance(
            node.value,
            (int, float),
        ):

            if (
                isinstance(
                    node.value,
                    float,
                )
                and
                not math.isfinite(
                    node.value
                )
            ):
                raise ExpressionError(
                    "Invalid number"
                )

            return node.value


        raise ExpressionError(
            "Invalid value"
        )


    if isinstance(
        node,
        ast.BinOp,
    ):

        operator_type = type(
            node.op
        )


        if (
            operator_type
            not in BINARY_OPERATORS
        ):
            raise ExpressionError(
                "Unsupported operator"
            )


        left = _evaluate_node(
            node.left
        )

        right = _evaluate_node(
            node.right
        )


        if (
            operator_type is ast.Div
            and
            right == 0
        ):
            raise ExpressionError(
                "Division by zero"
            )


        result = BINARY_OPERATORS[
            operator_type
        ](
            left,
            right,
        )


        if (
            isinstance(
                result,
                float,
            )
            and
            not math.isfinite(
                result
            )
        ):
            raise ExpressionError(
                "Calculation result is too large"
            )


        return result


    if isinstance(
        node,
        ast.UnaryOp,
    ):

        operator_type = type(
            node.op
        )


        if (
            operator_type
            not in UNARY_OPERATORS
        ):
            raise ExpressionError(
                "Unsupported unary operator"
            )


        operand = _evaluate_node(
            node.operand
        )


        return UNARY_OPERATORS[
            operator_type
        ](
            operand
        )


    raise ExpressionError(
        "Invalid expression"
    )


def _normalize_result(result):
    """优化浮点结果显示。"""

    if isinstance(
        result,
        float,
    ):

        if not math.isfinite(
            result
        ):
            raise ExpressionError(
                "Invalid calculation result"
            )


        result = round(
            result,
            12,
        )


        if result == 0:
            return 0


        if result.is_integer():
            return int(result)


    return result