class Player():
    def __init__(self,name,money,property,position,prison,prisoncard_community,prisoncard_event,bankrupt):
        """
        Konstruktoraufruf für Playerklasse
        """
        self.__name=name
        self.__geld=money
        self.__grundstücke=property
        self.__position=position
        self.__gefängnis=prison
        self.__gefängniskarte_gemein=prisoncard_community
        self.__gefängniskarte_ereignis=prisoncard_event
        self.__insolvent=bankrupt

    def dice(self):
        """
        2 zufählige Zahlen von 1-6 generieren, diese anschließend zu der Position addieren
        """
        
