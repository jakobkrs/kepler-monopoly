from game import Game
from draw import *

game = Game()

# Stellt initDraw game zur Verfügung und führt initDraw aus
initDraw(game)


print([game.getGameBoard()[i].getName() for i in range(len(game.getGameBoard()))])