import op

OP_SUM = 1
OP_MUL = 2
OP_SUB = 3
OP_DIV = 4

a 16 *
b 2 -
c 13 +
d 1 -
e 3 -
f 48 *
g 12 +
h 5 +

cmds = {
    'a': (0, 10, OP_SUM),
    'b': (0, (POSITIVE_INF, 0), OP_SUB)
}

def do_ops(cmd, lhs, rhs):
    if cmd == OP_SUM:
        return lhs + rhs
    elif cmd == OP_MUL:
        return lhs * rhs
    elif cmd == OP_SUB:
        m = lhs[0]
        M = lhs[1]
        return (min(m, rhs), max(M, rhs))

def solve(grid, cmds, x, y, out):
    for atmp in range(1, N):
        if atmp

        acc    = cmds[grid[x][y]][0]
        target = cmds[grid[x][y]][1]
        opr    = cmds[gird[x][y]][2]
        new_acc = do_ops(ops, acc, atmp)

        if new_acc > target:
            continue

        if y == MAX_Y and x == MAX_X:
            

        if x == MAX_X:
            solve(grid, cmds, 0, y + 1)
        else:
            solve(grid, cmds, x + 1, y)

def main():
    solve()
