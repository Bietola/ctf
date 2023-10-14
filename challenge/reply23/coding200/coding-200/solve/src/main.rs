use std::collections::HashSet;
use std::fs;
use std::str::FromStr;

#[derive(Debug)]
enum Bonus {
    Empty,
    DL,  // Double letter - Doubles the value of the letter placed there.
    TL,  // Triple letter - Triples the value of the letter placed there.
    DW,  // Double word - Doubles the value of the word substring up to the current letter.
    TW,  // Triple word - Triples the value of the word. It works similarly to the Double word bonus.
    M,   // Mine - Halves the value of the word, rounded down. It works similarly to the Double word bonus.
    Portals(i32, i32),  // Described in the portals section.
}

impl FromStr for Bonus {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        use Bonus::*;
        match s {
            "-" => Ok(Empty),
            "dl" => Ok(DL),
            "tl" => Ok(TL),
            "dw" => Ok(DW),
            "tw" => Ok(TW),
            "m" => Ok(M),
            "pr" => Ok(Portals(1, 0)),
            "pl" => Ok(Portals(-1, 0)),
            "pur" => Ok(Portals(1, -1)),
            "pul" => Ok(Portals(-1, -1)),
            "pdr" => Ok(Portals(1, 1)),
            "pdl" => Ok(Portals(-1, 1)),
            _ => Err(()),
        }
    }
}

fn parse_letters(file_path: &str) -> Vec<char> {
    fs::read_to_string(file_path).unwrap()
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect()
}

fn parse_bonuses(file_path: &str) -> Vec<Bonus> {
    fs::read_to_string(file_path).unwrap()
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect()
}

fn parse_vocab(file_path: &str) -> HashSet<String> {
    fs::read_to_string(file_path).unwrap()
        .split_whitespace().map(|s| s.to_string()).collect()
}

fn idx(x: usize, y: usize) -> usize {
    y * BOARD_WIDTH + x
}

// The solution of a level must be formatted as follows: `<word>_<sX><sY>_<direction>_<value>`, where:
// - **word** is the best word you can place. All letters must be uppercase.
// - **sX**, **sY** are the starting coordinates of the word
// - **direction** is the direction in which the word has been placed. Can be three values:
//     - right
//     - up_right
//     - down_right
// - **value** is the integer of the points scored with the solution.
struct Sol {
    word: String,
    sx: i32,
    sy: i32,
    dir: (i32, i32),
    value: i32,
}

fn solve(letters: &[char], x: i32, y: i32, sol: Sol) {
    // Try words starting in all possible letters, in all possible directions.
    if sol.word.is_empty() {
        for dir in DIRS {
            try_word(Sol {
                word: 
                dir: dir
        }
    }
    try_word(Sol {
        word: ""
    })
    for c in b'a'..=b'z' {
        out[idx(x, y)]
    }
    letters
}

fn main() {
    let vocab = parse_vocab("hexa_scrabble_vocabulary.txt");
    let letters = parse_letters("vadevwyu65gi_letters.txt");
    let bonuses = parse_bonuses("vadevwyu65gi_bonuses.txt");
    println!("{:?}", vocab);
    println!("{:?}", letters);
    println!("{:?}", bonuses);
}
