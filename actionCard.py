from gui import *

class ActionCard:
    def __init__(self, game, type: str, text : str, action : str, value : int):
        """
        Konstruktor der Klasse ActionCard setzt die benötigten Eigenschaften.
        """
        self.__type = type
        self.__text = text
        self.__action = action
        self.__value = value
        self.__game = game
    
    def execute(self):
        """
        Führt diese Aktionskarte aus.
        """
        player = self.__game.getCurrentPlayer()
        match self.__action:            # Führt entsprechende Aktionsart der Karte aus
            case "moveTo":
                player.goToPosition(self.__value)
            case "moveToNearestSupplyPlant":
                self.__moveToNearest(player, "supplyPlant")
            case "moveToNearestTrainStation":
                self.__moveToNearest(player, "trainStation")
            case "goToPrison":
                player.goToPrison()
            case "renovate":
                sum = 0
                for property in player.getProperties():
                    sum += 500 * min(property.getHouses(),4)
                if player.payBank(sum):
                    nextScreen()
            case "moveBack":
                player.goToPosition(player.getPosition() - self.__value, False)
            case "earnMoney":
                player.giveMoney(self.__value)
                nextScreen()
            case "payMoney":
                if player.payBank(self.__value):
                    nextScreen()
            case "earnFromPlayers":
                allCanPay = True
                for opponent in self.__game.getPlayers():
                    if opponent != player:
                        allCanPay = allCanPay and opponent.payPlayer(player, self.__value)      # Wenn ein Spieler nicht zahlen kann, ergibt die UND Verknüpfung False
                if allCanPay:
                    nextScreen()
            case "payPlayers":
                canPayAll = True
                for opponent in self.__game.getPlayers():
                    if opponent != player:
                        canPayAll = canPayAll and player.payPlayer(opponent, self.__value)      # Wenn ein Spieler nicht zahlen kann, ergibt die UND Verknüpfung False
                if canPayAll:
                    nextScreen()
    
    def __moveToNearest(self, player, type: str):   # Methode befindet sich nicht in der Klasse Player, da sie nur als Aktion der Aktionskarten gebraucht wird
        """
        Ermittelt das nächstliegende Feld eines bestimmten Typen und bewegt Spieler dort hin.
        """
        pos = player.getPosition()
        while  self.__game.getGameBoard()[pos].getType() != type:
            pos = (pos + 1) % len(self.__game.getGameBoard())
        player.goToPosition(pos)
    
    def getText(self) -> str:
        return self.__text
    
    def getType(self) -> str:
        return self.__type