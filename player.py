import random
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
        self.__doubleCount=0
        self.__game=game

    def startTurn(self):
        if self.__bankrupt:
            self.__game.nextPlayersTurn()
        else:
            doubleCheck=self.doubleCheck
            doubleCount=0
            num1,num2,num=self.rollDice()
            if doubleCheck=false:
                self.__position+=num
                #sonstige Spieler-Aktionen
            elif doubleCheck=true:
                doubleCount+=1
                if doubleCount==3:
                    self.__prison=True
                    self.__position=0 
                else:
                self.__position+=num
                #sonstige Spieler-Aktionen
                #Arbeit an würfeln
                
            else:
                self.__game.nextPlayersTurn()


    def rollDice():
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend addieren
        """
        num1= random.randint(1,6)
        num2= random.randint(1,6)
        num=num1+num2
        return num1,num2,num

    

    def doubleCheck(self):
        """
        checkt, ob Pasch
        """
        #Variablen noch ändern
        num1,num2,num=self.rollDice()
        if num1==num2:
            self.__doubleCount=True
        else:
            self.__doubleCount=False      
        return self.__doubleCount   


                


        
