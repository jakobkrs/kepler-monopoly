from player import Player
from square import Square
from property import Property
import os


class Game():
    def __init__(self):
        """
        Initialisation of the Game class. Set start values of class instance.
        """
        self.__currentPlayerId = 0
        self.__currentPlayer = None
        self.__playerCount = 0
        self.__playerOrder = []             # Füge die Reihenfolgebestimmung hinzu !later
        self.__players = []                 # Liste aller Objekten der Klasse Spieler
        self.__gameBoard = []               # Liste aller Objekten der Klasse Square (bzw. Property als Unterklasse von Square)
        self.__properties  =[]                # Liste aller Objekten der Klasse Property
        self.__communityCards = []
        self.__eventCards = []

        csvDirPath = os.path.dirname(os.path.abspath(__file__)) + "/CSV-files/"         # funktioniert hoffentlich auf windows, mac und linux
        
        squaresTable = self.__loadCSV(csvDirPath + "squares.csv")
        propertiesTable = self.__loadCSV(csvDirPath + "properties.csv")
        for square in squaresTable:
            print(square, square[2], (square[2] in ['property', 'trainStation', 'supplyPlant']))
            if square[2] in ['property', 'trainStation', 'supplyPlant']:
                for property in propertiesTable:
                    if property[0] == square[0]:     # Position ist gleich -> property und square gehören zusammen
                        propertyObject = Property(square[0],square[1],square[2],property[1],property[2],property[3])    # 
                        self.__gameBoard.append(propertyObject)
                        self.__properties.append(propertyObject)
            else:
                self.__gameBoard.append(Square(square[0],square[1],square[2]))
        
        


    def addPlayer(self, player: Player):
        """
        Fügt einen Spieler zur Liste aller Spieler hinzu.
        """
        self.__players.append(player)
        self.__playerCount += 1
        self.__playerOrder.append(self.__playerCount - 1)

    def shufflePlayerOrder(self):  # WIP !later
        pass

    def __loadCSV(self,filepath: str) -> list[list]:
        """
        Methode, um Square aus der CSV-Datei einzulesen
        """
        table = []
        # Datei öffnen zum Lesen
        file = open(filepath, "r")
        # Variable, um erste Zeile ignorieren zu können
        start = True
        for line in file:
            if start:                                                           # erste Zeile ignorieren
                start = not (start)
            else:
                a = line.rstrip().split(";")
                # Zeile in Feld auftrennen
                table.append(a)

        file.close
        return table

    def trade(self, player1: Player, player2: Player):
        pass

    def nextPlayersTurn(self):
        """
        Der nächste Spieler kommt zum Zug.
        """
        self.__currentPlayerId = (
            self.__currentPlayerId + 1) % self.__playerCount
        self.__currentPlayer = self.__players[self.__playerOrder[self.__currentPlayerId]]

        self.__currentPlayer.startTurn()



    



    def getGameBoard(self):
        return self.__gameBoard

    def getProperties(self):
        return self.__properties

    


game = Game()
