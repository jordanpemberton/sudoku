class Board:
    def __init__(self):
        self.tiles = set(['A', 'B', 'C', 'D'])
        self.size = 4
        self.region_size = 2
        self.board = [[None for i in range(self.size)] for j in range(self.size)]

    def fill_board(self, row=0, col=0):
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


    def move_is_safe(self, row, col, tile):
        for i in range(self.size):
            if self.board[row][i] == tile:
                return False
        for i in range(self.size):
            if self.board[i][col] == tile:
                return False
        # For checking regions:
        start_row = row - row % self.region_size
        start_col = col - col % self.region_size
        for i in range(self.region_size):
            for j in range(self.region_size):
                if self.board[i + start_row][j + start_col] == tile:
                    return False
        return True


if __name__ == '__main__':
    game = Board()
    # print(game.options)
    print(game.fill_board())
    print(game.board)