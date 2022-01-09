#sys.path.append('..')
from QuoridorBoard import QuoridorBoard
from QuoridorVisualizer import QuoridorVisualizer
from copy import deepcopy

class QuoridorGame:
    """
    Quoridor Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, n_players = 2, visualize = False):
        self._base_board = QuoridorBoard(n_players)
        self.visualize = visualize
        if visualize:
            self.visualizer = QuoridorVisualizer()

    def getInitBoard(self):
        return self._base_board

    def getActionSize(self):
        return self._base_board.width

    def getNextState(self, board, player, action):
        """Returns a copy of the board with updated move, original board is unmodified."""
        b = deepcopy(board)
        action.execute(b)
        next_player = b.next_player()
        return b, next_player

    def getValidMoves(self, board, player):
        "Any zero value in top row in a valid move"
        return self._base_board.get_valid_moves()

    def getGameEnded(self, board):
        return self._base_board.get_win_state()

    def getCanonicalForm(self, board, player):
        # Flip player from 1 to -1
        return board #* player

    def display(self, board):
        if self.visualize:
            self.visualizer.draw_board(board)

