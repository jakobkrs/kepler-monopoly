from player import Player
from square import Square
from property import Property
import random
import os
from gui import *


class Game():
    def __init__(self):
        """
        Initialisierung der Game Klasse. Setzt Startwerte der Klasseninstanz.
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
        self.__freeParkingMoney = 0
        self.__lastDrawnCard = None
        self.__selectedProperty = None

        csvDirPath = os.path.dirname(os.path.abspath(__file__)) + "/CSV-files/"         # funktioniert hoffentlich auf windows, mac und linux
        
        # Lade die Properties und Square Daten aus den CSV-Dateien
        squaresTable = self.__loadCSV(csvDirPath + "squares.csv")
        propertiesTable = self.__loadCSV(csvDirPath + "properties.csv")
        for square in squaresTable:
            if square[2] in ['property', 'trainStation', 'supplyPlant']:
                for property in propertiesTable:
                    if property[0] == square[0]:                                    # Position ist gleich -> property und square gehören zusammen
                        propertyObject = Property(self, int(square[0]),square[1],square[2],property[1],int(property[2]),int(property[3]))    # erstellt property Objekt und fügt dieses gamebBoard und properties hinzu
                        self.__gameBoard.append(propertyObject)
                        self.__properties.append(propertyObject)
            else:                                                                   # type ist weder property, noch trainStation noch supplyPlant
                self.__gameBoard.append(Square(self, int(square[0]),square[1],square[2]))          # erstellt square Objekt und fügt dieses zum Feld gameBoard hinzu
        
        # Lade die Gemeinschafts- und Ereigniskarten aus den CSV-Dateien
        communityTable = self.__loadCSV(csvDirPath + "communityCards.csv")
        for card in communityTable:
            self.__communityCards.append({'text': card[0], 'action': card[1], 'value': int(card[2])})
        eventTable = self.__loadCSV(csvDirPath + "eventCards.csv")
        for card in eventTable:
            self.__eventCards.append({'text': card[0], 'action': card[1], 'value': int(card[2])})
        


    def addPlayer(self, name: str, symbol: str):
        """
        Fügt einen Spieler zur Liste aller Spieler hinzu.
        """
        player = Player(self, name, symbol)
        self.__players.append(player)
        self.__playerCount += 1
        self.__playerOrder.append(self.__playerCount - 1)       # fügt neuen Spieler an letzter Position der Reihenfolge hinzu
        if self.__currentPlayer == None:
            self.__currentPlayer = player       # fill in value before its properly setup in startGame
    
    
    def startGame(self, shufflePlayerOrder = True):
        """
        Startet den Haupt-Spiel-Ablauf
        """
        # Mische Gemeinschafts- und Ereigniskarten
        self.__shuffleList(self.__communityCards)
        self.__shuffleList(self.__eventCards)
        
        if shufflePlayerOrder:
            self.__shufflePlayerOrder()
        self.__players[self.__playerOrder[0]].startTurn()       # Starte Zug des ersten Spielers
        

    def __shufflePlayerOrder(self):     # vielleicht später noch hinzufügen, dass Spieler wirklich würfeln und denn Augensummen entsprechend die Startreheinfolge festgelegt wird
        """
        Mischt die Spieler-Reihenfolge
        """
        self.__shuffleList(self.__playerOrder)
        self.__currentPlayer = self.__players[self.__playerOrder[0]]


    def __shuffleList(self, array: list):
        """
        Mischt eine Liste mit Hilfe der Python Random-Methode 
        """
        for i in range(len(array), 0, -1):
            element = array.pop(random.randint(0, i-1))
            array.append(element)


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

        self.setSelectedPropertyById(-1)
        self.__currentPlayer.startTurn()
        setScreen(SCREEN_ROLLDICE)


    def resetFreeParkingMoney(self):
        """
        Setzt Frei-Parken Geld zurück und gibt Geldwert zurück
        """
        money = self.__freeParkingMoney
        self.__freeParkingMoney = 0
        return money

    
    def addFreeParkingMoney(self, amount: int):
        """
        Fügt Geld zu Frei-Parken hinzu
        """
        self.__freeParkingMoney += amount
    
    def drawCard(self, type: str) -> object:
        """
        Zieht die oberste Gemeinschafts- oder Ereigniskarte und gibt deren Werte zurück.
        """
        if type == "community":
            card = self.__communityCards.pop(0)
            self.__communityCards.append(card)
        else:
            card = self.__eventCards.pop(0)
            self.__eventCards.append(card)
        card["type"] = type
        self.__lastDrawnCard = card
        return card


    

    def getPlayers(self) -> list[Player]:
        return self.__players

    def getGameBoard(self) -> list[Square]:
        return self.__gameBoard

    def getProperties(self) -> list[Property]:
        return self.__properties

    def getPlayerOrder(self) -> list[int]:
        return self.__playerOrder
    
    def getCurrentPlayer(self) -> Player:
        return self.__currentPlayer
    
    def getLastDrawnCard(self) -> object:
        return self.__lastDrawnCard
    
    def getSelectedProperty(self) -> Property:
        return self.__selectedProperty
    
    def setSelectedPropertyById(self, id: int):
        """
        Setzt selectedProperty ausgehend von der Property-Id
        """
        if id >= 0:
            self.__selectedProperty = self.__properties[id]
        else:
            self.__selectedProperty = None


if __name__ == "__main__":
    game = Game()
    for i in range(4): game.addPlayer(chr(65 + i), "")
    game.startGame()

    #game.getPlayers()[0].goToPosition(35)
    #game.getGameBoard()[2].playerLandedOn(game.getPlayers()[0])
    #print(game.getPlayers()[0])
