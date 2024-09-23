class Sol:
    word: String
    spos: (i32, i32)
    dir: (i32, i32)
    value: i32

def solve_cell(board, hand, pos, sol):
    for dir in DIRS:
        solve(board, hand, pos, best_sol=sol, Sol(
            word="",
            spos=pos,
            dir=dir,
            value=
        ))

def solve(board, hand: Counter, pos, best_sol, sol)
    # Previously constructed word counts: consider it.
    ## NB. First ever word is empty word, not considered by default.
    if sol.word in vocab:
        if Sol.cmp(sol, best_sol) > 0:
            best_sol.copy_from(sol)

    # Base case: end of board.
    if pos_oob(pos):
        return

    # Use letter already on board. 
    tile = board.tiles.at(pos)
    if tile != TILE_EMPTY:
        # Rec step.
        sol.add_tile(board, pos, tile)
        ### sol.word += tile
        ### sol.value = board.acc_value(pos, sol.value, tile)
        best_sol = solve(
            board, hand, board.step(pos, dir),
            sol,
            best_sol,
        )
        ## Rollback.
        ### sol.word = sol.word[:-1]
        sol.rollback(board, pos)

    # Use letter from hand (all combinations).
    for c in hand:
        # Rec step.
        sol.add_tile(board, pos, c)
        ### sol.word += tile
        ### sol.value = board.acc_value(pos, sol.value, tile)
        ## TODO: Don't copy hand.
        best_sol = solve(
            board, hand.decr(c), board.step(pos, dir),
            sol,
            best_sol,
        )
        ## Rollback.
        ### sol.word = sol.word[:-1]
        sol.rollback(board, pos)


def main():
    sol = Sol()
    for pos in CELLS_POS:
        solve_cell(board, pos, sol)

    print(sol.fmt())
