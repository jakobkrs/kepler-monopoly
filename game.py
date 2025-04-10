from player import Player
from square import Square
from property import Property
import random
import os


class Game():
    def __init__(self):
        """
        Initialisation of the Game class. Set start values of class instance.
        """
        self.__currentPlayerId = 0
        self.__currentPlayer = None
        self.__playerCount = 0
        self.__playerOrder = []             # Liste an ganzen Zahlen, die die postion der Spieler-Objekte in players angeben 
        self.__players = []                 # Liste aller Objekten der Klasse Spieler
        self.__gameBoard = []               # Liste aller Objekten der Klasse Square (bzw. Property als Unterklasse von Square)
        self.__properties  =[]              # Liste aller Objekten der Klasse Property
        self.__communityCards = []
        self.__eventCards = []

        csvDirPath = os.path.dirname(os.path.abspath(__file__)) + "/CSV-files/"         # funktioniert hoffentlich auf windows, mac und linux
        
        # Lade die Properties und Square Daten aus den CSV-Dateien
        squaresTable = self.__loadCSV(csvDirPath + "squares.csv")
        propertiesTable = self.__loadCSV(csvDirPath + "properties.csv")
        for square in squaresTable:
            if square[2] in ['property', 'trainStation', 'supplyPlant']:
                for property in propertiesTable:
                    if property[0] == square[0]:                                    # Position ist gleich -> property und square gehören zusammen
                        propertyObject = Property(square[0],square[1],square[2],property[1],property[2],property[3])    # erstellt property Objekt und fügt dieses gamebBoard und properties hinzu
                        self.__gameBoard.append(propertyObject)
                        self.__properties.append(propertyObject)
            else:                                                                   # type ist weder property, noch trainStation noch supplyPlant
                self.__gameBoard.append(Square(square[0],square[1],square[2]))          # erstellt square Objekt und fügt dieses zum Feld gameBoard hinzu
        
        # Lade die Gemeinschafts- und Ereigniskarten aus den CSV-Dateien
        communityTable = self.__loadCSV(csvDirPath + "communityCards.csv")
        for card in communityTable:
            self.__communityCards.append({'text': card[0], 'action': card[1], 'value': int(card[2])})
        eventTable = self.__loadCSV(csvDirPath + "eventCards.csv")
        for card in eventTable:
            self.__eventCards.append({'text': card[0], 'action': card[1], 'value': int(card[2])})
        


    def addPlayer(self, player: Player):
        """
        Fügt einen Spieler zur Liste aller Spieler hinzu.
        """
        self.__players.append(player)
        self.__playerCount += 1
        self.__playerOrder.append(self.__playerCount - 1)       # fügt neuen Spieler an letzter Position der Reihenfolge hinzu
    
    
    def startGame(self):
        """
        Startet die Haupt-Spiel-Ablauf
        """
        # Mische Gemeinschafts- un Ereigniskarten Felder
        self.__shuffleList(self.__communityCards)
        self.__shuffleList(self.__eventCards)
        
        self.__shufflePlayerOrder()
        self.__players[self.__playerOrder[0]].startTurn()       # Starte Zug des ersten Spielers
        

    def __shufflePlayerOrder(self):     # vielleicht später noch hinzufügen, dass Spieler wirklich würfeln und denn Augensummen entsprechend die Startreheinfolge festgelegt wird
        """
        Mischt die Spieler-Reihenfolge
        """
        self.__shuffleList(self.__playerOrder)


    def __shuffleList(self, array: list):
        """
        Mischt eine Liste mit Hilfe der Python Random-Methode 
        """
        for i in range(len(array), 0, -1):
            element = array.pop(random.randint(0, i-1))
            array.append(element)
        print(array)


    def __loadCSV(self,filepath: str) -> list[list]:
        """
        Methode, um Square aus der CSV-Datei einzulesen
        """
        table = []
        # Datei öffnen zum Lesen
        file = open(filepath, "r", encoding="utf-8")
        # Variable, um erste Zeile ignorieren zu können
        start = True
        for line in file:
            if start:                                                           # erste Zeile ignorieren
                start = not (start)
            else:
                a = line.rstrip().split(";")
                # Zeile in Feld auftrennen
                table.append(a)

        file.close()
        return table


    def trade(self, player1: Player, player2: Player):
        pass


    def nextPlayersTurn(self):
        """
        Der nächste Spieler kommt zum Zug.
        """
        self.__currentPlayerId = (
            self.__currentPlayerId + 1) % self.__playerCount
        self.__currentPlayer = self.__players[self.__playerOrder[self.__currentPlayerId]]       # aktualisiere currentPlayer auf aktuelles Spieler Objekt

        self.__currentPlayer.startTurn()



    



    def getGameBoard(self):
        return self.__gameBoard

    def getProperties(self):
        return self.__properties

    
# nur zu Testzwecken, später möglichst wieder entfernen !later
if __name__ == '__main__':
    game = Game()
    
    game.addPlayer(Player(game))
    game.addPlayer(Player(game))
    game.addPlayer(Player(game))
    game.addPlayer(Player(game))
    
    game.startGame()
