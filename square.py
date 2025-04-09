class Square():
    def __init__(self, position: int, name: str, squaretype: str):
        """
        Konstruktor der Klasse Square
        """
        self.__name = name
        self.__position = position
        self.__type = squaretype
        
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