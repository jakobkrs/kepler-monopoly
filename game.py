from player import Player
from square import Square
from property import Property
from actionCard import ActionCard
import random
import os
from gui import *


class Game():
    def __init__(self):
        """
        Initialisierung der Game Klasse. Setzt Startwerte der Klasseninstanz.
        """
        self.__currentPlayerId = 0
        self.__currentPlayer : Player = None
        self.__playerCount = 0
        self.__playerOrder : list[int] = []                     # Liste an ganzen Zahlen, die die postion der Spieler-Objekte in players angeben 
        self.__players : list[Player] = []                      # Liste aller Objekten der Klasse Spieler
        self.__gameBoard : list[Square | Property] = []         # Liste aller Objekten der Klasse Square (bzw. Property als Unterklasse von Square)
        self.__properties : list[Property] = []                 # Liste aller Objekten der Klasse Property
        self.__communityCards : list[ActionCard] = []           # Liste aller Gemeinschaftskarten als Objekte der Klasse ActionCard
        self.__eventCards : list[ActionCard] = []               # Liste aller Ereigniskarten als Objekte der Klasse ActionCard
        self.__freeParkingMoney = 0
        self.__lastDrawnCard : ActionCard = None
        self.__selectedProperty : Property = None
        self.__bankruptcyData : dict[str, Player | int] = {"player": None, "target": None, "amount": 0}
        self.__tradeData = [None, None]

        csvDirPath = os.path.dirname(os.path.abspath(__file__)) + "/CSV-files/"         # funktioniert hoffentlich auf windows, mac und linux
        
        # Lädt die Properties und Square Daten aus den CSV-Dateien
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
        
        # Lädt die Gemeinschafts- und Ereigniskarten aus den CSV-Dateien
        communityTable = self.__loadCSV(csvDirPath + "communityCards.csv")
        for card in communityTable:
            self.__communityCards.append(ActionCard(self, "community", card[0], card[1], int(card[2])))
        eventTable = self.__loadCSV(csvDirPath + "eventCards.csv")
        for card in eventTable:
            self.__eventCards.append(ActionCard(self, "event", card[0], card[1], int(card[2])))
        


    def addPlayer(self, name: str, symbol: str):
        """
        Fügt einen Spieler zur Liste aller Spieler hinzu.
        """
        player = Player(self, name, symbol)
        self.__players.append(player)
        self.__playerCount += 1
        self.__playerOrder.append(self.__playerCount - 1)       # fügt neuen Spieler voerst an letzter Position der Reihenfolge hinzu
        if self.__currentPlayer == None:
            self.__currentPlayer = player       # setzt den Wert, bevor diese in startGame richtig initialisiert wird
            self.__winner = player              # setzt den Wert temporär, bevor er am Ende des Spiel endgültig gesetzt wird
    
    
    def startGame(self, shufflePlayerOrder : bool = True):
        """
        Startet den Haupt-Spiel-Ablauf
        """
        # Mische Gemeinschafts- und Ereigniskarten
        self.__shuffleList(self.__communityCards)
        self.__shuffleList(self.__eventCards)
        
        if shufflePlayerOrder:
            self.__shufflePlayerOrder()
        
        self.__players[self.__playerOrder[0]].startTurn()       # Starte Zug des ersten Spielers
        

    def __shufflePlayerOrder(self):
        """
        Mischt die Reihenfolge der Spieler und setzt den aktuellen Spieler auf den ersten in der neuen Reihenfolge
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


    def __loadCSV(self, filepath: str) -> list[list[str]]:
        """
        Methode, um tabellenartige Daten aus CSV-Dateien einzulesen und als zweidimensionale Listen zurückzugeben
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


    def nextPlayersTurn(self):
        """
        Der nächste Spieler kommt zum Zug.
        """
        self.__currentPlayerId = (self.__currentPlayerId + 1) % self.__playerCount              # Erhöht den Spielerindex um 1. Falls  der letzte Spieler erreicht wurde, wird der Index auf 0 gesetzt
        self.__currentPlayer = self.__players[self.__playerOrder[self.__currentPlayerId]]       # aktualisiert currentPlayer auf das aktuelle Spieler Objekt

        self.setSelectedPropertyById(-1)        # Sorgt dafür, dass kein Grundstück selektiert ist und damit auch keines Angezeigt wird
        self.__currentPlayer.startTurn()        # Beginnt den Würfel- / Gefängniszug des nächsten Spielers

    # Methoden für Geld auf Frei Parken
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
    
    def drawCard(self, type: str) -> dict[str, str | int]:
        """
        Zieht die oberste Gemeinschafts- oder Ereigniskarte und gibt deren Werte zurück.
        """
        if type == "community":     # Gemeinschaftskarte
            card = self.__communityCards.pop(0)     # Entfernt erste Karte aus Karten-Reihenfolge
            self.__communityCards.append(card)      # Fügt entfernte KArte an der letzten Stelle der Reihenfolge wieder ein
        else:                       # Ereigniskarte
            card = self.__eventCards.pop(0)         # Entfernt erste Karte aus Karten-Reihenfolge
            self.__eventCards.append(card)          # Fügt entfernte KArte an der letzten Stelle der Reihenfolge wieder ein
        self.__lastDrawnCard = card
        return card


    # Handelsmethoden
    def selectPlayerForTrade(self, side: int, player: Player):
        """
        Wählt einen Spieler als Handelspartner aus, und weist diesem die entsprechende Seite zu. Wenn player den Wert "" hat, wird die Seite keinem Spieler zugewiesen.
        """
        if player == "":    # Handelspartner wird entfernt, bzw. kein neuer Handelspartner wird gesetzt
            self.__tradeData[side] = None
        else:
            self.__tradeData[side] = {"player": player, "properties": [], "money": 0}       # Initialisierung des Handelspartners
    
    def canPropertyBeAddedToTrade(self) -> bool:
        """
        Gibt zurück, ob das selektierte Grundstück zum Handel auf eine der beiden Seiten hinzugefügt werden kann.
        """
        if self.__selectedProperty is None:     # Breche Überprüfung mit negativen Resultat ab, falls kein Grundstück ausgewählt ist 
            return False
        ownerInTradeA = self.__tradeData[0] is not None and self.__selectedProperty.getOwner() == self.__tradeData[0]["player"]     # Überprüfung ob Besitzer des selektierten Grundstücks der erste selektierte Handelspartner ist
        ownerInTradeB = self.__tradeData[1] is not None and self.__selectedProperty.getOwner() == self.__tradeData[1]["player"]     # Überprüfung ob Besitzer des selektierten Grundstücks der zweite selektierte Handelspartner ist
        noHouseInGroup = self.__selectedProperty.groupHouseRange()[1] == 0          # Überprüfung ob kein Grundstück der Gruppe ein Haus hat
        return (ownerInTradeA or ownerInTradeB) and noHouseInGroup and not self.isPropertyInTrade()
        
    def isPropertyInTrade(self) -> bool:
        """
        Überprüft, ob das selektierte Grundstück bereits im Handel enthalten ist.
        """
        propertiesInTrade = []
        if self.__tradeData[0] is not None:
            propertiesInTrade += self.__tradeData[0]["properties"]      # Fügt Grundstücke, die beim ersten Handelspartner zum Handel hinzugefügt wurden zu Liste hinzu
        if self.__tradeData[1] is not None:
            propertiesInTrade += self.__tradeData[1]["properties"]      # Fügt Grundstücke, die beim zweiten Handelspartner zum Handel hinzugefügt wurden zu Liste hinzu
        return self.__selectedProperty in  propertiesInTrade            # Überprüft und gibt zurück, ob das aktuell selektierte Grundstück bereits in den Grundstücken des Handels enthalten ist
    
    def addPropertyToTrade(self):
        """
        Fügt das selektierte Grundstück zum Handel auf der entsprechende Seite des Besitzers hinzu.
        """
        property = self.__selectedProperty
        side = int(property.getOwner() != self.__tradeData[0]["player"])        # muss umgekehrt werden, da linke Seite 0 entspricht
        self.__tradeData[side]["properties"].append(property)
    
    def removePropertyFromTrade(self):
        """
        Entfernt das selektierte Grundstück vom Handel auf der entsprechende Seite des Besitzers.
        """
        property = self.__selectedProperty
        side = int(property.getOwner() != self.__tradeData[0]["player"])        # muss umgekehrt werden, da linke Seite 0 entspricht
        self.__tradeData[side]["properties"].remove(property)
    
    def addTradeMoney(self, side: int, amount: int):
        """
        Fügt Geld zu einer Seite des Handels hinzu, bzw. zieht der anderen Seite entsprechendes Geld ab,
        damit einer der Handelspartner immer bei null bleibt.
        """
        money = [0,0]
        for i in range(2):                              # Initialisierung mit bereits existierenden Geldwerten, unter Beachtung, dass eines noch nicht initialisiert sein kann 
            if self.__tradeData[i] is not None:
                money[i] += self.__tradeData[i]["money"]

        money[side] += amount       # Fügt Geldbetrag hinzu zur richtigen Seite hinzu
        doubleMoney = min(money)    # Speichert Betrag, der auf beiden Seiten abgezogen werden muss, um eine Seite auf 0 zu halten.
        
        for i in range(2):
            money[i] -= doubleMoney
            money[i] = max(0, money[i])         # Limitiert Geldbetrag auf Interval [0;∞[
            if self.__tradeData[i] is not None:
                money[i] = min(money[i], self.__tradeData[i]["player"].getMoney())      # Limiertiert Geldbetrag auf Interval [0; Spielergeld]
                self.__tradeData[i]["money"] = money[i]     # Aktualisiert originales Objekt für die Handelsdaten mit neuem Geldbetrag
        
    def trade(self):
        """
        Führt Handel, der vorher bestimmt wurde, durch.
        """
        if not None in self.getTradeData():     # Sicherheitsüberprüfung, falls nicht beide Handelspartner selektiert wurden
            for i in range(2):                                      # beide Handelspartner übertragen die angegebenen Güter ihrer Seite an den jeweils anderen Spieler
                side : dict = self.__tradeData[i]
                player = side["player"]
                otherPlayer = self.__tradeData[1-i]["player"]
                for property in side["properties"]:                 # alle Grundstücke der Handelsseite werden übertragen
                    player.givePropertyToOtherPlayer(property, otherPlayer)
                player.payPlayer(otherPlayer, side["money"])        # Geld wird übertragen
            self.resetTrade()
    
    def resetTrade(self):
        """
        Bricht den Handel ab und setzt Handelsdaten zurück.
        """
        self.selectPlayerForTrade(0, "")        # Kein Spieler ist für die linke Seite ausgewählt
        self.selectPlayerForTrade(1, "")        # kein Spieler ist für die rechte Seite ausgewählt
        setScreen(SCREEN_MANAGEMENT)
    

    def checkWin(self):
        """
        Überprüft, ob nur noch ein Spieler nicht bankrott ist und demnach gewonnen hat. Falls dies der Fall ist wird der Gewinner, auf dem entsprechendem Screen, ausgerufen.
        """
        winner = None
        for player in self.__players:
            if not player.getBankrupt():
                if winner is None:      # Überprüft ob nicht ein anderer Spieler auch nicht bankrott ist
                    winner = player
                else:
                    return      # Mehrere Spieler sind nicht bankrott. Es gibt keinen Gewinner, die Schleife wird abgebrochen.
        if winner is not None:      # Es gibt einen Gewinner, Sicherheitüberprüfung, die nicht notwendig sein sollte
            self.__winner = winner
            setScreen(SCREEN_WIN)
            
    
    # Getter-Methoden
    def getPlayers(self) -> list[Player]:
        return self.__players

    def getGameBoard(self) -> list[Square | Property]:
        return self.__gameBoard

    def getProperties(self) -> list[Property]:
        return self.__properties

    def getPlayerOrder(self) -> list[int]:
        return self.__playerOrder
    
    def getCurrentPlayer(self) -> Player:
        return self.__currentPlayer

    def getWinner(self) -> Player:
        return self.__winner
    
    def getLastDrawnCard(self) -> dict:
        return self.__lastDrawnCard
    
    def getFreeParkingMoney(self) -> int:
        return self.__freeParkingMoney
    
    def getSelectedProperty(self) -> Property:
        return self.__selectedProperty
    
    def getBankruptcyData(self) -> tuple:
        return self.__bankruptcyData
    
    def getTradeData(self) -> list:
        return self.__tradeData
    
    # Setter-Methoden
    def setSelectedPropertyById(self, id: int):
        """
        Setzt selectedProperty ausgehend vom Property-Index
        """
        if id >= 0:
            self.__selectedProperty = self.__properties[id]
        else:
            self.__selectedProperty = None
    
    def setBankruptcyData(self, data: dict[str, str | int]):
        self.__bankruptcyData = data
