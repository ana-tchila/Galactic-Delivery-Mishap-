#ID:5752030

import pygame
from sys import exit
from Graph import galaxy, starting, garage, police, diner, shop, parade, destination, celebration, Stack, bfs, make_connections_reciprocal
from shop_system import search, inventory, search_shop


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
def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + ' '
    if current_line:
        lines.append(current_line.strip())
    return lines



def build_choice_buttons(location, y_position=300):
    """Buttons for in-scene dialogue choices."""
    buttons = []
    if not location.choices:
        return buttons
    button_width = 500
    button_height = 40
    for i, choice_text in enumerate(location.choices.keys()):
        x = (800 - button_width) // 2
        y = y_position + i * 50
        buttons.append(Button(x, y, button_width, button_height, choice_text))
    return buttons 

def build_connection_buttons(location, y_position=300):
    """Buttons for navigating to connected locations."""
    buttons = []
    if not location.connections:
        return buttons
    button_width = 500
    button_height = 40
    for i, conn_name in enumerate(location.connections):
        x = (800 - button_width) // 2
        y = y_position + i * 50
        buttons.append(Button(x, y, button_width, button_height, f"Go to {conn_name}"))
    return buttons

def draw_scene(location, choice_buttons, connection_buttons, dialogue=""):
    screen.fill((0, 0, 0))
    title_text = title_font.render(location.name, False, (255, 255, 255))
    screen.blit(title_text, (320, 50))
    pygame.draw.rect(screen, (255, 255, 255), (300, 85, 200, 5))

    desc = wrap_text(location.description, font, 700)
    y = 150

    for line in desc:
        text_surface = font.render(line, False, (255,255,255))
        screen.blit(text_surface, (100, y))
        y += 30
    
    if dialogue != "":
        dialogue_lines = wrap_text(dialogue, font, 700)

        y += 20  # small gap

        for line in dialogue_lines:
            text_surface = font.render(line, False, (200,255,200))
            screen.blit(text_surface, (100, y))
            y += 30

    for button in choice_buttons:
        button.draw(screen)
    for button in connection_buttons:
        button.draw(screen)
    
    draw_inventory(player_inventory)

def draw_shop_scene():
    screen.fill((0, 0, 0))

    title_text = title_font.render("Shop", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    desc_text = wrap_text(shop.description, font, 700)
    y_offset = 150
    for line in desc_text:
        line_surface = font.render(line, False, (255, 255, 255))
        line_rect = line_surface.get_rect(center=(400, y_offset))
        screen.blit(line_surface, line_rect)
        y_offset += 40
    prompt_text = font.render("What do you want to buy?", False, (255, 255, 255))
    prompt_rect = prompt_text.get_rect(center=(400, y_offset + 20))
    screen.blit(prompt_text, prompt_rect)

    input_box = pygame.Rect(300, y_offset + 60, 200, 40)
    pygame.draw.rect(screen, (255, 255, 255), input_box, 2)

    hint_text = font.render("type and press Enter", False, (255, 255, 255))
    hint_rect = hint_text.get_rect(center=(400, y_offset + 110))
    screen.blit(hint_text, hint_rect)

    if shop_search_result:
        result = wrap_text(shop_search_result, font, 700)
        result_y = y_offset + 150

        for line in result:
            line_surface = font.render(line, False, (255, 255, 255))
            line_rect = line_surface.get_rect(center=(400, result_y))
            screen.blit(line_surface, line_rect)
            result_y += 40

    leave_shop_button.draw(screen)
    draw_inventory(player_inventory)


def draw_inventory(inventory):
    pygame.draw.rect(screen, (255, 255, 255), (50, 400, 200, 150))
    pygame.draw.line(screen, (255, 255, 255), (50, 400), (250, 550), 2)

    if player_inventory.items:
        inv_display = ", ".join(player_inventory.items)
    else:
        inv_display = "Empty"
    inv_text = font.render(f"Inventory: {inv_display}", False, (255, 255, 255))
    screen.blit(inv_text, (60, 410))

current_screen = "menu"
current_location = starting
movement_history = Stack()
current_dialogue = ""
player_inventory = inventory()
shop_search_text = ""
shop_search_result = ""

leave_shop_button = Button(300, 500, 200, 50, "Leave Shop")
choice_buttons = build_choice_buttons(current_location)
connection_buttons = build_connection_buttons(current_location)


start_button = Button(300, 400, 200, 50, "Start Game")

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
                for button in choice_buttons:
                    if button.is_clicked(event.pos):
                        choice_text = button.text
                        current_location = next_location
                        current_dialogue = ""
                        choice_buttons = []
                        connection_buttons = build_connection_buttons(current_location)
                        break

                for button in connection_buttons:
                    if button.is_clicked(event.pos):
                        dest_name = button.text.replace("Go to ", "")
                        if dest_name in current_location.connections:
                            next_location = current_location.connections[dest_name]
                            movement_history.push(current_location)
                            current_location = next_location
                            current_dialogue = current_location.description[choice_text]
                        
                        if current_location == shop:
                            current_screen = "shop"
                            shop_search_result = ""
                            shop_search_text = ""

                        elif current_screen == "shop":
                            if leave_shop_button.is_clicked(event.pos):
                                current_screen = "game"
                                current_location = shop
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    shop_search_result = search_shop(shop_search_text)
                                    shop_search_text = ""
                                elif event.key == pygame.K_BACKSPACE:
                                    shop_search_text = shop_search_text[:-1]
                                else:
                                    shop_search_text += event.unicode
                            choice_buttons = build_choice_buttons(current_location)
                            connection_buttons = build_connection_buttons(current_location)            


    


            choice_buttons = build_choice_buttons(current_location)
            connection_buttons = build_connection_buttons(current_location)
                            


    
    if current_screen == "menu":
        draw_menu()
    elif current_screen == "game":
        draw_scene(current_location, choice_buttons, connection_buttons, current_dialogue)
    elif current_screen == "shop":
        draw_shop_scene()
    pygame.display.flip()
    clock.tick(60)
