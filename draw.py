import pygame

# pygame initialisieren
pygame.init()
boardImage = pygame.image.load("board.png")

# Standardfenstergröße setzen
screenWidth, screenHeight = 1280, 720  # Sichere Standardwerte
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("KeplerMonopoly")

# Farben
white = (255, 255, 255)
black = (0, 0, 0)
lightGray = (200, 200, 200)

# Spielfeldgrößen berechnen
def recalculateSizes():
    global margin, boardWidth, boardHeight, boardX, boardY, boardImage, scaledBoardImage
    margin = min(screenWidth, screenHeight) // 20  # 5% Rand
    boardHeight = screenHeight - margin
    boardWidth = screenWidth // 2 - margin
    if boardHeight > boardWidth:
        boardHeight = boardWidth
    else:
        boardWidth = boardHeight
    boardX = margin  # Linker Rand
    boardY = (screenHeight - boardHeight) / 2  # Oberer Rand

    scaledBoardImage = pygame.transform.scale(boardImage, (boardHeight, boardWidth))

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
    screen.blit(scaledBoardImage, (boardX, boardY))

    pygame.display.update()

pygame.quit()
