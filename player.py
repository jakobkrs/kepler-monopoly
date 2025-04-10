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

    def goToPosition(self, position: int):
        """
        setzt Spieler auf richtige Position
        """
        self.__position=position % len(self.__game.getGameBoard())          # aktualisiere Postion und handelt das überschreiten von Los in der Positions-Variable
        self.__currentSquare=self.__game.getGameBoard()[self.__position]
        # Ergänzung von Code für Überschreiten von LOS notwendig

 
    def rollDice(self):
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend addieren
        """
        num1= random.randint(1,6)
        num2= random.randint(1,6)
        num=num1+num2
        return num1,num2,num

    def completeGroup(self,id: str):
        properties = self.__game.getProperties()

        owners = []

        for property in properties:
            if property.group == id:
                owners.append(property.owner)
        
        return all(x==owners[0] for x in owners)

        
    


                


        
