# re
import re

def get_all_combination():
    operators = [x for x in "+-*/%"]
    res = [''.join([a, b, c, d, e]) for a in operators \
          for b in operators \
          for c in operators \
          for d in operators \
          for e in operators]
    return [x for x in res if len(set(x)) == 5]

res = get_all_combination()
len(res)

valid = []
invalid = []

for each in res:
    try:
        re.compile(each)
        valid.append(each)
    except Exception as e:
        invalid.append(each)
