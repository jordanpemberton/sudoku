class Board:
    def __init__(self):
        self.tiles = set(['A', 'B', 'C'])
        self.board = [[None for i in range(3)] for j in range(3)]
        # self.options = [[self.tiles[:] for i in range(3)] for j in range(3)]
        self.unvisited = set((i, j) for j in range(3) for i in range(3))
        self.visited = []        # stack
        # self.filled_map = dict()     # filled in selections

    def fill_board(self, row=0, col=0):
        if row == 2 and col == 3:
            return True
        if col == 3:
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


    def move_is_safe(self, row, col, tile):
        for i in range(3):
            if self.board[row][i] == tile:
                return False
        for i in range(3):
            if self.board[i][col] == tile:
                return False
        # For checking regions
        # start_row = row - row % 3
        # start_col = col - col % 3
        # for i in range(3):
        #     for j in range(3):
        #         if self.board[i + start_row][j + start_col] == tile:
        #             return False
        return True


    # def fill_board(self):
    #     while self.unvisited:
    #         curr = self.unvisited.pop()
    #         print('curr:', curr)
    #         # Select next valid option
    #         validated_selection = False
    #         while not validated_selection:
    #             selection = self.make_selection(curr)
    #             print('selection:', selection)
    #             validated_selection = self.validate_selection(selection, curr)
    #         # Record valid selection, continue
    #         self.filled_map[curr] = selection
    #         # Push to stack
    #         self.visited.append(curr)
    #         print(self.filled_map)
    #         print(self.visited)
    #         print()

    # def make_selection(self, curr):
    #     row = curr[0]
    #     col = curr[1]
    #     # If no options here, backtrack until options:
    #     while not self.options[row][col]:
    #         # Reset options
    #         self.options[row][col] = self.tiles
    #         # Return curr to unvisited list
    #         self.unvisited.add(curr)
    #         # If in filled dict, remove
    #         if curr in self.filled_map:
    #             self.filled_map.pop(curr)
    #         # If no previous visited (?)
    #         if not self.visited:
    #             return
    #         # Pop last visited from stack
    #         curr = self.visited.pop(-1)
    #         print('curr:', curr)
    #         row = curr[0]
    #         col = curr[1]
    #     # Select an available option
    #     return self.options[row][col].pop()

    # def validate_selection(self, selection, curr):
    #     # Find adjacent indexes to check
    #     row = curr[0]
    #     col = curr[1]
    #     row_adjs = [(row, i) for i in range(3) if i != col]
    #     col_adjs = [(j, col) for j in range(3) if j != row]
    #     adjs = row_adjs + col_adjs
    #     # Check any filled adjs to see if selection is invalid
    #     for adj in adjs:
    #         if adj in self.filled_map:
    #             if self.filled_map[adj] == selection:
    #                 return False
    #     return True


if __name__ == '__main__':
    game = Board()
    # print(game.options)
    print(game.fill_board())
    print(game.board)