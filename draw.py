import pygame
import random
import tkinter as tk

global margin, boardWidth, boardHeight, boardX, boardY, boardImage, scaledBoardImage
global startX, startY, cornerSize, fieldWidth, fieldLenght, screenHeight, screenWidth

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

    figures = ["Hund", "Auto", "Schiff", "Hut", "Katze", "Boot", "Flugzeug", "Zug"]
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

def initDraw(game):
    # pygame initialisieren
    pygame.init()

    boardImage = pygame.image.load("images/board.png")
    
    # Standardfenstergröße setzen
    screenWidth, screenHeight = 1920, 1080  # Sichere Standardwerte
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE) # Möglichekeit Fenstergröße zu ändern
    pygame.display.set_caption("KeplerMonopoly")
    
    # Spielfeldgrößen berechnen
    def recalculateSizes():
        global margin, boardWidth, boardHeight, boardX, boardY, scaledBoardImage
        global startX, startY, cornerSize, fieldWidth, fieldLenght
        margin = min(screenWidth, screenHeight) / 20  # 5% Rand
        boardHeight = screenHeight - margin
        boardWidth = screenWidth / 2 - margin
        if boardHeight > boardWidth:
            boardHeight = boardWidth
        else:
            boardWidth = boardHeight
        boardX = margin  # Linker Rand
        boardY = (screenHeight - boardHeight) / 2  # Oberer Rand

        scaledBoardImage = pygame.transform.scale(boardImage, (boardHeight, boardWidth))
        
        startX = boardX + boardWidth
        startY = boardY + boardHeight
        
        # Berechnung der Eckengröße
        cornerSize = boardHeight / 7.5
        
        # Berechnung der Feldergröße
        fieldWidth = (boardWidth - 2 * cornerSize) / 9
        fieldLenght = cornerSize
        
  
   

    # Farben
    white = (255, 255, 255)
    black = (0, 0, 0)
    lightGray = (200, 200, 200)
    red = (255, 0, 0)
    
    # Initiale Berechnung der Spielfeldgrößen
    recalculateSizes()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screenWidth, screenHeight = event.size  # Neue Fenstergröße speichern
                screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)  # Fenster neu setzen
                recalculateSizes()  # Alle Werte neu berechnen
        
        screen.fill(white)

        # Spielfeld zeichnen
        pygame.draw.rect(screen, lightGray, (boardX, boardY, boardWidth, boardHeight))
        
        # Spielfeldbild
        screen.blit(scaledBoardImage, (boardX, boardY))
        
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
        
        """
        for i in range (0, 40):
            # Spielfelder zeichnen
            pygame.draw.rect(screen, black, (gameboard[i].getFieldCoord("x"), gameboard[i].getFieldCoord("y"), gameboard[i].getFieldCoord("width"), gameboard[i].getFieldCoord("height")))
        """
        
        
        pygame.display.update()

    pygame.quit()
