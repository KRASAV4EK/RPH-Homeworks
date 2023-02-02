from random import randint
import time

class MyPlayer:
    '''Bot which plays randomly!'''

    def __init__(self, my_color, opponent_color):
        self.name = 'timofili'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.wrong_dir = (-1, -1)
        self.board_size = 0

    def move(self, board):
        possible_moves = []
        self.board_size = len(board)
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == self.my_color:
                    # Getting the array of coordinates, where you can put
                    # your rock
                    array = self.directions(row, col, board)

                    # Checking if the coordinate isn't already in the array of
                    # possible moves and adding to the array
                    same_coord = 0
                    for counter in range(len(array)):
                        for coordinate in range(len(possible_moves)):
                            if array[counter] == possible_moves[coordinate]:
                                same_coord = 1
                        if same_coord == 1:
                            break
                        possible_moves.append(array[counter])

        # Checking if array of possible moves is empty
        if len(possible_moves) == 0:
            return None

        my_move = randint(0, len(possible_moves) - 1)

        # # Some tests :-)
        # print(possible_moves)
        # print("------------")
        # print(possible_moves[my_move])
        # print("------------")

        return possible_moves[my_move]

    def directions(self, row, col, board):
        possible_moves = []
        # Creating the array of directions, which we will you for finding
        # right move
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in dirs:
            # Getting an array of coordinates
            array = self.confirm_direction(row, col, dir, board)

            # Checking if coordinate is correct and adding to the array of
            # possible moves
            if array != (self.wrong_dir):
                possible_moves.append((array[0], array[1]))
        return possible_moves

    def range_check(self, row, col):
        # Checking if row and column are in right range
        return (row >= 0) and (col >= 0) and \
               (row < self.board_size) and (col < self.board_size)

    def confirm_direction(self, row, col, dir, board):
        # Getting the direction coordinate
        row += dir[0]
        col += dir[1]
        if self.range_check(row, col):
            if board[row][col] == self.opponent_color:
                # Going further the direction until find mine or opponent's rock
                while self.range_check(row, col):
                    row += dir[0]
                    col += dir[1]
                    if self.range_check(row, col):
                        if board[row][col] == -1:
                            return row, col
                        if board[row][col] == self.my_color:
                            return self.wrong_dir
        return self.wrong_dir

# Some tests :-)
if __name__ == "__main__":
    start_time = time.time()
    sample_board = [
        #   0   1   2   3   4   5   6   7
        # [-1, -1, -1, -1, -1, -1, -1,  1], # 0
        # [-1, -1, -1,  1, -1, -1,  0, -1], # 1
        # [-1, -1, -1, -1,  1,  0,  1,  1], # 2
        # [-1, -1, -1,  0,  0,  1, -1, -1], # 3
        # [-1, -1,  0,  0,  0,  1, -1, -1], # 4
        # [-1, -1,  0,  0,  0, -1, -1, -1], # 5
        # [-1, -1,  0, -1,  0, -1, -1, -1], # 6
        # [-1, -1, -1, -1, -1, -1, -1, -1], # 7

        # 0   1   2   3   4   5   6   7    13
        [ 1,  0,  0, -1,  0,  1, -1,  0],  # 0
        [ 0, -1, -1,  1, -1, -1,  0, -1],  # 1
        [ 0, -1, -1, -1,  1,  0,  1,  1],  # 2
        [ 0, -1, -1,  0,  0,  1, -1, -1],  # 3
        [ 0, -1,  0,  0,  0,  1, -1,  0],  # 4
        [ 0, -1,  0,  0,  0, -1, -1,  0],  # 5
        [ 0, -1,  0, -1,  0, -1, -1,  0],  # 6
        [-1,  0,  1, -1, -1, -1, -1,  1],  # 7

        #   0   1   2   3   4   5   6   7
        # [-1, -1, -1, -1, -1, -1, -1, -1], # 0
        # [-1, -1, -1, -1, -1, -1, -1, -1], # 1
        # [-1, -1, -1, -1, -1, -1, -1, -1], # 2
        # [-1, -1, -1,  0,  1, -1, -1, -1], # 3
        # [-1, -1, -1,  1,  0, -1, -1, -1], # 4
        # [-1, -1, -1, -1, -1, -1, -1, -1], # 5
        # [-1, -1, -1, -1, -1, -1, -1, -1], # 6
        # [-1, -1, -1, -1, -1, -1, -1, -1], # 7

    ]
    player = MyPlayer(1, 0)
    for row in sample_board:
        print(row)

    print("------------")

    player.move(sample_board)

    print("--- %s seconds ---" % (time.time() - start_time))
