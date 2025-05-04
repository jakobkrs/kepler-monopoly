from math import ceil
from square import Square
from gui import *

class Property(Square):
    def __init__(self, game, position: int, name: str, type: str, group: str, cost: int, baseRent: int):
        """
        Initialisierung und Festlegung der Werte eines Grundstücks
        """
        super().__init__(game, position, name, type)
        self.__group=group
        self.__houses=0
        self.__baseRent=baseRent   
        self.__cost=cost      
        self.__mortgage=False  # Startwert: keine Hypothek
        self.__owner=None      # Startwert: kein Besitzer
        self.__houseCost = ceil(position / 10) * 1000       # Kosten für Haus: Bereich des Spielfeldes [1;4] * 1000 $ 
        self.__game=game
        
    def __str__(self):
        return 'Property-Object{' + f'name: {super().getName()}, position: {super().getPosition()}, type: {super().getType()}, group: {self.__group}, rent: {self.__baseRent}, cost: {self.__cost}, owner: {(not (self.__owner is None) and self.__owner.getName()) or self.__owner}, mortgage: {self.__mortgage}' + '}'

    
    def __calculateRent(self):
        """
        Mietpreis neu Berechnen
        """
        if self.__owner is None: # Kein Besitzer 
            return 0
        elif self.__mortgage:
            return 0
        elif self.getType() == "supplyPlant":
            if self.__owner.completeGroup(self.__group):
                return 200 * (self.__game.getCurrentPlayer().getLastDiceRoll()[0]+self.__game.getCurrentPlayer().getLastDiceRoll()[1])
            else:
                return 80 * (self.__game.getCurrentPlayer().getLastDiceRoll()[0]+self.__game.getCurrentPlayer().getLastDiceRoll()[1])
        elif self.getType() == "trainStation":                                      # wenn ein owner existiert und das Grundstück ein Bahnhof ist, wird je nach Anzahl der besitzten Bahnhöfe die Miete berechnet
            return self.__baseRent * (2 ** (self.__owner.propertyCount("TS") - 1))
        else:
            if self.__owner.completeGroup(self.__group) and self.__houses == 0:      # wenn ein owner existiert und dieser alle Grundstücke einer Gruppe besitzt, auf denen keine Häuser gebaut wurden
                return 2 * self.__baseRent
            else:
                return [1,5,15,45,70,100][self.__houses] * self.__baseRent          # Liste enthält Faktoren für verschiedene Anzahlen an Häusern 
    
    
    def payRent(self, player):
        """
        Führt Mietzahlung vom Spieler an Besitzer aus und wechselt zum nächsten Screen. 
        """
        if player.payPlayer(self.__owner, self.getRent()):
            nextScreen()

    def getRent(self):
        return self.__calculateRent()

    def isHouseActionPossible(self, build = True) -> bool:
        """
        Ermittelt ob auf dem Grundstück ein Haus gebaut / verkauft werden kann.
        """
        return (self.__owner.completeGroup(self.__group) and            # Besitzer besitzt alle Grundstücke der Gruppe
                not self.__mortgage and                                 # keine Hypothek
                ((build and self.__houses < 5 and                       # Es soll gebaut werden und es ist noch kein Hotel gebaut
                 self.__owner.getMoney() >= self.__houseCost and        # und Spieler hat genug Geld zum kaufen
                 self.groupHouseRange()[0] == self.__houses) or         # und Hausanzahl in der Gruppe weicht nicht zu stark ab
                (not build and self.__houses > 0 and                    # Es soll verkauft werden und es gibt Häuser auf dem Grundstück
                self.groupHouseRange()[1] == self.__houses)))           # und Hausanzahl in der Gruppe weicht nicht zu stark ab
        
    def groupHouseRange(self) -> tuple:
        """
        Gibt die höchste und niedrigste Hausanzahl der eigenen Gruppe zurück, wobei eine Hypothek wie -1 gewertet wird.
        """
        minHouses = 5
        maxHouses = -1
        for property in self.__game.getProperties():
            if property.getGroup() == self.__group:
                houses = -1 if property.getMortgage() else property.getHouses()
                minHouses = min(minHouses, houses)
                maxHouses = max(maxHouses, houses)
        return (minHouses, maxHouses)
                
    def buildHouse(self):
        """
        Prozedur zum Erichten von Häusern auf einem Grundstück - Erhöt die Anzahl der Häuser auf einem Grundstück zieht Spieler entsprechendes Geld ab
        """
        if self.isHouseActionPossible(True):
            self.__owner.payBank(self.__houseCost, False)
            self.__houses +=1
    
    def sellHouse(self):
        """
        Prozedur zum VErkaufen von Häusern auf einem Grundstück - VErringert die Anzahl der Häuser auf einem Grundstück gibt Spieler entsprechendes Geld
        """
        if self.isHouseActionPossible(False):
            self.__owner.giveMoney(round(self.__houseCost * 0.5))
            self.__houses -=1

    def getHouses(self):
        return self.__houses

    def getOwner(self):
        return self.__owner

    def setOwner(self, owner):
        """
        Setzt Besitzer des Grundstücks und fügt Grundstück zur Besitzliste des Besitzers hinzu
        """
        self.__owner = owner
        if owner is not None:
            owner.addProperty(self)
    
    def getCost(self):
        return self.__cost
    
    def getHouseCost(self):
        return self.__houseCost

    def getGroup(self):
        return self.__group

    def getMortgage(self):
        return self.__mortgage
    
    def getBaseRent(self):
        return self.__baseRent

    def setMortgage(self, boolean: bool):
        self.__mortgage = boolean
        
    def raiseMortgage(self):
        """
        Nimmt Hypothek auf und gibt entsprechend Geld aus.
        """
        self.__owner.giveMoney(int(self.__cost * 0.5))
        self.__mortgage = True
    
    def cancelMortgage(self):
        """
        Löscht Hypothek und nimmt dementsprechend das Geld.
        """
        self.__owner.payBank(int(self.__cost * 0.55), False)
        self.__mortgage = False