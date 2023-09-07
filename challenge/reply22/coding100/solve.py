from pathlib import Path
from pprint import pprint
import numpy as np
from itertools import chain

grid = np.array(list(map(
    lambda s: s.split(),
    Path('test-grid.txt').read_text().splitlines()
)))

n, m = grid.shape

def find_word(word):
    def diags(mat):
        return (np.diagonal(grid, i) for i in range(-n+1, n))

    for r, row in enumerate(chain(grid, grid.T, diags(grid), diags(np.fliplr(grid)))):
        # Rows back and forth
        if (p := ''.join(row).find(word)) != -1:
            mat[r,p:p+len(word)] = '_'

        if word in ''.join(reversed(row)):
            if (p := ''.join(reversed(row)).find(word)) != -1:
                mat[r,p:p+len(word)] = '_'

    return False

print('\n'.join(list(filter(
    find_word,
    Path('test-words.txt').read_text().splitlines()
))))
