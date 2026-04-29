#ID:5752030
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

running = True
font = pygame.font.Font(None, size=40)
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    text = font.render("Intergalactic Delivery Guy", True, (0, 0, 0))
    screen.blit(text, (350, 280))

    pygame.display.flip()
