from gui import *

class Square():
    def __init__(self, game, position: int, name: str, squaretype: str):
        """
        Konstruktor der Klasse Square
        """
        self.__name = name
        self.__position = position
        self.__type = squaretype
        self.__game = game
    
    def __str__(self):
        return 'Square-Object{' + f'name: {self.__name}, position: {self.__position}, type: {self.__type}' + '}'
    
    
    def playerLandedOn(self, player):
        """
        Führt bei Betreten eine Feldes entsprechende Aktion aus.
        """ 
        match self.__type:
            case 'property' | 'trainStation' | 'supplyPlant':           # Spielfeld ist eine Art kaufbares Grundstück
                self.__game.setSelectedPropertyById(self.__game.getProperties().index(self))
                owner = self.getOwner()
                if owner is None:
                    setScreen(SCREEN_BUYOPTION)
                elif owner != player:
                    setScreen(SCREEN_PAYRENT)
                else:
                    setScreen(SCREEN_OWNPROPERTY)
            case 'community' | 'event':             # Spielfeld ist ein Aktionskartenfeld
                self.__game.drawCard(self.__type)
                setScreen(SCREEN_CARD)
            case 'taxes1' | 'taxes2':               # Spielfeld ist eines der Felder für Steuern
                setScreen(SCREEN_TAXES)
            case 'freeParking':
                setScreen(SCREEN_FREEPARKING)
            case 'goToPrison':
                setScreen(SCREEN_GOTOPRISON)
            case 'start' | 'prison':                # hier muss nichts besonderes (im GUI und Hintergrund) passieren
                setScreen(SCREEN_CONTINUE)                


    def setFieldCoord(self, x, y, width, height):
        """
        Setzt die Position und Maße des Feldes
        """
        self.__fieldX = x
        self.__fieldY = y
        self.__fieldWidth = width
        self.__fieldHeight = height
        

        
        
    def getFieldX(self):
        return self.__fieldX
    
    def getFieldY(self):
        return self.__fieldY
    
    def getFieldWidth(self):
        return self.__fieldWidth
    
    def getFieldHeight(self):
        return self.__fieldHeight

    def getName(self):
        return self.__name
    
    def getType(self):
        return self.__type
    
    def getPosition(self):
        return self.__position