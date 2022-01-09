from QuoridorGame import QuoridorGame
from HumanPlayer import HumanPlayer
#from Players.RandomPlayer import RandomPlayer
#from Players.MinimaxPlayer import MinimaxPlayer
#from Players.DrDongPlayer import DrDongPlayer

from Arena import Arena

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = QuoridorGame(n_players = 2, visualize = True)

# all players
#rp = RandomPlayer(g).play
hp = HumanPlayer(g).play
#mm4p = MinimaxPlayer(g, depth=4, randomized=True).play
#mm5p = MinimaxPlayer(g, depth=5, randomized=False).play
#ytp = DrDongPlayer(g).play

players = [hp, hp, hp, hp]
arena = Arena(players, g)


result, times = arena.playGame(verbose=True)
if result == 1:
    print("P1 won")
else:
    print("P2 won")

"""
p1wins, p2wins, draws, average_times = arena.playGames(num=10, verbose=True)

print('P1 won', p1wins, 'times')
print('P2 won', p2wins, 'times')
print('Draw', draws, 'times')
print('Average times', average_times)
"""
