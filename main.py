import multiprocessing
import os
from game import Game
from draw import *

def runDialog(queue):
    """
    Funktion für den Dialog, der die Spielerinformationen abfragt.
    """
    #result = startDialog()
    result = [('Spieler 1', 'Hund'), ('Spieler 2', 'Auto'), ('Spieler 3', 'Schiff')]
    queue.put(result)  # Ergebnisse in die Queue setzen

if __name__ == "__main__":
    # Erstelle eine Queue für die Kommunikation zwischen Prozessen
    queue = multiprocessing.Queue()

    # Starte den Dialog in einem neuen Prozess
    p = multiprocessing.Process(target=runDialog, args=(queue,))
    p.daemon = True  # Setze den Prozess als Daemon-Prozess
    p.start()
    try:
        gameSettings = queue.get(timeout=60)
    except Exception:
        p.terminate()
        os._exit(0)
    p.join()
 
    if gameSettings == []:
        os._exit(0)

    game = Game()
    playerCount = len(gameSettings)

    for i in range (playerCount):
        game.addPlayer(gameSettings[i][0], gameSettings[i][1])  # Spieler mit Namen und Figur hinzufügen

    for property in game.getProperties():
        property.setOwner(game.getPlayers()[0])
    # Stellt initDraw game zur Verfügung und führt initDraw aus
    initDraw(game)