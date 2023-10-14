class Sol:
    word: String
    spos: (i32, i32)
    dir: (i32, i32)
    value: i32

def solve_cell(board, hand, pos, sol):
    for dir in DIRS:
        solve(..., pos, {
            word: "",
            spos: pos,
            dir: dir,
            value: 0,
        })

def solve(board, hand: Counter, pos, sol, best_sol):
    # Base case: end of board.
    if pos_oob(pos):
        return best_sol

    # Use letter already on board. 
    tile = board.tiles.at(pos)
    if tile != TILE_EMPTY:
        # Rec step.
        best_sol = better_sol(best_sol, solve(
            board, hand, board.step(pos, dir),
            sol {
                word: OLD + tile,
                value: board.acc_value(pos, OLD, tile),
                sol..
            },
            best_sol,
        ))

    # Use letter from hand (all combinations).
    for c in hand:
        # Word counts: consider it.
        if sol.word in vocab:
            best_sol = better_sol(best_sol, sol)

        # Rec step.
        best_sol = better_sol(best_sol, solve(
            board, hand.decr(c), board.step(pos, dir),
            sol {
                word: OLD + c,
                value: board.acc_value(pos, OLD, c),
                sol..
            },
            best_sol,
        ))

    return best_sol


def main():
    cur = Sol::empty()
    for pos in CELLS_POS:
        for dir in DIRS:
            sol = solve_cell(board, pos, Sol {
                dir: dir,
                Sol::empty()..
            })
            cur = better_sol(sol, cur)

    print(fmt_sol(cur))
