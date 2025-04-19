import multiprocessing
from game import Game
from draw import *
from player import Player

def runDialog(queue):
    """
    Funktion für den Dialog, der die Spielerinformationen abfragt.
    """
    result = startDialog()
    queue.put(result)  # Ergebnisse in die Queue setzen

if __name__ == "__main__":
    # Erstelle eine Queue für die Kommunikation zwischen Prozessen
    queue = multiprocessing.Queue()

    # Starte den Dialog in einem neuen Prozess
    p = multiprocessing.Process(target=runDialog, args=(queue,))
    p.start()
    gameSettings = queue.get()  # Warte auf die Ergebnisse des Dialogs
    p.join()

    if gameSettings == []:
        exit()

    game = Game()
    playerCount = len(gameSettings)

    for i in range (playerCount):
        game.addPlayer(gameSettings[i][0], gameSettings[i][1])  # Spieler mit Namen und Figur hinzufügen

    #for i in range(2): game.addPlayer(chr(65 + i), "")    # zu Test zwecken, muss später durch UI ausgelöst werden
    
    print(game.getPlayers())

    # Stellt initDraw game zur Verfügung und führt initDraw aus
    initDraw(game)
    
    game.startGame()  # Spiel muss später durch UI Element gestartet werden, nachdem mindestens zwei Spieler hinzufügt wurden 
