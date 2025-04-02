class Property():
    def __init__(self,name,houses,rent,cost):
        """
        Initialisierung und Festlegung der Werte eines Grundstücks
        """
        self.__name=name
        self.__houses=houses
        self.__rent=rent       
        self.__cost=cost      
        self.__mortgage=False  #Startwert
        self.__owner=None      #Startwert

    """
    def setRent(self)
    muss noch erstellt werden
    --> rent abhängig von houses
    """

    def getRent(self):
        """
        Mietpreis eines Grundstücks festlegen
        """       
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
    

