from player import *
from square import *

class Game():
    def __init__(self):
        """
        Initialisation of the Game class. Set start values of class instance.
        """
        self.__currentPlayerId = 0
        self.__currentPlayer = None
        self.__playerCount = 0
        self.__playerOrder = []             # Füge die Reihenfolgebestimmung hinzu !later
        self.__players = []                 # Liste von Objekten der Klasse Spieler
        self.__gameBoard = []
        self.__communityCards = []
        self.__eventCards = []

        

    

    def addPlayer(self, player: Player):
        """
        Fügt einen Spieler zur Liste aller Spieler hinzu.
        """
        self.__players.append(player)
        self.__playerCount += 1
        self.__playerOrder.append(self.__playerCount - 1)

    def shufflePlayerOrder(self): #WIP !later
        pass

    def __loadCSV(filepath):    # wird später von anderem Teammitglied erstellt !later
        """
        Methode, um Square aus der CSV-Datei einzulesen
        """
        table =[]
        file = open(filepath,"r")                              # Datei öffnen zum Lesen
        start = True                                                            # Variable, um erste Zeile ignorieren zu können
        for line in file:
            if start:                                                           # erste Zeile ignorieren
                start = not(start)
            else:
                a = line.rstrip().split(";") 
                table.append(a)                                  # Zeile in Feld auftrennen

        file.close
        return table
        # return [[]]

    def trade(self,player1: Player,player2: Player):
        pass

    def nextPlayersTurn(self):
        """
        Der nächste Spieler kommt zum Zug.
        """
        self.__currentPlayerId = (self.__currentPlayerId + 1) % self.__playerCount
        self.__currentPlayer = self.__players[self.__playerOrder[self.__currentPlayerId]]

        self.__currentPlayer.startTurn()



game = Game()

