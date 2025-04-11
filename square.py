class Square():
    def __init__(self, position: int, name: str, squaretype: str):
        """
        Konstruktor der Klasse Square
        """
        self.__name = name
        self.__position = position
        self.__type = squaretype
    
    
    def playerLandedOn(self, player):
        match self.__type:
            case 'property' | 'trainStation' | 'supplyPlant':           # square ist ein Art von kaufbaren Feldern
                owner = self.getOwner()
                if owner is None:
                    pass                        # Möglichkeit Grundstück zu kaufen, später hinzufügen
                elif owner != player:
                    player.payPlayer(owner, self.getRent())     # Miete wird bezahlt
            
        
    def setFieldCoord(self, x, y, width, height):
        """
        Setzt die Position und Maße des Feldes
        """
        self.__fieldX = x
        self.__fieldY = y
        self.__fieldWidth = width
        self.__fieldHeight = height
        
    def getFieldCoord(self, whichInfo):
        """
        Gibt die Position und Maße des Feldes zurück
        "x" ==> x-Koordinate
        "y" ==> y-Koordinate
        "width" ==> Breite
        "height" ==> Höhe
        """
        if whichInfo == "x":
            return self.__fieldX
        elif whichInfo == "y":
            return self.__fieldY
        elif whichInfo == "width":
            return self.__fieldWidth
        elif whichInfo == "height":
            return self.__fieldHeight

    def getName(self):
        return self.__name