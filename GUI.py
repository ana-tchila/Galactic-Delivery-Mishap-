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

title_font = pygame.font.Font('font/Pixeltype.ttf', size=40)
font = pygame.font.Font('font/Pixeltype.ttf', size=30)

player = pygame.image.load('player/bike.png')
smaller_player = pygame.transform.scale(player, (70, 70))
player_x_pos = [0]
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
        text_surface = title_font.render(self.text, True, (0, 0, 0))
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


def draw_menu():
    screen.fill((0, 0, 0))
    start_button.draw(screen)  
    title_text = title_font.render("Intergalactic Delivery", False, (255, 255, 255))
    screen.blit(title_text, (270, 100))
    pygame.draw.rect(screen, (255, 255, 255), (270, 150, 265, 5))
   
    player_x_pos[0] += 2
    if player_x_pos[0] > 800:
        player_x_pos[0] = -70
    screen.blit(smaller_player, (player_x_pos[0], 200))


def draw_start():
    #scene title
    screen.fill((0, 0, 0))
    title_text = title_font.render("Starting point", False, (255, 255, 255))
    screen.blit(title_text, (320, 50))
    pygame.draw.rect(screen, (255, 255, 255), (300, 80, 200, 5))

    #scene description
    desc_text = font.render("You are an intergalactic space delivery driver.\n"
	"You have just received an urgent food order to Roupell Street SE1.\n"
    "Your GPS is calculating the fastest route.. . .  .\n"
			"ERROR: GPS CONNECTION LOST.\n" 
			"You must navigate through the galaxy on your own.", False, (255, 255, 255))
    dec_rect = desc_text.get_rect(center=(400, 200))
    pygame.draw.rect(screen, (255, 255, 255), (dec_rect.x - 10, dec_rect.y - 10, dec_rect.width + 20, dec_rect.height + 20), 2)
    screen.blit(desc_text, dec_rect)

    #prompt
    prompt_text = title_font.render("\nWhere do you want to go?", False, (255, 255, 255))

    screen.blit(prompt_text, (230, 400))
    garage_button.draw(screen)
    diner_button.draw(screen) 

def draw_garage():
    screen.fill((0, 0, 0))
    text = title_font.render("Garage Screen", False, (255, 255, 255))
    screen.blit(text, (325, 300))

def draw_diner():
    screen.fill((0, 0, 0))
    text = title_font.render("Diner Screen", False, (255, 255, 255))
    screen.blit(text, (325, 300))



start_button = Button(300, 400, 200, 50, "Start Game")
garage_button = Button(150, 480, 200, 50, "Go to Garage")
diner_button = Button(420, 480, 200, 50, "Go to Diner")
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "menu":
                if start_button.is_clicked(event.pos):
                    current_screen = "game"

            if current_screen == "game":
                if garage_button.is_clicked(event.pos):
                        current_screen = "garage"
                elif diner_button.is_clicked(event.pos):
                    current_screen = "diner"

    if current_screen == "menu":
        draw_menu()
    elif current_screen == "game":
        draw_start()
    elif current_screen == "garage":
        draw_garage()
    elif current_screen == "diner":
        draw_diner()

    


    pygame.display.flip()
    clock.tick(60)
