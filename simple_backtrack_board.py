import string


class Board:
    def __init__(self):
        self.size = 9
        self.zone_size = 3
        self.tiles = set(string.ascii_uppercase[:self.size])
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
        start_row = row - row % self.zone_size
        start_col = col - col % self.zone_size
        for i in range(self.zone_size):
            for j in range(self.zone_size):
                if self.board[i + start_row][j + start_col] == tile:
                    return False
        return True

    def print_board(self):
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
                if self.board[i][j] is not None:
                    out += self.board[i][j]
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


if __name__ == '__main__':
    game = Board()
    # print(game.options)
    game.fill_board()
    game.print_board()