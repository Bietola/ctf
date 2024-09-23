from enum import Enum
from pprint import pprint
from pathlib import Path
from collections import Counter
from itertools import chain
from pygtrie import CharTrie


class Dir(Enum):
    RIGHT = 0
    UPRIGHT = 1
    DOWNRIGHT = 2
    LEFT = 3
    UPLEFT = 4
    DOWNLEFT = 5

def dir_long_str(dir):
    if dir == Dir.RIGHT:
        return 'right'
    elif dir == Dir.UPRIGHT:
        return 'up_right'
    elif dir == Dir.DOWNRIGHT:
        return 'down_right'

WORD_DIRS = [Dir.RIGHT, Dir.UPRIGHT, Dir.DOWNRIGHT]


class BType(Enum):
    DL = "dl"
    TL = "tl"
    DW = "dw"
    TW = "tw"
    M = "m"
    PORTALS = "portals"


class Bonus:
    def __init__(self, type, dir=None):
        self.type = type
        self.dir = dir

    def __repr__(self):
        if self.type == BType.PORTALS:
            return f'portals({self.dir})'
        else:
            return self.type.name

    @classmethod
    def from_str(cls, s):
        bonus_map = {
            "-": None,
            "dl": BType.DL,
            "tl": BType.TL,
            "dw": BType.DW,
            "tw": BType.TW,
            "m": BType.M,
            "pr": (BType.PORTALS, Dir.RIGHT),
            "pl": (BType.PORTALS, Dir.LEFT),
            "pur": (BType.PORTALS, Dir.UPRIGHT),
            "pul": (BType.PORTALS, Dir.UPLEFT),
            "pdr": (BType.PORTALS, Dir.DOWNRIGHT),
            "pdl": (BType.PORTALS, Dir.DOWNLEFT)
        }

        bonus = bonus_map.get(s)
        if not bonus:
            return cls(None, dir=None)
        elif isinstance(bonus, tuple):
            return cls(*bonus)
        else:
            return cls(bonus, dir=None)


class Board:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.tiles = []
        self.bonuses = []
        self.vocab = CharTrie()
        self.points = {}
        self.starting_words = set()

    def search_portal(self, dir):
        l = list(filter(lambda b: b[1].dir == dir, enumerate(self.bonuses)))
        assert(len(l) == 1)
        pos = l[0][0]
        y = pos // self.width
        x = pos % self.width
        return x, y

    def step(self, pos, dir):
        x, y = pos

        bonus = self.bonus_at(pos)
        if  bonus.type == BType.PORTALS:
            if bonus.dir == Dir.RIGHT:
                return self.search_portal(Dir.LEFT)
            elif bonus.dir == Dir.UPRIGHT:
                return self.search_portal(Dir.UPLEFT)
            elif bonus.dir == Dir.DOWNRIGHT:
                return self.search_portal(Dir.DOWNLEFT)

        if dir == Dir.RIGHT:
            return x + 1, y
        elif dir == Dir.LEFT:
            return x - 1, y
        elif dir == Dir.UPRIGHT:
            if y % 2 == 0:
                return x, y - 1
            else:
                return x + 1, y - 1
        elif dir == Dir.DOWNRIGHT:
            if y % 2 == 0:
                return x, y + 1
            else:
                return x + 1, y + 1
        else:
            assert(False and 'Shouldn\'t try to step in this direction')

    def tile_at(self, pos):
        x, y = pos

        # if self.is_oob(pos):
        #     print(f'tile_at: pos oob: {pos}')
        #     assert(False)

        # print(f'tile_at: pos oob: {pos}')

        return self.tiles[y * self.width + x]

    def bonus_at(self, pos):
        x, y = pos
        return self.bonuses[y * self.width + x]

    def is_oob(self, pos):
        x, y = pos
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def parse_tiles(self, lines):
        lines = lines.strip()
        self.tiles = list(map(lambda l: l.split(), lines.split('\n')))
        self.width = len(self.tiles[0])
        self.height = len(self.tiles)
        self.tiles = list(chain.from_iterable(self.tiles))

    def parse_bonuses(self, lines):
        lines = lines.strip()
        self.bonuses = list(map(
            lambda l: list(map(Bonus.from_str, l.split())),
            lines.split('\n')
        ))
        self.width = len(self.bonuses[0])
        self.height = len(self.bonuses)
        self.bonuses = list(chain.from_iterable(self.bonuses))

    def parse_vocab(self, lines):
        lines = lines.strip()
        for word in lines.split():
            self.vocab[word] = True

    def parse_points(self, lines):
        lines = lines.strip()

        self.points = {k: int(v) for k, v in (tuple(l.split(' ')) for l in lines.split('\n'))}

    def scan_starting_words(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                pos = x, y
                tile = self.tile_at(pos)
                if tile != '-':
                    for dir in WORD_DIRS:
                        self.starting_words.update(self.collect_words(pos, dir))

    def collect_words(self, pos, dir):
        ret = set()
        tile = self.tile_at(pos)
        word = ""
        while tile != '-':
            word += tile
            if word in self.vocab:
                ret.add(word)
            pos = self.step(pos, dir)
            tile = self.tile_at(pos)
        return ret


class Sol:
    def __init__(self, word="", spos=(0, 0), dir=None, value=0):
        self.word = word
        self.spos = spos
        self.dir = dir
        self.value = value
        self.tiles_placed = 0
        self.intersections = 0

    def fmt(self):
        x, y = self.spos
        return f'{self.word}_{x}{y}_{dir_long_str(self.dir)}_{int(self.value)}'

    def gt(self, other):
        return self.value > other.value \
            or self.word > other.word \
            or self.spos[0] > other.spos[0] \
            or self.spos[1] > other.spos[1]

    def copy_from(self, other):
        self.word = other.word
        self.spos = other.spos
        self.dir = other.dir
        self.value = other.value
        self.tiles_placed = other.tiles_placed
        self.intersections = other.intersections

    def add_tile(self, board, pos, tile, intersection_happened=False, tile_placed=False):
        if intersection_happened:
            self.intersections += 1
        if tile_placed:
            self.tiles_placed += 1

        self.word += tile

        bonus = board.bonus_at(pos)
        letter_val = board.points[tile]
        if bonus.type == BType.DL:
            letter_val *= 2
        elif bonus.type == BType.TL:
            letter_val *= 3
        self.value += letter_val
        if bonus.type == BType.DW:
            self.value *= 2
        elif bonus.type == BType.DW:
            self.value *= 3
        elif bonus.type == BType.M:
            self.value /= 2

    def rollback(self, board, pos, tile, intersection_happened=False, tile_placed=False):
        if intersection_happened:
            self.intersections -= 1
        if tile_placed:
            self.tiles_placed -= 1

        assert(tile == self.word[-1])
        self.word = self.word[:-1]

        bonus = board.bonus_at(pos)
        if bonus.type == BType.DW:
            assert(self.value % 2 == 0)
            self.value /= 2
        elif bonus.type == BType.DW:
            assert(self.value % 3 == 0)
            self.value /= 3
        elif bonus.type == BType.M:
            self.value *= 2
        letter_val = board.points[tile]
        if bonus.type == BType.DL:
            letter_val *= 2
        elif bonus.type == BType.TL:
            letter_val *= 3
        self.value -= letter_val


def solve_cell(board, hand, pos, sol):
    # TODO/DB
    print(pos)

    for dir in WORD_DIRS:
        solve(board, hand, pos, sol, Sol(
            word="",
            spos=pos,
            dir=dir,
            value=0
        ))

def solve(board, hand, pos, best_sol, sol):
    # TODO/DB
    # print(sol.word)

    # After first letter of word has been chosen.
    if len(sol.word) > 0:
        # Base case: Created invalid word.
        pass

        # Previously constructed word counts: consider it.
        # NB. First ever word is empty word, not considered by default.
        if sol.word in board.vocab \
                and sol.word not in board.starting_words \
                and sol.intersections > 0 \
                and sol.tiles_placed >= 1:
            if sol.gt(best_sol):
                best_sol.copy_from(sol)


    # Base case: end of board.
    if board.is_oob(pos):
        return

    # Use letter already on board. 
    tile = board.tile_at(pos)
    if tile != '-':
        # Rec step.
        sol.add_tile(board, pos, tile, intersection_happened=True)
        solve(
            board, hand,
            board.step(pos, sol.dir),
            best_sol,
            sol
        )
        ## Rollback.
        sol.rollback(board, pos, tile, intersection_happened=True)

    # Use letter from hand (all combinations).
    for tile in hand:
        # Kill if prefix not in vocab.
        if not board.vocab.has_subtrie(sol.word + tile):
            continue

        # Rec step.
        sol.add_tile(board, pos, tile, tile_placed=True)
        ## TODO/OPT: Don't copy hand.
        solve(
            board, hand - Counter(tile),
            board.step(pos, sol.dir),
            best_sol,
            sol
        )
        ## Rollback.
        sol.rollback(board, pos, tile, tile_placed=True)


def main():
    board = Board();
    board.parse_tiles(Path('./vadevwyu65gi_letters.txt').read_text())
    board.parse_bonuses(Path('./vadevwyu65gi_bonuses.txt').read_text())
    board.parse_vocab(Path('./hexa_scrabble_vocabulary.txt').read_text())
    board.parse_points(Path('./letter_points.txt').read_text())
    # print([l.split(' ') for l in Path('./letter_points.txt').read_text().strip().split('\n')])
    board.scan_starting_words()

    print(f'width: {board.width}')
    print(f'height: {board.height}')

    # print(board.tiles)
    # pprint(board.bonuses)

    hand = Counter(Path('./vadevwyu65gi_hand.txt').read_text())

    sol = Sol()
    for y in range(0, board.height):
        for x in range(0, board.width):
            solve_cell(board, hand, (x, y), sol)

    print(sol.fmt())

main()
