# Implementation a Calculator

## Basic Version

[calculator.py](./calculator.py)

### Example

```py
>>> 1 + 1
2
>>> 3 * 4
12
>>> 6 / 2
3
>>> 6 / 4
1
>>> 2 / 0
divide by zero.
>>> 3 - 1
2
>>> ls
Invalid expression
>>> exit
```

### Description

```text
Input: a simple math arthimetic expression, which only has two integer operands and one operator between them.
eg. "1+1", notice that there can be arbitary spaces between the operand and operators.

Output: an integer if input is valid else invalid expression or divide by zero exception.
```

For example the given input is "1 + 1", and we want the return value 2.

First of all, we should check whether the input is valid. Here I use a simple regular expression:

```py
# match expression
pattern = re.compile('\d+\s*[*/+-]\s*\d+')
```

Then we can get a valid expression if it matches such a pattern. Now just parse it:

```py
# find operator
pattern = re.compile('%*/+-')
```

Finally we can calculate it:

```py
# expr = "1 + 1"
# operator = "+"
a, b = expr.split(operator)
```

That's all.