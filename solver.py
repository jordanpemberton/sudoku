import math
import os
import sys


def solve(size, board, row, col):
    # If end of board reached
    if row == size - 1 and col == size:
        return True

    # If end of row reached
    if col == size:
        row += 1
        col = 0

    # If cell already filled
    if board[row][col] is not None:
        return solve(size, board, row, col+1)

    # guess
    for x in range(1, size+1):
        if check_if_valid_entry(size, board, row, col, x):
            board[row][col] = x

            if solve(size, board, row, col+1):
                return True

        board[row][col] = None

    return False


def check_if_valid_entry(size, board, row, col, entry):
    # Check column
    for c in range(size):
        if board[row][c] == entry:
            if c != col:
                return False

    # Check row
    for r in range(size):
        if board[r][col] == entry:
            if r != row:
                return False

    # Check zone
    zone_size = int(math.sqrt(size))
    start_row = row - row % zone_size
    start_col = col - col % zone_size

    for r in range(start_row, start_row + zone_size):
        for c in range(start_col, start_col + zone_size):
            if board[r][c] == entry:
                if (r, c) != (row, col):
                    return False

    return True



def test( testid, size, clues, solu ):
    # clues = "6...5.....73..8.2.854.27...2.17..53.4...69..7.8....9...273.1.84.6.54...93.......1"
    # solu  = "612453798973618425854927163291784536435269817786135942527391684168542379349876251"
    # size = 9

    print(f"\ntest\t{testid}\t")

    board = [[None for _ in range(size)] for _ in range(size) ]

    for i in range( size * size ):
        if clues[i] != '.':
            board[i//size][i%size] = int(clues[i])

    print( solve(size, board, 0, 0) )

    print( f"clues:\t{clues}" )
    print( f"result:\t{board}" )
    print( f"expected:\t{solu}" )

    correct = True
    for i in range( size * size ):
        exp = 0
        if solu[i] != '.':
            exp = int( solu[i] )

        if exp != board[i//size][i%size]:
            print( f"failed at index\t{i}\texp: {exp}\t res: {board[i//size][i%size]}" )
            correct = False

    if correct:
        print( f"test\t{testid}\tPASSED" )
    else:
        print( f"teste\t{testid}\tFAILED" )


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("USAGE: python3 solve.py <testsfile>")

    else:
        filename = sys.argv[1]

        infile = open(filename)

        count = 1

        for line in infile.readlines():
            clues, num_solu, solu = line.split(":")
            size = int(math.sqrt( len(clues) ))

            test(count, size, clues, solu)

            count += 1

        infile.close()
