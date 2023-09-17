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

    for row in chain(grid, grid.T, diags(grid), diags(np.fliplr(grid))):
        # Rows back and forth
        if word in ''.join(row) or word in ''.join(reversed(row)):
            return True

    return False

print('\n'.join(list(filter(
    find_word,
    Path('test-words.txt').read_text().splitlines()
))))
