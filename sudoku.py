# (1) Generate a full, solved board (save solution board)
#       indexes = {index: [tile options]}
#       filled = stack[indexes in order filled] for backtracking
#
#       (a) Fill by the 9 sub regions, starting with two opposite corners
#       (b) Pick a random index from remaining empties in the region (range(9))
#       (c) Tile to insert is next up in this index's list of options
#       (d) If there is a next option:
#               - Check row, coll, and region to make sure option is valid
#               - If invalid, remove from list, try next until valid option found or...
#       (e) If no remaining options for this index, you need to backtrack:
#               - Grab most recent insert from top of stack
#               - Choose the next option in the list of options
#               - If no remaining options here, reset all options, and
#                 keep popping next most recent insert/ resetting their options
#                 until you've found one with a next option to try.
#
# (2) Remove tiles until you have a puzzle board (save as puzzle board)
# (3) Validate that the board is solveable (solve)
# (4) Let player input coords and vals
#       (a) validate if moves are valid (empty square)
#       (b) check if board is full
#       (c) once full, compare to solution board


from typing import List, Optional, Text, Tuple, Union
import random


class Sudoku:
    """
    """
    def __init__(self, how_many_start_tiles=17):
        self._start_num = how_many_start_tiles
        self.solution_board = self._fill_solution_board()
        self.starting_board = self._make_starting_board()
        self.playing_board = self._make_new_empty_board()
        self.tiles = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'}

    def _fill_solution_board(self):
        solu_board = self._make_new_empty_board()

        # indexes = {index: [tile options]}
        index_opt_map = {i: {t for t in self.tiles} for i in range(81)}
        filled_stack = []           # stack of indexes in order filled for backtracking

        # (a) Fill by the 9 sub regions, starting with two opposite corners
        # Region 1 (top left)
        region_rows = [0, 1, 2]
        region_cols = [0, 1, 2]
        # (b) Pick a random index from remaining empties in the region (range(9))
        random.shuffle(region_rows)
        random.shuffle(region_cols)
        for row in region_rows:
            for col in region_cols:
                self._fill_cell(solu_board, row, col, index_opt_map, filled_stack)


        return solu_board

    def _fill_cell(self, board, row, col, index_map, fill_stack):
        # Fill in this cell
        index = row * 9 + col
        opts = index_map[index]

        # Tile to insert is next up in this index's list of options
        opt_is_valid = False

        # While no valid opt picked and more options to check:
        while not opt_is_valid and len(opts) > 0:
            opt_is_valid = True

            opt = opts[0]
            # Check row, col, and region to make sure option is valid
            if opt in board[row]:
                opt_is_valid = False
            elif opt in board[col]:
                opt_is_valid = False
            else:
                other_region_rows_to_check = []
                other_region_cols_to_check = []

                if row % 3 == 0:
                    other_region_rows_to_check.append(row + 1, row + 2)
                elif row % 3 == 1:
                    other_region_rows_to_check.append(row + 1, row - 1)
                else:
                    other_region_rows_to_check.append(row - 1, row - 2)

                if col % 3 == 0:
                    other_region_cols_to_check.append(col + 1, col + 2)
                elif col % 3 == 1:
                    other_region_cols_to_check.append(col + 1, col - 1)
                else:
                    other_region_cols_to_check.append(col - 1, col - 2)

                while opt_is_valid:
                    for check_row in other_region_rows_to_check:
                        for check_col in other_region_cols_to_check:
                            if board[check_row][check_col] == opt:
                                opt_is_valid = False

            # If option is invalid, remove from list, try again until valid option found or...
            if not opt_is_valid:
                opts = opts[1:]

        # If no remaining options for this index, you need to backtrack
        if not opt_is_valid and len(opts) == 0:
            return False

        # Valid option(s), update filled stack and continue
        filled_stack.append(index)
        return board, filled_stack


    def _backtrack_boardfill(self):

        #         - Grab most recent insert from top of stack
        #         - Choose the next option in the list of options
        #         - If no remaining options here, reset all options, and
        #             keep popping next most recent insert/ resetting their options
        #             until you've found one with a next option to try.


    def _make_starting_board(self):
        # Make a new board, with solution copied into
        start_board = self._make_new_empty_board(self.solution_board)
        # Remove all but the number of starting tiles
        n = 81
        cells = [i for i in range(81)]
        while n > self._start_num and len(cells) > 0:
            # Pick random cell on board
            rand_cell = random.choice(cells)
            cells.remove(rand_cell)
            rand_row = rand_cell // 9
            rand_col = rand_cell % 9
            # If filled, make empty, n--
            if start_board[rand_row][rand_col] != 0:
                start_board[rand_row][rand_col] = 0
                n -= 1
        return start_board



    def _make_new_empty_board(self, board_to_copy=[]):
        board = [[0 for c in range(9)] for r in range(9)]
        # If given a board to copy:
        for row in range(9):
            for col in range(9):
                board[row][col] = board_to_copy[row][col]

        return board

