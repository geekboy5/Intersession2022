class YOURNAMESPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board, valid_moves):
        for move in valid_moves:
            if self.moves_in_right_direction(board, move.coord):
                return move

        return valid_moves[0]

    # Determines if a given move moves the pawn toward the right point
    def moves_in_right_direction(self, board, new_coord, player = -1):
        if player == -1:
            player = board.current_player

        if len(board.pawns) == 2:
            if player == 0:
                return new_coord.y > board.pawns[0].y
            if player == 1:
                return new_coord.y < board.pawns[1].y
        if len(self.pawns) == 4:
            if player == 0:
                return new_coord.y > board.pawns[0].y
            if player == 1:
                return new_coord.x > board.pawns[1].x
            if player == 2:
                return new_coord.y < board.pawns[2].y
            if player == 3:
                return new_coord.x < board.pawns[3].x
