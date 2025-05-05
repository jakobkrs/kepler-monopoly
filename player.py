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
        self.__bankrupt=False
        self.__lastDiceRoll = []
        self.__game=game
        self.__doubleCount = 0
        self.__roundsInPrison=0

    
    def __str__(self):
        """
        Strukturierte Ausgabe der Spielerinformationen
        """
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
        """
        Startet den Zug des Spielers, überprüft ob der Spieler Bankrott ist oder im Gefängnis sitzt.
        """
        if self.__bankrupt:
            self.__game.nextPlayersTurn()
        elif self.__prison:
            setScreen(SCREEN_PRISON)
        else:
            self.__doubleCount = 0
            self.__lastDiceRoll = []
            setScreen(SCREEN_ROLLDICE)
            

    def goToPrison(self):
        """
        Spieler geht ins Gefängnis, wird auf das Gefängnisfeld gesetzt und der nächste Screen wird gesetzt.
        """
        global nextScreens
        self.__prison=True
        self.__roundsInPrison = 0
        self.goToPosition(10, False)
        if len(nextScreens) > 0: nextScreens = []   # löscht alle möglicherweise bestehenden Screens 
        setScreen(SCREEN_MANAGEMENT)      # setzt nächsten Screen direkt wieder
        
    def instantPrisonEscape(self):
        """
        Sofortige Freilassung aus dem Gefängnis
        """
        self.payBank(1000, False)
        self.__prison=False
        setScreen(SCREEN_PRISONESCAPED)

    def tryPrisonEscape(self):
        """
        Spieler versucht aus dem Gefängnis zu kommen
        """
        self.__roundsInPrison += 1
        num1, num2, _ = self.__rollDice()
        if num1 == num2:
            self.__prison=False
            setScreen(SCREEN_PRISONESCAPED)
        elif self.__roundsInPrison >= 3:
            setScreen(SCREEN_FAILEDPRISONESCAPE)
        else:
            setScreen(SCREEN_MANAGEMENT)
                
        


    def turn(self):
        """
        Einmal würfeln
        """
        num1,num2,num=self.__rollDice()
    
        if num1 == num2 and self.__doubleCount >= 2:
            self.goToPrison()
            return
        
        self.goToPosition(self.__position+num)

        if num1 != num2:
            addScreenToQueue(SCREEN_MANAGEMENT)       # kein Pasch. normales fortfahren
        else:
            self.__doubleCount += 1
            addScreenToQueue(SCREEN_ROLLDICEAGAIN)  # Pasch, es wird nochmal gewürfelt
        

    def goToPosition(self, position: int, moneyForExceedingStart : bool = True):
        """
        setzt Spieler auf richtige Position
        """
        position = position % len(self.__game.getGameBoard())               # Überschreiten von Los
        if position < self.__position and not moneyForExceedingStart:       # Geld erhalten bei Überschreiten von Los
            self.giveMoney(4000)                                            
        self.__position=position                                            # aktualisiere Postion
        self.__currentSquare=self.__game.getGameBoard()[self.__position]
        self.__currentSquare.playerLandedOn(self)                             # behandelt landen des Spielers auf Feld

 
    def __rollDice(self):
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend addieren
        """
        num1= random.randint(1,6)
        num2= random.randint(1,6)
        sum=num1+num2
        self.__lastDiceRoll = [num1, num2]
        return num1,num2,sum

    def completeGroup(self,id: str):
        """
        Überprüft ob ein Spieler alle Grundstücke einer Gruppe besitzt
        """
        owners = []
        for property in self.__game.getProperties():
            if property.getGroup() == id and not property.getMortgage():
                owners.append(property.getOwner())
        
        return all(x==owners[0] for x in owners)
    
    def propertyCount(self, id: str):
        """
        Gibt die Anzahl der Grundstücke einer Gruppe zurück, die der Spieler besitzt
        """
        count = 0
        for property in self.__game.getProperties():
            if property.getGroup() == id and property.getOwner() == self:
                count += 1
        return count
    
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

    def givePropertyToOtherPlayer(self, property, player):
        """
        Überträgt ein Grundstück von diesem Spieler auf einen Anderen.
        """
        if property in self.__properties:       # Sicherheitsüberrüfung, ob Spieler das Grundstück wirklich besitzt
            property.setOwner(player)
            self.__properties.remove(property)

    # Geldbezogene Methoden

    def __pay(self, amount: int) -> bool:
        """
        Spieler muss Geld bezahlen, wobei überprüft wird ob der Spieler bezahlen kann und gegebenenfalls die Option für Hypotheken oder Bankrott gehen gegeben werden. Sie gibt ob der Spieler Zahlungsfähig ist.
        """
        if self.__money >= amount:
            self.__money -= amount
            return True     # Spieler kann zahlen
        else:
            return False    # Spieler hat zu wenig Geld.
    
    def payPlayer(self, player, amount: int) -> bool:
        """
        Transferiert Geld von diesem Spieler zum angegebenen
        """
        if self.__pay(amount):
            player.giveMoney(amount)
            return True
        else:
            self.__game.setBankruptcyData({"player": self, "target": player, "amount": amount})
            setScreen(SCREEN_BANCRUPTCY)
            return False
        
    def payBank(self, amount: int, freeParking = True) -> bool:
        """
        Spieler zahlt Geld an Bank bzw. in den Frei Parken Pot 
        """
        if self.__pay(amount):
            if freeParking:
                self.__game.addFreeParkingMoney(amount)     # Geld wird zu Frei Parken hinzugefügt
            return True
        else:
            self.__game.setBankruptcyData({"player": self, "target": 0, "amount": amount})      # 0 steht für Bank
            setScreen(SCREEN_BANCRUPTCY)
            return False
    
    def giveMoney(self, amount: int):
        """
        Spieler erhält Geld von beliebiger Quelle
        """
        self.__money += amount
    
    
    # Bankrott
    def executeBankruptcy(self, target = 0):
        """
        Spieler ist Bankrott und übergibt gesamten Besitz an Zielspieler / die Bank.
        """
        for property in self.__properties:
            if target == 0:     # Ziel ist die Bank
                property.setOwner(None)
            else:
                property.setOwner(target)
        if target != 0: target.giveMoney(self.__money)      # Gibt Spieler alles Geld
        self.__properties = []      # Spieler besitzt keine Properties mehr
        self.__money = 0            # Spielr besitzt kein geld mehr
        self.__bankrupt = True
        setScreen(SCREEN_MANAGEMENT)
        self.__game.checkWin()
    
    
    
    def getName(self) -> str:
        return self.__name
    
    def getMoney(self) -> int:
        return self.__money
    
    def getPosition(self) -> int:
        return self.__position
    
    def getProperties(self) -> Property:
        return self.__properties
    
    def getSymbol(self) -> str:
        return self.__symbol
    
    def getCurrentSquare(self) -> Square:
        return self.__currentSquare
    
    def getBankrupt(self) -> bool:
        return self.__bankrupt
    
    def getPrison(self) -> bool:
        return self.__prison
    
    def getRoundsInPrison(self) -> int:
        return self.__roundsInPrison
    
    def getLastDiceRoll(self) -> tuple:
        return self.__lastDiceRoll


