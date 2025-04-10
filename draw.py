import pygame

global margin, boardWidth, boardHeight, boardX, boardY, boardImage, scaledBoardImage
global startX, startY, cornerSize, fieldWidth, fieldLenght, screenHeight, screenWidth
    
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
        
    
        for i in range (0, 40):
            # Spielfelder zeichnen
            pygame.draw.rect(screen, black, (gameboard[i].getFieldCoord("x"), gameboard[i].getFieldCoord("y"), gameboard[i].getFieldCoord("width"), gameboard[i].getFieldCoord("height")))

        # Eckfelder in square-Objekte von Game registrieren
        """
        # Eckfelder zeichnen
        pygame.draw.rect(screen, black, (boardX, boardY, cornerSize, cornerSize))  # Oben links
        pygame.draw.rect(screen, black, (boardX + boardWidth - cornerSize, boardY, cornerSize, cornerSize))  # Oben rechts
        pygame.draw.rect(screen, black, (boardX, boardY + boardHeight - cornerSize, cornerSize, cornerSize))  # Unten links
        pygame.draw.rect(screen, black, (boardX + boardWidth - cornerSize, boardY + boardHeight - cornerSize, cornerSize, cornerSize))  # Unten rechts
        
        # Spielfelder zeichnen
        for i in range (0, 9):
            pygame.draw.rect(screen, red, (boardX + cornerSize + (i) * fieldWidth, boardY, fieldWidth, fieldLenght))
            pygame.draw.rect(screen, red, (boardX, boardY + cornerSize + (i) * fieldWidth, fieldLenght, fieldWidth))
            pygame.draw.rect(screen, red, (boardX + boardWidth - cornerSize, boardY + cornerSize + (i) * fieldWidth, fieldLenght, fieldWidth))
            pygame.draw.rect(screen, red, (boardX + cornerSize + (i) * fieldWidth, boardY + boardHeight - cornerSize, fieldWidth, fieldLenght))
        """
        
        
        
        pygame.display.update()

    pygame.quit()
