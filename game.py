class Game():
    def __init__(self):
        """
        Initialisation of the Game class. Set start values of class instance.
        """
        self.__currentPlayer = 0
        self.__playerCount = 0
        self.__playerOrder = []             # add shuffling mechanic !later
        self.__players = []                 # list of object from class Player
        self.__gameBoard = []
        self.__communityCrads = []
        self.__eventCards = []

        

    

    def __addPlayer(self, player: Player):
        self.__players.append(player)
        self.__playerCount += 1
        self.__playerOrder.append(self.__playerCount - 1)

    def __shufflePlayerOrder(self): #WIP !later
        pass

    def __loadCSV():    #added !later by other teammember
        pass

    def __trade(self):
        pass


