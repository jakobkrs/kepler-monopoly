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
        self.__rent=self.__baseRent     
        self.__cost=cost      
        self.__mortgage=False  # Startwert: keine Hypothek
        self.__owner=None      # Startwert: kein Besitzer
        self.__game=game
        
    def __str__(self):
        return 'Property-Object{' + f'name: {super().getName()}, position: {super().getPosition()}, type: {super().getType()}, group: {self.__group}, rent: {self.__baseRent}, cost: {self.__cost}, owner: {(not (self.__owner is None) and self.__owner.getName()) or self.__owner}, mortgage: {self.__mortgage}' + '}'

    
    def calculateRent(self):
        """
        Mietpreis neu Berechnen
        """
        if self.__owner and self.__owner.completeGroup(self.__group) and self.__houses == 0:       # wenn ein owner existiert und dieser alle Grundstücke einer Gruppe besitzt, auf denen keine Häuser gebaut wurden
            self.__rent = 2 * self.__baseRent
        elif self.__mortgage:
            self.__rent = 0
        else:
            self.__rent = [1,5,15,45,70,100][self.__houses] * self.__baseRent          # Liste enthält Faktoren für verschiedene Anzahlen an Häusern 
    
    def payRent(self, player):
        """
        Führt Mietzahlung vom Spieler an Besitzer aus und ändert Screens. 
        """
        if player.payPlayer(self.__owner, self.getRent()):
            roll = self.__game.getCurrentPlayer().getLastDiceRoll()
            if roll[0] != roll[1]:
                setScreen(SCREEN_CONTINUE)
            else:
                setScreen(SCREEN_ROLLDICEAGAIN)

    def getRent(self):
        if self.__owner is None: # Kein Besitzer 
            return 0
        else:
            return self.__rent                  # Es gibt einen Besitzer -> Standardmiete oder Miete mit Häusern

    def buildHouse(self): 
        """
        Prozedur zum Erichten von Häusern auf einem Grundstück - Erhöt die Anzahl der Häuser auf einem Grundstück
        """
        if (not self.__owner is None) and self.__houses < 5:        #Haus bauen nur, wenn es Besitzer gibt und noch nicht 5 Häuser gebaut sind
            self.__houses +=1

    def getHouses(self):
        return self.__houses

    def getOwner(self):
        return self.__owner

    def setOwner(self, owner):
        """
        Setzt Besitzer des Grundstücks und fügt Grundstück zur Besitzliste des Besitzers hinzu
        """
        self.__owner = owner
        owner.addProperty(self)
    
    def getCost(self):
        return self.__cost

    def getMortgage(self):
        return self.__mortgage

    def setMortgage(self, boolean):
        self.__mortgage = boolean