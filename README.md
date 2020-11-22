# Sudoku

## Game Rules

Sudoku is traditionally played on a 9 x 9 board that is subdivided into 9 "zones", each size 3 x 3.

You can play Sudoku on boards of other sizes as well, as long as the board is a square (n x n), and the length of its sides is a square number, so that the board can be subdivided into n "zones", each of size sqrt(n) x sqrt(n).

For example, a board of size 4 x 4, with zones size 2 x 2, is valid.  Likewise a board of size 16 x 16, with zones size 4 x 4, is valid.  The largest board this program generates is a 16 x 16 board (although it may take some time).  The smallest board this program generates is size 4 x 4.  You could technically also play on a 1 x 1 board or even a 0 x 0 board, but those might not be very fun.

The game is played by filling the entire board with a given set of "tiles".

In a tradition Sudoku game using a 9 x 9 board, these tiles are the numbers 1 through 9.

The tiles can be any values, as long as there are exactly n distinct values (n being the size of the board).  On a 4 x 4 board, you will need 4 distinct tiles, and on a 16 x 16 board, you will need 16, etc..

The starting board contains a number of starting tiles which cannot be moved or altered.

To win, the rest of the board must be filled, following these rules:

* Each row must contain each tile exactly once.

* Each column must contain each tile exactly once.

* Each zone must contain each tile exactly once.

Once the entire board is filled and these guidelines are satisfied, you have solved the puzzle!


## Notes

...
