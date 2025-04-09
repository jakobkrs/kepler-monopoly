import random
from square import * 
from property import *
class Player():
    def __init__(self,game):
        """
        Konstruktoraufruf für Playerklasse
        """
        self.__name=[]
        self.__money=0                          #wird noch geändert auf Startkapital
        self.__properties=property
        self.__position=0
        self.__currentSquare=game.getGameBoard()[self.__position] 
        self.__prison=False
        self.__prisoncardCommunity=False
        self.__prisoncardEvent=False
        self.__bankrupt=False
        self.__game=game

    def startTurn(self):
        if self.__bankrupt:
            self.__game.nextPlayersTurn()
        else:
            self.__doubleCount = 0
            self.turn()
                
            

    def goToPrison(self):
        """
        gehe ins Gefängnis
        """
        self.__prison=True
        self.goToPosition(10)
        self.__game.nextPlayersTurn()

    def turn(self):
        """
        Einmal würfeln
        """
        num1,num2,num=self.rollDice()

        if num1 != num2 and self.__doubleCount >= 2:
            self.goToPrison()
            return
        
        self.goToPosition(self.__position+num)
        #miete und sonstiges
        
        if num1 != num2:
            self.__game.nextPlayersTurn()
        else:
            self.__doubleCount += 1
            self.turn

    def goToPosition(self, position):
        """
        setzt Spieler auf richtige Position
        """
        self.__position=position
        self.__currentSquare=game.getGameBoard()[self.__position]

 
    def rollDice():
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend addieren
        """
        num1= random.randint(1,6)
        num2= random.randint(1,6)
        num=num1+num2
        return num1,num2,num

    


                


        
