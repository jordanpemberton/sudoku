# Sudoku

## Brief Description & Game Rules

Sudoku is played on a grid of size n<sup>2</sup> x n<sup>2</sup>, that is subdivided into n<sup>2</sup> equal "zones", each of size n x n.  A set of n<sup>2</sup> distinct symbols are used to fill these cells.  Initially, some cells on the board contain a symbol, and these starting "clue" cells cannot be altered.  Moves are made by inserting symbols into empty or non-starting cells.

To win, the entire board must filled, following these rules:

1. Each row must contain each symbol exactly once.

2. Each column must contain each symbol exactly once.

3. Each zone must contain each symbol exactly once.

A standard game of Sudoku uses a board of size 9 x 9 that is subdivided into 9 equal zones, each size 3 x 3.  In a standard Sudoku game, the 9 distinct symbols used are the numbers 1 through 9, and to solve the game, each row, column, and zone must contain each number 1 through 9 exactly once.

This program generates, solves, and allows users to play Sudoku on boards of size 4 x 4, 9 x 9, or 16 x 16.  16 x 16 boards might be (very) slow to generate, but 16 x 16 boards with more starting tiles (>~130) should generate faster.

By default, the "tiles" used are the numbers 1 through n<sup>2</sup>, but players can also chose to use letter tiles.

The number of starting tiles can be changed, as long the number of starting tiles is more than a required minimum, and less than the total number of cells.


## How to Run

Run this program with Python3.  This program will not run in Python2.

Run this program by running the file `sudoku.py` via the command line however you normally run Python3 files, i.e.

    python3 sudoku.py

or, if on Windows,

    py -3 sudoku.py

or, if Python3 is your default version of Python, simply

    python sudoku.py


## How to Play

Upon starting a game, you may choose to use the default game options (9 x 9 board, 17 starting tiles, number tiles), or you may customize your game by selecting a board size (4 x 4, 9 x 9, or 16 x 16), number of starting clue tiles, and tile set (numbers or letters).

The game is played via the terminal.  Upon each move, you will be shown the board, and asked to enter a row, column, and tile to make a move.  Once you have filled the board, if the game is not yet solved, you can continue playing. If the game is solved, you can choose to begin a new game or exit.

![Sudoku Screengrab](/docs/sudoku_screengrab.png)

Happy solving!


## Write-Up on NP-Completeness, Algorithms Used, & Time Complexity

![Sudoku Writeup](/docs/sudoku_writeup.pdf)
