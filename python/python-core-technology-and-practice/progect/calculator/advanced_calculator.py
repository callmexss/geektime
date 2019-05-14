'''
File:          advanced_calculator.py
File Created:  Monday, 13th May 2019 8:38:53 pm
Author:        xss (callmexss@126.com)
Description:   advanced calculator
-----
Last Modified: Monday, 13th May 2019 8:38:57 pm
Modified By:   xss (callmexss@126.com)
-----
'''

import re
import string
import unittest

import pysnooper

from calculator import Calculator
from calculator import process


class AdvancedCalculator(Calculator):
    def __init__(self):
        self.operator = "+-*/^"
        self.float = re.compile(r"^((-?\d+))(\.\d+)?$")
        self.valid_chars = string.digits + "+-*/%^()." + string.whitespace
        self.parenthesis_pattern = re.compile("[()]")
        self.expr_without_parenthesis = re.compile("[^()]")
        self.advanced_pattern = re.compile(r"""(
            (^((-?\d+)(\.\d+)?)\s*)                        # float number with some spaces
            ((([%*/+-])\s*(-?\d+)(\.\d+)?\s*)*)            # one or more operator with float numbers as end
        )""", re.VERBOSE)

    def _extract_all_parenthesis(self, expr):
        return re.findall(self.parenthesis_pattern, expr)

    def _extract_expr_without_parenthesis(self, expr):
        return re.findall(self.expr_without_parenthesis, expr)

    def _check_parenthesis(self, expr):
        """Use a stack to check whether there are invalid parenthesis in expression.

        :param expr: expression only contains valid characters
        :type expr: str
        :return: if no parenthesis or valid parenthesis True else False
        :rtype: bool
        """
        parenthesis = self._extract_all_parenthesis(expr)
        if not parenthesis:
            return True

        stack = []
        for each in parenthesis:
            if each is '(':
                stack.append(each)
            else:
                if not stack:
                    return False
                stack.pop()

        if stack:
            return False
        return True

    def _check_expr_without_parenthesis(self, expr):
        expr = self._extract_expr_without_parenthesis(expr)
        if re.match(self.advanced_pattern, "".join(expr)):
            return True
        return False

    def _check(self, expr):
        expr = self._clean(expr)
        if any([x not in self.valid_chars for x in expr]):
            return False
        if not self._check_parenthesis(expr):
            return False
        if not self._check_expr_without_parenthesis(expr):
            return False
        return True

    def _clean(self, expr):
        return super()._clean(expr)

    # @pysnooper.snoop()
    def _infix_to_postfix(self, infixexpr):
        opstack = []
        output = []
        operators = {
            '^': 4,
            '*': 3,
            '/': 3,
            '%': 3,
            '+': 2,
            '-': 2,
            '(': 1
        }

        num = []
        for i, token in enumerate(infixexpr):
            # put digits in a stack
            if token in string.whitespace:
                continue

            if token in string.digits or token is '.':
                if i == len(infixexpr) - 1:
                    if num:
                        num.append(token)
                        output.append(''.join(num))
                        num = []
                    else:
                        output.append(token)
                    break
                else:
                    num.append(token)
                    continue
            
            if num:
                output.append(''.join(num))
                num = []

            if token is '(':
                opstack.append(token)
            elif token is ')':
                while opstack[-1] is not '(':
                    output.append(opstack.pop())
                opstack.pop()
            elif token in operators:
                if not opstack:
                    opstack.append(token)
                else:
                    while opstack:
                        if operators[opstack[-1]] >= operators[token]:
                            output.append(opstack.pop())
                        else:
                            break
                    opstack.append(token)

        while opstack:
            output.append(opstack.pop())

        return ' '.join(output)

    def _convert_str_to_num(self, n):
        if isinstance(n, int) or isinstance(n, float):
            return n
        else:
            try:
                return float(n)
            except Exception as e:
                print(e)

    def _inner_calculate(self, first, second, token):
        try:
            first = self._convert_str_to_num(first)
            second = self._convert_str_to_num(second)
        except Exception:
            return None

        if token is '+':
            return first + second
        if token is '-':
            return first - second
        if token is '*':
            return first * second
        if token is '/':
            return first / second
        if token is '%':
            return first % second
        if token is '^':
            return first ** second
        else:
            return None

    # @pysnooper.snoop()
    def _postfix_eval(self, postfixexpr):
        operand_stack = []

        for token in postfixexpr.split():
            if re.match(self.float, token):
                operand_stack.append(token)
            elif token in self.operator:
                later = operand_stack.pop()
                former = operand_stack.pop()
                operand_stack.append(self._inner_calculate(former, later, token))
        
        return operand_stack.pop()


    # @pysnooper.snoop()
    def _calculate(self, expr):
        expr = self._clean(expr)
        postfix = self._infix_to_postfix(expr)
        return self._postfix_eval(postfix)

    # @pysnooper.snoop()
    def calculate(self, expr):
        return super().calculate(expr)
    

class TestAdvancedCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = AdvancedCalculator()
        self.valid = ["3 * 4 - 2",
                      "(2 * 3) + (3 * 4)",
                      "1 + 2 * 3 + (4 / 5)",
                      ]
        self.invalid = ["3a * 4 - 2",
                        "(2 * 4) + 3 * 2)",
                        ]

    def test__check(self):
        for expr in self.valid:
            self.assertTrue(self.calculator._check(expr))
        for expr in self.invalid:
            self.assertFalse(self.calculator._check(expr))

    def test__extract_parenthesis(self):
        self.assertEqual(self.calculator._extract_all_parenthesis(
            "(3*4)+2"), [x for x in "()"])
        self.assertEqual(self.calculator._extract_all_parenthesis(
            "(3*4)+(2*4)"), [x for x in "()()"])
        self.assertEqual(self.calculator._extract_all_parenthesis(
            "(3*4)+(2(*4)"), [x for x in "()(()"])

    def test__check_parenthesis(self):
        self.assertTrue(self.calculator._check_parenthesis(""))
        self.assertTrue(self.calculator._check_parenthesis("()"))
        self.assertTrue(self.calculator._check_parenthesis("()()"))
        self.assertTrue(self.calculator._check_parenthesis("()(())"))

    def test_expr_without_parenthesis(self):
        for expr in self.valid:
            self.assertEqual(
                self.calculator._extract_expr_without_parenthesis(expr),
                [x for x in expr if x not in "()"]
            )

    def test__inifx_to_postfix(self):
        infix_to_postfix = self.calculator._infix_to_postfix
        self.assertEqual(infix_to_postfix("4 - 2"), "4 2 -")
        self.assertEqual(infix_to_postfix("5 * 3 ^ (4 - 2)"), "5 3 4 2 - ^ *")
        self.assertEqual(infix_to_postfix("3 + 4 * 2"), "3 4 2 * +")
        self.assertEqual(infix_to_postfix("(3 + 4) * 2"), "3 4 + 2 *")
        self.assertEqual(infix_to_postfix("(12 + 4) * 20"), "12 4 + 20 *")
        self.assertEqual(infix_to_postfix("1 - 0.5"), "1 0.5 -")
        self.assertEqual(infix_to_postfix("(1 - 0.5) / 2"), "1 0.5 - 2 /")

    def test__inner_calculate(self):
        calculate = self.calculator._inner_calculate
        self.assertAlmostEqual(calculate(1, 2, '+'), 1 + 2)
        self.assertAlmostEqual(calculate(1, 2, '*'), 1 * 2)
        self.assertAlmostEqual(calculate(1, 2, '/'), 1 / 2)
        self.assertAlmostEqual(calculate(1, 2, '%'), 1 % 2)
        self.assertAlmostEqual(calculate(2, 2, '^'), 2 ** 2)
        self.assertAlmostEqual(calculate(1, 0.5, '-'), 1 - 0.5)
        self.assertEqual(calculate(1, -0.5, '/'), 1 / -0.5)

    def test_calculate(self):
        calculate = self.calculator.calculate
        self.assertEqual(calculate("(3 * 4) + 4 - 2"), (3 * 4) + 4 - 2)
        self.assertEqual(calculate("4 - 2"), 4 - 2)
        self.assertEqual(calculate("5 * 3 ^ (4 - 2)"), 5 * 3 ** (4 - 2))
        self.assertEqual(calculate("3 + 4 * 2"), 3 + 4 * 2)
        self.assertEqual(calculate("(3 + 4) * 2"), (3 + 4) * 2)
        self.assertEqual(calculate("12 + 12"), 12 + 12)
        self.assertEqual(calculate("(12 + 4) * 20"), (12 + 4) * 20)
        self.assertEqual(calculate("3.14 + 1"), 3.14 + 1)
        # self.assertEqual(calculate("3.14 * -1"), 3.14 * -1) # how to handle this input


if __name__ == '__main__':
    # unittest.main()
    calculator = AdvancedCalculator()
    process(calculator)
    