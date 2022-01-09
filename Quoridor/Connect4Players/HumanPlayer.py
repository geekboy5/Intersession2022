import numpy as np


class HumanConnect4Player():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        valid_moves = self.game.getValidMoves(board, 1)
        print('\nMoves:', [i + 1 for (i, valid) in enumerate(valid_moves) if valid])

        while True:
            move = int(input()) - 1
            if 0 <= move < len(valid_moves) and valid_moves[move]:
                break
            else:
                print('Invalid move')
        return move