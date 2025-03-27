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
            # sonstige Spieler-Aktionen
            position=self.move()
            self.__position=position


            self.__game.nextPlayersTurn()


    def rollDice():
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend addieren
        """
        num1= random.randint(1,6)
        num2= random.randint(1,6)
        num=num1+num2
        return num1,num2,num

    def move(self):
        """
        bewegt Spieler um die gewürfelte Zahl, wenn er nicht im Gefängnis ist
        """
        if self.__prison==False:
            num1,num2,num=self.rollDice()
            self.__position+= num
        return self.__position

    def double(self):
        """
        erneutes Würfeln bei Pasch; bei 3* Pasch in Folge in Knast
        """
        num1,num2,num=self.rollDice()
        if self.__prison==False:
            if num1==num2:
                self.__doubleCount+=1
                if self.__doubleCount==3:
                    self.__prison=True
                    self.__position=0               #Position des Gefängnisses muss noch eingefügt werden
                self.rollDice()
            else:
                self.__doubleCount=0


                


        
