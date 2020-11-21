# (1) Generate a full, solved board (save solution board)
#       (a) Start by filling two opposite corner zones with shuffles tiles
#       (b) Recursively fill the rest of the board, returning False if not valid
# (2) Remove tiles until you have a puzzle board (save as puzzle starting board)
# (3) Validate that the board is solveable (solve)
# (4) Play! Let player input coords and tile vals
#       (a) validate if moves are valid (empty square or edit-able)
#       (b) check if board is full
#       (c) once full, compare to solution to check for win


from typing import Dict, List, Optional, Set, Text, Tuple, Union
Board = List[List[Optional[Text]]]
import random
import string
import copy


class Sudoku:
    """
    Class representing a Sudoku Board.
    """
    def __init__(self,
                 how_many_start_tiles: int =None,     # must be >=17 if 9x9
                 tile_type: Text ='numeric',
                 size: int =9
                ) -> None:
        """
        Call new game to initiate, start a new game.
        """
        self.new_game(how_many_start_tiles, tile_type, size)

    def new_game(self,
                 how_many_start_tiles: int =None,
                 tile_type: Text ='numeric',
                 size: int =9
                ) -> None:
        """
        """
        valid_sizes = {
                       4:  2,
                       9:  3,
                       16: 4,
                       # 25: 5
                      }
        default_start_count = {
                               4 : 7,
                               9 : 17,
                               16: 31,
                               # 25, 49
                              }

        if size not in valid_sizes:
            size = 9

        if (how_many_start_tiles is None or
            how_many_start_tiles >= (size * size) or
            how_many_start_tiles < (2 * size - 1)):
            how_many_start_tiles = default_start_count[size]
            # print('Start count not given or invalid, start count = ', how_many_start_tiles)

        self.size = size
        self.zone_size = valid_sizes[size]
        self.how_many_start_tiles = how_many_start_tiles

        self.tile_type = tile_type
        self.tiles = self.make_tile_set(tile_type, size)

        self.empty_board = [
                            [None for i in range(size)]
                            for j in range(size)
                           ]
        self.temp_board = copy.deepcopy(self.empty_board)
        self.solution_board = self.fill_board()
        self.playing_board_empties = set([i for i in range(size)])
        self.starting_board = self.make_start_board(how_many_start_tiles)
        self.playing_board = copy.deepcopy(self.starting_board)
        # Start playing!
        self.play_game()

    def make_tile_set(self, tile_type, size: int) -> Set[Text]:
        # Using alpha letters
        if tile_type == 'alpha':
            tiles_itr = string.ascii_uppercase
        # Using numerals
        else:
            tiles_itr = [str(i) for i in range(1, size + 1)]
        # Crop to match size, return set
        return set(tiles_itr[:size])

    def print_solution_board(self) -> Text:
        return self.print_board(self.solution_board)

    def print_starting_board(self) -> Text:
        return self.print_board(self.starting_board)

    def print_playing_board(self) -> Text:
        return self.print_board(self.playing_board)

    def print_temp_board(self) -> Text:
        return self.print_board(self.temp_board)

    def print_board(self,
                    board
                   ) -> Text:
        """ To display a board """
        thick_vert = '|'
        thin_vert =  ':'
        thick_horz = '-----'
        thin_horz =  ' . . '

        out = '     '
        # Column number labels
        for col in range(self.size):
            out += '   ' + str(col) + '  '
        out += '\n'
        # Rows
        for row in range(self.size):
            # Horizontal border row
            out += '     '
            for c in range(self.size):
                if c % self.zone_size == 0:
                    out += thick_vert
                else:
                    out += thin_vert
                if row % self.zone_size == 0:
                    out += thick_horz
                else:
                    out += thin_horz
            out += thick_vert + '\n'

            # Row number label
            out += '  ' + str(row) + '  '
            # Row contents
            for c in range(self.size):
                if c % self.zone_size == 0:
                    out += thick_vert + '  '
                else:
                    out += thin_vert + '  '
                # Cell contents
                if board[row][c] is not None:
                    out += str(board[row][c])
                else:
                    out += ' '
                out += '  '
            out += thick_vert + '\n'
        # Bottom border
        out += '     '
        for c in range(self.size):
            if c % self.zone_size == 0:
                out += thick_vert
            else:
                out += thin_vert
            out += thick_horz
        out += thick_vert + '\n'
        print(out)
        return out

    def fill_board(self) -> Board:
        """
        Fill the entire board with a valid solution.
        uses self.temp_board
        """
        solvable = False
        while not solvable:
            # Copy the empty board
            self.temp_board = copy.deepcopy(self.empty_board)
            # Start by filling two opposite zones
            self.fill_two_starter_zones()
            # Fill (solve) the rest of the board
            solvable = self.solve_board()
        # Board is solvable and filled
        return self.temp_board

    def fill_two_starter_zones(self) -> None:
        """
        Start by filling two corner zones
        (with no shared rows or columns).
        Uses self.temp_board.
        """
        # Fill top left zone on temp board
        start = 0
        end = self.zone_size
        self.fill_starter_zone(start, end)

        # Fill bottom right zone on temp board
        start = self.size - self.zone_size
        end = self.size
        self.fill_starter_zone(start, end)

    def fill_starter_zone(self,
                          start: int,
                          end: int
                         ) -> None:
        """
        Fill one of the two starter corner zones.
        Uses self.temp_board.
        """
        # Make a list of tiles, random shuffle
        tiles = list(copy.deepcopy(self.tiles))
        random.shuffle(tiles)
        # Enter tiles into zone:
        for r in range(start, end):
            for c in range(start, end):
                # Fill in zone on temp board
                self.temp_board[r][c] = tiles.pop()

    def solve_board(self,
                    row: int =0,
                    col: int =0
                   ) -> bool:
        """
        Recursive function to solve /fill board.
        Uses self.temp_board.  (Copy the board
        you want to solve into temp board first)
        Returns True or False.
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
            return self.solve_board(row, col + 1)
        # Choose a tile, check if safe, insert tile
        for tile in self.tiles:
            if self.check_if_valid_entry(row, col, tile):
                self.temp_board[row][col] = tile
                # Recursively call fill func until all filled
                if self.solve_board(row, col + 1):
                    return True
            # If move invalid continue
            self.temp_board[row][col] = None
        # If no more options, return False
        return False

    def check_if_valid_entry(self,
                             row: int,
                             col: int,
                             entry: Text =None
                            ) -> bool:
        """
        Check if entry is valid.
        Uses temp board.
        """
        # If not entering a new tile
        if entry is None:
            entry = self.temp_board[row][col]
        # Check column
        for c in range(self.size):
            if self.temp_board[row][c] == entry:
                return False
        # Check row
        for r in range(self.size):
            if self.temp_board[r][col] == entry:
                return False
        # Check zone
        start_row = row - row % self.zone_size
        start_col = col - col % self.zone_size
        for r in range(start_row, start_row + self.zone_size):
            for c in range(start_col, start_col + self.zone_size):
                if self.temp_board[r][c] == entry:
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
            while remaining_tile_count > how_many_start_tiles:
                i = indexes_remaining.pop()
                row = i // self.size
                col = i % self.size
                board[row][col] = None
                remaining_tile_count -= 1
            # Check if start board is solvable
            # (Save to temp board first)
            self.temp_board = copy.deepcopy(board)
            solvable = self.solve_board()
        # Board is solvable, save which indexes were removed
        self.playing_board_empties -= set(indexes_remaining)
        return board

    def is_game_solved(self) -> bool:
        # If there are multiple solutions, comparing to solution
        # board won't work, so need to check using solve func
        # return self.playing_board == self.solution_board
        self.temp_board = copy.deepcopy(self.playing_board)
        return self.solve_board()

    def play_game(self):
        solved = False
        while not solved:
            if not self.playing_board_empties:
                print('hmm, not quite right...')
                self.take_move()
            while self.playing_board_empties:
                # Print the playing board
                self.print_playing_board()
                # Take /make a move
                self.take_move()
            # All cells have been filled, check if solved:
            solved = self.is_game_solved
        # Game solved!
        print('YOU WIN!!')
        # Start new game...
        print('New game? (Y/N)')
        start_new_game = input()
        if start_new_game.upper() == 'Y':
            self.new_game(size=self.size,
                          how_many_start_tiles=self.how_many_start_tiles,
                          tile_type=self.tile_type)

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
            if row not in range(self.size):
                print('    Out of range')
        while not isinstance(col, int) or not col in range(self.size):
            print('Please enter a column:   ', end='')
            col = input()
            try:
                col = int(col)
            except:
                print('    That is not a number')
            if col not in range(self.size):
                print('    Out of range')
        return row, col

    def get_tile_input(self) -> Text:
        print('Please chose a value from these available values:')
        print(self.tiles)
        tile = input()
        while tile.upper() not in self.tiles:
            print('    Invalid choice, try again')
            tile = input()
        return tile.upper()

    def take_move(self) -> None:
        row, col = self.get_row_col_input()
        # If a starting index
        while self.starting_board[row][col] is not None:
            print('    That cell cannot be edited. Please try again.')
            row, col  = self.get_row_col_input()
        # If editing a cell
        while self.playing_board[row][col] is not None:
            print('Would you like to edit this cell? Y/N')
            to_edit = input()
            while to_edit.upper() != 'N' and to_edit.upper() != 'Y':
                print('    Eh???')
                to_edit = input()
            if to_edit.upper() == 'N':
                row, col = self.get_row_col_input()
            else:
                # Empty the cell
                index = row * self.size + col
                self.playing_board_empties.add(index)
                self.playing_board[row][col] = None
        # Get tile input
        tile = self.get_tile_input()
        self.make_move(row, col, tile)

    def make_move(self,
                  row: int,
                  col: int,
                  tile: Text
                 ) -> None:
        # Enter the selection onto board
        self.playing_board[row][col] = tile
        # Remove index from empties set
        index = row * self.size + col
        self.playing_board_empties.remove(index)


if __name__ == '__main__':
    game = Sudoku(tile_type='alpha',
                  size =4,
                  how_many_start_tiles =14
                 )
