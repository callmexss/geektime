import re

p = re.compile(r"""(
            (^((-?\d+)(\.\d+)?)\s*)                     # float number with some spaces
            ((([%*/+-])\s*(-?\d+)(\.\d+)?\s*)*)             # one or more operator with float numbers as end
        )""", re.VERBOSE)

res = re.match(p, "2 * 3 + 3 * 4")
print(res.group())

help(re.sub)


'''
^((-?\d+)(\.\d+)?)\s*(([%*/+-])\s*(-?\d+)(\.\d+)?\s*)*
'''
