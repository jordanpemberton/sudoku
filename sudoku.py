# (1) Generate a full, solved board (save solution board)
#       indexes = {index: [tile options]}
#       filled = stack[indexes in order filled] for backtracking
#       (a) Start by filling two opposite corner zones with shuffles tiles
#       (b) Pick a random index from remaining empties on the board
#       (c) Tile to insert is next up in this index's list of options
#       (d) If there is a next option:
#               - Check row, coll, and "zone" to make sure option is valid
#               - If invalid, remove from list, try next until valid option found or...
#       (e) If no remaining options for this index, you need to backtrack:
#               * Backtracking should be Depth first, so recursive :(
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


from typing import Dict, List, Optional, Set, Text, Tuple, Union
import random


class SudokuBoard:
    """
    """
    def __init__(self, how_many_start_tiles: int =17):
        self.index_opts_map = {}
        self.filled_stack = []
        self.board =


class Sudoku:
    """
    """
    def __init__(self, how_many_start_tiles: int =17):
        self._start_num = how_many_start_tiles
        self.solution_board = self._fill_solution_board()
        self.starting_board = self._make_starting_board()
        self.playing_board = self._make_new_empty_board()
        self.tiles = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'}

    def _fill_solution_board(self):
        solu_board = self._make_new_empty_board()

        # indexes = {index: [tile options]}
        index_opts_map = {i: {t for t in self.tiles} for i in range(81)}
        filled_stack = []           # stack of indexes in order filled for backtracking

        # (a) Fill by the 9 sub zones, starting with two opposite corners
        # zone 1 (top left)
        zone_rows = [0, 1, 2]
        zone_cols = [0, 1, 2]

        # (b) Pick a random index from remaining empties in the zone (range(9))
        random.shuffle(zone_rows)
        random.shuffle(zone_cols)
        for row in zone_rows:
            for col in zone_cols:
                # Attempt to fill cell
                res = self._fill_cell(solu_board, row, col, index_opts_map, filled_stack)
                # If invalid, backtrack:
                if res is None:
                    res = self._backtrack_boardfill(solu_board, index_opts_map, filled_stack)
                # If valid, continue

        return solu_board

    def _fill_cell(self,
                   board: List[List[Text]],
                   row: int,
                   col: int,
                   index_opts_map: Dict[int, Set[Text]],
                   filled_stack: List[int]
                  ) -> Optional[Tuple[List[List[int]], List[int]]]:
        # Fill in cell at this index
        index = row * 9 + col
        # Find options for this index in index opts map
        opts = index_opts_map[index]

        opt_is_valid = False

        # While no valid opt yet picked and more opts remaining to check:
        while not opt_is_valid and opts.size > 0:
            opt = opts.pop()
            opt_is_valid = True

            # Check board row for duplicate
            if opt in board[row]:
                opt_is_valid = False
            # Check board col for duplicate
            elif opt in board[col]:
                opt_is_valid = False
            # Check board zone for duplicate
            else:
                # 2 other rows, cols in zone to check:
                zone_row_a = row
                zone_row_b = row
                zone_col_a = col
                zone_col_b = col

                if row % 3 == 0:
                    zone_row_a += 1
                    zone_row_b += 2
                elif row % 3 == 1:
                    zone_row_a += 1
                    zone_row_b -= 1
                else:
                    zone_row_a -= 1
                    zone_row_b -= 2

                if col % 3 == 0:
                    zone_col_a += 1
                    zone_col_b += 2
                elif col % 3 == 1:
                    zone_col_a += 1
                    zone_col_b -= 1
                else:
                    zone_col_a -= 1
                    zone_col_b -= 2

                while opt_is_valid:
                    for r in [zone_row_a, zone_row_b]:
                        for c in [zone_col_a, zone_col_b]:
                            if board[r][c] == opt:
                                opt_is_valid = False

            # If opt is not valid, try again until valid opt found or...

        # If no remaining opts for this index, you need to backtrack
        if not opt_is_valid:
            return

        # Valid option(s), update filled stack and continue
        filled_stack.append(index)
        return board, filled_stack

    def _backtrack_boardfill(self,
                             board: List[List[int]],
                             index_opts_map: Dict[int, Set[Text]],
                             filled_stack: List[int]
                            ) -> Optional[List[]]:
        # Grab most recent insert from top (end) of stack
        last_filled = filled_stack[-1]
        # Choose the next option in the list of options
        # If no remaining options here, reset all options, and
        # keep popping next most recent insert/ resetting their options
        # until you've found one with a next option to try.
        pass

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
        board = [['' for c in range(9)] for r in range(9)]
        # If given a board to copy:
        for row in range(9):
            for col in range(9):
                board[row][col] = board_to_copy[row][col]

        return board

