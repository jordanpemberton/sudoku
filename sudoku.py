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
import copy


class SudokuBoard:
    """
    Class representing a Sudoku Board.
    """
    def __init__(self,
                 how_many_start_tiles: int =17,     # must be >=17 if 9x9
                 tile_type: Text ='numeric',
                 size: int =9,
                 zone_size: int =3
                ) -> None:
        """
        """
        if zone_size > size:
            return
        if how_many_start_tiles >= (size * size):
            return

        self.size = size
        self.zone_size = zone_size
        self.tile_type = tile_type
        self.tiles = self.make_tile_set(tile_type, size)

        self.empty_board = [
                            [None for i in range(size)]
                            for j in range(size)
                           ]
        self.solution_board = self.fill_board()
        self.playing_board_empties = set([i for i in range(size)])
        self.starting_board = self.make_start_board(how_many_start_tiles)
        self.playing_board = copy.deepcopy(self.starting_board)
        self.temp_board = None

    def make_tile_set(self, tile_type, size: int) -> Set[Tile]:
        # Using alpha letters
        if tile_type == 'alpha':
            tiles_itr = string.ascii_uppercase
        # Using numerals
        else:
            tiles_itr = [i for i in range(1, size + 1)]
        # Crop to match size, return set
        return set(tiles_itr[:size])

    def print_solution_board(self) -> Text:
        return self.print_board(self.solution_board)

    def print_starting_board(self) -> Text:
        return self.print_board(self.starting_board)

    def print_playing_board(self) -> Text:
        return self.print_board(self.playing_board)

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
                if board[i][j] is not None:
                    out += str(board[i][j])
                else:
                    out += ' '
                out += '  '
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

    def fill_board(self
                  ) -> Board:
        """
        Fill the entire board with a valid solution.
        """
        filled_board = False
        while not filled_board:
            board = copy.deepcopy(self.empty_board)
            # Start by filling two opposite zones
            board = self.fill_two_starter_zones(board)
            # Fill (solve) the rest of the board
            filled_board = self.solve_board(board)
        # Board is solvable and filled
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
        """
        Fill one of the two starter corner zones.
        """
        # Make a list of tiles, random shuffle
        tiles = list(copy.copy(self.tiles))
        random.shuffle(tiles)
        # Enter tiles into zone:
        for r in range(start, end):
            for c in range(start, end):
                board[r][c] = tiles.pop()
        return board

    def solve_board(self,
                    board: Board
                   ) -> Board:
        """
        Make a copy of the board and try
        to solve /fill.
        """
        solved = False
        while not solved:
            # Set temp board to board to solve
            self.temp_board = copy.deepcopy(board)
            # Attempt to solve /fill
            solved = self.recurs_solve_board()
        return self.temp_board

    def recurs_solve_board(self,
                    row: int =0,
                    col: int =0
                   ) -> bool:
        """
        Recursive function to solve /fill board.
        """
        # If end of board reached
        if row == self.size - 1 and col == self.size:
            return True
        # If end of row reached
        if col == self.size:
            row += 1
            col = 0
        # If cell already filled
        if self.temp_board[row][col] is not None:
            return self.recurs_solve_board(row, col + 1)
        # Choose a tile, check if safe, insert tile
        for tile in self.tiles:
            if self.check_if_valid_entry(self.temp_board, row, col, tile):
                self.temp_board[row][col] = tile
                # Recursively call fill func until all filled
                if self.recurs_solve_board(row, col + 1):
                    return True
            # If move invalid continue
            self.temp_board[row][col] = None
        # If no more options, return False
        return False

    def check_if_valid_entry(self,
                             board: Board,
                             row: int,
                             col: int,
                             entry: Tile =None
                            ) -> bool:
        """
        Check if entry is valid
        """
        # If not entering a new tile
        if entry is None:
            entry = board[row][col]
        # Check column
        for c in range(self.size):
            if board[row][c] == entry:
                return False
        # Check row
        for r in range(self.size):
            if board[r][col] == entry:
                return False
        # Check zone
        start_row = row - row % self.zone_size
        start_col = col - col % self.zone_size
        for r in range(start_row, start_row + self.zone_size):
            for c in range(start_col, start_col + self.zone_size):
                if board[r][c] == entry:
                    return False
        return True

    def make_start_board(self,
                         how_many_start_tiles: int
                        ) -> Board:
        """
        Remove tiles to make a starting puzzle board.
        Check if solvable.
        """
        solvable = False
        while not solvable:
            # Start with solution board copy
            board = copy.deepcopy(self.solution_board)
            n = self.size * self.size
            # Make list of indexes, random shuffle
            indexes_remaining = [i for i in range(n)]
            self.playing_board_empties = set(indexes_remaining)
            random.shuffle(indexes_remaining)
            # Count how many tiles remaining
            remaining_tile_count = n
            # Remove tiles until target num remaining
            while remaining_tile_count >= how_many_start_tiles:
                i = indexes_remaining.pop()
                row = i // self.size
                col = i % self.size
                board[row][col] = None
                remaining_tile_count -= 1

            solvable = self.solve_board(board)
        # Board is solvable, save which indexes were removed
        self.playing_board_empties -= set(indexes_remaining)
        return board

    def is_game_solved(self) -> bool:
        for row in self.playing_board:
            for col in row:
                if not self.check_if_valid_entry(self.playing_board, row, col):
                    return False
        return True

    def play_game(self):
        while self.playing_board_empties:
            # Print the playing board
            self.print_playing_board()
            # Take /make a move
            self.take_move()
        if self.is_game_solved:
            print('YOU WIN!!')
        else:
            print('hmm, not quite right...')

    def get_row_col_input(self) -> Tuple[int, int]:
        row = None
        col = None
        while not isinstance(row, int) or not row in range(self.size):
            print('Please enter a row:      ', end='')
            row = input()
            try:
                row = int(row)
            except:
                print('    That is not a number')
        while not isinstance(col, int) or not col in range(self.size):
            print('Please enter a column:   ', end='')
            col = input()
            try:
                col = int(col)
            except:
                print('that is not a number')
        return row, col

    def get_tile_input(self) -> Tile:
        print('Please chose a value from these available values:')
        print(self.tiles)
        tile = input()
        while tile.upper() not in self.tiles:
            tile = input()
        return tile.upper()

    def take_move(self) -> None:
        row, col = self.get_row_col_input()
        # If a starting index
        while self.starting_board[row][col] is not None:
            print('That cell cannot be edited. Please try again.')
            row, col  = self.get_row_col_input()
        # If editing a cell
        if self.playing_board[row][col] is not None:
            print('Would you like to edit this cell? Y/N')
            to_edit = input()
            while to_edit.upper() != 'N' and to_edit.upper() != 'Y':
                print('Eh???')
                to_edit = input()
            if to_edit.upper() == 'N':
                row, col = self.get_row_col_input()
        tile = self.get_tile_input()
        self.make_move(row, col, tile)

    def make_move(self,
                  row: int,
                  col: int,
                  tile: Tile
                 ) -> None:
        # Enter the selection onto board
        self.playing_board[row][col] = tile
        # Remove index from empties set
        index = row * self.size + col
        self.playing_board_empties.remove(index)


if __name__ == '__main__':
    game = SudokuBoard()
    # game.print_solution_board()
    game.play_game()
