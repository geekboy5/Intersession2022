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
            v = self.heuristic(canonicalBoard)
            return -min(max(v, -1), 1)  # Constrains invalid heuristic range

        # Mask of valid moves
        valids = self.game.getValidMoves(canonicalBoard, 1)

        # Best value and action so far
        cur_best = -float('inf')
        # Iterate over valid moves and recursively minimax
        for a in range(self.game.getActionSize()):
            if valids[a]:
                next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
                next_s = self.game.getCanonicalForm(next_s, next_player)
                v = self._compute_minimax_recursive(next_s, remaining_depth - 1, a)
                if v > cur_best:
                    cur_best = v
        return -cur_best


class MinimaxPlayer():
    def __init__(self, game, depth=6, randomized=False):
        self.game = game
        self.depth = depth
        self.randomized = randomized

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
        return 0

    def play(self, board):
        mini = Minimax(self.game, self.board_heuristic, self.randomized)
        v, a = mini.compute_minimax(self.game.getCanonicalForm(board, 1), self.depth)
        return a