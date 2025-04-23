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
    def __init__ (self: pygame_gui.elements, screenList: list[str]):
        self.__screenList = screenList
        guiElementList.append(self)
    
    def updateVisibility(self):
        """
        Aktualisiert die Visibilität eines Elements abhängig vom aktuellen Screen
        """
        if self.isInCurrentScreen():                                  # Element ist sichtbar, wenn es beim aktuellen screen sichtbar sein soll
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
        def __init__(self, screenList = ['*'], manager=managerInstance, *args, **kwargs):
            pygameGuiElementClass.__init__(self, manager=manager, *args, **kwargs)
            BaseGuiElement.__init__(self, screenList)
    return GuiElement

# definieren der speziellen guiElementKlassen
class UpdatingLabel(createGuiElementClass(pygame_gui.elements.UILabel)):
    def __init__(self, textFunction, *args, **kwargs):
        super().__init__(text='', *args, **kwargs)
        self.__textFunction = textFunction

    def updateElement(self):
        """
        Aktualisiert den Textinhalt des Labels, entsprechend der lambda-Function.
        """
        text = str(self.__textFunction())
        if self.text != text:
            self.set_text(text)

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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Panel(createGuiElementClass(pygame_gui.elements.UIPanel)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Label(createGuiElementClass(pygame_gui.elements.UILabel)):
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
        relative_rect = pygame.Rect(0, 0, 0, 0),
        screenList = [SCREEN_ROLLDICE, SCREEN_ROLLDICEAGAIN, SCREEN_PAYRENT, SCREEN_BUYOPTION, SCREEN_CARD, SCREEN_CONTINUE, SCREEN_PLAYERMANAGMENT],
        anchors = {'top': 'top'},
        container = guiContainer
    )
    
    # debug
    UpdatingLabel(  # zeigt den aktuellen Screen an
        relative_rect = pygame.Rect(0, 0, -1, -1),
        textFunction = lambda: f"Debug: {currentScreen}",
        anchors = {'left': 'left', 'top': 'top'},
        object_id = 'debug',
        container = guiContainer
    )
    
    # Spieler Liste
    yOffset = 0
    for player in game.getPlayers():
        Label(      # Label um ungemischte Spielernamen anzuzeigen
            relative_rect = pygame.Rect(0, yOffset, container.relative_rect.width, -1),
            text = player.getName(),
            screenList = [SCREEN_STARTGAME],
            manager = manager,
            container = playerInfoContainer,
        )
        yOffset += 25 # Abstand zwischen den Labels
    
    
    def startGameButtonMethod(shufflePlayerOrder=True):
        """
        Startet Spiel und mischt eventuell Spielerreihenfolge.
        """
        game.startGame(shufflePlayerOrder)
        # Erstellung der Spieler Informationsanzeige
        yOffset = 0
        for i in game.getPlayerOrder():
            player = game.getPlayers()[i]
            UpdatingLabel(      # Zeigt Spieler Informationen an
                relative_rect = pygame.Rect(0, yOffset, guiContainer.relative_rect.width - 10, -1),
                textFunction = lambda player=player: f"{'> ' if player == game.getCurrentPlayer() else ''}{player.getName()}: Pos {player.getPosition()} | Geld: {player.getMoney()}€",
                container = playerInfoContainer,
            )
            yOffset += 35 # Abstand zwischen den Labels
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
    def setDiceText() -> str:
        """
        Gibt den richtigen Text für das Würfel Resultat zurück.
        """
        roll = game.getCurrentPlayer().getLastDiceRoll()
        if len(roll) == 0: return ""
        else: return f"Dein Würfelergebnis: {roll[0]}, {roll[1]}{ ' - Pasch' if roll[0] == roll[1] else ''}"     # f"{chr(roll[0] + 9855)} {chr(roll[1] + 9855)}" Weg mit ⚀⚁⚂⚃⚄⚅ funktionier nicht in Standard-Font
    UpdatingLabel(      # Zeigt Würfelergebnis
        relative_rect = pygame.Rect(0, 0, guiContainer.relative_rect.width, -1),
        textFunction = setDiceText,
        container = diceResultContainer
    )
    UpdatingLabel(      # Zeigt Feld auf dem Spieler gelandet ist.
        relative_rect = pygame.Rect(0, 30, guiContainer.relative_rect.width, -1),
        textFunction = lambda: f"Du bist auf dem Feld {game.getCurrentPlayer().getCurrentSquare().getName()} gelandet.",
        container = diceResultContainer
    )
    
    
    payRentContainer = Container(   # Container zum Miete Bezahlen
        relative_rect = pygame.Rect(0, yOffset + 100, 0, 0),
        screenList = [SCREEN_PAYRENT],
        anchors = {'centerx': 'centerx', 'top': 'top'},
        container = guiContainer
    )
    UpdatingLabel(
        relative_rect = pygame.Rect(0, 0, guiContainer.relative_rect.width, -1),
        textFunction = lambda: f"Das Grundstück gehört bereits {game.getCurrentPlayer().getCurrentSquare().getOwner().getName()}. Du musst {game.getCurrentPlayer().getCurrentSquare().getRent()} $ Miete zahlen.",
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
    UpdatingLabel(
        relative_rect = pygame.Rect(0, 0, guiContainer.relative_rect.width, -1),
        textFunction = lambda: f"Dieses Grundstück gehört noch niemanden. Du kannst es für {game.getCurrentPlayer().getCurrentSquare().getCost()} $ kaufen.",
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
    UpdatingLabel(  # Zeigt Typ der Karte
        relative_rect = pygame.Rect(0, 0, cardPanel.relative_rect.width, -1),
        textFunction = lambda: f"{'Gemeinschafts' if game.getLastDrawnCard()['type'] == 'community' else 'Ereignis'}karte",
        container = cardPanel
    )
    UpdatingLabel(
        relative_rect = pygame.Rect(0, 30, cardPanel.relative_rect.width, -1),
        textFunction = lambda: game.getLastDrawnCard()["text"],
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