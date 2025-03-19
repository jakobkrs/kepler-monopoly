class Player():
    def __init__(self):
        """
        Konstruktoraufruf für Playerklasse
        """
        self.__name=[]
        self.__money=0                          #wird noch geändert auf Startkapital
        self.__properties=property
        self.__position=0
        self.__currentSquare=Square 
        self.__prison=False
        self.__prisoncardCommunity=False
        self.__prisoncardEvent=False
        self.__bankrupt=False

    def rollDice(self):
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend zu der Position addieren
        """
        
