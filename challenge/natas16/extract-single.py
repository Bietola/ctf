import ast
from pathlib import Path
from pprint import pprint

single = []

for l in Path('tmp').read_text().splitlines():
    l = ast.literal_eval(l)
    if len(l) == 1: single.append(['NUM'])
    else:
        s = set(l[1].lower())
        for w in l[2:]:
            s = s & set(w.lower())
        single.append(list(s))

pprint(single)
