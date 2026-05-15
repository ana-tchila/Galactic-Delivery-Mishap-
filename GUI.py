#ID:5752030

from collections import deque
import random

import pygame
from sys import exit
from Graph import galaxy, starting, garage, diner, police, shop, parade, destination, celebration, Stack, bfs, make_connections_reciprocal
from shop_system import search, inventory, search_shop
from police_station import generate_licence, police_scan, player_licence


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Intergalactic Delivery")
clock = pygame.time.Clock()
pygame.mixer.music.load('sound/music.OGG')
pygame.mixer.music.play(-1)
running = True

title_font = pygame.font.Font('font/Pixeltype.ttf', size=40)
font = pygame.font.Font('font/Pixeltype.ttf', size=26)
small_font = pygame.font.Font('font/Pixeltype.ttf', size=20)
player = pygame.image.load('player/bike.png')
smaller_player = pygame.transform.scale(player, (70, 70))
player_x_pos = [0]


# the Button class represents interactive buttons in the GUI, with methods to draw itself and check for clicks and hover states.
class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), (self.x, self.y, self.width, self.height))
        chosen_font = small_font if len(self.text) > 18 else font
        text_surface = chosen_font.render(self.text, True, (0, 0, 0))
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

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    for paragraph in str(text).split('\n'):
        words = paragraph.split(' ')
        line = "" 
        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        if line:
            lines.append(line.strip())

        if paragraph == "":
            lines.append("")
    return lines


def render_text_block(text, x, y, max_width, font_used, color=(255, 255, 255), line_spacing=5):
    lines = wrap_text(text, font_used, max_width)
    for line in lines:
        text_surface = font_used.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += text_surface.get_height() + line_spacing
    return y

def draw_inventory_bar():
    pygame.draw.rect(screen, (40, 40, 40), (0, 555, 800, 45))
    pygame.draw.line(screen, (255, 255, 255), (0, 555), (800, 555), 2)

    if player_inventory.items:
        inv_display = ", ".join(player_inventory.items)
    else:
        inv_display = "Empty"

    text_surface = font.render(inv_display, False, (255, 255, 255))
    screen.blit(text_surface, (10, 565))


def get_visible_routes(location):
    if location == starting:
        return [garage.name, diner.name]
    elif location == diner:
        return [shop.name, parade.name]
    elif location == shop:
        return [garage.name]
    elif location == garage:
        if not movement_history.peek() == shop:
            return [diner.name]
        elif movement_history.peek() and gps_installed: 
            return [police.name]
    elif location == police:
        return [destination.name]
    return []

def get_visible_choices(location):
    if location == garage and gps_installed:
        return []
    if location in (parade, destination, celebration):
        return []
    return list(location.choices.keys())

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

def draw_intro():
    screen.fill((0, 0, 0))
    title_text = title_font.render("Intergalactic Delivery", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 100))
    screen.blit(title_text, title_rect)

    intro = (
        "Great! You have accepted the delivery.\n"
        "Your GPS is calculating the fastest route...\n"
        "ERROR: GPS CONNECTION LOST.\n\n"
        "You must navigate through the galaxy on your own."
    )

    render_text_block(intro, 220, 210, 700, font)
    continue_button.draw(screen)


def draw_location_screen():
    screen.fill((0, 0, 0))
    title_text = title_font.render(current_location.name, False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, (255, 255, 255), (300, 85, 200, 5))

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    body_text = current_location.description
    if current_dialogue:
        body_text += "\n\n" + current_dialogue

    render_text_block(body_text, panel.x + 15, panel.y + 15, panel.width - 30, font)

    for button in action_buttons:
        button.draw(screen)
    draw_inventory_bar()


def draw_choice_screen():
    screen.fill((0, 0, 0))
    title_text = title_font.render(current_location.name, False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, (255, 255, 255), (300, 70, 200, 3))

    panel = pygame.Rect(40, 90, 720, 280)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    body_text = current_location.description
    if current_dialogue:
        body_text += "\n\n" + current_dialogue
    render_text_block(body_text, panel.x + 15, panel.y + 15, panel.width - 30, font)

    hint_text = small_font.render("Click a choice to continue", False, (255, 255, 255))
    hint_rect = hint_text.get_rect(center=(400, 380))
    screen.blit(hint_text, hint_rect)

    for button in choice_buttons:
        button.draw(screen)
    draw_inventory_bar()

def draw_route_screen():
    screen.fill((0, 0, 0))
    title_text = title_font.render(current_location.name, False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, (255, 255, 255), (300, 70, 200, 3))

    panel = pygame.Rect(40, 90, 720, 280)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)
    render_text_block(current_location.description, panel.x + 15, panel.y + 15, panel.width - 30, font)

    hint_text = small_font.render("Click a destination to travel", False, (255, 255, 255))
    hint_rect = hint_text.get_rect(center=(400, 380))   
    screen.blit(hint_text, hint_rect)

    for button in route_buttons:
        button.draw(screen)
    
    draw_inventory_bar()


def draw_shop_scene():
    screen.fill((0, 0, 0))

    title_text = title_font.render("Shop", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, (255, 255, 255), (300, 70, 200, 3))

    panel = pygame.Rect(40, 90, 720, 280)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    shop_text = shop.description
    if current_dialogue:
        shop_text += "\n\n" + current_dialogue
    render_text_block(shop_text, panel.x + 15, panel.y + 15, panel.width - 30, font)

    

    input_box = pygame.Rect(200, 350, 400, 30)
    pygame.draw.rect(screen, (30, 30, 30), input_box)
    pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
    typed_text = font.render(shop_search_text, False, (255, 255, 255))
    screen.blit(typed_text, (input_box.x + 5, input_box.y + 5))

    hint_text = font.render("type and press Enter", False, (255, 255, 255))
    screen.blit(hint_text, (50, 385))

    leave_shop_button.draw(screen)
    draw_inventory_bar()

def draw_ending_screen(won):
    screen.fill((0, 0, 0))
    if won:
        title_text = title_font.render("Congratulations!", False, (255, 255, 255))
    else:
        title_text = title_font.render("Game Over", False, (255, 255, 255))

    title_rect = title_text.get_rect(center=(400, 100))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 150, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)  
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)
    render_text_block(end_message, panel.x + 15, panel.y + 15, panel.width - 30, font)

    restart_button.draw(screen)


# converting the boss game into functions to integrate to the GUI

def begin_find_boss():
    global current_screen, boss_door, search_low, search_high, boss_message
    current_screen = "find_boss" # Set the current screen to the boss challenge
    boss_door = random.randint(1, 15)
    search_low = 1
    search_high = 15
    boss_message = "You enter the building and see 15 doors. The boss is behind one of them. Which one do you choose?"
##############
def draw_find_boss():
    screen.fill((0, 0, 0))
    title_text = title_font.render("Find the Boss", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    render_text_block(boss_message, panel.x + 15, panel.y + 15, panel.width - 30, font)
    door_buttons = []
    for i in range(1, 16):
        button = Button(30 + (i - 1) * 50, 450, 40, 40, str(i))
        button.draw(screen)
        door_buttons.append(button)

    return door_buttons
    
def click_door(door_number):
    global search_low, search_high, boss_message, current_screen

    middle_search = (search_high + search_low) // 2 # Get the middle value 

    #Force player to choose the middle door 
    if door_number != middle_search: 
        boss_message = (f"You have to pick the middle door: {middle_search}")
        return 
    
    # Correct door found 
    elif door_number == boss_door: 
        boss_message = ("You found the boss")
        draw_signal_sequence()
        return 
    
    #Behind lower value door 
    elif door_number > boss_door: 
        search_high = middle_search - 1 
        boss_message =("You must pick a lower value door.\n"  
        f"Search between {search_low} and {search_high}"
        )
        return 
    
    #Behind higher value door
    else: 
        search_low = middle_search + 1 
        boss_message = ("You must pick a higher value door.\n"  
        f"Search between {search_low} and {search_high}"
        )
        return 

def draw_signal_sequence():
    global current_screen, signal_message, boss_health, sequence_show_time
    screen.fill((0, 0, 0))

    title_text = title_font.render("Boss Battle", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    sequance_dispaly = " ".join(signal_sequence)
    info = (f"Memorize the sequence: {sequance_dispaly}"
                      f"[{sequance_dispaly}\n\n"
                        f"You have 5 seconds to memorize the sequence]")
    render_text_block(info, panel.x + 15, panel.y + 15, panel.width - 30, font)
    
def draw_show_sequence():
    global sequence_show_time
    sequence_show_time = pygame.time.get_ticks()
    screen.fill((0, 0, 0))

    title_text = title_font.render("Boss Battle", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    sequance_dispaly = " ".join(signal_sequence)
    info = (f"Memorize the sequence: {sequance_dispaly}\n\n"
            f"[{sequance_dispaly}]\n\n"
            f"You have 5 seconds to memorize the sequence")
    render_text_block(info, panel.x + 15, panel.y + 15, panel.width - 30, font)

def begin_attack_input():
    global current_screen, siganls_remaining, attack_message
    current_screen = "attack_input"
    siganls_remaining = deque(signal_sequence)
    attack_message = "Repeat the sequence by clicking the signals in the correct order."

def draw_attack_input():
    screen.fill((0, 0, 0))

    title_text = title_font.render("Boss Battle", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)
    info = (f"{attack_message}\n\n Boss Health: {boss_health}\n\n Score: {score}")
    render_text_block(info, panel.x + 15, panel.y + 15, panel.width - 30, font)

    direction_buttons = []
    layout = [("Up", 0, 0), ("Down", 1, 0), ("Left", 0, 1), ("Right", 1, 1)]
    button_width = 100
    button_height = 50
    gap = 20
    start_x = (800 - (2 * button_width + gap)) // 2
    start_y = 340
    for lebal, row, col in layout:
        x = start_x + col * (button_width + gap)
        y = start_y + row * (button_height + gap)
        button = Button(x, y, button_width, button_height, lebal)
        button.draw(screen)
        direction_buttons.append(button)
    return direction_buttons

def click_direction(direction):
    global boss_health, score, attack_message, current_screen
    expected = siganls_remaining[0]
    if direction == expected:
        siganls_remaining.popleft()
        attack_message = "Correct! Keep going."
        if not siganls_remaining:
            boss_health -= 1
            score += 1
            if boss_health == 0:
                begin_route_map()
            else:
                attack_message = f"You hit the boss! Boss health is now {boss_health}."
                signal_sequence()
    else:
        attack_message = f"Wrong signal! Try again. Expected {expected}. The boss blocked your attack!"
        current_screen = "attack_failed"

def draw_attack_failed():
    screen.fill((0, 0, 0))

    title_text = title_font.render("Boss Survived", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    render_text_block(attack_message + "\n\nMove to the route challenge", panel.x + 15, panel.y + 15, panel.width - 30, font)

    continue_to_route_button.draw(screen)


def begin_route_map():
    global current_screen, optimal_route, optimal_cost, route_map_message
    current_screen = "route_map"
    
    space_graph = {
        "Base": {"Moon": 4, "Mars": 5},
        "Moon": {"Destination": 8},
        "Mars": {"Jupiter": 3, "Venus": 6},
        "Jupiter": {"Destination": 2},
        "Venus": {"Destination": 4},
        "Destination": {},
    }


    #dijkstra's algorithm to find the optimal route
    distance = {node: float('inf') for node in space_graph}
    predecessor = {node: None for node in space_graph}
    distance["Base"] = 0
    unexplored = list(space_graph)

    while unexplored:
        current = min(unexplored, key=lambda node: distance[node])
        unexplored.remove(current)

        for neighbor, cost in space_graph[current].items():
            alt = distance[current] + cost
            if alt < distance[neighbor]:
                distance[neighbor] = alt
                predecessor[neighbor] = current

    optimal_route = []
    current = "Destination"
    while current is not None:
        optimal_route.append(current)
        current = predecessor[current]
    optimal_route = distance["Destination"]
    route_map_message = "Choose the route with the lowest total cost to reach the destination safely."


def draw_route_map():
    screen.fill((0, 0, 0))

    title_text = title_font.render("Route Map Challenge", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    map_info = ( f"{route_map_message}\n\n"
        "ROUTE MAP:\n"
        "Base -> Moon (cost 4)\n"
        "Base -> Mars (cost 5)\n"
        "Moon -> Destination (cost 8)\n"
        "Mars -> Jupiter (cost 3)\n"
        "Mars -> Venus (cost 6)\n"
        "Jupiter -> Destination (cost 2)\n"
        "Venus -> Destination (cost 4)" )
    
    render_text_block(map_info, panel.x + 15, panel.y + 15, panel.width - 30, font)

    route_options_buttons = []
    routes = [
        "A: Base -> Moon -> Destination",
        "B: Base -> Mars -> Jupiter -> Destination",
        "C: Base -> Mars -> Venus -> Destination", ]
    
    button_y = 395
    for i, route in enumerate(routes):
        button = Button(50, button_y + i * 60, 700, 50, route)
        button.draw(screen)
        route_options_buttons.append(button)

    return route_options_buttons

def click_route_option(option):
    global current_screen, score, current_dialogue

    route_choices = {
        "A": ["Base -> Moon -> Destination"],
        "B": ["Base -> Mars -> Jupiter -> Destination"],
        "C": ["Base -> Mars -> Venus -> Destination"]
    }
    chosen_letter = option[0]
    chosen_route = route_choices[chosen_letter]

    if chosen_route == optimal_route:
        score += 1
        result = "You chose the optimal route and reached the destination safely! You win!"
    else:
        result = "You chose a suboptimal route and got caught by space pirates! Game over."

    current_dialogue = (
        f"{result}\n\nTotal fuel cost of the best route: {optimal_cost}\n\n"
        "You defeated the Alien King! You can now take his ship anywhere."
    )
    current_screen = "after_boss"

def draw_police_screen(): 
    screen.fill((0,0,0)) #Fill screen

    title_text = title_font.render("Police Checkpoint", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400,100)) 
    screen.blit(title_text, title_rect) #Draws title text on the rectangle 
    
    panel = pygame.Rect(40, 130, 720, 300) 
    pygame.draw.rect(screen, (0, 0, 0), panel) # Black textbox 
    pygame.draw.rect(screen, (255, 255, 255), panel, 2) # White outline 

    text = current_dialogue
    render_text_block(text, panel.x + 15, panel.y + 15, panel.width - 30, font) # Text placement and font

    #Scan button to process the licence
    scan_button.draw(screen)

current_screen = "menu"
current_location = starting
movement_history = Stack()
current_dialogue = ""
player_inventory = inventory()
shop_search_text = ""

gps_installed = False
end_message = ""

boss_health = 3
boss_door = 0
search_low = 1
search_high = 15
boss_message = ""
signal_sequence = deque()
siganls_remaining = deque()
score = 0
attack_message = ""
sequence_show_time = 0
optimal_route = []
optimal_cost = 0
route_map_message = ""

start_button = Button(300, 400, 200, 50, "Start Game")
continue_button = Button(300, 470, 200, 50, "Continue")
leave_shop_button = Button(560, 395, 200, 40, "Leave Shop")
restart_button = Button(300, 480, 200, 50, "Play Again")
continue_to_route_button = Button(300, 480, 200, 50, "Continue")
back_button = Button(50, 460, 150, 50, "Back")
talk_button = Button(120, 460, 230, 60, "Talk / Search")
travel_button = Button(450, 460, 230, 60, "Choose Route")
proceed_button = Button(300, 460, 200, 60, "Continue")
scan_button = Button(300, 460, 200, 60, "Scan Licence")

def build_action_buttons(location):
    buttons = []
    has_choices = get_visible_choices(location)
    has_routes = get_visible_routes(location)

    if has_choices and has_routes:
        buttons.append(talk_button)
        buttons.append(travel_button)
    elif has_choices:
        buttons.append(Button(285, 460, 230, 60, "Talk / Search"))
    elif has_routes:
        buttons.append(Button(285, 460, 230, 60, "Choose Route"))

    return buttons

def build_choice_buttons(location):
    buttons = []
    choices = get_visible_choices(location)
    for i, choice in enumerate(choices):
        x = (800 - 600) // 2
        y = 420 + i * 55
        buttons.append(Button(x, y, 600, 45, choice))
    return buttons

def build_route_buttons(location):
    buttons = []
    routes = get_visible_routes(location)
    for i, route in enumerate(routes):
        x = (800 - 700) // 2
        y = 410 + i * 60
        buttons.append(Button(x, y, 700, 50, f"Go to {route}"))
    return buttons

def travel_to(location):
    global current_location, current_screen, current_dialogue
    global gps_installed, end_message
    
    previous_location = current_location
    movement_history.push(previous_location)
    current_location = location
    current_dialogue = ""

    if current_location == parade:
        begin_find_boss()
        return

    if current_location == shop:
        current_screen = "shop"
        current_dialogue = (
            "Welcome to my humble shop, stranger! "
            "Type the name of an item to search for it.\n"
            "Items available: Raygun, GPS, Cap, Gloop" # We don't need the small items available box 
        )
        return
    
    if current_location == garage and previous_location == shop:
        if player_inventory.has("GPS"):
            gps_installed = True
            current_dialogue = (
            "Mechanic: GPS installed and working perfectly!\n\n"
            "GPS calculating fastest route...\n"
            "Best path: Garage -> Police Checkpoint -> Destination"
            )
            current_screen = "location"
        else:
            end_message = ("You return to the garage empty-handed.\n\n"
                "Mechanic: You came back with nothing? "
                "I can't fix your GPS without the part!\n\n"
                "Without a GPS, you can't find Brad Cooper's house. "
                "The delivery fails. Your boss fires you on the spot."
            )
            current_screen = "ended_lose"
        return
    
    if current_location == police: 
        current_screen = "police"
        current_dialogue = ("POLICE CHECKPOINT\n" 
        "Officer: Show your licence"
        )
        return 

    if current_location == destination:
        if player_inventory.has("GPS"):
            # Use BFS to find path to celebration as the algorithm showcase
            make_connections_reciprocal()
            path_to_celebration = bfs(destination, celebration)
            path_text = " -> ".join(loc.name for loc in path_to_celebration) if path_to_celebration else "Celebration"
            current_dialogue = (
                "Congratulations! Package delivered to Brad Cooper on time.\n\n"
                "Boss: Great job! You earned a promotion. "
                "Come to my celebration party!\n\n"
                f"GPS calculating route to celebration:\n{path_text}"
            )
            current_screen = "destination_reached"
        else:
            end_message = (
                "Without a GPS, you wandered the streets and couldn't find "
                "Brad Cooper's house. The food arrived cold and late. "
                "Your boss is furious. You're fired."
            )
            current_screen = "ended_lose"
        return
    
    
    if current_location == celebration:
        end_message = (
            "You made it to the celebration party!\n\n"
            "Promotion confirmed. Drinks on the boss.\n\n"
            "THE END."
        )
        current_screen = "ended_win"
        return
    
    
    current_screen = "location"


while running:
    
    action_buttons = build_action_buttons(current_location)
    choice_buttons = build_choice_buttons(current_location)
    route_buttons = build_route_buttons(current_location)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        
        if event.type == pygame.KEYDOWN and current_screen == "shop":
            if event.key == pygame.K_RETURN:
                if shop_search_text.strip():
                    current_dialogue = search_shop(shop, shop_search_text.strip(), player_inventory)
                    shop_search_text = ""
            elif event.key == pygame.K_BACKSPACE:
                shop_search_text = shop_search_text[:-1]
            else:
                if event.unicode.isprintable() and len(shop_search_text) < 24:
                    shop_search_text += event.unicode
        
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            
            if current_screen == "menu":
                if start_button.is_clicked(event.pos):
                    current_screen = "intro"
            
            
            elif current_screen == "intro":
                if continue_button.is_clicked(event.pos):
                    current_screen = "location"
            
           
            elif current_screen == "location":
                for button in action_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Talk / Search":
                            current_screen = "choices"
                        elif button.text == "Choose Route":
                            current_screen = "routes"
                        break
            
            
            elif current_screen == "choices":
                for button in choice_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Back":
                            current_screen = "location"
                        else:
                            current_dialogue = current_location.choices[button.text]
                            current_screen = "location"
                        break
            
            
            elif current_screen == "routes":
                location_table = {
                    starting.name: starting, garage.name: garage,
                    diner.name: diner, shop.name: shop,
                    parade.name: parade, police.name: police,
                    destination.name: destination, celebration.name: celebration,
                }
                for button in route_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Back":
                            current_screen = "location"
                        elif button.text.startswith("Go to "):
                            target_name = button.text.replace("Go to ", "")
                            if target_name in location_table:
                                travel_to(location_table[target_name])
                        break
            
            
            elif current_screen == "shop":
                if leave_shop_button.is_clicked(event.pos):
                    current_screen = "location"
                    current_dialogue = ""
                
            elif current_screen == "police": 
                
                #Checks if the scan button is clicked 
                if scan_button.is_clicked(event.pos): 
                    
                    # Use the Bloom Filter instance
                    result = police_scan(player_licence)

                    if result == "Let the driver pass": 

                        current_dialogue =(
                            "POLICE CHECKPOINT\n" 
                            "Officer: Licence is valid\n"
                            "Let driver pass.\n"
                        )

                        # Let's the player pick the location 
                        current_screen = "location" 

                    else: 

                        end_message = ( 
                            "POLICE CHECKPOINT\n"
                            "Officer: Inalid licence\n"
                            "GAME OVER\n"
                        )
                        
                        # Terminate the game 
                        current_screen = "ended_lose"
            
            elif current_screen == "find_boss":
                door_buttons = draw_find_boss()
                for button in door_buttons:
                    if button.is_clicked(event.pos):
                        click_door(int(button.text))
                        break
            
            
            elif current_screen == "attack_input":
                direction_buttons = draw_attack_input()
                for button in direction_buttons:
                    if button.is_clicked(event.pos):
                        click_direction(button.text)
                        break
            
            
            elif current_screen == "attack_failed":
                if continue_to_route_button.is_clicked(event.pos):
                    begin_route_map()
            
            
            elif current_screen == "route_map":
                option_buttons = draw_route_map()
                for button in option_buttons:
                    if button.is_clicked(event.pos):
                        click_route_option(button.text)
                        break
            
            
            elif current_screen == "after_boss":
                if proceed_button.is_clicked(event.pos):
                    travel_to(destination)
            
            
            elif current_screen == "destination_reached":
                if proceed_button.is_clicked(event.pos):
                    travel_to(celebration)
            
            
            elif current_screen in ("ended_win", "ended_lose"):
                if restart_button.is_clicked(event.pos):
                    
                    current_screen = "menu"
                    current_location = starting
                    movement_history = Stack()
                    player_inventory = inventory()
                    current_dialogue = ""
                    shop_search_text = ""
                    gps_installed = False
                    boss_score = 0
                    boss_health = 3
    
    
    if current_screen == "show_sequence":
        if pygame.time.get_ticks() - sequence_show_time > 4000:
            begin_attack_input()
    
    
    if current_screen == "menu":
        draw_menu()
    elif current_screen == "intro":
        draw_intro()
    elif current_screen == "location":
        draw_location_screen()
    elif current_screen == "choices":
        draw_choice_screen()
    elif current_screen == "routes":
        draw_route_screen()
    elif current_screen == "shop":
        draw_shop_scene()
    elif current_screen == "police": 
        draw_police_screen()
    elif current_screen == "find_boss":
        draw_find_boss()
    elif current_screen == "show_sequence":
        draw_show_sequence()
    elif current_screen == "attack_input":
        draw_attack_input()
    elif current_screen == "attack_failed":
        draw_attack_failed()
    elif current_screen == "route_map":
        draw_route_map()
    elif current_screen == "after_boss":
        
        screen.fill((0, 0, 0))
        title_text = title_font.render("Boss Defeated", False, (100, 255, 100))
        title_rect = title_text.get_rect(center=(400, 35))
        screen.blit(title_text, title_rect)
        panel = pygame.Rect(40, 90, 720, 320)
        pygame.draw.rect(screen, (0, 0, 0), panel)
        pygame.draw.rect(screen, (255, 255, 255), panel, 2)
        render_text_block(current_dialogue, panel.x + 15, panel.y + 15, panel.width - 30, small_font)
        proceed_button.draw(screen)
    elif current_screen == "destination_reached":
        screen.fill((0, 0, 0))
        title_text = title_font.render("Delivery Successful!", False, (100, 255, 100))
        title_rect = title_text.get_rect(center=(400, 35))
        screen.blit(title_text, title_rect)
        panel = pygame.Rect(40, 90, 720, 320)
        pygame.draw.rect(screen, (0, 0, 0), panel)
        pygame.draw.rect(screen, (255, 255, 255), panel, 2)
        render_text_block(current_dialogue, panel.x + 15, panel.y + 15, panel.width - 30, small_font)
        proceed_button.draw(screen)
    elif current_screen == "ended_win":
        draw_ending_screen(won=True)
    elif current_screen == "ended_lose":
        draw_ending_screen(won=False)
    
    pygame.display.flip()
    clock.tick(60)
