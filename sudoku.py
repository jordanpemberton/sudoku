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
Tile = Union[int, Text]
Board = List[List[Optional[Tile]]]
import random
import string


class SudokuBoard:
    """
    Class representing a Sudoku Board.
    """
    def __init__(self,
                 how_many_start_tiles: int =17,     # must be >=17
                 size: int =9,
                 zone_size: int =3,
                 tiles: Union[List[Tile], Text]
                    # =[i for i in range(1, 10)]            # using numerals
                    =string.ascii_uppercase                 # using letters
                ) -> None:
        """
        """
        self.size = size
        self.zone_size = zone_size
        self.tiles = set(tiles[:self.size])     # crop to match size
        self.empty_board = [
                            [None for i in range(self.size)]
                            for j in range(self.size)
                           ]
        self.solution_board = self.fill_board(self.empty_board)
        self.starting_board = self.make_start_board(self.solution_board, how_many_start_tiles)

    def print_solution_board(self) -> Text:
        return self.print_board(self.solution_board)

    def print_starting_board(self) -> Text:
        return self.print_board(self.starting_board)

    def print_board(self,
                    board
                   ) -> Text:
        """ To display a board """
        thick_vert = '|'
        thin_vert =  ':'
        thick_horz = '-----'
        thin_horz =  ' . . '

        out = ''
        for i in range(self.size):
            for j in range(self.size):
                if j % self.zone_size == 0:
                    out += thick_vert
                else:
                    out += thin_vert
                if i % self.zone_size == 0:
                    out += thick_horz
                else:
                    out += thin_horz
            out += thick_vert + '\n'
            for j in range(self.size):
                if j % self.zone_size == 0:
                    out += thick_vert + '  '
                else:
                    out += thin_vert + '  '
                out += board[i][j] + '  '
            out += thick_vert + '\n'
        for j in range(self.size):
            if j % self.zone_size == 0:
                out += thick_vert
            else:
                out += thin_vert
            out += thick_horz
        out += thick_vert + '\n'
        print(out)
        return out

    def fill_board(self,
                   board: Board
                  ) -> Board:
        """
        Fill the entire board with a valid solution.
        """
        # Start by filling two opposite zones
        board = self.fill_two_starter_zones(board)
        # Fill the rest of the board
        filled_board = False
        while not filled_board:
            filled_board = self.solve_board(board)
        return filled_board

    def fill_two_starter_zones(self,
                               board: Board
                              ) -> Board:
        """
        Start by filling two corner zones
        (with no shared rows or columns).
        """
        # Zone 1, top left
        start = 0
        end = start + self.zone_size
        board = self.fill_starter_zone(board, start, end)
        # Zone 9, bottom right
        start = self.size - self.zone_size          # 9 - 3 = 6
        end = self.size
        board = self.fill_starter_zone(board, start, end)
        return board

    def fill_starter_zone(self,
                          board: Board,
                          start: int,
                          end: int
                         ) -> Board:
        """ Fill one of the two starter corner zones. """
        tiles = self.tiles.copy()
        for r in range(start, end):
            for c in range(start, end):
                board[r][c] = tiles.pop()
        return board

    def solve_board(self,
                          board: Board,
                          row: int =0,
                          col: int =0
                         ) -> Union[Board, bool]:
        """
        Recursive function to solve /fill board.
        """
        # If end of board reached
        if row == self.size - 1 and col == self.size:
            # return True
            return board
        # If end of row reached
        if col == self.size:
            row += 1
            col = 0
        # If cell already filled
        if board[row][col] != None:
            return self.solve_board(board, row, col + 1)
        # Choose a tile, check if safe, insert tile
        for tile in self.tiles:
            if self.move_is_safe(board, row, col, tile):
                board[row][col] = tile
                # Recursively call fill func until all filled
                if self.solve_board(board, row, col + 1):
                    # return True
                    return board
            # If move invalid continue
            board[row][col] = None
        # If no more options, return False
        return False

    def move_is_safe(self,
                     board: Board,
                     row: int,
                     col: int,
                     tile: Tile
                    ) -> bool:
        """
        Check if a move (inserting tile into
        empty cell) is valid.
        """
        # Check column
        for c in range(self.size):
            if board[row][c] == tile:
                return False
        # Check row
        for r in range(self.size):
            if board[r][col] == tile:
                return False
        # Check zone
        start_row = row - row % self.zone_size
        start_col = col - col % self.zone_size
        for r in range(start_row, self.zone_size):
            for c in range(start_col, self.zone_size):
                if board[r][c] == tile:
                    return False
        return True

    def make_start_board(self,
                         board,
                         how_many_start_tiles: int
                        ) -> Board:
        """
        Remove tiles to make a starting puzzle board.
        Check if solvable.
        """
        tiles_remaining = self.size * self.size
        # while tiles_remaining >=
        return board

class Sudoku:
    """
    """
    def __init__(self,
                 how_many_start_tiles: int =17
                ) -> None:
        self.starting_tiles_num = how_many_start_tiles
        self.board = SudokuBoard(how_many_start_tiles)



if __name__ == '__main__':
    game = Sudoku()
    game.board.print_solution_board()