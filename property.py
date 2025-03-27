import csv

class Property():
    def __init__(self,name,houses,rent,cost,mortgage,owner):
        """
        Initialisierung und Festlegung der Werte eines Grundstücks
        """
        self.__name=""
        self.__houses=0
        self.__rent=0       #Fester Wert aus einer .CSV Date
        self.__cost=0      #Fester Wert aus einer .CSV Datei
        self.__mortgage=0  #Fester Wert aus einer .CSV Datei
        self.__owner=None

    def setRent(self):
        """
        Mietpreis eines Grundstücks festlegen
        """       
        if self.__owner is None: # Kein Besitzer 
            return 0
        else:
            #Es gibt einen besitzer -> Standartmiete oder Miete mit Häusern
            return self.__rent                  

    def buildHouses(self): 
        """
        Prozedur zum erichten von Häusern auf einem Grundstück - Erhöt die Anzahl der Häuser auf einem Grundstück
        """
        if self.__owner is None: #Kein Besitzer
            return 0 #IDK WASS HIER HIN SOLL!!! #Haus kann nicht gebaut werden da dieses Grundstück noch keinen besitzer hat.

        if self.__houses >= 5 #4 Häuser + 1 Hotel als Maximum
            return 0

        self.__houses +=1
        #print("Ein Haus wurde auf " + self.name + " gebaut. Neue Anzahl: self.__houses")

    def getHouseCount(self):
        """
        Prozedur zum abrufen der Anzahl von Häusern auf einem Grundstück
        """
        return self.__houses

    def setOwner(self, owner):
        """
        Stellt einen neuen Besitzer für das Grundstück fest
        """
        self.__owner = owner
    

