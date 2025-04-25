import random
from square import * 
from property import *
from gui import *
class Player():
    def __init__(self,game, name: str, symbol: str):
        """
        Konstruktoraufruf für Playerklasse
        """
        self.__name=name
        self.__symbol=symbol
        self.__money=30000                          # Startkapital
        self.__properties=[]
        self.__position=0
        self.__currentSquare=game.getGameBoard()[self.__position]
        self.__prison=False
        #self.__prisoncardCommunity=False           # Budget spar Maßnahme
        #self.__prisoncardEvent=False
        self.__bankrupt=True if name == 'Spieler 3' else False      # zu Test Zwecken
        self.__lastDiceRoll = []
        self.__game=game
    
    def __str__(self):
        propertyStr = 'properties: ['
        for property in self.__properties:
            propertyStr += f'\n\t\t{property}'
            if property == self.__properties[len(self.__properties)-1]:
                propertyStr += '\n\t'
            else:
                propertyStr += ','
        propertyStr += ']'
        return 'Player-Object{\n' + f'\tname: {self.__name},\n\tmoney: {self.__money},\n\tposition: {self.__position},\n\tcurrentSquare: {self.__currentSquare},\n\t{propertyStr},\n\tprison: {self.__prison},\n\tbankrupt: {self.__bankrupt}\n' + '}'



    def startTurn(self):
        if self.__bankrupt:
            self.__game.nextPlayersTurn()
        else:
            self.__doubleCount = 0
            self.__lastDiceRoll = []
            setScreen(SCREEN_ROLLDICE)
                
            

    def goToPrison(self):
        """
        gehe ins Gefängnis
        """
        self.__prison=True
        self.goToPosition(10)
        self.__game.nextPlayersTurn()

    def turn(self):
        """
        Einmal würfeln
        """
        num1,num2,num=self.rollDice()

        if num1 == num2 and self.__doubleCount >= 2:
            self.goToPrison()
            return
        
        self.goToPosition(self.__position+num)
        # sonstiges

        if num1 != num2:
            addScreenToQueue(SCREEN_CONTINUE)
        else:
            self.__doubleCount += 1
            addScreenToQueue(SCREEN_ROLLDICEAGAIN)

    def goToPosition(self, position: int):
        """
        setzt Spieler auf richtige Position
        """
        self.__position=position % len(self.__game.getGameBoard())          # aktualisiere Postion und handelt das überschreiten von Los in der Positions-Variable
        if position > 39:
            self.giveMoney(4000)                                            # Geld erhalten bei Überschreiten von Los
        self.__currentSquare=self.__game.getGameBoard()[self.__position]
        self.__currentSquare.playerLandedOn(self)                             # behandelt landen des Spielers auf Feld

 
    def rollDice(self):
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend addieren
        """
        num1= random.randint(1,6)
        num2= random.randint(1,6)
        num=num1+num2
        self.__lastDiceRoll = [num1, num2]
        return num1,num2,num

    def completeGroup(self,id: str):
        """
        Überprüft ob ein Spieler alle Grundstücke einer Gruppe besitzt
        """
        properties = self.__game.getProperties()

        owners = []
        for property in properties:
            if property.group == id:
                owners.append(property.owner)
        
        return all(x==owners[0] for x in owners)
    
    def buyProperty(self, property):
        """
        Erwerben des Grundstücks.
        """
        self.payBank(property.getCost(), False)
        property.setOwner(self)
        nextScreen()
        
    def addProperty(self, property):
        """
        Fügt eine neue Property als Besitzung des Spielers hinzu
        """
        self.__properties.append(property)



    # Geldbezogene Methoden
    
    def __pay(self, amount: int):
        """
        Spieler muss Geld bezahlen, wobei überprüft wird ob der Spieler bezahlen kann und gegebenenfalls die OPtion für Hypotheken oder Bankrott gehen gegeben werden. Sie gibt ob der Spieler Zahlungsfähig ist.
        """
        if self.__money >= amount:
            self.__money -= amount
            return True     # Spieler kann zahlen
        else:
            return False    # Spieler hat zu wenig Geld. Option zum Hypotheken eingehen, oder Bankrott gehen muss hinzugefügt werden und entsprechend der Rückgabewert angepasst werden.
    
    def payPlayer(self, player, amount: int):
        """
        Transferiert Geld von diesem Spieler zum angegebenen
        """
        if self.__pay(amount):
            player.giveMoney(amount)
            return True
        else:
            self.choose_mortgage(amount)
            pass # Spieler ist Bankrott und muss allen Besitz an neuen Spieler abgeben
        
    def payBank(self, amount: int, freeParking = True):
        """
        Spieler zahlt Geld an Bank bzw. in den Frei Parken Pot 
        """
        if self.__pay(amount):
            if freeParking:
                self.__game.addFreeParkingMoney(amount)     # Geld wird zu Frei Parken hinzugefügt
        else:
            pass # Spieler ist Bankrott und muss allen Besitz wieder zur freien Verfügbarkeit freigeben
    
    def giveMoney(self, amount: int):
        """
        Spieler erhält Geld von beliebiger Quelle
        """
        self.__money += amount
    
    
    def getName(self):
        return self.__name
    
    def getMoney(self):
        return self.__money
    
    def getPosition(self):
        return self.__position
    
    def getProperties(self):
        return self.__properties
    
    def getSymbol(self):
        return self.__symbol
    
    def getCurrentSquare(self):
        return self.__currentSquare
    
    def getBankrupt(self):
        return self.__bankrupt
    
    def getLastDiceRoll(self):
        return self.__lastDiceRoll

    
    def choose_mortgage(self, amount):
        """
        Methode zum Auswählen einer Hypothek
        """
