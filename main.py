from game import Game
from draw import *
from player import Player

game = Game()

gameSettings = startDialog()
print(gameSettings)  # Testausgabe

# Stellt initDraw game zur Verfügung und führt initDraw aus
initDraw(game)

for i in range(2): game.addPlayer(Player(game, chr(65 + i)))    # zu Test zwecken, muss später durch UI ausgelöst werden
game.startGame()                # Spiel muss später durch UI Element gestartet werden, nachdem mindestens zwei Spieler hinzufügt wurden 
