# ID:5752030

from collections import deque
import random

import pygame
from sys import exit
from Graph import ( 
    galaxy, starting, garage, diner, police, shop, parade, destination, 
    celebration, Stack, bfs, make_connections_reciprocal
)
from shop_system import search, inventory, search_shop
from police_station import generate_licence, police_scan, player_licence, all_licences


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


# the Button class represents interactive buttons in the GUI, with methods
# to draw itself and check for clicks and hover states.
class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255),
                         (self.x, self.y, self.width, self.height))
        chosen_font = small_font if len(self.text) > 18 else font
        text_surface = chosen_font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(
            center=(
                self.x + self.width // 2,
                self.y + self.height // 2))
        surface.blit(text_surface, text_rect)
        if self.is_hovered(pygame.mouse.get_pos()):
            pygame.draw.rect(surface, (200, 200, 200),
                             (self.x, self.y, self.width, self.height), 3)
        else:
            pygame.draw.rect(surface, (100, 100, 100),
                             (self.x, self.y, self.width, self.height), 3)

    def is_clicked(self, pos):
        return self.x <= pos[0] <= self.x + \
            self.width and self.y <= pos[1] <= self.y + self.height

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


def render_text_block(text, x, y, max_width, font_used,
                      color=(255, 255, 255), line_spacing=5):
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
    title_text = title_font.render(
        "Intergalactic Delivery", False, (255, 255, 255))
    screen.blit(title_text, (270, 100))
    pygame.draw.rect(screen, (255, 255, 255), (270, 150, 265, 5))

    player_x_pos[0] += 2
    if player_x_pos[0] > 800:
        player_x_pos[0] = -70
    screen.blit(smaller_player, (player_x_pos[0], 200))


def draw_intro():
    screen.fill((0, 0, 0))
    title_text = title_font.render(
        "Intergalactic Delivery", False, (255, 255, 255))
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
    title_text = title_font.render(
        current_location.name, False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, (255, 255, 255), (300, 85, 200, 5))

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    body_text = current_location.description
    if current_dialogue:
        body_text += "\n\n" + current_dialogue

    render_text_block(
        body_text,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font)

    for button in action_buttons:
        button.draw(screen)
    draw_inventory_bar()


def draw_choice_screen():
    screen.fill((0, 0, 0))
    title_text = title_font.render(
        current_location.name, False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, (255, 255, 255), (300, 70, 200, 3))

    panel = pygame.Rect(40, 90, 720, 280)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    body_text = current_location.description
    if current_dialogue:
        body_text += "\n\n" + current_dialogue
    render_text_block(
        body_text,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font)

    hint_text = small_font.render(
        "Click a choice to continue", False, (255, 255, 255))
    hint_rect = hint_text.get_rect(center=(400, 380))
    screen.blit(hint_text, hint_rect)

    for button in choice_buttons:
        button.draw(screen)
    draw_inventory_bar()


def draw_route_screen():
    screen.fill((0, 0, 0))
    title_text = title_font.render(
        current_location.name, False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, (255, 255, 255), (300, 70, 200, 3))

    panel = pygame.Rect(40, 90, 720, 280)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)
    render_text_block(
        current_location.description,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font)

    hint_text = small_font.render(
        "Click a destination to travel", False, (255, 255, 255))
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
    render_text_block(
        shop_text,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font)

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
        title_text = title_font.render(
            "Congratulations!", False, (255, 255, 255))
    else:
        title_text = title_font.render("Game Over", False, (255, 255, 255))

    title_rect = title_text.get_rect(center=(400, 100))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 150, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)
    render_text_block(
        end_message,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font)

    restart_button.draw(screen)


# converting the boss game into functions to integrate to the GUI
boss_attempts: int = 3  # How many wrong clicks the player is allowed in the boss battle


def begin_find_boss():
    """
    Set up the Find the Boss challenge.
    Picks a random boss door and resets the binary search range.
    """
    global current_screen, boss_door, search_low, search_high
    global boss_message, boss_attempts, boss_health

    current_screen = "find_boss"

    # Pick a random door for the boss to hide behind
    boss_door = random.randint(1, 15)

    # Set the full search range — binary search will narrow this down
    search_low = 1
    search_high = 15

    # Reset lives and health for the battle ahead
    boss_attempts = 3
    boss_health = 3

    boss_message = (
        "You enter the building and see 15 doors. "
        "The boss is behind one of them. "
        "Which one do you choose?"
    )


def draw_find_boss():
    """
    Draw the Find the Boss screen.
    Shows the message panel and 15 door buttons for the player to click.
    Returns a list of door buttons so the game loop can check clicks.
    """
    screen.fill((0, 0, 0))

    title_text = title_font.render("Find the Boss", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    # White-bordered panel for the message text
    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    render_text_block(
        boss_message,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font
    )

    # Build a row of 15 door buttons across the bottom of the screen
    door_buttons = []

    for i in range(1, 16):
        # Space buttons evenly: each is 50px wide with a 10px gap on the left
        button = Button(30 + (i - 1) * 50, 450, 40, 40, str(i))
        button.draw(screen)
        door_buttons.append(button)

    return door_buttons


def click_door(door_number):
    """
    Handle the door the player clicked.
    Uses binary search to narrow down which door the boss is behind.
    The player must always pick the middle door of the remaining range.
    """
    global search_low, search_high, boss_message, boss_attempts

    # Cast to int to ensure the value is the correct type for comparison.
    # If something unexpected is passed in, catch it and show an error.
    try:
        door_number = int(door_number)
    except (ValueError, TypeError):
        boss_message = "Invalid door selection. Please click a door number."
        return

    # Binary search: the only valid guess is the midpoint of the range
    middle_search = (search_high + search_low) // 2

    # Force the player to follow binary search — reject any other door
    if door_number != middle_search:
        boss_message = f"You have to pick the middle door: {middle_search}"
        return

    # The player found the boss — move on to the signal battle
    if door_number == boss_door:
        boss_message = "You found the boss."
        boss_attempts = 3
        begin_signal_sequence()
        return

    # Boss is behind a lower door — discard the upper half of the range
    if door_number > boss_door:
        search_high = middle_search - 1
        boss_message = (
            "You must pick a lower value door.\n"
            f"Search between {search_low} and {search_high}"
        )
        return

    # Boss is behind a higher door — discard the lower half of the range
    search_low = middle_search + 1
    boss_message = (
        "You must pick a higher value door.\n"
        f"Search between {search_low} and {search_high}"
    )


def begin_signal_sequence():
    """
    Generate a random sequence of 3 directions and show it to the player.
    Uses a deque so signals can be read and removed from the front in order.
    The player has 5 seconds to memorise before the input screen appears.
    """
    global current_screen, signal_sequence, sequence_show_time

    # Generate 3 random directions and store them in a queue
    signal_sequence = deque(
        random.choices(["UP", "DOWN", "LEFT", "RIGHT"], k=3)
    )

    # Record when the sequence was shown so we can time the 5-second window
    sequence_show_time = pygame.time.get_ticks()
    current_screen = "show_sequence"


def draw_signal_sequence():
    """
    Draw the screen that shows the signal sequence to the player.
    Displays the full sequence for the player to memorise.
    """
    screen.fill((0, 0, 0))

    title_text = title_font.render("Boss Battle", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    # Join the deque into a readable string with spacing between signals
    sequence_display = "   ".join(signal_sequence)

    info = (
        f"Memorise the sequence: {sequence_display}\n\n"
        "You have 5 seconds to memorise the sequence."
    )

    render_text_block(
        info,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font
    )


def begin_attack_input():
    """
    Start the input phase of the Boss Battle.
    Copies the signal sequence into a working deque that gets consumed
    as the player clicks each direction.
    """
    global current_screen, signals_remaining, attack_message

    current_screen = "attack_input"

    # Copy the sequence into a working deque — we pop from this as the
    # player enters each signal, without destroying the original
    signals_remaining = deque(signal_sequence)

    attack_message = (
        "Repeat the sequence by clicking the signals in the correct order."
    )


def draw_attack_input():
    """
    Draw the Boss Battle input screen.
    Shows the attack prompt, boss health, score, mistake allowance,
    and four direction buttons for the player to click.
    Returns a list of direction buttons so the game loop can check clicks.
    """
    screen.fill((0, 0, 0))

    title_text = title_font.render("Boss Battle", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    # Show live stats so the player knows how they are doing
    info = (
        f"{attack_message}\n\n"
        f"Boss Health: {boss_health}\n"
        f"Score: {score}\n"
        f"Boss Mistakes Left: {boss_attempts}"
    )

    render_text_block(
        info,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font
    )

    direction_buttons = []

    # Tuple of (label, row, col) — a tuple is used here because this
    # layout never changes, making it immutable and safer than a list
    layout = (
        ("UP", 0, 0),
        ("DOWN", 1, 0),
        ("LEFT", 0, 1),
        ("RIGHT", 1, 1)
    )

    button_width = 100
    button_height = 50
    gap = 20

    # Centre the 2x2 grid horizontally on the 800px wide screen
    start_x = (800 - (2 * button_width + gap)) // 2
    start_y = 400

    for label, row, col in layout:
        x = start_x + col * (button_width + gap)
        y = start_y + row * (button_height + gap)

        button = Button(x, y, button_width, button_height, label)
        button.draw(screen)
        direction_buttons.append(button)

    return direction_buttons


def click_direction(direction):
    """
    Handle the player clicking a direction button in the Boss Battle.
    Checks if the direction matches the next signal in the deque.
    A full correct sequence damages the boss by one health point.
    Three total wrong clicks across all sequences ends the game.
    """
    global boss_health, score, attack_message, current_screen
    global boss_attempts, end_message

    # The next expected signal is always at the front of the queue
    expected = signals_remaining[0]

    if direction == expected:
        # Correct — remove this signal from the front of the queue
        signals_remaining.popleft()
        attack_message = "Correct! Keep going."

        # All signals entered — the player successfully attacked the boss
        if not signals_remaining:
            boss_health -= 1
            score += 1

            if boss_health == 0:
                # Boss defeated — move to the final route map challenge
                begin_route_map()
            else:
                attack_message = (
                    f"You hit the boss! Boss health is now {boss_health}."
                )
                # Start a new sequence for the next attack round
                begin_signal_sequence()

        return

    # Wrong direction — use up one of the player's mistake allowances
    boss_attempts -= 1

    if boss_attempts == 0:
        # No attempts left — the boss wins
        end_message = (
            "You made 3 mistakes in the boss battle.\n\n"
            "The boss defeated you.\n\n"
            "Game over."
        )
        current_screen = "ended_lose"
        return

    # Still have attempts left — show feedback and restart the sequence
    attack_message = (
        f"Wrong signal! Expected {expected}.\n\n"
        f"Boss mistakes left: {boss_attempts}"
    )
    begin_signal_sequence()


def begin_route_map():
    """
    Set up the Route Map challenge.
    Runs Dijkstra's algorithm on the space graph to find the cheapest
    route from Base to Destination. Stores the result for the player
    to compare against their choice.
    """
    global current_screen, optimal_route, optimal_cost, route_map_message

    current_screen = "route_map"

    # Weighted graph where each value is the fuel cost between locations
    space_graph = {
        "Base": {"Moon": 4, "Mars": 5},
        "Moon": {"Destination": 8},
        "Mars": {"Jupiter": 3, "Venus": 6},
        "Jupiter": {"Destination": 2},
        "Venus": {"Destination": 4},
        "Destination": {},
    }

    # Start all distances at infinity — we haven't explored anything yet
    distance = {node: float('inf') for node in space_graph}

    # predecessor stores the previous node on the best known path to each node
    predecessor = {node: None for node in space_graph}

    # The start node costs nothing to reach
    distance["Base"] = 0
    unexplored = list(space_graph)

    # Dijkstra's main loop — always visit the cheapest unexplored node next
    while unexplored:
        current = min(unexplored, key=lambda node: distance[node])
        unexplored.remove(current)

        for neighbor, cost in space_graph[current].items():
            alt = distance[current] + cost

            # If this path is cheaper, update the best known distance
            if alt < distance[neighbor]:
                distance[neighbor] = alt
                predecessor[neighbor] = current

    # Trace back from Destination to Base using the predecessor chain
    optimal_route = []
    current = "Destination"

    while current is not None:
        optimal_route.append(current)
        current = predecessor[current]

    # The trace goes backwards, so reverse it to read start to finish
    optimal_route.reverse()

    # Convert the list to a human-readable route string
    optimal_route = " -> ".join(optimal_route)

    # Store the total fuel cost of the best route
    optimal_cost = distance["Destination"]

    route_map_message = (
        "You need to outrun the Alien King to defeat him "
        "and take his ship."
    )


def draw_route_map():
    """
    Draw the Route Map challenge screen.
    Shows all routes and their fuel costs, then presents three
    route buttons for the player to choose from.
    Returns a list of route buttons so the game loop can check clicks.
    """
    screen.fill((0, 0, 0))

    title_text = title_font.render(
        "Route Map Challenge", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    # Display the full map so the player can calculate the best route
    map_info = (
        f"{route_map_message}\n\n"
        "ROUTE MAP:\n"
        "Base -> Moon (cost 4)\n"
        "Base -> Mars (cost 5)\n"
        "Moon -> Destination (cost 8)\n"
        "Mars -> Jupiter (cost 3)\n"
        "Mars -> Venus (cost 6)\n"
        "Jupiter -> Destination (cost 2)\n"
        "Venus -> Destination (cost 4)"
    )

    render_text_block(
        map_info,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font
    )

    route_options_buttons = []

    # The three possible routes the player can choose from
    routes = [
        "A: Base -> Moon -> Destination",
        "B: Base -> Mars -> Jupiter -> Destination",
        "C: Base -> Mars -> Venus -> Destination",
    ]

    button_y = 395

    for i, route in enumerate(routes):
        button = Button(50, button_y + i * 60, 700, 50, route)
        button.draw(screen)
        route_options_buttons.append(button)

    return route_options_buttons


def click_route_option(option):
    """
    Handle the route the player chose.
    Compares their choice against the optimal route from Dijkstra's.
    A correct choice wins the boss battle, a wrong choice ends the game.
    """
    global current_screen, score, current_dialogue
    global optimal_route, optimal_cost, end_message

    # Map each letter to its full route string for easy comparison
    route_choices = {
        "A": "Base -> Moon -> Destination",
        "B": "Base -> Mars -> Jupiter -> Destination",
        "C": "Base -> Mars -> Venus -> Destination",
    }

    # Extract just the letter from the button text to look up the route.
    # Cast to str to be safe, then take the first character.
    # If the letter is not in route_choices, catch the KeyError gracefully.
    try:
        chosen_letter = str(option)[0]
        chosen_route = route_choices[chosen_letter]
    except (KeyError, IndexError):
        end_message = (
            "Something went wrong with the route selection.\n\n"
            "Game over."
        )
        current_screen = "ended_lose"
        return

    if chosen_route == optimal_route:
        # Player picked the cheapest route — boss battle won
        score += 1

        result = (
            "You chose the optimal route and reached "
            "the destination safely! You win!"
        )

        current_dialogue = (
            f"{result}\n\n"
            # Cast optimal_cost to str explicitly for safe string formatting
            f"Total fuel cost of the best route: {str(optimal_cost)}\n\n"
            "You defeated the Alien King! You can now take his ship anywhere."
        )
        current_screen = "after_boss"
        return

    else:
        # Player picked a slower route and got caught
        end_message = (
            "You chose a suboptimal route and got caught by space pirates!\n\n"
            "Game over."
        )
        current_screen = "ended_lose"
        return 

# 5758609
def draw_licence_select():
    """
    Draw the licence selection screen.
    Shows all 10 generated licences as buttons for the player to pick from.
    The player does not know which ones are valid — that is the challenge.
    Returns a list of licence buttons so the game loop can check clicks.
    """
    screen.fill((0, 0, 0))
 
    title_text = title_font.render("Police Checkpoint", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
 
    panel = pygame.Rect(40, 80, 720, 80)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)
 
    render_text_block(
        "Officer: Show your licence.\nPick one of the licences below.",
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font
    )
 
    # Build two rows of 5 licence buttons
    licence_buttons = []
 
    for i, licence in enumerate(all_licences):
        row = i // 5  # 0 for first row, 1 for second row
        col = i % 5   # column position 0 to 4
        x = 50 + col * 145
        y = 200 + row * 80
        button = Button(x, y, 130, 50, licence)
        button.draw(screen)
        licence_buttons.append(button)
 
    return licence_buttons
 
 
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
player_licence = None  # Set to None until the player picks one at the checkpoint
 
boss_health = 3
boss_door = 0
search_low = 1
search_high = 15
boss_message = ""
signal_sequence = deque()
signals_remaining = deque()
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
            # We don't need the small items available box
            "Items available: Raygun, GPS, Cap, Gloop"
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
            end_message = ("You didn't pick up the GPS in the shop.\n"
                    "You had to go back to the diner.\n"
                    "There you got really, really, really drunk.\n" 
                    "You were dissapointed in yourself.\n"
                    "In your misery you wandered out of the diner.\n"
                    "You got so lost you are still trying to find your way.\n"
                    "THE END"
                           )
            current_screen = "ended_lose"
        return
 
    # Player arrives at police — show licence selection screen first
    if current_location == police:
        current_screen = "licence_select"
        return
 
    if current_location == destination:
            # Use BFS to find path to celebration as the algorithm showcase
            make_connections_reciprocal()
            path_to_celebration = bfs(destination, celebration)
            path_text = " -> ".join(
                loc.name for loc in path_to_celebration) if path_to_celebration else "Celebration"
            current_dialogue = (
                "Congratulations! Package delivered to Brad Cooper on time.\n\n"
                "Boss: Great job! You earned a promotion. "
                "Come to my celebration party!\n\n"
                f"GPS calculating route to celebration:\n{path_text}"
            )
            current_screen = "destination_reached"
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
                    current_dialogue = search_shop(
                        shop, shop_search_text.strip(), player_inventory)
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
 
            # Player picks a licence from the list
            elif current_screen == "licence_select":
                licence_buttons = draw_licence_select()
                for button in licence_buttons:
                    if button.is_clicked(event.pos):
                        player_licence = button.text
                        current_dialogue = (
                            "POLICE CHECKPOINT\n"
                            f"Your licence: {player_licence}\n"
                            "Officer: Let me scan that."
                        )
                        current_screen = "police"
                        break
 
            elif current_screen == "police": 
                
                if scan_button.is_clicked(event.pos):

                    if scan_button.text == "Scan Licence":
                        result = police_scan(player_licence)

                        if result == "Let the driver pass":
                            current_dialogue = (
                            "POLICE CHECKPOINT\n"
                            "Officer: Licence is valid\n"
                            "Let driver pass.\n\n"
                            "Click Continue."
                            )
                            scan_button.text = "Continue"

                        else:
                            end_message = (
                            "POLICE CHECKPOINT\n"
                            "Officer: Invalid licence\n"
                            "GAME OVER\n"
                            )
                            current_screen = "ended_lose"

                        
                    elif scan_button.text == "Continue":
                        scan_button.text = "Scan Licence"
                        travel_to(destination)
            
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
                    score = 0
                    boss_health = 3
                    player_licence = None  # Reset licence on restart
 
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
    elif current_screen == "licence_select":
        draw_licence_select()
    elif current_screen == "police": 
        draw_police_screen()
    elif current_screen == "find_boss":
        draw_find_boss()
    elif current_screen == "show_sequence":
        draw_signal_sequence()
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
        render_text_block(
            current_dialogue,
            panel.x + 15,
            panel.y + 15,
            panel.width - 30,
            small_font)
        proceed_button.draw(screen)
    elif current_screen == "destination_reached":
        screen.fill((0, 0, 0))
        title_text = title_font.render(
            "Delivery Successful!", False, (100, 255, 100))
        title_rect = title_text.get_rect(center=(400, 35))
        screen.blit(title_text, title_rect)
        panel = pygame.Rect(40, 90, 720, 320)
        pygame.draw.rect(screen, (0, 0, 0), panel)
        pygame.draw.rect(screen, (255, 255, 255), panel, 2)
        render_text_block(
            current_dialogue,
            panel.x + 15,
            panel.y + 15,
            panel.width - 30,
            small_font)
        proceed_button.draw(screen)
    elif current_screen == "ended_win":
        draw_ending_screen(won=True)
    elif current_screen == "ended_lose":
        draw_ending_screen(won=False)
 
    pygame.display.flip()
    clock.tick(60)
