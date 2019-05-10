'''
File:          calculator.py
File Created:  Friday, 10th May 2019 3:59:28 pm
Author:        xss (callmexss@126.com)
Description:   simple calculator
-----
Last Modified: Friday, 10th May 2019 4:08:06 pm
Modified By:   xss (callmexss@126.com)
-----
'''

import re
import unittest

import pysnooper

# todo: simple add, subtract, multiple, divition
class Calculator():
    def __init__(self):
        """Initialize a calculator."""
        # self.simple_pattern = re.compile(r"\d*\s*[\\+-\\*/]\s*\d+")
        self.simple_pattern = re.compile(r"\d*\s*[*/+-]\s*\d+")
        self.sign_pattern = re.compile("[*/+-]")

    def _check(self, expr):
        if not isinstance(expr, str):
            return False
        
        return True if re.match(self.simple_pattern, expr) else False

    def _calculate(self, expr):
        sign = re.findall(self.sign_pattern, expr)[0]
        a, b = [int(x) for x in expr.split(sign)]
        if sign == "+":
            return a + b
        if sign == "-":
            return a - b
        if sign == "*":
            return a * b
        if sign == "/":
            if b == 0:
                raise(ZeroDivisionError)
            else:
                return a // b

    def _clean(self, expr):
        return expr.replace(" ", "")

    def calculate(self, expr):
        """try to calculate given expression
        
        :param expr: expression to calculate
        :type expr: str
        :return: output
        :rtype: int
        """
        if not self._check(expr):
            print("Invalid expression")
            return

        # expr = self._clean(expr);

        return self._calculate(expr)


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test__check(self):
        self.assertTrue(self.calculator._check("1+1"))
        self.assertTrue(self.calculator._check("1*   2"))
        self.assertTrue(self.calculator._check("1/1"))
        self.assertTrue(self.calculator._check("1   - 1"))
        self.assertFalse(self.calculator._check("a * 1"))
        self.assertFalse(self.calculator._check("a / b"))

    def test_sign(self):
        self.assertEqual(re.findall(self.calculator.sign_pattern, "1   +1")[0], "+")
        self.assertEqual(re.findall(self.calculator.sign_pattern, "1 -  1")[0], "-")
        self.assertEqual(re.findall(self.calculator.sign_pattern, "1 /1")[0], "/")

    def test_clean(self):
        self.assertTrue(self.calculator._clean("1 + 1"), "1+1")
        self.assertTrue(self.calculator._clean("1 +      1"), "1+1")
        self.assertTrue(self.calculator._clean("1     +     1"), "1+1")

    def test_calculate(self):
        self.assertEqual(self.calculator.calculate("1+1"), 2)
        self.assertEqual(self.calculator.calculate("1*3"), 3)
        self.assertEqual(self.calculator.calculate("21-1"), 20)

        with self.assertRaises(ZeroDivisionError):
            self.calculator.calculate("1/0")


if __name__ == '__main__':
    # unittest.main()
    calculator = Calculator()

    while True:
        try:
            expr = input(">>> ")
            print(calculator.calculate(expr))
        except ZeroDivisionError as e:
            print("divide by zero.")
        except KeyboardInterrupt as e:
            break 
