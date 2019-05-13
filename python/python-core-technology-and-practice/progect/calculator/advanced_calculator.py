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
        self.valid_chars = string.digits + "+-*/%()." + string.whitespace
        self.parenthesis_pattern = re.compile("[()]")
        self.expr_without_parenthesis = re.compile("[^()]")
        self.advanced_pattern = re.compile(r"""(
            (^((-?\d+)(\.\d+)?)\s*)                        # float number with some spaces
            ((([%*/+-])\s*(-?\d+)(\.\d+)?\s*)*)             # one or more operator with float numbers as end
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

    @pysnooper.snoop()
    def _calculate(self, expr):
        expr = self._clean(expr)

    @pysnooper.snoop()
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

    def test_calculate(self):
        pass


if __name__ == '__main__':
    # unittest.main()
    calculator = AdvancedCalculator()
    process(calculator)
    
