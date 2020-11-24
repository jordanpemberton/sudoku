# (1) Generate a full, solved board (save solution board)
#       (a) Start by filling two opposite corner zones with shuffles tiles
#       (b) Recursively fill the rest of the board, returning False if not valid
# (2) Remove tiles until you have a puzzle board (save as puzzle starting board)
# (3) Validate that the board is solveable (solve)
# (4) Play! Let player input coords and tile vals
#       (a) validate if moves are valid (empty square or edit-able)
#       (b) check if board is full
#       (c) once full, compare to solution to check for win

# size 16 might take a while...
# size 25 takes forever

from typing import Dict, List, Optional, Set, Text, Tuple, Union
Board = List[List[Optional[Text]]]
import random
import string
import copy


class Sudoku:
    """
    Class representing a Sudoku Board.
    """
    def __init__(self) -> None:
        """
        Call new game to initiate, start a new game.
        """
        self.default_tile_set = 'N'
        self.default_size = 9
        self.valid_sizes = {
                            4:  2,
                            9:  3,
                            16: 4
                            # 25: 5
                           }
        self.default_start_counts = {
                                     4 : 4,
                                     9 : 17,
                                     16: 54
                                     # 25: 132
                                    }
        self.new_game()

    def customize_new_game(self) -> None:
        print('Would you like to customize your new game?  (Y/N)')
        do_customize = input()
        while do_customize.upper() != 'Y' and do_customize.upper() != 'N':
            print('     Please enter \'Y\' for yes or \'N\' for no.')
            do_customize = input()
        if do_customize.upper() == 'Y':
            self.get_new_game_input()

    def get_new_game_input(self) -> None:
        # Board size
        self.get_board_size_input()
        # How many starting tiles
        self.get_how_many_starting_tiles_input()
        # Tile set
        self.get_tile_set_input()

    def get_board_size_input(self) -> None:
        valid_size = False
        sizes_str = '  '.join(str(key) for key in self.valid_sizes.keys())
        print('What size board would you like?')
        while not valid_size:
            print('Please choose from these available sizes:')
            print(sizes_str)
            size = input()
            try:
                size = int(size)
            except:
                pass
            if size in self.valid_sizes:
                valid_size = True
        self.size = size

    def get_how_many_starting_tiles_input(self) -> None:
        valid_starting_num = False
        max_start_tiles = self.size * self.size
        min_start_tiles = self.default_start_counts[self.size] - 1
        print('How many starting tiles would you like?')
        while not valid_starting_num:
            print('Number of starting tiles must be less than ' +
                  str(max_start_tiles) +
                  ' and more than ' +
                  str(min_start_tiles) +
                  '.'
                 )
            how_many_start_tiles = input()
            try:
                how_many_start_tiles = int(how_many_start_tiles)
            except:
                pass
            if (how_many_start_tiles > min_start_tiles and
                how_many_start_tiles < max_start_tiles):
                valid_starting_num = True
        self.how_many_start_tiles = how_many_start_tiles

    def get_tile_set_input(self) -> None:
        valid_tile_set = False
        print('Would you like to use number or letter tiles?')
        while not valid_tile_set:
            print('Enter \'N\' for numbers or \'L\' for letters:')
            tile_set = input()
            if tile_set.upper() == 'N' or tile_set.upper() == 'L':
                valid_tile_set = True
        self.tile_set = tile_set.upper()

    def new_game(self) -> None:
        """
        """
        # Start with default values
        self.size = self.default_size
        self.how_many_start_tiles = self.default_start_counts[self.size]
        self.tile_set = self.default_tile_set
        # Allow player to change defaults
        self.customize_new_game()
        # Make your set of tiles
        self.tiles = self.make_tile_set()
        # Determine correct zone size
        self.zone_size = self.valid_sizes[self.size]

        # Make an empty board
        self.empty_board = [
                            [None for i in range(self.size)]
                            for j in range(self.size)
                           ]

        # Empty cells on playing board (determined when starting board is made)
        self.playing_board_empties = set([i for i in range(self.size)])

        # Temp board used for solving
        self.temp_board = copy.deepcopy(self.empty_board)
        # Answer board
        self.solution_board = self.fill_board()

        # Starting puzzle board
        self.starting_board = self.make_start_board(self.how_many_start_tiles)
        # Playing board
        self.playing_board = copy.deepcopy(self.starting_board)

        # Start playing!
        self.play_game()

    def make_tile_set(self) -> List[Text]:
        # Using alpha letters
        if self.tile_set.upper() == 'L':
            tiles_itr = string.ascii_uppercase
        # Using numerals (default)
        else:
            tiles_itr = [str(i) for i in range(1, self.size + 1)]
        # Crop to match size, return set
        return list(tiles_itr[:self.size])

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
        starting_tile_emp_left = '['
        starting_tile_emp_right = ']'

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
            if row > 9:
                out += ' ' + str(row) + '  '
            else:
                out += '  ' + str(row) + '  '

            # Row contents
            for c in range(self.size):
                if c % self.zone_size == 0:
                    out += thick_vert
                else:
                    out += thin_vert
                # Cell contents
                if board[row][c] is not None:
                    tile = board[row][c]
                    # If a starting tile
                    if self.solution_board[row][c] is not None:
                        out += (' ' +
                                starting_tile_emp_left +
                                tile +
                                starting_tile_emp_right
                               )
                    else:
                        out += '  ' + tile + ' '
                    if len(tile) == 1:
                        out += ' '
                else:
                    out += '     '
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

    def get_zone_order(self) -> List[Tuple[int, int]]:
        """
        Determine the order in which to search zones.
        """
        order = []
        end = self.zone_size
        mid = self.zone_size // 2 + 1
        for i in range(mid):
            order.append((i, i))
            if end - i - 1 != i:
                order.append((end - i - 1, end - i - 1))
            for j in range(i):
                order.append((i, j))
                order.append((j, i))
                order.append((end - i - 1, end - j - 1))
                order.append((end - j - 1, end - i - 1))

        return order

    def fill_board_by_zones(self) -> bool:
        """
        Attempting to fill the board in a 'smarter'
        way, but not quite working.
        """
        # (filling zones in linear order:)
        # for z_row in range(self.zone_size):
        #     for z_col in range(self.zone_size):
        #       ...

        # Solve zones working out from starting corners,
        # along the outer sides and across the corner-corner diagonal:
        zone_order = self.get_zone_order()
        print(zone_order)

        for z_row, z_col in zone_order:
            start_row = z_row * self.zone_size
            end_row = start_row + self.zone_size
            start_col = z_col * self.zone_size
            end_col = start_col + self.zone_size
            zone_solved = self.solve_zone(start_row, end_row, start_col, end_col, start_row, start_col)

            if not zone_solved:
                break

        return zone_solved

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

            # (attempting to fill by zone...)

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

    def solve_zone(self,
                   start_row: int,
                   end_row: int,
                   start_col: int,
                   end_col: int,
                   row: int,
                   col: int,
                  ) -> bool:
        """
        Solve a single zone, return True if solvable,
        else return False.
        Note: Zone range is not inclusive, and end_row
        and end_col not included in the current zone.
        Uses self.temp_board.
        """
        # If end of row reached:
        if col == end_col:
            # Next row:
            row += 1
            col = start_col
            # If end of row reached:
            if row == end_row:
                return True

        # If cell already filled:
        if self.temp_board[row][col] is not None:
            return self.solve_zone(start_row, end_row, start_col, end_col, row, col + 1)

        # Choose a tile, check if safe, insert tile if safe
        for tile in self.tiles:
            if self.check_if_valid_entry(row, col, tile):
                self.temp_board[row][col] = tile
                # Recursively fill zone
                if self.solve_zone(start_row, end_row, start_col, end_col, row, col + 1):
                    return True
            # If tile ivalid continue
            self.temp_board[row][col] = None

        return False

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
                if c != col:
                    return False
        # Check row
        for r in range(self.size):
            if self.temp_board[r][col] == entry:
                if r != row:
                    return False
        # Check zone
        start_row = row - row % self.zone_size
        start_col = col - col % self.zone_size
        for r in range(start_row, start_row + self.zone_size):
            for c in range(start_col, start_col + self.zone_size):
                if self.temp_board[r][c] == entry:
                    if (r, c) != (row, col):
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
        # board won't work, so need to check for solution
        self.temp_board = copy.deepcopy(self.playing_board)
        self.print_temp_board()
        for index in range(self.size * self.size):
            row = index // self.size
            col = index % self.size
            if not self.check_if_valid_entry(row, col):
                return False
        return True

    def play_game(self):
        # print('New game!')
        # print('Enter \'RESET\' at any point to reset game to starting state.')
        # how would make reset opt?
        solved = False
        while not solved:
            # Print the playing board
            self.print_playing_board()
            # If board is filled
            if not self.playing_board_empties:
                # Check if solved
                solved = self.is_game_solved()
                # If not solved, continue playing
                if not solved:
                    print('     Hmmm, that\'s not quite right...')
            # Get the next move:
            if not solved:
                self.take_move()

        # Game solved!
        print('YOU WIN!!')
        # Start new game...
        print('New game?  (Y/N)')
        start_new_game = input()
        if start_new_game.upper() == 'Y':
            self.new_game()

    def get_row_col_input(self) -> Tuple[int, int]:
        row = None
        col = None
        while not isinstance(row, int) or not row in range(self.size):
            print('Please enter a row:      ', end='')
            row = input()
            try:
                row = int(row)
            except:
                print('    That is not a number.')
            if row not in range(self.size):
                print('    Out of range.')
        while not isinstance(col, int) or not col in range(self.size):
            print('Please enter a column:   ', end='')
            col = input()
            try:
                col = int(col)
            except:
                print('    That is not a number.')
            if col not in range(self.size):
                print('    Out of range.')
        return row, col

    def get_tile_input(self) -> Text:
        print('Please choose from these available values:')
        print('     ' + '  '.join(tile for tile in self.tiles))
        tile = input()
        while tile.upper() not in self.tiles:
            print('    Invalid choice, please try again.')
            tile = input()
        return tile.upper()

    def take_move(self) -> None:
        row, col = self.get_row_col_input()
        # If a starting index
        while self.starting_board[row][col] is not None:
            print('    That cell cannot be edited. Please choose a different cell.')
            row, col  = self.get_row_col_input()
        # If editing a cell
        while self.playing_board[row][col] is not None:
            print('Would you like to edit cell (' + str(row) +
                  ', ' + str(col) + ')?  Y/N')
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
    game = Sudoku()
