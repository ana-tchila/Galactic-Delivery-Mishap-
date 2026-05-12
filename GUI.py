#ID:5752030
import pygame
from sys import exit

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Intergalactic Delivery")
clock = pygame.time.Clock()
pygame.mixer.music.load('sound/music.OGG')
pygame.mixer.music.play(-1)
running = True
font = pygame.font.Font('font/Pixeltype.ttf', size=40)
player = pygame.image.load('player/bike.png')
smaller_player = pygame.transform.scale(player, (70, 70))
player_x_pos = 0
current_screen = "menu"


class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height))
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        surface.blit(text_surface, text_rect)
        if self.is_hovered(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, (200, 200, 200), (self.x, self.y, self.width, self.height), 3)
        else:
            pygame.draw.rect(surface, (100, 100, 100), (self.x, self.y, self.width, self.height), 3)
    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height
    
    def is_hovered(self, pos):
        return self.is_clicked(pos)

start_button = Button(300, 400, 200, 50, "Start Game")
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "menu":
                if start_button.is_clicked(event.pos):
                    current_screen = "game"
    if current_screen == "menu":
        screen.fill((0, 0, 0))
        start_button.draw(screen)  
        text = font.render("Intergalactic Delivery", False, (255, 255, 255))
        screen.blit(text, (270, 100))
        pygame.draw.rect(screen, (255, 255, 255), (270, 150, 265, 5))
        player_x_pos += 2
        if player_x_pos > 800:
            player_x_pos = -70
        screen.blit(smaller_player, (player_x_pos, 200))
    elif current_screen == "game":
        screen.fill((0, 0, 0))
        text = font.render("Game Screen", False, (255, 255, 255))
        screen.blit(text, (350, 280))

    


    pygame.display.flip()
    clock.tick(60)
