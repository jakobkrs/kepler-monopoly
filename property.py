from square import Square
#from player import Player

class Property(Square):
    def __init__(self, position: int, name: str, type: str, group: str, baseRent: int, cost: int):
        """
        Initialisierung und Festlegung der Werte eines Grundstücks
        """
        super().__init__(position, name, type)
        self.__group=group
        self.__houses=0
        self.__baseRent=baseRent
        self.__rent=self.__baseRent     
        self.__cost=cost      
        self.__mortgage=False  #Startwert
        self.__owner=None      #Startwert

    
    def setRent(self):
        """
        Mietpreis neu Berechnen
        """
        if self.__owner and self.__owner.completeGroup():       # wenn ein owner existiert und dieser alle Grundstücke einer Gruppe besitzt
            self.__rent = 2 * self.__baseRent
        else:
            self.__rent = [1,5,15,45,70,100][self.__houses] * self.__baseRent
    

    def getRent(self):
        if self.__owner is None: # Kein Besitzer 
            return 0
        else:
            #Es gibt einen besitzer -> Standartmiete oder Miete mit Häusern
            return self.__rent                  

    def buildHouse(self): 
        """
        Prozedur zum Erichten von Häusern auf einem Grundstück - Erhöt die Anzahl der Häuser auf einem Grundstück
        """
        if (not self.__owner is None) and self.__houses < 5:        #Haus bauen nur, wenn es Besitzer gibt und noch nicht 5 Häuser gebaut sind
            self.__houses +=1

    def getHouses(self):
        """
        Prozedur zum abrufen der Anzahl von Häusern auf einem Grundstück
        """
        return self.__houses

    def setOwner(self, owner):
        """
        legt einen neuen Besitzer für das Grundstück fest
        """
        self.__owner = owner

