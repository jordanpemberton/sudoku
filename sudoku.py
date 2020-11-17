# (1) Generate a full, solved board (save solution board)
#       (a) Start by filling two opposite corner zones with shuffles tiles
#       (b) Recursively fill the rest of the board, returning False if not valid
# (2) Remove tiles until you have a puzzle board (save as puzzle board)
# (3) Validate that the board is solveable (solve)
# (4) Let player play by inputting coords and tile vals
#       (a) validate if moves are valid (empty square)
#       (b) check if board is full
#       (c) once full, compare to solution board


from typing import Dict, List, Optional, Set, Text, Tuple, Union
# import random
import string


class SudokuBoard:
    """
    """
    def __init__(self,
                 how_many_start_tiles: int =17,
                 size: int =9,
                 region_size: int =3,
                 tiles: Union[List[Union[int, Text]],Text]
                    # =[i for i in range(1, 10)]
                    =string.ascii_uppercase
                ) -> None:
        """
        """
        self.size = size
        self.region_size = region_size
        self.tiles = set(tiles[:self.size])
        self.board = [
                      [None for i in range(self.size)]
                      for j in range(self.size)
                     ]

    def __str__(self) -> Text:
        out = (' ___' * self.size) + '\n'
        for row in self.board:
            out += '| '
            for cell in row:
                out += cell + ' | '
            out += '\n'
            out += ('|___' * self.size) + '|\n'
        return out

    def fill_board(self,
                   row: int =0,
                   col: int =0
                  ) -> bool:
        """
        """
        if row == self.size - 1 and col == self.size:
            return True
        if col == self.size:
            row += 1
            col = 0
        if self.board[row][col] != None:
            return self.fill_board(row, col + 1)
        for tile in self.tiles:
            if self.move_is_safe(row, col, tile):
                self.board[row][col] = tile
                if self.fill_board(row, col + 1):
                    return True
            self.board[row][col] = None
        return False

    def move_is_safe(self,
                     row: int,
                     col: int,
                     tile: Union[int, Text]
                    ) -> bool:
        """
        """
        for c in range(self.size):
            if self.board[row][c] == tile:
                return False
        for r in range(self.size):
            if self.board[r][col] == tile:
                return False
        start_row = row - row % self.region_size
        start_col = col - col % self.region_size
        for r in range(self.region_size):
            for c in range(self.region_size):
                if self.board[start_row + r][start_col + c] == tile:
                    return False
        return True


class Sudoku:
    """
    """
    def __init__(self, how_many_start_tiles: int =17):
        self.starting_tiles_num = how_many_start_tiles
        self.solution_board = SudokuBoard(how_many_start_tiles)
        self.solution_board.fill_board()
        self.starting_board = None
        self.playing_board = None

    def print_solution_board(self):
        print(self.solution_board)


if __name__ == '__main__':
    game = Sudoku()
    print(game.solution_board)
    game.print_solution_board()