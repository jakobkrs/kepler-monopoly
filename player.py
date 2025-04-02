import random
import Square 
class Player():
    def __init__(self,game):
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
        self.__game=game

    def startTurn(self):
        if self.__bankrupt:
            self.__game.nextPlayersTurn()
        else:
            num1,num2,num=self.rollDice()
            if num1 != num2:
                self.__position+=num
                #sonstige Spieler-Aktionen
                self.__game.nextPlayersTurn()
            else:
                self.__position+=num
                #sonstige Spieler-Aktionen
                self.turn
                
            

    def goToPrison(self):
        """
        gehe ins Gefängnis
        """
        self.__prison=True
        self.__position=0 
        self.__game.nextPlayersTurn()

    def turn(self):
        """
        Durchlauf nach Pasch
        """
        num1,num2,num=self.rollDice()
        if num1 != num2:
            self.__position+=num
            #sonstige Spieler-Aktionen
            self.__game.nextPlayersTurn()
        else:
            self.__position+=num
            #sonstige Spieler-Aktionen
            self.turn2

    def turn2(self):
        """
        Durschlauf nach 2.Pasch
        """
        num1,num2,num=self.rollDice()
        if num1 != num2:
            self.__position+=num
            #sonstige Spieler-Aktionen
            self.__game.nextPlayersTurn()
        else:
            self.goToPrison

 
    def rollDice():
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend addieren
        """
        num1= random.randint(1,6)
        num2= random.randint(1,6)
        num=num1+num2
        return num1,num2,num

    


                


        
