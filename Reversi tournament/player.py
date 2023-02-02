class MyPlayer:
    '''Bot choose best move, based on best enemy move, using score map'''

    def __init__(self, my_color, opponent_color):
        self.name = 'timofili'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.wrong_dir = (-1, -1)
        self.board_size = 0

    def move(self, board):
        # Filling the array with my possible moves
        my_possible_moves = self.get_valid_moves(board, self.my_color,
                                                  self.opponent_color)

        # Filling the array with values
        # [My coordinates, earned rocks, lost rocks, table score]
        # Earned rocks - amount of rocks, that I'll receive after my move
        # Lost rocks - amount of rocks, that I'll lose after enemy move
        # Table score - position price
        array = self.prices_list(board, my_possible_moves)

        # Returning nothing if aren't valid moves
        if len(array) == 0:
            return None

        # Returning my best move
        return self.best_move(array)

    def best_move(self, array):
        best_plus = -100
        best_coord = 0
        best_score = 0
        for coord in array:
            addition = coord[1] + coord[2] + coord[3]
            if addition > best_plus:
                best_plus = addition
                best_coord = coord[0]
                best_score = coord[3]

            if addition == best_plus:
                if coord[3] > best_score:
                    best_coord = coord[0]

        return best_coord

    def rocks_counter(self, board, my_possible_move, enemy_color):
        # Going through all directions and calculating amount of earned rocks
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)]
        counter = 1
        for dir in dirs:
            row = my_possible_move[0] + dir[0]
            col = my_possible_move[1] + dir[1]
            if self.range_check(row, col):
                if board[row][col] == enemy_color:
                    counter += 1
                    while self.range_check(row, col):
                        row += dir[0]
                        col += dir[1]
                        if self.range_check(row, col):
                            if board[row][col] == enemy_color:
                                counter += 1
                            else:
                                continue
        return counter

    def prices_list(self, board, my_possible_moves):
        array = []
        for my_possible_move in my_possible_moves:
            # Finding earned rocks, lost rocks after my move, table score of
            # rocks coordinates
            earned_rocks = self.rocks_counter(board, my_possible_move,
                                              self.opponent_color)
            lost_rocks = self.best_opp_earn(board, my_possible_move)
            score = self.table_score(my_possible_move)

            # Checking if enemy can't do anything
            if lost_rocks is None:
                lost_rocks = 0

            array.append((my_possible_move, earned_rocks, lost_rocks, score))

        return array

    def best_opp_earn(self, board, my_possible_move):
        # Calculating, how much rocks I'll lose after my move, if enemy plays
        # the best move, that he can
        r = my_possible_move[0]
        c = my_possible_move[1]

        # Saving previous amount of square
        buffer = board[r][c]
        # Putting my rock at square with coordinates of my move
        board[r][c] = self.my_color

        max_profit = 0  # Creating the variable of maximum enemy profit

        # Searching possible enemy moves
        op_valid_moves = self.get_valid_moves(board, self.opponent_color,
                                              self.my_color)

        # Controlling if array isn't empty
        if op_valid_moves is None:
            return None

        # Searching the best enemy move and calculating his max profit
        for op_valid_move in op_valid_moves:
            enemy_profit = self.rocks_counter(board, op_valid_move,
                                              self.my_color)
            table_score = self.table_score(op_valid_move)
            enemy_profit += table_score

            if enemy_profit > max_profit:
                max_profit = enemy_profit

        # Returning previous amount of square
        board[r][c] = buffer

        return max_profit

    def table_score(self, my_possible_move):
        r = my_possible_move[0]
        c = my_possible_move[1]

        board = [
                [100, -20,  20,   5,   5,  20, -20, 100],
                [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
                [ 20,  -5,  15,   3,   3,  15,  -5,  20],
                [  5,  -5,   3,   3,   3,   3,  -5,   5],
                [  5,  -5,   3,   3,   3,   3,  -5,   5],
                [ 20,  -5,  15,   3,   3,  15,  -5,  20],
                [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
                [100, -20,  20,   5,   5,  20, -20, 100]
                 ]
        return board[r][c]

    def get_valid_moves(self, board, my_color, op_color):
        possible_moves = []
        self.board_size = len(board)
        for row in range(self.board_size):
            for col in range(self.board_size):
                if board[row][col] == my_color:
                    # Getting the array of coordinates, where I can put rock
                    array = self.directions(row, col, board, my_color, op_color)

                    # Checking if the coordinates aren't already in the array of
                    # possible moves and adding to that array
                    same_coord = 0
                    for counter in range(len(array)):
                        for coordinate in range(len(possible_moves)):
                            if array[counter] == possible_moves[coordinate]:
                                same_coord = 1
                        if same_coord == 1:
                            break
                        possible_moves.append(array[counter])

        # Checking if array of possible moves is empty and returning
        if len(possible_moves) == 0:
            return None

        return possible_moves


    def directions(self, row, col, board, my_color, op_color):
        possible_moves = []
        # Creating the array of directions
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in dirs:
            # Getting an array of coordinates
            array = self.confirm_direction(row, col, dir, board, my_color,
                                           op_color)

            # Checking if coordinates are correct and adding to the array of
            # possible moves
            if array != (self.wrong_dir):
                possible_moves.append((array[0], array[1]))
        return possible_moves

    def range_check(self, row, col):
        # Checking if row and column are in right range
        return (row >= 0) and (col >= 0) and \
               (row < self.board_size) and (col < self.board_size)

    def confirm_direction(self, row, col, dir, board, my_color, op_color):
        # Getting the direction coordinate
        row += dir[0]
        col += dir[1]
        # Going further with that direction, until find enemy rock
        if self.range_check(row, col):
            if board[row][col] == op_color:
                # Going further, until find own rock or free space
                while self.range_check(row, col):
                    row += dir[0]
                    col += dir[1]
                    if self.range_check(row, col):
                        # Returning coordinates, which can use in game
                        if board[row][col] == -1:
                            return row, col
                        # Returning coordinates, which can't use
                        if board[row][col] == my_color:
                            return self.wrong_dir
        # Returning coordinates, which can't use
        return self.wrong_dir


# Some tests :-)
if __name__ == "__main__":
    sample_board = [
        # # 0   1   2   3   4   5   6   7
        # [-1, -1, -1, -1, -1, -1, -1,  1], # 0
        # [-1, -1, -1,  1, -1, -1,  0, -1], # 1
        # [-1, -1, -1, -1,  1,  0,  1,  1], # 2
        # [-1, -1, -1,  0,  0,  1, -1, -1], # 3
        # [-1, -1,  0,  0,  0,  1, -1, -1], # 4
        # [-1, -1,  0,  0,  0, -1, -1, -1], # 5
        # [-1, -1,  0, -1,  0, -1, -1, -1], # 6
        # [-1, -1, -1, -1, -1, -1, -1, -1], # 7

        # # 0   1   2   3   4   5   6   7    13
        # [ 1,  0,  0, -1,  0,  1, -1,  0],  # 0
        # [ 0, -1, -1,  1, -1, -1,  0, -1],  # 1
        # [ 0, -1, -1, -1,  1,  0,  1,  1],  # 2
        # [ 0, -1, -1,  0,  0,  1, -1, -1],  # 3
        # [ 0, -1,  0,  0,  0,  1, -1,  0],  # 4
        # [ 0, -1,  0,  0,  0, -1, -1,  0],  # 5
        # [ 0, -1,  0, -1,  0, -1, -1,  0],  # 6
        # [-1,  0,  1, -1, -1, -1, -1,  1],  # 7

        # 0   1   2   3   4   5   6   7
        [-1, -1, -1, -1, -1, -1, -1, -1],  # 0
        [-1, -1, -1, -1, -1, -1, -1, -1],  # 1
        [-1, -1,  1,  0,  0,  0, -1, -1],  # 2
        [-1, -1,  1,  0,  0,  0, -1, -1],  # 3
        [-1, -1,  1,  0,  0,  0, -1, -1],  # 4
        [-1, -1,  1,  1,  0,  0, -1, -1],  # 5
        [-1, -1, -1, -1, -1, -1, -1, -1],  # 6
        [-1, -1, -1, -1, -1, -1, -1, -1],  # 7

    ]
    player = MyPlayer(1, 0)
    # for row in sample_board:
    #     print(row)
    #
    # print("------------")

    player.move(sample_board)

    # print("--- %s seconds ---" % (time.time() - start_time))
