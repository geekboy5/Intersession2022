from copy import deepcopy
import math
from re import search
import time
from Coordinate import Coordinate
import random
from QuoridorBoard import Fence
from QuoridorMove import QuoridorMove
from QuoridorMove import QuoridorMoveType

class TAlanSPlayer():
    def __init__(self, game):
        self.game = game
        self.prev_coord = None


    def play(self, board, valid_moves):
        # if opponent out of fences and player is closer, immediately rush goal line
        two_player_enemy_ind = (board.current_player + 1) % 2
        player_path = self.path_to_win(board, board.current_player)
        if len(board.pawns) == 2 and board.fences[two_player_enemy_ind] == 0 and len(self.path_to_win(board, board.current_player)) <= len(self.path_to_win(board, two_player_enemy_ind)):
            return QuoridorMove.move_pawn(player_path[0], board.current_player)

        # try to move forward if in starting position
        if self.prev_coord is None and board.pawns[board.current_player] == self.get_player_starting_coord(board, board.current_player):
            for move in board.get_legal_moves_for_player(board.current_player):
                # move directly towards goal
                if(self.moves_in_right_direction(board, move.coord, board.current_player)):
                    self.save_pos(board)
                    return move

        # try to place vertical fence next to player
        # if board.fences[board.current_player] > 8:
        if board.fences[board.current_player] > 8:
            next_enemy = (board.current_player + 1) % len(board.pawns)

            if board.fences[board.current_player] == 10:
                # try to immediately place vertical wall against opponent (intermediate opening)
                enemy_coord = board.pawns[next_enemy]
                is_horizontal_side_wall = self.get_player_starting_coord(board, next_enemy).y == 4

                if is_horizontal_side_wall:
                    fence_y = max(enemy_coord.y, 1)
                    fence_x = min(enemy_coord.x, 7)
                else:
                    fence_y = min(enemy_coord.y, 7)
                    fence_x = max(enemy_coord.x, 1)
                
                test_fence = Fence(Coordinate(fence_x, fence_y), is_horizontal_side_wall)
                if board.check_if_possible(test_fence):
                    self.save_pos(board)
                    return QuoridorMove.add_fence(test_fence, board.current_player)
            # 30% chance of trying to directly block enemy with fence
            if random.randint(0, 10) > 7:
                enemy_path = self.path_to_win(board, next_enemy)
                for fence_move in board.get_legal_fences(board.current_player):
                    potential_enemy_path = self.path_to_win(self.game.getNextState(board, board.current_player, fence_move)[0], next_enemy)
                    if len(potential_enemy_path) > len(enemy_path):
                        self.save_pos(board)
                        return fence_move
        depth = 2
        best_heuristic = None
        best_move = None

        # valid_moves = board.get_legal_moves_for_player(board.current_player)
        start_time = time.time()
        max_time = 5
        for i, move in enumerate(valid_moves):
            # try a move, evaluate
            if time.time() >= start_time + max_time and best_move is not None:
                break
            potential_board = self.game.getNextState(board, board.current_player, move)[0]
            minimaxValue = self.get_minimax_heuristic(potential_board)
            # minimaxValue = self.minimax_best_heuristic(potential_board, depth)
            if best_heuristic == None or minimaxValue > best_heuristic:
                best_heuristic = minimaxValue
                best_move = move
        if self.prev_coord is not None and best_move.type == QuoridorMoveType.MOVE and best_move.coord == self.prev_coord:
            # prevent player from repeating previous movement
            best_move = QuoridorMove.move_pawn(self.path_to_win(board, board.current_player)[0], board.current_player)
        self.save_pos(board)
        return best_move
    
    def save_pos(self, board):
        self.prev_coord = board.pawns[board.current_player]
    
    # returns best heuristic value from depth search
    def minimax_best_heuristic(self, board, depth):
        if depth == 0: return self.get_minimax_heuristic(board)
        valid_moves = board.get_valid_moves()
        best = None

        for move in valid_moves:
            cur_board = self.game.getNextState(board, board.current_player, move)[0]
            test_score = self.minimax_best_heuristic(cur_board, depth - 1)
            if best == None or test_score > self.get_minimax_heuristic(cur_board): 
                best = test_score
        return best
    
    # returns heuristic score based on board state
    def get_minimax_heuristic(self, board):
        # return player opp dist - player dist
        # future dist, predict future opponent moves, look for easily closable gaps along path?
        enemy_sum = 0
        player_ind = (board.current_player - 1) % len(board.pawns)
        # target player with opposite starting point
        enemy_ind = board.current_player if len(board.pawns) == 2 else (player_ind + 1) % len(board.pawns)
        enemy_sum = len(self.path_to_win(board, enemy_ind))
        player_path = self.path_to_win(board, player_ind)
        # duct tape to fix unknown error where path to win returns none
        if player_path is None:
            return enemy_sum
        return enemy_sum - len(player_path)
    
    # returns array of moves containing shortest path to win using A* pathfinding
    def path_to_win(self, board, player):
        win_condition = board.get_target(player)

        # list of nodes to store parent and coord
        start_node = Node(board.pawns[player], None)
        start_node.setHeuristics(board, player)
        nodes_to_search = [start_node]
        searched_nodes = []

        # while still moves to be searched
        while len(nodes_to_search) > 0:
            current_node = None #move with lowest heuristic (euclidean distance to goal + path distance to start)
            # pick lowest heuristic node through iteration
            for i, test_node in enumerate(nodes_to_search):
                if current_node == None or test_node.getHeuristic() < current_node.getHeuristic():
                    current_node = test_node

            # remove current node from unsearched nodes
            nodes_to_search.pop(nodes_to_search.index(current_node))
            searched_nodes.append(current_node)

            # check if target node reached
            if win_condition(current_node.coord):
                moves = []
                backtrack_node = current_node
                # backtrack through parent nodes to find path
                while backtrack_node.parent != None:
                    moves.append(backtrack_node.coord)
                    backtrack_node = backtrack_node.parent
                moves.reverse()
                if moves is None:
                    print(f'Path from {coord_to_string(board.pawns[player])} is {route_to_string(moves)}')
                return moves
            
            # get adjacent nodes
            new_legal_moves = board.get_legal_move_positions(current_node.coord)
            # iterate through adjacent coords
            for new_coord in new_legal_moves:
                new_child_node = Node(new_coord, current_node)
                new_child_node.setHeuristics(board, player)
                # skip if node has already been accounted for
                to_skip = False
                for searched_node in searched_nodes:
                    if new_child_node.coord.x == searched_node.coord.x and new_child_node.coord.y == searched_node.coord.y:
                        to_skip = True
                for to_search in nodes_to_search:
                    if new_child_node.coord.x == searched_node.coord.x and new_child_node.coord.y == searched_node.coord.y:
                        to_skip = True
                    # if to_search == new_child_node and to_search.path_distance > new_child_node.path_distance: to_skip = True
                if not to_skip: nodes_to_search.append(new_child_node)
        print("didn't find path, returning rand move")
        return [QuoridorMove.move_pawn(random.choice(board.get_legal_move_positions(board.pawns[player])), player)]

    # Determines if a given move moves the pawn toward the right point
    def moves_in_right_direction(self, board, new_coord, player = -1):
        if player == -1:
            player = board.current_player

        if len(board.pawns) == 2:
            if player == 0:
                return new_coord.y > board.pawns[0].y
            if player == 1:
                return new_coord.y < board.pawns[1].y
        if len(board.pawns) == 4:
            if player == 0:
                return new_coord.y > board.pawns[0].y
            if player == 1:
                return new_coord.x > board.pawns[1].x
            if player == 2:
                return new_coord.y < board.pawns[2].y
            if player == 3:
                return new_coord.x < board.pawns[3].x

    def get_player_starting_coord(self, board, player):
        if player == 0:
            return Coordinate(4, 0)
        if player == 1:
            if len(board.pawns) == 2:
                return Coordinate(4, 8)
            elif len(board.pawns) == 4:
                return Coordinate(0, 4)
        if player == 2:
            return Coordinate(4, 8)
        if player == 3:
            return Coordinate(8, 4)
    
# utility function for printing coordinates
def coord_to_string(coord):
    return "(" + str(coord.x) + ", " + str(coord.y) + ")"

# utility function for printing route of coords
def route_to_string(route):
    str = ""
    for coord in route:
        coord_str = coord_to_string(coord)
        str += coord_str + ", "
    return str

class Node:
    def __init__(self, coord, parent = None):
        self.coord = coord
        self.parent = parent
    
    def __str__(self):
        return coord_to_string(self.coord)

    def __repr__(self):
        return coord_to_string(self.coord)
    
    def __eq__(self, other):
        if other == None: return False
        return self.coord.x == other.coord.x and self.coord.y == other.coord.y
    
    def setHeuristics(self, board, player):
        parent = self.parent
        dist = 0
        while parent != None:
            dist += 1
            parent = parent.parent
        self.path_distance = dist

        y_max = None
        target_value = None
        if player == 0:
            y_max = True
            target_value = 8
        if player == 1:
            if len(board.pawns) == 2:
                y_max = True
                target_value = 0
            elif len(board.pawns) == 4:
                y_max = False
                target_value = 8
        if player == 2:
            y_max = True
            target_value = 0
        if player == 3:
            y_max = False
            target_value = 0

        # only take into account direct line between player and goal line
        if y_max:
            self.euclidean_distance = abs(target_value - self.coord.y)
        else:
            self.euclidean_distance = abs(target_value - self.coord.x)

    def getHeuristic(self):
        return self.path_distance + self.euclidean_distance
