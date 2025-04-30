import pygame
import pygame_gui

managerInstance = None
guiContainer = None
currentScreen = ''
nextScreens = []
SCREEN_STARTGAME = 'start-game'
SCREEN_ROLLDICE = 'roll-dice'
SCREEN_ROLLDICEAGAIN = 'roll-dice-again'
SCREEN_PAYRENT = 'pay-rent'
SCREEN_BUYOPTION = 'player-can-buy-property'
SCREEN_OWNPROPERTY = 'own-property'
SCREEN_CARD = 'draw-card'
SCREEN_FREEPARKING = 'free-parking'
SCREEN_TAXES = 'taxes'
SCREEN_GOTOPRISON = 'go-to-prison'
SCREEN_PLAYERMANAGMENT = 'player-management'
SCREEN_CONTINUE = 'player-continue-with-management'
SCREEN_BANCRUPTCY = 'player-can-not-pay'
SCREEN_PRISON = "player-in-prison"

class BaseGuiElement:
    def __init__ (self: pygame_gui.elements, screenList: list[str], visibilityCondition, useContainerWidth: bool, positionFunction, dimensionsFunction):
        """
        Die Konstruktor Methode der Grundlegenden GUI-Element-Klasse
        """
        self.__screenList = screenList
        self.__visibilityCondition = visibilityCondition
        if not positionFunction is None:
            self.updatePosition = lambda: updatePosition(positionFunction)
        if useContainerWidth or not dimensionsFunction is None:
            self.updateDimensions = lambda: updateDimensions(dimensionsFunction, useContainerWidth)
        
        guiElementList.append(self)
        
        def updatePosition(positionFunction):
            """
            Methode die Abhängig von der Positionsfunktion die neuen Position berechnet und setzt 
            """
            position = self.relative_rect.topleft
            if not positionFunction is None:
                values = positionFunction()
                position = (values[0] if values[0] >= 0 else position[0], values[1] if values[1] >= 0 else position[1])
            self.set_position(position)
        
        def updateDimensions(dimensionsFunction, useContainerWidth):
            """
            Methode die Abhängig von den Parametern die neuen Dimensionen berechnet und setzt 
            """
            dimensions = self.relative_rect.size
            if not dimensionsFunction is None:
                values = dimensionsFunction()
                dimensions = (values[0] if values[0] >= 0 else dimensions[0], values[1] if values[1] >= 0 else dimensions[1])
            if useContainerWidth:
                dimensions = (self.ui_container.relative_rect.width, dimensions[1])
            self.set_dimensions(dimensions)
            self.relative_rect.width    # maybe update
            
    
    def updateVisibility(self):
        """
        Aktualisiert die Visibilität eines Elements abhängig vom aktuellen Screen
        """
        if self.isInCurrentScreen() and self.__visibilityCondition():          # Element ist sichtbar, wenn es beim aktuellen screen sichtbar sein soll und die zusätzliche Bedingung (standard True) wahr ist
            self.show()
        else:
            self.hide()
    
    def isInCurrentScreen(self):
        """
        Gibt Wahrheitwert zurück, ob Element beim aktuellen Screen enthalten ist.
        """
        global currentScreen
        a = currentScreen in self.__screenList                          # Element soll bei aktuellem Screen direkt gezeigt werden
        b = '*' in self.__screenList and self.ui_container.visible      # '*' ist eine Wildcard. Element wird immer angezeigt, wenn Container angezeigt wird
        return a or b

def createGuiElementClass(pygameGuiElementClass):
    """
    Erstellt eine neue Klasse, die eine pygame_gui.element-Klasse und die BaseGuiElement Klasse kombiniert.
    """
    global managerInstance
    class GuiElement(pygameGuiElementClass, BaseGuiElement):
        def __init__(self, screenList = ['*'], manager=managerInstance, visibilityCondition = lambda: True, useContainerWidth = False, positionFunction = None, dimensionsFunction = None, *args, **kwargs):
            pygameGuiElementClass.__init__(self, manager=manager, *args, **kwargs)
            BaseGuiElement.__init__(self, screenList, visibilityCondition, useContainerWidth, positionFunction, dimensionsFunction)
    return GuiElement

# definieren der speziellen guiElementKlassen
class Label(createGuiElementClass(pygame_gui.elements.UILabel)):
    def __init__(self, text='', textFunction=None, *args, **kwargs):
        super().__init__(text=text, *args, **kwargs)
        if not textFunction is None:
            self.updateElement = lambda: self.set_text(str(textFunction()))

class Button(createGuiElementClass(pygame_gui.elements.UIButton)):
    def __init__(self, onClickMethod, text='', textFunction=None, *args, **kwargs):
        super().__init__(text=text, *args, **kwargs)
        self.__onCLickMethod = onClickMethod
        if not textFunction is None:
            self.updateElement = lambda: self.set_text(str(textFunction()))
    
    def executeClick(self):
        """
        Führt die entsprechende Methode aus, wenn das Element angclickt wird.
        """
        self.__onCLickMethod()

class Container(createGuiElementClass(pygame_gui.elements.UIAutoResizingContainer)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Panel(createGuiElementClass(pygame_gui.elements.UIPanel)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Image(createGuiElementClass(pygame_gui.elements.UIImage)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def setScreen(screen: str):
    """
    Ändert den aktuellen Screen auf den angegebenen.
    """
    global currentScreen
    currentScreen = screen

def addScreenToQueue(screen: str):
    """
    Fügt Screen in Queue hinzu.
    """
    global nextScreens
    nextScreens.append(screen)

def nextScreen():
    """
    Setzt den Screen auf den nächsten aus der Queue
    """
    global nextScreens
    setScreen(nextScreens.pop(0))


def drawCurrentScreen():
    """
    Zeichnet den aktuellen Screen
    """
    global currentScreen, guiElementList
    
    for element in guiElementList:
        element.updateVisibility()
        if element.isInCurrentScreen():
            if hasattr(element, 'updateElement'):
                element.updateElement()
        if hasattr(element, 'updatePosition'):
            element.updatePosition()
        if hasattr(element, 'updateDimensions'):        # es ist notwendig das Update unabhängig der visibilität umzusetzen, da sonst komische update Reihenfolgen Fehler entstehen
            element.updateDimensions()

def executeButtonPress(event):
    """
    Sucht Knopf auf den geklickt wurde und führt verknüpfte Funktion aus.
    """
    for element in guiElementList:
        if type(element) == Button and event.ui_element == element:
            element.executeClick()

def getClickedField(clickedPos, game):
    """
    Gibt das Spielfeld zurück, auf das geklickt wurde.
    """
    for square in game.getProperties():
        x = square.getFieldCoord("x")
        y = square.getFieldCoord("y")
        width = square.getFieldCoord("width")
        height = square.getFieldCoord("height")
        if x <= clickedPos[0] <= x + width and y <= clickedPos[1] <= y + height:
            return square.getPosition()


def initGUI(manager: pygame_gui.ui_manager, game, container):
    """
    Initialisiert und erstellt alle GUI Elemente und Screens
    """
    global currentScreen, guiElementList, managerInstance, guiContainer
    currentScreen = SCREEN_STARTGAME
    guiElementList = []
    managerInstance = manager
    guiContainer = container    
    
    playerInfoContainer = Container(    # Container der Spieler Informationen enthält
        relative_rect = pygame.Rect(70, 0, 0, 0),
        useContainerWidth = True,
        screenList = [SCREEN_ROLLDICE, SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_BUYOPTION, SCREEN_OWNPROPERTY, SCREEN_CARD, SCREEN_FREEPARKING, SCREEN_TAXES, SCREEN_GOTOPRISON, SCREEN_CONTINUE, SCREEN_PLAYERMANAGMENT, SCREEN_BANCRUPTCY],
        object_id = "#playerInfoContainer",
        container = guiContainer
    )
    
    # Spieler Liste
    playerListContainer = Container(    # Container der Liste aller Spieler enthält
        relative_rect = pygame.Rect(0, 0, 0, 0),
        screenList = [SCREEN_STARTGAME],
        container = guiContainer
    )
    yOffset = 0
    for player in game.getPlayers():
        Label(      # Label um ungemischte Spielernamen anzuzeigen
            relative_rect = pygame.Rect(50, yOffset, playerListContainer.relative_rect.width, -1),
            text = player.getName(),
            screenList = [SCREEN_STARTGAME],
            manager = manager,
            container = playerListContainer,
        )
        yOffset += 25 # Abstand zwischen den Labels
    
    
    def startGameButtonMethod(shufflePlayerOrder=True):
        """
        Startet Spiel und mischt eventuell Spielerreihenfolge.
        """
        game.startGame(shufflePlayerOrder)
        initPlayerInformationContainer()  # Erstellung der Spieler Informationsanzeige
    Button(     # Button zum Spiel starten und ohne die Spielerreihenfolge zu mischen
        relative_rect = pygame.Rect(0, yOffset + 10, -1, -1),
        text = ' Spielstart mit dieser Spielereihenfolge ',
        screenList = [SCREEN_STARTGAME],
        onClickMethod = lambda: startGameButtonMethod(False),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )
    Button(     # Button zum Spiel starten und Spielerreihenfolge mischen
        relative_rect = pygame.Rect(0, yOffset + 40, -1, -1),
        text = ' Spielstart mit gemischter Spielereihenfolge ',
        screenList = [SCREEN_STARTGAME],
        onClickMethod = lambda: startGameButtonMethod(True),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )
    
    yOffset = len(game.getPlayers()) * 140 + 30

    
    diceResultContainer = Container (       # Container der Würfelergebnis und neues Feld anzeigt
        relative_rect = pygame.Rect(70, yOffset, 0, -1),
        dimensionsFunction = lambda: (guiContainer.relative_rect.width-170, -1),
        screenList = [SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_BUYOPTION, SCREEN_OWNPROPERTY, SCREEN_CARD, SCREEN_FREEPARKING, SCREEN_TAXES, SCREEN_GOTOPRISON, SCREEN_CONTINUE],
        container = guiContainer
    )
    def setDiceTextMethod() -> str:
        """
        Gibt den richtigen Text für das Würfel Resultat zurück.
        """
        roll = game.getCurrentPlayer().getLastDiceRoll()
        if len(roll) == 0: return ""
        else: return f"Dein Würfelergebnis: {roll[0]}, {roll[1]}{ ' - Pasch' if roll[0] == roll[1] else ''}"     # f"{chr(roll[0] + 9855)} {chr(roll[1] + 9855)}" Weg mit ⚀⚁⚂⚃⚄⚅ funktionier nicht in Standard-Font
    Label(      # Zeigt Würfelergebnis
        relative_rect = pygame.Rect(0, 0, guiContainer.relative_rect.width, -1),
        useContainerWidth = True,
        textFunction = setDiceTextMethod,
        object_id = "@centerLabel",
        container = diceResultContainer
    )
    Label(      # Zeigt Feld auf dem Spieler gelandet ist.
        relative_rect = pygame.Rect(0, 30, guiContainer.relative_rect.width, -1),
        useContainerWidth = True,
        textFunction = lambda: f"Du bist auf dem Feld {game.getCurrentPlayer().getCurrentSquare().getName()} gelandet.",
        object_id = "@centerLabel",
        container = diceResultContainer
    )
    
    squareActionContainer = Container(
        relative_rect = pygame.Rect(70, yOffset + 60, 0, -1),
        dimensionsFunction = lambda: (guiContainer.relative_rect.width-170, -1),
        container = guiContainer
    )
    Button(     # Button um Würfel Aktion auszulösen
        relative_rect = pygame.Rect(0, 60, -1, -1),
        text = ' Würfeln ',
        onClickMethod = lambda: game.getCurrentPlayer().turn(),
        screenList = [SCREEN_ROLLDICE, SCREEN_ROLLDICEAGAIN],
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )  
    # Miete bezahlen
    Label(      # Label um Grundstücksbesitzer anzuzeigen
        relative_rect = pygame.Rect(0, 0, 0, -1),
        useContainerWidth = True,
        textFunction = lambda: f"Das Grundstück gehört bereits {game.getCurrentPlayer().getCurrentSquare().getOwner().getName()}.",
        screenList = [SCREEN_PAYRENT],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    Label(      # Label um anzuzeigen, falls eine Hypothek auf dem Grundstück lasstet.
        relative_rect = pygame.Rect(0, 20, 0, -1),
        useContainerWidth = True,
        text = "Auf dem Grundstück lastet eine Hypothek.",
        screenList = [SCREEN_PAYRENT],
        visibilityCondition = lambda: game.getCurrentPlayer().getCurrentSquare().getMortgage() ,
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    Button(     # Knopf zum bezahlen der Miete
        relative_rect = pygame.Rect(0, 60, -1, -1),
        textFunction = lambda: f" Miete Bezahlen {game.getCurrentPlayer().getCurrentSquare().getRent()} $ ",
        onClickMethod = lambda: game.getCurrentPlayer().getCurrentSquare().payRent(game.getCurrentPlayer()),
        screenList = [SCREEN_PAYRENT],
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )
    # Spieler ist bereits Besitzer
    Label(      # Label um Grundstücksbesitzer anzuzeigen
        relative_rect = pygame.Rect(0, 0, 0, -1),
        useContainerWidth = True,
        text = "Das Grundstück gehört dir.",
        screenList = [SCREEN_OWNPROPERTY],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
     # Als Knopf wird der Standard "Fortfahren"-Knopf verwendet
    # Grundstück kaufen
    Label(
        relative_rect = pygame.Rect(0, 0, guiContainer.relative_rect.width, -1),
        useContainerWidth = True,
        textFunction = lambda: f"Dieses Grundstück gehört noch niemanden.",
        screenList = [SCREEN_BUYOPTION],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 60, -1, -1),
        textFunction = lambda: f" Grundstück kaufen {game.getCurrentPlayer().getCurrentSquare().getCost()} $ ",
        onClickMethod = lambda: game.getCurrentPlayer().buyProperty(game.getCurrentPlayer().getCurrentSquare()),
        anchors = {'centerx': 'centerx'},
        screenList = [SCREEN_BUYOPTION],
        visibilityCondition = lambda: game.getCurrentPlayer().getCurrentSquare().getCost() <= game.getCurrentPlayer().getMoney(),
        container = squareActionContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 90, -1, -1),
        text = ' Grundstück nicht kaufen ',
        onClickMethod = nextScreen,
        anchors = {'centerx': 'centerx'},
        screenList = [SCREEN_BUYOPTION],
        container = squareActionContainer
    )

    cardPanel = Panel(   # Panel um gezogene Karte anzuzeigen
        relative_rect = pygame.Rect(0, 60, 400, 160),
        screenList = [SCREEN_CARD],
        anchors = {'centerx': 'centerx'},
        object_id = "#cardPanel",
        container = squareActionContainer
    )
    Label(      # Zeigt Typ der Karte
        relative_rect = pygame.Rect(0, 0, cardPanel.relative_rect.width, -1),
        textFunction = lambda: f"{'Gemeinschafts' if game.getLastDrawnCard()['type'] == 'community' else 'Ereignis'}karte",
        object_id = "@centerLabel",
        container = cardPanel
    )
    Label(      # Text der Karte
        relative_rect = pygame.Rect(0, 30, cardPanel.relative_rect.width, -1),
        textFunction = lambda: game.getLastDrawnCard()["text"],
        object_id = "@centerLabel",
        container = cardPanel
    )
    Button(     # Button um Karte auszuführen
        relative_rect = pygame.Rect(0, 120, -1, -1),
        screenList = [SCREEN_CARD],
        text = ' Ausführen ',
        onClickMethod = lambda: game.getCurrentPlayer().getCurrentSquare().executeCard(),
        anchors = {'centerx': 'centerx'},
        container = cardPanel
    )
    
    # Frei Parken
    Label(
        relative_rect = pygame.Rect(0, 0, guiContainer.relative_rect.width, -1),
        useContainerWidth = True,
        textFunction = lambda: f"Auf Frei Parken liegen {game.getFreeParkingMoney()} $.",
        screenList = [SCREEN_FREEPARKING],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    def freeParkingButtonMethod():
        """
        Gibt Spieler Frei Parken Geld und fährt mit nächstem Screen fort. 
        """
        game.getCurrentPlayer().giveMoney(game.resetFreeParkingMoney())     # Seit Frei Parken Geld auf 0 zurück gibt den Betrag dem Spieler
        nextScreen()
    Button(     # Knopf zum Einsammeln des Frei Parken Geldes
        relative_rect = pygame.Rect(0, 60, -1, -1),
        textFunction = lambda: f" Geld Annehmen {game.getFreeParkingMoney()} $ ",
        onClickMethod = freeParkingButtonMethod,
        screenList = [SCREEN_FREEPARKING],
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )
    
    # Steuern
    def taxesButtonMethod():
        """
        Lässt Spieler Steuern bezahlen und fährt mit nächstem Screen fort.
        """
        if game.getCurrentPlayer().getCurrentSquare().getType() == "taxes1":  amount = 4000
        else: amount = 2000
        game.getCurrentPlayer().payBank(amount, False)
        nextScreen()
    Button(     # Knopf zum Bezahlen der Steuern
        relative_rect = pygame.Rect(0, 60, -1, -1),
        textFunction = lambda: f" Zahlung durchführen {4000 if game.getCurrentPlayer().getCurrentSquare().getType() == "taxes1" else 2000} $ ",
        onClickMethod = taxesButtonMethod,
        screenList = [SCREEN_TAXES],
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )
    
    # Gehe ins Gefängnis
    def goToPrisonButtonMethod():
        """
        Setzt den aktuellen Spieler ins Gefängnis und bricht dessen laufenden Zug ab.
        """
        game.getCurrentPlayer().goToPrison()
        setScreen(SCREEN_CONTINUE)
    Button(     # Knopf zum Bestätigen, dass der Spieler ins Gefängnis geht.
        relative_rect = pygame.Rect(0, 60, -1, -1),
        text = " Zu Frau Frigge gehen ",
        onClickMethod = goToPrisonButtonMethod,
        screenList = [SCREEN_GOTOPRISON],
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )
    

    Button(     # Button um mit nächstem Spieler fortzufahren
        relative_rect = pygame.Rect(0, 60, -1, -1),
        text = ' Fortfahren ',
        screenList = [SCREEN_OWNPROPERTY, SCREEN_CONTINUE],
        onClickMethod = lambda: game.nextPlayersTurn(),
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )


    # Bankrott
    bankruptcyContainer = Container (       # Container der Würfelergebnis und neues Feld anzeigt
        relative_rect = pygame.Rect(70, yOffset, 0, -1),
        dimensionsFunction = lambda: (guiContainer.relative_rect.width-170, -1),
        screenList = [SCREEN_BANCRUPTCY],
        container = guiContainer
    )
    Label(
        relative_rect = pygame.Rect(0, 0, 0, -1),
        useContainerWidth = True,
        textFunction = lambda: f"Du musst {game.getBankruptcyData()["amount"]} $ zahlen, doch hast zu wenig Geld.",
        object_id = "@centerLabel",
        container = bankruptcyContainer
    )
    Label(
        relative_rect = pygame.Rect(0, 30, 0, -1),
        useContainerWidth = True,
        text = "Verkaufe Häuser oder nehme Hypotheken auf um das Geld aufzubringen.",
        object_id = "@centerLabel",
        container = bankruptcyContainer
    )
    def payDebtButtonMethod():
        """
        Bezahlt die Schulden des Spielers.
        """
        data = game.getBankruptcyData()
        if data["target"] == 0:                # Geld wird Bank geschuldet
            data["player"].payBank(True)
        else:
            data["player"].payPlayer(data["target"])
        nextScreen()
    Button(
        relative_rect = pygame.Rect(0, 60, -1, -1),
        textFunction = lambda: f" Schulden bezahlen {game.getBankruptcyData()["amount"]} $ ",
        onClickMethod = payDebtButtonMethod,
        anchors = {'centerx': 'centerx'},
        visibilityCondition = lambda: game.getBankruptcyData()["amount"] <= game.getCurrentPlayer().getMoney(),
        container = bankruptcyContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 90, -1, -1),
        text = ' Bankrott ',
        onClickMethod = lambda: (),
        anchors = {'centerx': 'centerx'},
        container = bankruptcyContainer
    )


    def initSelectedPropertyCard():
        """
        Erstellt die Besitzrechtskartenelemente.
        """
        propertyCardContainer = Container(      # Zeigt selektiertes Grundstück an
            relative_rect = pygame.Rect(450, 10, 200, -1),
            #positionFunction = lambda: (guiContainer.relative_rect.width - 200, -1),
            screenList = [SCREEN_ROLLDICE, SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_BUYOPTION, SCREEN_OWNPROPERTY, SCREEN_CARD, SCREEN_FREEPARKING, SCREEN_TAXES, SCREEN_GOTOPRISON, SCREEN_CONTINUE, SCREEN_PLAYERMANAGMENT, SCREEN_BANCRUPTCY],
            visibilityCondition = lambda: not game.getSelectedProperty() is None,
            container = guiContainer
        )
        for group in ["A","B","C","D","E","F","G","H","SP","TS"]:
            namePanel = Panel(      # Hintergrund der Leiste des selektierten Grundstücks
                relative_rect = pygame.Rect(0, 0, 200, 50),
                object_id = f"#group{group}",
                visibilityCondition = lambda group=group: not game.getSelectedProperty() is None and game.getSelectedProperty().getGroup() == group,
                container = propertyCardContainer
            )
            Label(
                relative_rect = pygame.Rect(0,0,namePanel.relative_rect.width,50),
                textFunction = lambda: game.getSelectedProperty().getName(),
                object_id = pygame_gui.core.ObjectID(class_id='@centerLabel', object_id = f"#group{group}"),
                container = namePanel
            )
        propertyCardBottomPanel = Panel(      # Hintergrund der Daten des Selektierten Grundstücks
            relative_rect = pygame.Rect(0, 50-5, 200, 310),
            object_id = "@whitePanel",
            container = propertyCardContainer
        )
        Label(      # Grundstückswert
            relative_rect = pygame.Rect(10,10,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"Grundstückswert: {game.getSelectedProperty().getCost()} $",
            container = propertyCardBottomPanel
        )
        Label(      # Hypothekenwert
            relative_rect = pygame.Rect(10,30,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"Hypothekenwert: {int(game.getSelectedProperty().getCost() * 0.5)} $",
            container = propertyCardBottomPanel
        )
        # normalen Property
        propertyRentContainer = Container(      # Container für Mieten einer normalen Property
            relative_rect = pygame.Rect(0,60,namePanel.relative_rect.width-10,210),
            visibilityCondition = lambda: game.getSelectedProperty().getType() == "property",
            container = propertyCardBottomPanel
        )
        Label(      # Basis-Miete
            relative_rect = pygame.Rect(10,0,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"Basis-Miete: {game.getSelectedProperty().getBaseRent()} $",
            container = propertyRentContainer
        )
        Label(      # 1 Haus-Miete
            relative_rect = pygame.Rect(10,20,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"1 Haus: {game.getSelectedProperty().getBaseRent() * 5} $",
            container = propertyRentContainer
        )
        Label(      # 2 Häuser-Miete
            relative_rect = pygame.Rect(10,40,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"2 Häuser: {game.getSelectedProperty().getBaseRent() * 15} $",
            container = propertyRentContainer
        )
        Label(      # 3 Häuser-Miete
            relative_rect = pygame.Rect(10,60,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"3 Häuser: {game.getSelectedProperty().getBaseRent() * 45} $",
            container = propertyRentContainer
        )
        Label(      # 4 Häuser-Miete
            relative_rect = pygame.Rect(10,80,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"4 Häuser: {game.getSelectedProperty().getBaseRent() * 70} $",
            container = propertyRentContainer
        )
        Label(      # Hotel-Miete
            relative_rect = pygame.Rect(10,100,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"   Hotel: {game.getSelectedProperty().getBaseRent() * 100} $",
            container = propertyRentContainer
        )
        propertyHousePanel = Panel(     # Container für Häuseranzahl und Hauskauf
            relative_rect = pygame.Rect(-5, 130-5, namePanel.relative_rect.width+5, 80),
            object_id = "@whitePanel",
            visibilityCondition = lambda: (not game.getSelectedProperty().getOwner() is None and                                            # hat Besitzer
                                        game.getSelectedProperty().getOwner().completeGroup(game.getSelectedProperty().getGroup())),     # Besitzer besitzt alle Grundstücke der Gruppe
            container = propertyRentContainer
        )
        for i in range(6):
            Image(      # Haus-Anzahl-Bider
                relative_rect = pygame.Rect(5, 5, 25 * ((i-1) % 4 + 1), 25),
                image_surface = pygame.image.load(f"images/houses/{i}.png").convert_alpha(),
                visibilityCondition = lambda i=i: game.getSelectedProperty().getHouses() == i,
                container = propertyHousePanel,
            )
        Button(     # Knopf zum Haus bauen
            relative_rect = pygame.Rect(5, 35, -1, 20),
            textFunction = lambda: f" Bauen {game.getSelectedProperty().getHouseCost()} $",
            onClickMethod = lambda: game.getSelectedProperty().buildHouse(),
            visibilityCondition = lambda: (game.getSelectedProperty().isHouseActionPossible(True) and           # Haus Aktion 'Bauen' ist möglich
                                          game.getSelectedProperty().getOwner() in [game.getCurrentPlayer(), game.getBankruptcyData()["player"]]),        # Besitzer ist aktueller Spieler oder Bankrott
            container = propertyHousePanel
        )
        Button(     # Knopf zum Haus verkaufen
            relative_rect = pygame.Rect(5, 55, -1, 20),
            textFunction = lambda: f" Verkaufen {int(game.getSelectedProperty().getHouseCost() * 0.5)} $",
            onClickMethod = lambda: game.getSelectedProperty().sellHouse(),
            visibilityCondition = lambda: (game.getSelectedProperty().isHouseActionPossible(False) and          # Haus Aktion 'Verkaufen' ist möglich
                                          game.getSelectedProperty().getOwner() in [game.getCurrentPlayer(), game.getBankruptcyData()["player"]]),        # Besitzer ist aktueller Spieler oder Bankrott
            container = propertyHousePanel
        )
        # Bahnhof
        trainStationRentContainer = Container(      # Container für Mieten eines Bahnhofs
            relative_rect = pygame.Rect(0,60,namePanel.relative_rect.width-10,-1),
            visibilityCondition = lambda: game.getSelectedProperty().getType() == "trainStation",
            container = propertyCardBottomPanel
        )
        Label(      # "Miete mit..."-Label
            relative_rect = pygame.Rect(10,0,namePanel.relative_rect.width-10,-1),
            text = "Miete mit...",
            container = trainStationRentContainer
        )
        Label(      # 1 Bahnhof-Miete
            relative_rect = pygame.Rect(20,20,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"1 Bahnhof: {game.getSelectedProperty().getBaseRent()} $",
            container = trainStationRentContainer
        )
        Label(      # 2 Bahnhöfe-Miete
            relative_rect = pygame.Rect(20,40,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"2 Bahnhöfen: {game.getSelectedProperty().getBaseRent() * 2} $",
            container = trainStationRentContainer
        )
        Label(      # 3 Bahnhöfe-Miete
            relative_rect = pygame.Rect(20,60,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"3 Bahnhöfen: {game.getSelectedProperty().getBaseRent() * 4} $",
            container = trainStationRentContainer
        )
        Label(      # 4 Bahnhöfe-Miete
            relative_rect = pygame.Rect(20,80,namePanel.relative_rect.width-10,-1),
            textFunction = lambda: f"4 Bahnhöfen: {game.getSelectedProperty().getBaseRent() * 8} $",
            container = trainStationRentContainer
        )
        # Versorgungswerk
        supplyPlantRentContainer = Container(      # Container für Mieten eines Bahnhofs
            relative_rect = pygame.Rect(0,60,namePanel.relative_rect.width-10,-1),
            visibilityCondition = lambda: game.getSelectedProperty().getType() == "supplyPlant",
            container = propertyCardBottomPanel
        )
        Label(      # "Miete mit..."-Label
            relative_rect = pygame.Rect(10,0,namePanel.relative_rect.width-10,-1),
            text = "Miete mit...",
            container = supplyPlantRentContainer
        )
        Label(      # 1 Werk-Miete
            relative_rect = pygame.Rect(20,20,namePanel.relative_rect.width-10,-1),
            text = "1 Werk: 80-fache",
            container = supplyPlantRentContainer
        )
        Label(      # 2 Werke-Miete
            relative_rect = pygame.Rect(20,40,namePanel.relative_rect.width-10,-1),
            text = "2 Werken: 200-fache",
            container = supplyPlantRentContainer
        )
        Label(      # "Augensumme der Würfel"-Label
            relative_rect = pygame.Rect(10,60,namePanel.relative_rect.width-10,-1),
            text = "Augensumme der Würfel",
            container = supplyPlantRentContainer
        )
        
        propertyCardMortgagePanel = Panel(      # Panel mit Hypothek Aktionen
            relative_rect = pygame.Rect(-5, 260, 200+5, 50),
            object_id = "@whitePanel",
            visibilityCondition = lambda: not game.getSelectedProperty().getOwner() is None,
            container = propertyCardBottomPanel
        )
        Label(      # Label für Hypothek Status
            relative_rect = pygame.Rect(10, 0, 200, 20),
            textFunction = lambda: f"Hypothek: {"bestehend" if game.getSelectedProperty().getMortgage() else "nicht bestehend"}",
            container = propertyCardMortgagePanel
        )
        Button(     # Knopf zum Hypothek aufnehmen
            relative_rect = pygame.Rect(10,20,-1,20),
            textFunction = lambda: f" Aufnehmen {int(game.getSelectedProperty().getCost() * 0.5)} $",
            onClickMethod = lambda: game.getSelectedProperty().raiseMortgage(),
            visibilityCondition = lambda: (not game.getSelectedProperty().getMortgage() and                                                         # keine Hypothek aufgenommen
                                        game.getSelectedProperty().groupHouseRange()[1] == 0 and                                                    # keine Häuser in Gruppe
                                        game.getSelectedProperty().getOwner() in [game.getCurrentPlayer(), game.getBankruptcyData()["player"]]),    # Besitzer ist aktueller Spieler oder Bankrott
            container = propertyCardMortgagePanel
        )
        Button(     # Knopf zum Hypothek löschen
            relative_rect = pygame.Rect(10,20,-1,20),
            textFunction = lambda: f" Aufheben {int(game.getSelectedProperty().getCost() * 0.55)} $",
            onClickMethod = lambda: game.getSelectedProperty().cancelMortgage(),
            visibilityCondition = lambda: (game.getSelectedProperty().getMortgage() and                                                                 # Hypothek aufgenommen
                                        game.getSelectedProperty().getOwner().getMoney() >= int(game.getSelectedProperty().getCost() * 0.55) and        # ausreichend Geld
                                        game.getSelectedProperty().getOwner() in [game.getCurrentPlayer(), game.getBankruptcyData()["player"]]),        # Besitzer ist aktueller Spieler oder Bankrott
            container = propertyCardMortgagePanel
        )
    
    initSelectedPropertyCard()      # Erstelle Besitzrechtskarte
    
    def initPlayerInformationContainer():
        """
        Erstellt die Spielerinformations-Elemente
        """
        propertyCardGrid = [                # deklariert an welcher Position welche Grundstückskarte angezeigt werden soll; -1 steht für keine Nutzung des Platzes
            [0,3,6,11,14,18,22,26,2,17],
            [1,4,8,12,15,19,23,27,10,25],
            [-1,5,9,13,16,21,24,-1,7,20]
        ]
        
        for i in game.getPlayerOrder():
            player = game.getPlayers()[i]
            
            playerContainer = Container(      # enthält gesamten Eintrag für einen Spieler
                relative_rect = pygame.Rect(0, 10 + 140 * game.getPlayerOrder().index(i), 0, -1),
                useContainerWidth = True,
                container = playerInfoContainer
            )
            
            Label(      # Zeigt an ob Spieler am Zug ist
                relative_rect = pygame.Rect(-65, 0, 0, -1),
                useContainerWidth = True,
                textFunction = lambda player=player: '>' if player == game.getCurrentPlayer() else '',
                container = playerContainer
            )
            Image(      # Zeigt Spielersymbol an
                relative_rect = pygame.Rect(-53, -15, 50, 50),
                image_surface = pygame.image.load(f"images/playerSymbols/{player.getSymbol()}.png").convert_alpha(),
                container = playerContainer,
            )
            Label(      # Zeigt Spieler Name (und Position) an
                relative_rect = pygame.Rect(0, 0, 0, -1),
                useContainerWidth = True,
                textFunction = lambda player=player: f"{player.getName()}: Pos {player.getPosition()}{" - bei Frau Frigge" if player.getPrison() else ""}",
                container = playerContainer,
            )
            Label(      # Zeigt Geld / bankrott an
                relative_rect = pygame.Rect(5, 20, 0, -1),
                useContainerWidth = True,
                textFunction = lambda player=player: f"{'Bankrott' if player.getBankrupt() else f'Geld: {player.getMoney()} $'}",
                container = playerContainer,
            )
            
            propertyCardContainer = Container(      # Enthält alle Grundstücks-Karten
                relative_rect = pygame.Rect(0, 50, 0, 0),
                useContainerWidth = True,
                container = playerContainer
            )
            for row in range(len(propertyCardGrid)):                
                for col in range(len(propertyCardGrid[row])):
                    id = propertyCardGrid[row][col]
                    property = game.getProperties()[id]
                    if id >= 0:
                        Button(
                            relative_rect = pygame.Rect(col * 35, row * 25, 35, 25),
                            onClickMethod = lambda id=id: game.setSelectedPropertyById(id),
                            visibilityCondition = lambda property = property, player = player: property in player.getProperties(),
                            object_id = f"#group{property.getGroup()}",
                            container = propertyCardContainer
                        )
