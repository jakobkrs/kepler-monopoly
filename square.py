class Square():
    def __init__(self, game,  position: int, name: str, squaretype: str):
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
            case 'property' | 'trainStation' | 'supplyPlant':           # square ist ein Art von kaufbaren Feldern
                owner = self.getOwner()
                if owner is None:
                    pass                        # Möglichkeit Grundstück zu kaufen, später hinzufügen
                elif owner != player:
                    player.payPlayer(owner, self.getRent())     # Miete wird bezahlt
            case 'community':
                self.__cardField(player, "community")
            case 'event':
                self.__cardField(player, "event")
            case 'taxes1':
                player.payBank(4000)
            case 'taxes2':
                player.payBank(2000)
            case 'freeParking':
                money = self.__game.resetFreeParkingMoney()     # Seit Frei Parken Geld auf 0 zurück und speichert den Betrag in money
                player.giveMoney(money)
            case 'goToJail':
                player.goToPrison()
            case 'start' | 'jail':      # hier muss nichts passieren
                pass

    def __cardField(self, player, type: str):
        """
        Zieht bei Betreten eines Karten Feldes eine Karte und führt entsprechende Aktion aus.
        """
        if type == "community":
            card = self.__game.drawCommunityCard()
        else:
            card = self.__game.drawEventCard()
        match card["action"]:
            case "moveTo":
                player.goToPosition(card["value"])
            case "moveToNearestSupplyPlant":
                self.moveToNearest(player, "supplyPlant")
            case "moveToNearestTrainStation":
                self.moveToNearest(player, "trainStation")
            case "goToJail":
                player.goToPrison()
            case "renovate":
                sum = 0
                for property in player.getProperties():
                    sum += 500 * min(property.getHouses(),4)
                player.payBank(sum)
            case "moveBack":
                player.goToPosition(player.getPosition() - card["value"])
            case "earnMoney":
                player.giveMoney(card["value"])
            case "payMoney":
                player.payBank(card["value"])
            #case "getOutOfJail":
                #pass
            case "earnFromPlayers":
                for opponent in self.__game.getPlayers():
                    if opponent != player:
                        opponent.payPlayer(player, card["value"])    
            case "payPlayers":
                for opponent in self.__game.getPlayers():
                    if opponent != player:
                        player.payPlayer(opponent, card["value"])

            
    def moveToNearest(self, player, type: str):
        """
        Ermittelt das nächstliegende Feld eines bestimmten Typen und bewegt Spieler dort hint
        """
        pos = player.getPosition()
        while  self.__game.getGameBoard()[pos].getType() != type:
            pos = (pos + 1) % len(self.__game.getGameBoard())
        player.goToPosition(pos)
                


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
    
    def getType(self):
        return self.__type
    
    def getPosition(self):
        return self.__position