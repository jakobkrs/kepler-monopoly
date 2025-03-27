import pygame

# pygame initialisieren
pygame.init()

# Fenster
screenWidth, screenHeight = pygame.display.get_desktop_sizes()[0]
print(screenWidth, screenHeight)
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("KeplerMonopoly")

white = (255, 255, 255)
black = (0, 0, 0)
lightGray = (200, 200, 200)

margin = min(screenWidth, screenHeight) // 20  # 5% Rand
boardWidth = screenWidth // 2 - margin
boardHeight = boardWidth
print(boardWidth)
boardX = margin  # Linker Rand
boardY = (screenHeight - boardHeight) / 2 # Oberer Rand



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill(white)
    
    # Spielfeld zeichnen
    pygame.draw.rect(screen, lightGray, (boardX, boardY, boardWidth, boardHeight))
    pygame.draw.rect(screen, black, (0,0,100,100))
    pygame.display.update()

pygame.quit()
