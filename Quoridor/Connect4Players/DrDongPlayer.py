import numpy as np
import random


class Minimax():
    """
    Performs minimax tree search on a game
    Arguments
        game: connect4 game instance
        heuristic: heuristic function for how good the board is for the player
            with pieces "1" given player "1" is about to move. If the board looks
            good for player "1" the heuristic should return a value near 1 and if
            it looks good for the other player "-1" the heuristic should return a
            value near -1.
        randomized: when multiple actions are tied for the same value, randomized
            determines if the move is picked randomly or just the first move in
            the list
    """

    def __init__(self, game, heuristic=lambda x: 0, randomized=False):
        self.game = game
        self.heuristic = heuristic
        self.randomized = randomized
        self.memory = {}

    # A function to convert a numpy board into a compact representation
    # (you cannot use a normal numpy array as a dictionary key)
    def _to_bytes(self, board):
        return board.astype('int8').tobytes()

    def compute_minimax(self, canonicalBoard, remaining_depth):
        """
        Recursively computes the minimax value of a board position with given depth

        Arguments
            canonicalBoard: the board state (as given by game.getCanonicalForm)
            remaining_depth: search depth remaining (if this is 2 then we will search
                down two more layers on the tree)
        Returns
            value: the negation of the maximal guaranteed value as given by minimax
                (between -1 and 1)
            action: action to take to achieve that value (-1 if no action by game end
                or evaluated by heuristic)
        """

        self.short_term_memory = {}

        end_value = self.game.getGameEnded(canonicalBoard, 1)
        if end_value != 0:  # Game ended
            # terminal node
            return -end_value, -1

        if remaining_depth <= 0:
            v = self.heuristic(canonicalBoard)
            return -min(max(v, -1), 1), -1   # Constrains invalid heuristic range

        # Mask of valid moves
        valids = self.game.getValidMoves(canonicalBoard, 1)

        # Best value and action so far
        cur_best = -float('inf')
        best_actions = [-1]
        # Iterate over valid moves and recursively minimax
        for a in range(self.game.getActionSize()):
            if valids[a]:
                next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
                # Swaps board representation to next player
                next_s = self.game.getCanonicalForm(next_s, next_player)
                v = self._compute_minimax_recursive(next_s, remaining_depth - 1, a)
                if v > cur_best:
                    cur_best = v
                    best_actions = [a]
                elif v == cur_best:
                    best_actions.append(a)
        if not self.randomized:
            return -cur_best, best_actions[0]
        return -cur_best, random.choice(best_actions)

    def _compute_minimax_recursive(self, canonicalBoard, remaining_depth, previous_action):
        # recursive helper which requires the previous action to reduce computation

        end_value = self.game.getGameEndedIncremental(canonicalBoard, 1, previous_action)
        if end_value != 0:  # Game ended
            # terminal node
            return -end_value

        # Evaluate heuristic at leaf node
        if remaining_depth <= 0:
            compressed_board = self._to_bytes(canonicalBoard)
            if compressed_board in self.memory:
                return self.memory[compressed_board]
            v = self.heuristic(canonicalBoard)
            result = -min(max(v, -1), 1)  # Constrains invalid heuristic range
            self.memory[compressed_board] = result
            return result  

        # Mask of valid moves
        valids = self.game.getValidMoves(canonicalBoard, 1)

        # Best value and action so far
        cur_best = -float('inf')
        # Iterate over valid moves and recursively minimax
        for a in range(self.game.getActionSize()):
            if valids[a]:
                next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
                next_s = self.game.getCanonicalForm(next_s, next_player)
                bit_version = self._to_bytes(next_s)
                if bit_version in self.short_term_memory:
                    v = self.short_term_memory[bit_version]
                else:
                    v = self._compute_minimax_recursive(next_s, remaining_depth - 1, a)
                    self.short_term_memory[bit_version] = v

                if v > cur_best:
                    cur_best = v
        return -cur_best




class DrDongPlayer():
    def __init__(self, game):
        self.game = game
        self.depth = 5
        self.randomized = True

    def check_array(self, array): # Array of size 4
        ones_in_a_row = 0
        has_opposites = False

        for element in array:
            if element == 1:
                if ones_in_a_row > 0:
                    ones_in_a_row += 1
                else:
                    if ones_in_a_row < 0:
                        has_opposites = True
                    ones_in_a_row = 1

            if element == -1:
                if ones_in_a_row < 0:
                    ones_in_a_row -= 1
                else:
                    if ones_in_a_row > 0:
                        has_opposites = True
                    ones_in_a_row = -1

        if not has_opposites:
            ones_in_a_row *= 10

        if abs(ones_in_a_row) > 1:
            return ones_in_a_row
        else:
            return 0

    def board_heuristic(self, board):
        """
        Given a board state evaluates how well player "1" is doing.
        Arguments
            board: a numpy array (basically a list of lists) with a
                representation of the connect 4 board. For example
                [[ 0  0  0  0  0  0  0]
                 [ 0  0  0  0  0  0  0]
                 [ 0  0  0 -1  0  0  1]
                 [ 0  0  0  1  0  0 -1]
                 [ 0  0  0  1 -1  0 -1]
                 [-1  1 -1  1 -1  1  1]]
        Returns
            value: a number between 1 and -1 representing the value of the game
                for player "1". Should be close to 1 if player "1" is winning.
        """

        board[0][0] = 1

        height = len(board)
        width = len(board[0])
        array_size = 4

        total = 0

        # Horizontal search
        for i_row in range(height):
            for i_column in range(width - array_size + 1):
                array = [board[i_row][i_column], board[i_row][i_column + 1], board[i_row][i_column + 2], board[i_row][i_column + 3]]
                total += self.check_array(array)

        # Vertical search
        for i_column in range(width):
            for i_row in range(height - array_size + 1):
                array = [board[i_row][i_column], board[i_row + 1][i_column], board[i_row + 2][i_column], board[i_row + 3][i_column]]
                total += self.check_array(array)
        
        # Diagonal search
        for i_column in range(width - array_size + 1):
            for i_row in range(height - array_size + 1):
                array = [board[i_row][i_column], board[i_row + 1][i_column + 1], board[i_row + 2][i_column + 2], board[i_row + 3][i_column + 3]]
                total += self.check_array(array)

        # Other diagonal
        for i_column in range(width - array_size + 1):
            for i_row in range(3, height):
                array = [board[i_row][i_column], board[i_row - 1][i_column + 1], board[i_row - 2][i_column + 2], board[i_row - 3][i_column + 3]]
                total += self.check_array(array)

        return total / 100 # Divide by 100 to keep the total less than 1

    def play(self, board):
        mini = Minimax(self.game, self.board_heuristic, self.randomized)
        v, a = mini.compute_minimax(self.game.getCanonicalForm(board, 1), self.depth)
        return a