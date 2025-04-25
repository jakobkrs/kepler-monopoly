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
SCREEN_CARD = 'draw-card'
SCREEN_PLAYERMANAGMENT = 'player-management'
SCREEN_CONTINUE = 'player-continue-with-management'

class BaseGuiElement:
    def __init__ (self: pygame_gui.elements, screenList: list[str], visibilityCondition):
        self.__screenList = screenList
        self.__visibilityCondition = visibilityCondition
        guiElementList.append(self)
    
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
        def __init__(self, screenList = ['*'], manager=managerInstance, visibilityCondition = lambda: True, *args, **kwargs):
            pygameGuiElementClass.__init__(self, manager=manager, *args, **kwargs)
            BaseGuiElement.__init__(self, screenList, visibilityCondition)
    return GuiElement

# definieren der speziellen guiElementKlassen
class Label(createGuiElementClass(pygame_gui.elements.UILabel)):
    def __init__(self, text='', textFunction=None, *args, **kwargs):
        super().__init__(text=text, *args, **kwargs)
        if not textFunction is None:
            self.updateElement = lambda: self.set_text(str(textFunction()))

class Button(createGuiElementClass(pygame_gui.elements.UIButton)):
    def __init__(self, onClickMethod, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__onCLickMethod = onClickMethod
    
    def executeClick(self):
        """
        Führt die entsprechende Methode aus, wenn das Element angclickt wird.
        """
        self.__onCLickMethod()

class Container(createGuiElementClass(pygame_gui.elements.UIAutoResizingContainer)):
    def __init__(self, relative_rect = pygame.Rect(0,0,0,0).copy(), positionFunction = None, *args, **kwargs):
        if not positionFunction is None:
            self.updateElement = lambda: self.set_relative_position(positionFunction())
            rect = pygame.Rect(positionFunction(), (relative_rect[2],relative_rect[3]))
        else:
            rect = relative_rect
        super().__init__(relative_rect = rect, *args, **kwargs)
        

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

def nextScreen() -> str:
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
        if element.isInCurrentScreen() and hasattr(element, 'updateElement'):
            element.updateElement()

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
    Initialisiert alle GUI Elemente und Screens
    """
    global currentScreen, guiElementList, managerInstance
    currentScreen = SCREEN_STARTGAME
    guiElementList = []
    managerInstance = manager
    guiContainer = container    
    
    playerInfoContainer = Container(    # Container der Spieler Informationen enthält
        relative_rect = pygame.Rect(100, 0, guiContainer.relative_rect.width, 0),
        screenList = [SCREEN_ROLLDICE, SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_BUYOPTION, SCREEN_CARD, SCREEN_CONTINUE, SCREEN_PLAYERMANAGMENT],
        object_id = "playerInfoContainer",
        container = guiContainer
    )
    
    # debug
    Label(  # zeigt den aktuellen Screen an
        relative_rect = pygame.Rect(-350, 0, -1, -1),
        textFunction = lambda: f"Debug: {currentScreen}, selectedCard: {'' if game.getSelectedProperty() is None else game.getSelectedProperty().getName()}",
        anchors = {'right': 'right', 'top': 'top'},
        object_id = 'debug',
        container = guiContainer
    )
    
    # Spieler Liste
    playerListContainer = Container(    # Container der Liste aller Spieler enthält
        relative_rect = pygame.Rect(0, 0, 0, 0),
        screenList = [SCREEN_STARTGAME],
        anchors = {'top': 'top'},
        container = guiContainer
    )
    yOffset = 0
    for player in game.getPlayers():
        Label(      # Label um ungemischte Spielernamen anzuzeigen
            relative_rect = pygame.Rect(0, yOffset, container.relative_rect.width, -1),
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
        onClickMethod = lambda state=False: startGameButtonMethod(state),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )
    Button(     # Button zum Spiel starten und Spielerreihenfolge mischen
        relative_rect = pygame.Rect(0, yOffset + 40, -1, -1),
        text = ' Spielstart mit gemischter Spielereihenfolge ',
        screenList = [SCREEN_STARTGAME],
        onClickMethod = lambda state=True: startGameButtonMethod(state),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )
    
    yOffset = 500   # temporary needs to get changed
    
    Button(     # Button um Würfel Aktion auszulösen
        relative_rect = pygame.Rect(10, yOffset + 180, -1, -1),
        text = ' Würfeln ',
        screenList = [SCREEN_ROLLDICE, SCREEN_ROLLDICEAGAIN],
        onClickMethod = lambda: game.getCurrentPlayer().turn(),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )
    
    
    diceResultContainer = Container (   # Container der Würfelergebnis und neues Feld anzeigt
        relative_rect = pygame.Rect(0, yOffset + 50, 0, 0),
        screenList = [SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_CARD, SCREEN_BUYOPTION, SCREEN_CONTINUE],
        anchors = {'centerx': 'centerx', 'top': 'top'},
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
        textFunction = setDiceTextMethod,
        object_id = "centerLabel",
        container = diceResultContainer
    )
    Label(      # Zeigt Feld auf dem Spieler gelandet ist.
        relative_rect = pygame.Rect(0, 30, guiContainer.relative_rect.width, -1),
        textFunction = lambda: f"Du bist auf dem Feld {game.getCurrentPlayer().getCurrentSquare().getName()} gelandet.",
        object_id = "centerLabel",
        container = diceResultContainer
    )
    
    
    payRentContainer = Container(   # Container zum Miete Bezahlen
        relative_rect = pygame.Rect(0, yOffset + 100, 0, 0),
        screenList = [SCREEN_PAYRENT],
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )
    Label(
        relative_rect = pygame.Rect(0, 0, guiContainer.relative_rect.width, -1),
        textFunction = lambda: f"Das Grundstück gehört bereits {game.getCurrentPlayer().getCurrentSquare().getOwner().getName()}. Du musst {game.getCurrentPlayer().getCurrentSquare().getRent()} $ Miete zahlen.",
        object_id = 'centerLabel',
        container = payRentContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 70, -1, -1),
        text = ' Miete Bezahlen ',
        onClickMethod = lambda: game.getCurrentPlayer().getCurrentSquare().payRent(game.getCurrentPlayer()),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = payRentContainer
    )

    buyPropertyContainer = Container(   # Container zum Grundstück kaufen
        relative_rect = pygame.Rect(0, yOffset + 100, 0, 0),
        screenList = [SCREEN_BUYOPTION],
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )
    Label(
        relative_rect = pygame.Rect(0, 0, guiContainer.relative_rect.width, -1),
        textFunction = lambda: f"Dieses Grundstück gehört noch niemanden. Du kannst es für {game.getCurrentPlayer().getCurrentSquare().getCost()} $ kaufen.",
        object_id = "centerLabel",
        container = buyPropertyContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 70, -1, -1),
        text = ' Grundstück kaufen ',
        onClickMethod = lambda: game.getCurrentPlayer().buyProperty(game.getCurrentPlayer().getCurrentSquare()),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = buyPropertyContainer
    )
    Button(
        relative_rect = pygame.Rect(0, 100, -1, -1),
        text = ' Grundstück nicht kaufen ',
        onClickMethod = nextScreen,
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = buyPropertyContainer
    )

    cardPanel = Panel(   # Panel um gezogene Karte anzuzeigen
        relative_rect = pygame.Rect(0, yOffset + 120, 400, 160),
        screenList = [SCREEN_CARD],
        anchors = {'centerx': 'centerx', 'top': 'top'},
        object_id = "cardPanel",
        container = guiContainer
    )
    Label(  # Zeigt Typ der Karte
        relative_rect = pygame.Rect(0, 0, cardPanel.relative_rect.width, -1),
        textFunction = lambda: f"{'Gemeinschafts' if game.getLastDrawnCard()['type'] == 'community' else 'Ereignis'}karte",
        object_id = "centerLabel",
        container = cardPanel
    )
    Label(
        relative_rect = pygame.Rect(0, 30, cardPanel.relative_rect.width, -1),
        textFunction = lambda: game.getLastDrawnCard()["text"],
        object_id = "centerLabel",
        container = cardPanel
    )
    Button(     # Button um Karte auszuführen
        relative_rect = pygame.Rect(0, 120, -1, -1),
        screenList = [SCREEN_CARD],
        text = ' Ausführen ',
        onClickMethod = lambda: game.getCurrentPlayer().getCurrentSquare().executeCard(),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = cardPanel
    )
    
    
    Button(     # Button um mit nächstem Spieler fortzufahren
        relative_rect = pygame.Rect(10, yOffset + 180, -1, -1),
        text = ' Fortfahren ',
        screenList = [SCREEN_CONTINUE],
        onClickMethod = lambda: game.nextPlayersTurn(),
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )

        


    def initPlayerInformationContainer():
        """
        Erstellt die Spielerinformations-Elemente
        """
        propertyCardGrid = [                # deklariert an welcher Position welche Grundstückskarte angezeigt werden soll
            [0,3,6,11,14,18,22,26,2,17],
            [1,4,8,12,15,19,23,27,10,25],
            [-1,5,9,13,16,21,24,-1,7,20]
        ]
        

        for i in game.getPlayerOrder():
            player = game.getPlayers()[i]
            
            playerContainer = Container(      # enthält gesamten Eintrag für einen Spieler
                relative_rect = pygame.Rect(0, 10 + 140 * i, playerInfoContainer.relative_rect.width, -1),
                container = playerInfoContainer,
            )
            containerWidth = playerContainer.relative_rect.width
            
            Label(      # Zeigt an ob Spieler am Zug ist
                relative_rect = pygame.Rect(-65, 0, containerWidth, -1),
                textFunction = lambda player=player: '>' if player == game.getCurrentPlayer() else '',
                container = playerContainer,
            )
            Image(      # Zeigt Spielersymbol an
                relative_rect = pygame.Rect(-53, -15, 50, 50),
                image_surface = pygame.image.load(f"images/playerSymbols/{player.getSymbol()}.png").convert_alpha(),
                container = playerContainer,
            )
            Label(      # Zeigt Spieler Name (und Position) an
                relative_rect = pygame.Rect(0, 0, containerWidth, -1),
                textFunction = lambda player=player: f"{player.getName()}: Pos {player.getPosition()}",
                container = playerContainer,
            )
            Label(      # Zeigt Geld / bankrott an
                relative_rect = pygame.Rect(5, 20, containerWidth, -1),
                textFunction = lambda player=player: f"{'Bankrott' if player.getBankrupt() else f'Geld: {player.getMoney()} €'}",
                container = playerContainer,
            )
            
            propertyCardContainer = Container(      # Enthält alle Grundstücks-Karten
                relative_rect = pygame.Rect(0, 50, containerWidth, 0),
                container = playerContainer
            )
            for row in range(len(propertyCardGrid)):                
                for col in range(len(propertyCardGrid[row])):
                    id = propertyCardGrid[row][col]
                    property = game.getProperties()[id]
                    if id >= 0:
                        Button(          # muss mit Bildern ersetzt werden
                            relative_rect = pygame.Rect(col * 35, row * 25, 35, 25),
                            text = '',
                            onClickMethod = lambda id=id: game.setSelectedPropertyById(id),     # füge Methode hinzu
                            visibilityCondition = lambda property = property, player = player: property in player.getProperties(),
                            object_id = f"group{property.getGroup()}",
                            container = propertyCardContainer
                        )


"""
Benötigte Screens
- (Spielerreihenfolge festlegen und anzeigen ⚀⚁⚂⚃⚄⚅)
- Würfeln (mit Button zum Würfeln)
- Grundstück Kaufen (mit Buttons zum kaufen und nicht kaufen)
- Miete Zahlen
- Ereignis- / Gemeinschaftskarte anschauen (mit Button zum ausführen und fortfahren)
- Spieler Inventar (mit Option zum Häuser Bauen/Abreißen, Hypothek aufnehmen/aufheben, Handel auslösen, mit nächstem Spieler fortfahren)

Container
- Spielerdaten
"""