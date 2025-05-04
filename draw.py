import pygame
import pygame_gui
import tkinter as tk
from gui import *
from collections import Counter, defaultdict


def startDialog():
    def submitPlayerCount():
        try:
            count = int(playerCountEntry.get())
            if count < 2 or count > len(figures):
                return
            showPlayerSetup(count)
        except:
            return

    def showPlayerSetup(count):
        setupWindow = tk.Toplevel(root)
        setupWindow.title("Spielereinstellungen")
        playerEntries = []
        figureVars = []

        def submitPlayers():
            selectedFigures = [var.get() for var in figureVars]
            if len(set(selectedFigures)) != len(selectedFigures):
                return  # Doppelte Figur
            result = []
            for i in range(count):
                result.append((
                    playerEntries[i].get(),
                    figureVars[i].get(),
                ))
            nonlocal finalPlayers
            finalPlayers = result
            setupWindow.destroy()
            root.quit()  # beendet mainloop

        for i in range(count):
            tk.Label(setupWindow, text=f"Spieler {i+1} Name:").grid(row=i, column=0)
            entry = tk.Entry(setupWindow)
            entry.insert(0, f"Spieler {i+1}")
            entry.grid(row=i, column=1)
            playerEntries.append(entry)

            tk.Label(setupWindow, text="Figur:").grid(row=i, column=2)
            figureVar = tk.StringVar(setupWindow)
            figureVar.set(figures[i])  # Vorauswahl
            option = tk.OptionMenu(setupWindow, figureVar, *figures)
            option.grid(row=i, column=3)
            figureVars.append(figureVar)

        tk.Button(setupWindow, text="Start", command=submitPlayers).grid(row=count, column=1)
        root.wait_window(setupWindow)  # wartet, bis setupWindow zerstört wird

    figures = ["Hund", "Auto", "Pinguin", "Fingerhut", "Schiff", "Katze", "Ente", "Hut"]
    finalPlayers = []

    root = tk.Tk()
    root.title("Spiel starten")
    tk.Label(root, text="Anzahl der Spieler (2-{}):".format(len(figures))).pack()
    playerCountEntry = tk.Entry(root)
    playerCountEntry.pack()
    tk.Button(root, text="Weiter", command=submitPlayerCount).pack()
    root.mainloop()  # Hauptloop startet, wartet bis root.quit() aufgerufen wird
    root.destroy()
    tk._default_root = None
    return finalPlayers

def drawPlayerSymbols(game, screen, imagesCache):
    """
    Zeichnet die Spielerfiguren auf dem Spielfeld.
    """
    players = game.getPlayers()
    gameboard = game.getGameBoard()
    playerPositions = [p.getPosition() for p in players]
    playerCounterPerField = Counter(playerPositions)
    drawnPlayersPerField = defaultdict(int)

    for player in players:
        playerPos = player.getPosition()
        symbolName = player.getSymbol()
        currentPlayerIndex = drawnPlayersPerField[playerPos]
        totalPlayersOnField = playerCounterPerField[playerPos]

        field = gameboard[playerPos]
        fieldX = field.getFieldCoord("x")
        fieldY = field.getFieldCoord("y")
        fieldWidth = field.getFieldCoord("width")
        fieldHeight = field.getFieldCoord("height")

        playerSymbol = imagesCache.get(symbolName)
    

        # Berechnung des zugeteilten Bereichs pro Spieler
        allocatedWidth = fieldWidth / totalPlayersOnField
        allocatedHeight = fieldHeight
        symbolSize = min(allocatedWidth, allocatedHeight)

        # Sonderfall bei Eckfeldern für gleiche Maximalgröße
        if fieldWidth == fieldHeight:  
            symbolSize = fieldHeight * 0.62
        
        scaledSymbol = pygame.transform.scale(playerSymbol, (int(symbolSize), int(symbolSize)))

        # Zentriere das Symbol im zugeteilten Bereich
        symbolX = fieldX + currentPlayerIndex * allocatedWidth + (allocatedWidth - symbolSize) / 2
        symbolY = fieldY + (allocatedHeight - symbolSize) / 2

        screen.blit(scaledSymbol, (symbolX, symbolY))

        drawnPlayersPerField[playerPos] += 1

def drawHouses(game, screen, houseImages):
    """
    Zeichnet die Häuser auf dem Spielfeld.
    """
    gameboard = game.getGameBoard()
    for field in gameboard:
        if field.getType() == "property":
            houses = field.getHouses()
            fieldX = field.getFieldCoord("x")
            fieldY = field.getFieldCoord("y")
            fieldWidth = field.getFieldCoord("width")
            fieldHeight = field.getFieldCoord("height")
            if houses > 0:
                for i in range(houses):
                    if 0 < field.getPosition() < 10 and houses > 0:
                        house = houseImages[houses]
                        origWidth, origHeight = houseImages[houses].get_size()
                        houseHeight = fieldWidth * 0.25
                        houseWidth = houseHeight * (origWidth / origHeight)
                        houseImageScaled = pygame.transform.scale(house, (int(houseWidth), int(houseHeight)))
                        houseX = fieldX + fieldWidth * 0.5 - houseWidth * 0.5
                        houseY = fieldY + fieldHeight*0.03
                        screen.blit(houseImageScaled, (houseX, houseY))
                    elif 10 < field.getPosition() < 20 and houses > 0:
                        house = houseImages[houses+5]
                        origWidth, origHeight = houseImages[houses+5].get_size()
                        houseWidth = fieldHeight * 0.25
                        houseHeight = houseWidth * (origHeight / origWidth)
                        houseImageScaled = pygame.transform.scale(house, (int(houseWidth), int(houseHeight)))
                        houseY = fieldY + fieldHeight * 0.5 - houseHeight * 0.5
                        houseX = fieldX + fieldWidth - fieldWidth*0.03 - houseWidth
                        screen.blit(houseImageScaled, (houseX, houseY))
                    elif 20 < field.getPosition() < 30 and houses > 0:
                        house = houseImages[houses]
                        origWidth, origHeight = houseImages[houses].get_size()
                        houseHeight = fieldWidth * 0.25
                        houseWidth = houseHeight * (origWidth / origHeight)
                        houseImageScaled = pygame.transform.scale(house, (int(houseWidth), int(houseHeight)))
                        houseX = fieldX + fieldWidth * 0.5 - houseWidth * 0.5
                        houseY = fieldY + fieldHeight - fieldHeight*0.03 - houseHeight
                        screen.blit(houseImageScaled, (houseX, houseY))
                    elif 30 < field.getPosition() < 40 and houses > 0:
                        house = houseImages[houses+5]
                        origWidth, origHeight = houseImages[houses+5].get_size()
                        houseWidth = fieldHeight * 0.25
                        houseHeight = houseWidth * (origHeight / origWidth)
                        houseImageScaled = pygame.transform.scale(house, (int(houseWidth), int(houseHeight)))
                        houseY = fieldY + fieldHeight * 0.5 - houseHeight * 0.5
                        houseX = fieldX + fieldWidth*0.03
                        screen.blit(houseImageScaled, (houseX, houseY))

def initDraw(game):
    # pygame initialisieren
    pygame.init()

    boardImage = pygame.image.load("images/board2.png")
    
    # Standardfenstergröße setzen
    screenWidth, screenHeight = 1920, 1080  # Sichere Standardwerte
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE) # Möglichekeit Fenstergröße zu ändern
    pygame.display.set_caption("KeplerMonopoly")

    # Manager für pygame_gui
    manager = pygame_gui.UIManager((screenWidth, screenHeight), 'theme.json')
    
    # Spielfeldgrößen berechnen
    def recalculateSizes():
        global margin, boardWidth, boardHeight, boardX, boardY, scaledBoardImage
        global cornerSize, fieldWidth, fieldLenght, panelHeight, panelWidth, panelX, panelY
        margin = min(screenWidth, screenHeight) / 20  # 5% Rand
        
        # Berechnung der Spielfeldgröße im linken Bereich
        boardHeight = screenHeight - margin
        boardWidth = screenWidth / 2 - margin
        if boardHeight > boardWidth:
            boardHeight = boardWidth
        else:
            boardWidth = boardHeight

        # Berechnung der Startkoordinaten für das Spielfeld
        boardX = margin  # Linker Rand
        boardY = (screenHeight - boardHeight) / 2  # Oberer Rand

        # Berechnung der Bildgröße passend zum Spielfeld
        scaledBoardImage = pygame.transform.scale(boardImage, (boardHeight, boardWidth))
    
        # Berechnung der Größe für die Eckfelder
        cornerSize = boardHeight / 7.5
        
        # Berechnung der Größe für die restlichen Spielfelder
        fieldWidth = (boardWidth - 2 * cornerSize) / 9
        fieldLenght = cornerSize
        
        # Berechnung der Größe für das Anzeige Panel im rechten Bereich
        panelHeight = boardHeight
        panelWidth = screenWidth - boardWidth - 3 * margin

        # Berechnung der Position des Panels
        panelX = boardX + boardWidth + margin
        panelY = boardY

        gameboard = game.getGameBoard()
        
        # Eckfelder speichern
        gameboard[0].setFieldCoord(boardX + boardWidth - cornerSize, boardY + boardHeight - cornerSize, cornerSize, cornerSize)
        gameboard[10].setFieldCoord(boardX, boardY + boardHeight - cornerSize, cornerSize, cornerSize)
        gameboard[20].setFieldCoord(boardX, boardY, cornerSize, cornerSize)
        gameboard[30].setFieldCoord(boardX + boardWidth - cornerSize, boardY, cornerSize, cornerSize)

        # Spielfeldfelder speichern
        for i in range (1, 10):
            # Spielfelder unten
            gameboard[i].setFieldCoord(boardX + boardWidth - cornerSize - i * fieldWidth, boardY + boardHeight - cornerSize, fieldWidth, fieldLenght)
            # Speilfelder links
            gameboard[i + 10].setFieldCoord(boardX, boardY + boardHeight - cornerSize - i * fieldWidth, fieldLenght, fieldWidth)
            # Spielfelder oben
            gameboard[i + 20].setFieldCoord(boardX + cornerSize + (i-1) * fieldWidth, boardY, fieldWidth, fieldLenght)
            # Spielfelder rechts
            gameboard[i + 30].setFieldCoord(boardX + boardWidth - cornerSize, boardY + cornerSize + (i-1) * fieldWidth, fieldLenght, fieldWidth)
  
    # Farben
    white = (255, 255, 255)
    black = (0, 0, 0)
    lightGray = (200, 200, 200)
    red = (255, 0, 0)
    
    # Initiale Berechnung der Spielfeldgrößen
    recalculateSizes()
    
    # erstelle UI-Scrollcontainer im Panelbereich
    scrollContainer = pygame_gui.elements.UIScrollingContainer(
        relative_rect=pygame.Rect(panelX, panelY, panelWidth, panelHeight),
        manager=manager,
        container=None
    )
    
    # initialisiert Gui-Element System
    initGUI(manager, game, scrollContainer)

    symbolImages = {}
    for player in game.getPlayers():
        symbolName = player.getSymbol()
        symbolPath = f"images/playerSymbols/{symbolName}.png"
        symbolImages[symbolName] = pygame.image.load(symbolPath).convert_alpha()

    houseImages = {}
    for i in range(1,6):
        houseImages[i] = pygame.image.load(f"images/houses/{i}.png").convert_alpha()
        houseImages[i+5] = pygame.image.load(f"images/houses/{i}v.png").convert_alpha()
    

    sizeUpdate = True       # Initiales Update der Größe aller Elemente, die Größenfunktionen besitzen

    clock = pygame.time.Clock()
    timeDelta = clock.tick(60)  # Zeitdifferenz für die Aktualisierung der GUI
    running = True

    # Prüft dauerhaft auf Ereignisse
    while running:
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.VIDEORESIZE:
                    screenWidth, screenHeight = event.size  # Neue Fenstergröße speichern
                    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)  # Fenster neu setzen
                    manager.set_window_resolution((screenWidth, screenHeight)) 
                    recalculateSizes()
                    scrollContainer.set_relative_position((panelX, panelY))
                    scrollContainer.set_dimensions((panelWidth, panelHeight))
                    scrollContainer.set_scrollable_area_dimensions((max(650, panelWidth - 30), len(game.getPlayers()) * 140 + 500))
                    sizeUpdate = True
                case pygame_gui.UI_BUTTON_PRESSED:
                    executeButtonPress(event)
                case pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    dropDownMenuSelect(event)
                case pygame.MOUSEBUTTONDOWN:
                    mousePos = event.pos
                    clickedFieldIndex = getClickedField(mousePos, game)
                    propertyPostionList = [property.getPosition() for property in game.getProperties()]     # Liste mit den Positionen der Grundstücke
                    if clickedFieldIndex in propertyPostionList:
                        game.setSelectedPropertyById(propertyPostionList.index(clickedFieldIndex))


            manager.process_events(event) 
        
        screen.fill(white)

        # Spielfeld zeichnen
        pygame.draw.rect(screen, lightGray, (boardX, boardY, boardWidth, boardHeight))
        
        # Spielfeldbild
        screen.blit(scaledBoardImage, (boardX, boardY))
        
        drawCurrentScreen(sizeUpdate)

        drawPlayerSymbols(game, screen, symbolImages)

        drawHouses(game, screen, houseImages)

        manager.update(timeDelta)
        manager.draw_ui(screen)
        pygame.display.update()
        
        sizeUpdate = False

    pygame.quit()

