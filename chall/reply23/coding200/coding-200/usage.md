# Honey for Scarabs

## In a Nutshell
You are given a Honeycomb Scrabble grid and a list of available letters which is your hand. The goal is to find the best play possible (put a word on the grid) to achieve the highest amount of points.

## The grid
The grid is made of honeycomb (hexagonal) cells. 
Every cell of the grid can be empty or contain a letter. Each cell could have a peculiar property: a bonus.

The coordinates convention is the following:
- The upper left cell has coordinates 0, 0
- The bottom right cell has coordinates size, size

A visual representation of the grid and coordinates can be found in the file `example_coords.jpg`.

Two files are provided for each grid: letters and bonuses. Both files contain information for the same grid.

### Letters
The file named `<id>_letters.txt` contains the bi-dimensional representation of the Honeycomb grid letters. The cells are divided by a space. If a cell is empty, it is represented by a minus character (`-`).

### Bonuses
The file named `<id>_bonuses.txt` contains the bi-dimensional representation of the Honeycomb grid bonuses. 
The bonuses are the following:
- `dl` - _Double letter_ - Doubles the value of the letter placed there;
- `tl` - _Triple letter_ - Triples the value of the letter placed there;
- `dw` - _Double word_ - Doubles the value of the word **substring up to the current letter**.
- `tw` - _Triple word_ - Triples the value of the word. It works similarly to the Double word bonus.
- `m` - _Mine_ - Halves the value of the word, rounded down. It works similary to the Double word bonus.
- `portals` - Described in the portals section.

More details on the bonuses in the Score Computation section.

### Portals
There is one last bonus you can find in the bonuses grid: portals. They are referenced as `pr`, `pl`, `pur`, `pul`, `pdr`, `pdl`. Respectively `portal right`, `portal left`, `portal up right`, `portal up left`, `portal down right`, `portal down left`.
Portals modify the adjacency of two cells. If I am in a cell with a portal and I move in the **corresponding direction**, I end up in the **opposite portal**.

For example:
- If you are on `portal right` and move **right**, you end up in `portal left`.
- If you are on `portal up right` and move **up_right**, you end up in `portal down_left`.
- If you are on `portal down right` and move **down_right**, you end up in `portal up_left`.

And vice versa.
After the "teleportation" occurs, you keep moving in the same direction.

Note that if, for example, you are on `portal up right` and move **down_right** (or **right**), nothing special happens and you move normally.

An example of the portals movement can be found on the image `filled_grid_example.jpg`.

### Hand
The file named `<id>_hand.txt` contains a list of letters available for the current level. Each single character can be used only once. For example, if the file contains the string `AFIODA` you can use two `A`s but only one `F`.

## How to place a word
There are some rules you have to follow to legally place a word on the grid:
- You can place words only in directions: `right`, `up_right`, `down_right`.
- You cannot place a word already present on the grid.
- The word must link (overlap on) to a single letter of at least one word already on the grid.
- The word you place cannot, in any way, touch a letter of a word already on the grid. Of course with the exception of the linking letter from the rule above.
- You can extend a word already placed on the grid, but the complete word must be a valid one (MAKE -> MAKERS).
- You can use only the letters given as your 'hand'. Each letter in the 'hand' must be treated like a physical object, you cannot use the same letter twice (i.e. if your hand is [E, R, E, A] you can use up to 2 'E' but only one 'A'). You are not required to use all the letters.
- When you connect your word with a word already on the grid, you don't need to use a letter from your hand, the letter is already down on the grid.
- You must stay between the boundaries of the Honeycomb grid.

Please note that a portal effectively changes the adjacency between two cells: the north west cell of a cell with `portal_up_left` is the one with `portal_down_right`, and not the cell "geometrically" on the north west side.

## Score Computation
Example on points computation:
- Word: HOUSE
- Scores: H->2, O->1, U->3, S->1, E->1
- Bonuses: O placed on `dl`, U placed on `dw`

Score computation: 
- \+ 2 for H = 2
- \+ 1*2 (`dl`) for O = 4
- \+ 3 for U = 7
- \* 2 (U is on `dw`) = 14
- \+ 1 for S = 15
- \+ 1 for E = 16

Total score: 16

## The solution
For each level, given the board (grid), the values of the letters, the vocabulary and your hand, you must provide the best word you can place on the grid. The word must be legal considering all the rules written above.
The "best" solution is the one providing most points.
This is how ties are broken:
- Alphabetical order: GREEN > TUNE
- X coordinate (lower is better)
- Y coordinate (lower is better)
- down_right > right > up_right

The solution of a level must be formatted as follows: `<word>_<sX><sY>_<direction>_<value>`, where:
- **word** is the best word you can place. All letters must be uppercase.
- **sX**, **sY** are the starting coordinates of the word
- **direction** is the direction in which the word has been placed. Can be three values:
    - right
    - up_right
    - down_right
- **value** is the integer of the points scored with the solution.
 
### IMPORTANT!
Some tools have issues when extracting encrypted zip archives, saying the password is invalid. For unzipping archives we strongly recommend using 7zip.
