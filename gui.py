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
SCREEN_BUYOPTION = 'buy-property'
SCREEN_OWNPROPERTY = 'own-property'
SCREEN_CARD = 'draw-card'
SCREEN_FREEPARKING = 'free-parking'
SCREEN_TAXES = 'taxes'
SCREEN_GOTOPRISON = 'go-to-prison'
SCREEN_CONTINUE = 'continue'
SCREEN_MANAGEMENT = 'player-management'
SCREEN_BANCRUPTCY = 'player-can-not-pay'
SCREEN_PRISON = "player-in-prison"
SCREEN_PRISONESCAPED = "escaped-prison"
SCREEN_FAILEDPRISONESCAPE = "failed-to-escape-prison"
SCREEN_TRADE = "trading"
SCREEN_WIN = "win"

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
    def __init__(self, text='', textFunction=None, useContainerWidth=True, *args, **kwargs):
        super().__init__(text=text, useContainerWidth=useContainerWidth, *args, **kwargs)
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
        Führt die entsprechende Methode aus, wenn das Element angeklickt wird.
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

class Input(createGuiElementClass(pygame_gui.elements.UITextEntryLine)):
    def __init__(self, allowed_characters = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if allowed_characters is not None:
            self.set_allowed_characters(allowed_characters)

class DropDownMenu(createGuiElementClass(pygame_gui.elements.UIDropDownMenu)):
    def __init__(self, onValueSelectionMethod, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__onValueSelectionMethod = onValueSelectionMethod
    
    def executeValueSelection(self, text: str):
        """
        Führt die entsprechende Methode aus, wenn ein Wert selektiert wurde.
        """
        self.__onValueSelectionMethod(text)
        


def setScreen(screen: str):
    """
    Ändert den aktuellen Screen auf den angegebenen.
    """
    global currentScreen
    currentScreen = screen
    drawCurrentScreen(True)

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


def drawCurrentScreen(sizeUpdate: bool = False):
    """
    Zeichnet den aktuellen Screen
    """
    global currentScreen, guiElementList
    
    for element in guiElementList:
        element.updateVisibility()
        if element.isInCurrentScreen():
            if hasattr(element, 'updateElement'):
                element.updateElement()
        #if hasattr(element, 'updatePosition'):         # nicht benutzt
        #    element.updatePosition()
        if sizeUpdate and hasattr(element, 'updateDimensions'):        # es ist notwendig das Update unabhängig der visibilität umzusetzen, da sonst unerwartete Fehler aufgrund der Aktualisierungsreihenfolge auftreten
            element.updateDimensions()

def executeButtonPress(event):
    """
    Sucht Knopf auf den geklickt wurde und führt verknüpfte Methode aus.
    """
    for element in guiElementList:
        if type(element) == Button and event.ui_element == element:
            element.executeClick()

def dropDownMenuSelect(event):
    """
    Sucht Dropdownmenü, dessen Wert Selektiert wurde und führt die verknüpfte Methode aus.
    """
    for element in guiElementList:
        if type(element) == DropDownMenu and event.ui_element == element:
            element.executeValueSelection(event.text)

def getClickedField(clickedPos, game):
    """
    Gibt das Spielfeld zurück, auf das geklickt wurde.
    """
    for square in game.getProperties():
        x = square.getFieldX()
        y = square.getFieldY()
        width = square.getFieldWidth()
        height = square.getFieldHeight()
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
    
    # debug
    Label(  # zeigt den aktuellen Screen an
        relative_rect = pygame.Rect(0, -20, -1, 20),
        textFunction = lambda: f"Debug: {currentScreen}",
        object_id = 'debug',
        anchors = {'bottom': 'bottom'},
        container = guiContainer
    )
    
    playerInfoContainer = Container(    # Container der Spieler Informationen enthält
        relative_rect = pygame.Rect(70, 0, 0, 0),
        useContainerWidth = True,
        screenList = [SCREEN_ROLLDICE, SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_BUYOPTION, SCREEN_OWNPROPERTY, SCREEN_CARD, SCREEN_FREEPARKING, SCREEN_TAXES, SCREEN_GOTOPRISON, SCREEN_CONTINUE, SCREEN_PRISON, SCREEN_PRISONESCAPED, SCREEN_FAILEDPRISONESCAPE, SCREEN_MANAGEMENT, SCREEN_BANCRUPTCY, SCREEN_TRADE],
        object_id = "#playerInfoContainer",
        container = guiContainer
    )
    
    # Spieler Liste
    playerListContainer = Container(    # Container der Liste aller Spieler enthält
        relative_rect = pygame.Rect(guiContainer.relative_rect.width / 2 - 100, 0, -1, -1),
        screenList = [SCREEN_STARTGAME],
        container = guiContainer
    )
    yOffset = 0
    for player in game.getPlayers():
        Label(      # Label um ungemischte Spielernamen anzuzeigen
            relative_rect = pygame.Rect(0, yOffset, -1, -1),
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
        dimensionsFunction = lambda: (max(400,guiContainer.relative_rect.width-170), -1),
        screenList = [SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_BUYOPTION, SCREEN_OWNPROPERTY, SCREEN_CARD, SCREEN_FREEPARKING, SCREEN_TAXES, SCREEN_GOTOPRISON, SCREEN_CONTINUE, SCREEN_PRISONESCAPED, SCREEN_FAILEDPRISONESCAPE, SCREEN_MANAGEMENT],
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
        visibilityCondition = lambda: not (game.getCurrentPlayer().getPrison() or currentScreen == SCREEN_PRISONESCAPED),      # Spieler ist nicht im Gefängnis
        container = diceResultContainer
    )
    
    squareActionContainer = Container(
        relative_rect = pygame.Rect(70, yOffset + 60, 0, -1),
        dimensionsFunction = lambda: (max(400,guiContainer.relative_rect.width-170), -1),
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
        useContainerWidth = False,
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
        if game.getCurrentPlayer().payBank(amount, False):
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
        setScreen(SCREEN_MANAGEMENT)
    Button(     # Knopf zum Bestätigen, dass der Spieler ins Gefängnis geht.
        relative_rect = pygame.Rect(0, 60, -1, -1),
        text = " Zu Frau Frigge gehen ",
        onClickMethod = goToPrisonButtonMethod,
        screenList = [SCREEN_GOTOPRISON],
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )
    
    # Spieler ist bereits Besitzer, Startfeld, Gefängnis nur zu Besuch
    Button(     # Button mit nächstem Screen fortzufahren
        relative_rect = pygame.Rect(0, 60, -1, -1),
        text = ' Fortfahren ',
        screenList = [SCREEN_OWNPROPERTY, SCREEN_CONTINUE],
        onClickMethod = nextScreen,
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )
    
    # Gefängnis
    Label(
        relative_rect = pygame.Rect(0, 0, 0, -1),
        text = "Du bist bei Frau Frigge. Versuche einen Pasch zu würfeln oder besteche sie um zu entkommen.",
        screenList = [SCREEN_PRISON],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    Label(
        relative_rect = pygame.Rect(0, 30, 0, -1),
        textFunction = lambda: f"Es verbleiben dir noch {3 - game.getCurrentPlayer().getRoundsInPrison()} Versuche, um einen Pasch zu würfeln, bevor du zahlen musst.",
        screenList = [SCREEN_PRISON],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 60, -1, -1),
        textFunction = lambda: f" Besteche Frau Frigge mit 1000 $ ",
        onClickMethod = lambda: game.getCurrentPlayer().instantPrisonEscape(),
        anchors = {'centerx': 'centerx'},
        screenList = [SCREEN_PRISON],
        visibilityCondition = lambda: 1000 <= game.getCurrentPlayer().getMoney(),
        container = squareActionContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 90, -1, -1),
        text = " Versuche dein Glück, wähle Gambling ",
        onClickMethod = lambda: game.getCurrentPlayer().tryPrisonEscape(),
        screenList = [SCREEN_PRISON],
        visibilityCondition = lambda: (game.getCurrentPlayer().getRoundsInPrison() < 3),
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )
    # aus Gefängnis frei gekommen
    Label(
        relative_rect = pygame.Rect(0, 0, 0, -1),
        text = "Du bist aus dem Gefängnis frei freigekommen.",
        screenList = [SCREEN_PRISONESCAPED],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    # fehlgeschlagener Gefängnis Ausbruchversuch (3 Runden kein Pasch)
    Label(
        relative_rect = pygame.Rect(0, 0, 0, -1),
        text = "Du hast es dreimal nicht geschafft eine Pasch zu würfeln.",
        screenList = [SCREEN_FAILEDPRISONESCAPE],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    Label(
        relative_rect = pygame.Rect(0, 30, 0, -1),
        text = "Zahle 1000 $ und komme aus dem Gefängnis raus.",
        screenList = [SCREEN_FAILEDPRISONESCAPE],
        object_id = "@centerLabel",
        container = squareActionContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 60, -1, -1),
        text = " Zahle 1000 $ ",
        onClickMethod = lambda: game.getCurrentPlayer().instantPrisonEscape(),
        anchors = {'centerx': 'centerx'},
        screenList = [SCREEN_FAILEDPRISONESCAPE],
        container = squareActionContainer
    )
    

    Button(     # Button um mit nächstem Spieler fortzufahren
        relative_rect = pygame.Rect(0, 60, -1, -1),
        text = ' Mit nächstem Spieler Fortfahren ',
        screenList = [SCREEN_PRISONESCAPED, SCREEN_MANAGEMENT],
        onClickMethod = lambda: game.nextPlayersTurn(),
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )
    
    def openTradeMenu():
        """
        Initialisiert und öffnet das Handelsmenu.
        """
        game.selectPlayerForTrade(0, game.getCurrentPlayer())     # Wählt aktuellen Spieler als ersten Handelspartner 
        
        players = game.getPlayers()
        playerNames = [player.getName() for player in players]
        filteredPlayers = list(filter(lambda player: (player != game.getCurrentPlayer()) and not player.getBankrupt(), players))    # Spieler ist nicht der erste Handelspartner und nicht bankrott
        filteredPlayerNames = [player.getName() for player in filteredPlayers]
        
        tradePlayerDropDown.remove_options(playerNames)         # Entfernen aller Optionen
        tradePlayerDropDown.add_options(filteredPlayerNames)    # Hinzufügen der neuen Optionen
        tradePlayerDropDown.selected_option = ("","")
        
        setScreen(SCREEN_TRADE)
    Button(     # Button um Handel mit anderem Spieler auszuführen
        relative_rect = pygame.Rect(0, 90, -1, -1),
        text = ' Mit anderem Spieler handeln ',
        screenList = [SCREEN_PRISONESCAPED, SCREEN_MANAGEMENT],
        onClickMethod = openTradeMenu,
        visibilityCondition = lambda: not game.getCurrentPlayer().getBankrupt(),
        anchors = {'centerx': 'centerx'},
        container = squareActionContainer
    )


    # Bankrott
    bankruptcyContainer = Container (       # Container der Würfelergebnis und neues Feld anzeigt
        relative_rect = pygame.Rect(70, yOffset, 0, -1),
        dimensionsFunction = lambda: (max(400,guiContainer.relative_rect.width-170), -1),
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
        onClickMethod = lambda: game.getCurrentPlayer().executeBankruptcy(game.getBankruptcyData()["target"]),
        anchors = {'centerx': 'centerx'},
        container = bankruptcyContainer
    )


    # Handelsmenu
    tradeContainer = Container (        # Container, der alle Elemente zum Handeln enthält
        relative_rect = pygame.Rect(70, yOffset, 0, -1),
        dimensionsFunction = lambda: (max(500,guiContainer.relative_rect.width-170), -1),
        screenList = [SCREEN_TRADE],
        container = guiContainer
    )
    
    tradeLeftPlayerContainer = Container(       # Container für ersten Handelspartner (Initiator des Handels)
        relative_rect = pygame.Rect(0, 0, 200, -1),
        container = tradeContainer
    )
    Label(
        relative_rect = pygame.Rect(0,0,-1,-1),
        textFunction = lambda: game.getCurrentPlayer().getName(),
        container = tradeLeftPlayerContainer
    )
    
    tradeCenterContainer = Container(       # Container für die Knöpfe in der Mitte zwischen den Handelspartnern
        relative_rect = pygame.Rect(210, 10, 80, -1),
        container = tradeContainer
    )
    Button(     # Knopf um Handel durchzuführen
        relative_rect = pygame.Rect(0,0,-1,-1),
        text = " Handel ",
        onClickMethod = game.trade,
        visibilityCondition = lambda: not None in game.getTradeData(),      # ausgeblendet, wenn nicht beide Spieler selektiert wurden
        anchors = {"centerx": "centerx"},
        container = tradeCenterContainer
    )
    Button(     # Knopf um Handel abzubrechen
        relative_rect = pygame.Rect(0,30,-1,-1),
        text = " Abbruch ",
        onClickMethod = game.resetTrade,
        anchors = {"centerx": "centerx"},
        container = tradeCenterContainer
    )
    
    tradeRightPlayerContainer = Container(      # Container für zweiten Handelspartner
        relative_rect = pygame.Rect(300, 0, 200, -1),
        container = tradeContainer
    )
    def selectTradePartner(playerName: str):
        """
        Sucht das Player-Objekt abhängig vom Namen und selektiert den Handelspartner.
        """
        if playerName == "":
            game.selectPlayerForTrade(1, "")
        else:
            players = game.getPlayers()
            playerNames = [player.getName() for player in players]
            player = players[playerNames.index(playerName)]
            game.selectPlayerForTrade(1, player)
    tradePlayerDropDown = DropDownMenu(     # Auswahl Dropdownmenü für Handelspartner
        relative_rect = pygame.Rect(0,0,200,30),
        options_list = [""],            # leere Zeichenkette muss als Standard-Auswahloption existieren, um grafische Fehler zu VErmeiden
        starting_option = "",
        expansion_height_limit = 1000,
        onValueSelectionMethod = selectTradePartner,
        container = tradeRightPlayerContainer
    )

    def tradePropertyLabelTextFunction(propertyIndex: int, side: int) -> str:
        """
        Ermittelt den Textinhalt der Label für die Anzeige der selektierten Grundstücke für das Handeln
        """
        tradeSideData = game.getTradeData()[side]
        if tradeSideData is None or propertyIndex >= len(tradeSideData["properties"]):
            return ""
        else:
            return "- " + tradeSideData["properties"][propertyIndex].getName()
    
    for side in range(2):       # Wiederholung für beide Seiten
        sideContainer = tradeLeftPlayerContainer if side == 0 else tradeRightPlayerContainer
        tradeMoneyContainer = Container(        # Container um Geld hinzuzufügen und anzuzeigen
            relative_rect = pygame.Rect(0,40,-1,-1),
            visibilityCondition = lambda side=side: game.getTradeData()[side] is not None,
            container = sideContainer
        )
        moneyInput = Input(      # Eingabe für Geldbetrag, der dem Handel hinzugefügt werden soll
            relative_rect = pygame.Rect(0,0,150,25),
            initial_text = "0",
            allowed_characters = "numbers",
            container = tradeMoneyContainer
        )
        Button(     # Knopf um Geld zum Handel hinzuzufügen
            relative_rect = pygame.Rect(0,30,-1,-1),
            text = " Geld hinzufügen ",
            onClickMethod = lambda side=side, moneyInput=moneyInput: game.addTradeMoney(side, int(moneyInput.get_text())),
            container = tradeMoneyContainer
        )
        Label(
            relative_rect = pygame.Rect(0,60,-1,-1),
            textFunction = lambda side=side: f"Geld: {game.getTradeData()[side]["money"] if game.getTradeData()[side] is not None else ""} $",
            container = tradeMoneyContainer
        )
        
        for i in range(len(game.getProperties())):
            Label(      # Label für Grundstücke, die zum Handeln ausgewählt wurden
                relative_rect = pygame.Rect(10, 130 + 25 * i, -1, -1),
                textFunction = lambda i=i: tradePropertyLabelTextFunction(i, 0),
                visibilityCondition = lambda i=i, side=side: (game.getTradeData()[side] is not None and i < len(game.getTradeData()[side]["properties"])),
                container = sideContainer
            )


    propertyTradeActionContainer = Container(       # Container für die Knöpfe um Grundstück zu Handel hinzuzufügen oder zu entfernen.
        relative_rect = pygame.Rect(-200,380,200,-1),
        screenList = [SCREEN_TRADE],
        anchors = {"right": "right"},
        container = guiContainer
    )
    Button(     # Knopf um Grundstück zum Handel hinzuzufügen.
        relative_rect = pygame.Rect(0,0,-1,-1),
        text = " Zum Handel hinzufügen ",
        onClickMethod = game.addPropertyToTrade,
        visibilityCondition = game.canPropertyBeAddedToTrade,
        anchors = {"centerx": "centerx"},
        container = propertyTradeActionContainer
    )
    Button(     # Knopf um Grundstück aus Handel zu entfernen.
        relative_rect = pygame.Rect(0,0,-1,-1),
        text = " Aus Handel entfernen ",
        onClickMethod = game.removePropertyFromTrade,
        visibilityCondition = game.isPropertyInTrade,
        anchors = {"centerx": "centerx"},
        container = propertyTradeActionContainer
    )
    
    
    # Gewinner
    winContainer = Container(
        relative_rect = pygame.Rect(70, 100, 0, -1),
        dimensionsFunction = lambda: (max(500,guiContainer.relative_rect.width-170), -1),
        screenList = [SCREEN_WIN],
        container = guiContainer
    )
    Label(
        relative_rect = pygame.Rect(0,0,400,-1),
        textFunction = lambda: f"{game.getWinner().getName()} hat das Spiel gewonnen",
        object_id = "@centerBigLabel",
        container = winContainer
    )
    Button(     # Knopf um Applikation zu schließen
        relative_rect = pygame.Rect(0,50,-1,-1),
        text = " Spiel beenden ",
        onClickMethod = lambda: pygame.event.post(pygame.event.Event(pygame.QUIT)),     # Löst das pygame.QUIT Ereignis aus, um das Fenster zu schließen
        anchors = {"centerx": "centerx"},
        container = winContainer
    )
    

    def initSelectedPropertyCard():
        """
        Erstellt die Besitzrechtskartenelemente.
        """
        propertyCardContainer = Container(      # Zeigt selektiertes Grundstück an
            relative_rect = pygame.Rect(-200, 10, 200, -1),
            screenList = [SCREEN_ROLLDICE, SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_BUYOPTION, SCREEN_OWNPROPERTY, SCREEN_CARD, SCREEN_FREEPARKING, SCREEN_TAXES, SCREEN_GOTOPRISON, SCREEN_CONTINUE, SCREEN_PRISON, SCREEN_PRISONESCAPED, SCREEN_FAILEDPRISONESCAPE, SCREEN_MANAGEMENT, SCREEN_BANCRUPTCY, SCREEN_TRADE],
            visibilityCondition = lambda: not game.getSelectedProperty() is None,
            anchors = {"right": "right"},
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
                                          game.getSelectedProperty().getOwner() in [game.getCurrentPlayer(), game.getBankruptcyData()["player"]] and        # Besitzer ist aktueller Spieler oder Bankrott
                                          not game.isPropertyInTrade()),        # Grundstück befindet sich nicht in Handelsauswahl. Verhindert, dass Spieler Grundstücke mit Häusern handeln kann
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
                container = playerInfoContainer
            )
            
            Label(      # Zeigt an ob Spieler am Zug ist
                relative_rect = pygame.Rect(-65, 0, -1, -1),
                textFunction = lambda player=player: '>' if player == game.getCurrentPlayer() else '',
                container = playerContainer
            )
            Image(      # Zeigt Spielersymbol an
                relative_rect = pygame.Rect(-53, -15, 50, 50),
                image_surface = pygame.image.load(f"images/playerSymbols/{player.getSymbol()}.png").convert_alpha(),
                container = playerContainer,
            )
            Label(      # Zeigt Spieler Name (und Position) an
                relative_rect = pygame.Rect(0, 0, -1, -1),
                textFunction = lambda player=player: f"{player.getName()}: Pos {player.getPosition()}{" - bei Frau Frigge" if player.getPrison() else ""}",
                container = playerContainer,
            )
            Label(      # Zeigt Geld / bankrott an
                relative_rect = pygame.Rect(5, 20, -1, -1),
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
