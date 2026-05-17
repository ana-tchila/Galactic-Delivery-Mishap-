# ID:5752030


# Imports
from collections import deque
import random
import pygame
from sys import exit
from Graph import (
    galaxy, starting, garage, diner, police, shop, parade, destination,
    celebration, Stack, bfs, make_connections_reciprocal
)
from shop_system import search, Inventory, search_shop
from police_station import assign_player_licence, police_scan


# Pygame intallation and asset
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Intergalactic Delivery")
clock = pygame.time.Clock()

# Error handling to ensure the file works if it didnt find a the costume font and the music file.
# if not it playes with no music and handles the image
try:
    pygame.mixer.music.load('sound/music.ogg')
except pygame.error:
    print("Music file not found, continuing without sound.")
pygame.mixer.music.play(-1)
running = True
try:
    title_font = pygame.font.Font('font/Pixeltype.ttf', size=40)
    font = pygame.font.Font('font/Pixeltype.ttf', size=26)
    small_font = pygame.font.Font('font/Pixeltype.ttf', size=20)
except FileNotFoundError:
    print("Custom font not found — falling back to default font.")
    title_font = pygame.font.SysFont(None, 40)
    font = pygame.font.SysFont(None, 26)
    small_font = pygame.font.SysFont(None, 20)
try:
    player = pygame.image.load('player/bike.png')
    smaller_player = pygame.transform.scale(player, (70, 70))
except (pygame.error, FileNotFoundError):
    # Fallback to a coloured rectangle if the image is missing
    print("Player image not found — using fallback rectangle.")
    smaller_player = pygame.Surface((70, 70))
    smaller_player.fill((100, 200, 255))

player_x_pos = [0]

# Button class


class Button:
    """
    A clickable rectangular button with text label and hover effect.
    Buttons store their position, dimensions, and label text. The class
    provides methods to render the button, detect mouse clicks, and 
    detect mouse hover (which changes the border colour).

    Attributes:
        x (int): Top-left x coordinate of the button.
        y (int): Top-left y coordinate of the button.
        width (int): Width of the button in pixels.
        height (int): Height of the button in pixels.
        text (str): Text label displayed on the button.

    """

    def __init__(self, x, y, width, height, text):
        """
        Initialise a button with position, size, and text label.

        Args:
            x: Top-left x coordinate.
            y: Top-left y coordinate.
            width: Button width in pixels.
            height: Button height in pixels.
            text: Label text shown on the button.

        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, surface):
        """

        Render the button on the given Pygame surface.

        The button is drawn with a white fill and a black text label.
        The border changes colour when the mouse is hovering over it.
        Long text uses a smaller font to fit within the button.

        Args:
            surface: The Pygame surface to draw the button on.

        """

        # Use the smaller font for long text labels so they fit
        # inside the button without overflowing.
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
        """
        Check if a position lies within the button's bounds.

        Args:
            pos: A (x, y) tuple representing the mouse position.

        Returns:
            True if pos is inside the button rectangle.

        """
        return self.x <= pos[0] <= self.x + \
            self.width and self.y <= pos[1] <= self.y + self.height

    def is_hovered(self, pos):
        """

        Check if the mouse is hovering over the button.

        Currently identical to is_clicked since both check whether
        the mouse position falls inside the button's bounds.

        Args:
            pos: A (x, y) tuple representing the mouse position.

        Returns:
            True if pos is inside the button rectangle.

        """
        return self.is_clicked(pos)

# Text rendering helpers


def wrap_text(text, font, max_width):
    """
    Wrap long text into multiple lines that fit within a maximum width,
    as it splits the input text into words and groups them into lines based on
    the rendered pixel width of the given font. 

    Args:
        text: The input string to wrap.
        font: The Pygame font object used to measure text width.
        max_width: Maximum pixel width for each line.

    Returns:
      A list of strings, each fitting within max_width.

    """
    # First split on \n so explicit newlines in the source text
    # become paragraph breaks. Then word-wrap each paragraph
    # separately based on pixel width.
    words = text.split(' ')
    lines = []
    for paragraph in str(text).split('\n'):
        words = paragraph.split(' ')
        line = ""
        for word in words:
            test_line = line + word + " "

            # If adding this word keeps the line under max_width,
            # extend the line. Otherwise, save the current line
            # and start a new one with this word.
            if font.size(test_line)[0] <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        if line:
            lines.append(line.strip())
        # Preserve blank paragraphs (e.g. from "\n\n") so dialogue
        # spacing renders correctly.
        if paragraph == "":
            lines.append("")
    return lines


def render_text_block(text, x, y, max_width, font_used,
                      color=(255, 255, 255), line_spacing=5):
    """

    Render wrapped text onto the screen at a given position,
    as it wraps the text using wrap_text(), then renders each line below
    the previous one with consistent spacing. Returns the y-coordinate
    immediately after the last rendered line for chained rendering.

    Args:
        text: The text string to render (can contain \\n for line breaks).
        x: The x-coordinate where rendering begins.
        y: The y-coordinate where the first line is drawn.
        max_width: Maximum pixel width before wrapping to a new line.
        font_used: The Pygame font object used to render text.
        color: RGB tuple for text colour. Defaults to white.
        line_spacing: Extra pixels between consecutive lines.

    Returns:
        int: The y-coordinate just below the last rendered line.



    """

    lines = wrap_text(text, font_used, max_width)
    for line in lines:
        text_surface = font_used.render(line, True, color)
        screen.blit(text_surface, (x, y))
        y += text_surface.get_height() + line_spacing
    return y


def draw_inventory_bar():
    """

    Draw the player's inventory as a horizontal bar at the bottom of the screen.

    The bar shows a comma-separated list of items currently held by the
    player. If the inventory is empty, it displays "Empty" instead.

    Uses the global player_inventory variable as its data source.

    """
    pygame.draw.rect(screen, (40, 40, 40), (0, 555, 800, 45))
    pygame.draw.line(screen, (255, 255, 255), (0, 555), (800, 555), 2)

    if player_inventory.items:
        inv_display = ", ".join(player_inventory.items)
    else:
        inv_display = "Empty"

    text_surface = font.render(inv_display, False, (255, 255, 255))
    screen.blit(text_surface, (10, 565))


def get_visible_routes(location):
    """

    Return the list of route names visible at a given location.

    Not all graph connections should be shown to the player. This function
    filters the available routes based on the story flow and game state
    (e.g. the police checkpoint is only visible at the garage after the
    GPS has been installed by the mechanic).

    Args:
        location: A Location object from the graph.

    Returns:
         Names of locations the player can travel to from here


    """
    if location == starting:
        return [garage.name, diner.name]
    elif location == diner:
        return [shop.name, parade.name]
    elif location == shop:
        return [garage.name]
    elif location == garage:
        # The police checkpoint only unlocks after the player
        # visits the shop AND the mechanic installs the GPS.
        # Otherwise the only route back is the diner.
        if movement_history.peek() == shop and gps_installed:
            return [police.name]
        else:
            return [diner.name]
    elif location == police:
        return [destination.name]
    return []


def get_visible_choices(location):
    """

    Return the dialogue choices visible at a given location.

    Filters out dialogue options that no longer make sense given the
    game state. For example, the mechanic dialogue at the garage is
    hidden once the GPS has been installed.

    Args:
        location: A Location object from the graph.

    Returns:
        Choice text strings available at this location.



    """

    # Once the GPS is installed, the mechanic dialogue at the
    # garage is not wanted (hide it.)
    if location == garage and gps_installed:
        return []

    # These locations are event triggers (boss fight, ending),
    # not dialogue scenes.
    if location in (parade, destination, celebration):
        return []
    return list(location.choices.keys())


# Scene Drawing Functions

def draw_menu():
    """

    Draw the main menu screen with title and animated bike.

    Renders the game title, the Start Game button, and a player with a bike
    that scrolls across the screen. The player position updates each
    frame using the player_x_pos global, wrapping around when it
    leaves the right edge.

    """

    # Fill the screen with black and draw the button and text over it
    # Occurs in each scene/screen
    screen.fill((0, 0, 0))
    start_button.draw(screen)
    title_text = title_font.render(
        "Intergalactic Delivery", False, (255, 255, 255))
    screen.blit(title_text, (270, 100))
    pygame.draw.rect(screen, (255, 255, 255), (270, 150, 265, 5))

    # Animate the bike: move 2 pixels right each frame. When the
    # bike goes off the right edge, wrap it to just before the
    # left edge so it loops continuously.
    player_x_pos[0] += 2
    if player_x_pos[0] > 800:
        player_x_pos[0] = -70
    screen.blit(smaller_player, (player_x_pos[0], 200))


def draw_intro():
    """

    Draw the story introduction screen shown after Start Game.

    Displays the game title and a short narrative explaining that the
    player's GPS has failed. Includes a Continue button that proceeds
    to the first location screen when clicked.

    """
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
    """

    Draw the main location view with description and action buttons.

    Shows the current location's name, its description, and any active
    dialogue inside a bordered panel. Renders the action buttons
    (Talk / Search and/or Choose Route) below the panel, plus the
    inventory bar at the bottom.

    Uses globals: current_location, current_dialogue, action_buttons.


    """
    screen.fill((0, 0, 0))
    title_text = title_font.render(
        current_location.name, False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)
    pygame.draw.rect(screen, (255, 255, 255), (300, 85, 200, 5))

    # Bordered Panel for the dialogue
    # Occurs in every scene with a dialogue
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
    """

    Draw the dialogue choice screen at the current location.

    Displays the location description, any existing dialogue, a hint
    line, and the list of dialogue choice buttons. The player clicks
    a button to talk to that character or selects Back to return to
    the location screen.

    Uses globals: current_location, current_dialogue, choice_buttons.


    """
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
    """

    Draw the route selection screen with travel buttons.

    Lists the visible routes from the current location as buttons. The
    player clicks a button to travel there or selects Back to return
    to the location screen.

    Uses globals: current_location, route_buttons.


    """
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
    """

    Draw the antique shop screen with item search interface.

    Renders the shop description, the shopkeeper's dialogue or last
    search result, a text input box for typing item names, and the
    Leave Shop button. The player types an item name and presses
    Enter to run a linear search against the shop's inventory.

    Uses globals: shop, current_dialogue, shop_search_text.


    """
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
    # Search input box where the player types item names
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
    """

    Draw the final win or lose screen with the closing message.

    Shows a green "Congratulations!" title for wins, or a red
    "Game Over" title for losses, followed by the end_message text
    inside a bordered panel. A Play Again button below resets the
    game state and returns to the main menu.

    Args:
        won: True for the win screen, False for the lose screen.

    """
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


def begin_find_boss():
    global current_screen, boss_door, search_low, search_high, boss_message

    current_screen = "find_boss"  # Set the current screen to the boss challenge
    boss_door = random.randint(1, 15)
    search_low = 1
    search_high = 15

    boss_message = (
        "You see a large ship in the sky.\n"
        "You know the model of the ship and know it has GPS.\n"
        "You decide to defeat the Alien king and take the ship\n\n"
        "You enter a corridor with 15 locked doors.\n"
        "The boss is hiding behind one of them.\n"
        "Your scanner can split the door zone in half.\n"
        "Pick the middle door for better optimisation.\n"
    )


def draw_find_boss():
    screen.fill((0, 0, 0))  # empty screen

    title_text = title_font.render("Find the Boss", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    render_text_block(
        boss_message,
        panel.x + 15,
        panel.y + 15,
        panel.width - 30,
        font)

    # Create a list to store the buttons, so they doen't get overwritten
    door_buttons = []

    for i in range(1, 16):  # Create buttons for doors 1 to 15
        button = Button(30 + (i - 1) * 50, 450, 40, 40,
                        str(i))  # button placement and size
        button.draw(screen)
        door_buttons.append(button)  # Add to list - to the end

    return door_buttons

# This function is called when a door button is clicked, with the door number as an argument.


def click_door(door_number):

    global search_low, search_high, boss_message, current_screen

    middle_search = (search_high + search_low) // 2  # Get the middle value

    # Force player to choose the middle door
    if door_number != middle_search:
        boss_message = (f"You have to pick the middle door: {middle_search}")
        return

    # Correct door found
    elif door_number == boss_door:
        boss_message = ("You found the boss")

        begin_signal_sequence()  # move to the next challenge
        return

    # Behind lower value door
    elif door_number > boss_door:
        search_high = middle_search - 1
        boss_message = ("You must pick a lower value door.\n"
                        f"Search between {search_low} and {search_high}"
                        )
        return

    # Behind higher value door
    else:
        search_low = middle_search + 1
        boss_message = ("You must pick a higher value door.\n"
                        f"Search between {search_low} and {search_high}"
                        )
        return


def begin_signal_sequence():
    global current_screen, signal_sequence, sequence_show_time

    # Generate a random sequence of 3 signals and store in a deque
    signal_sequence = deque(random.choices(
        ["UP", "DOWN", "LEFT", "RIGHT"], k=3))

    # Get current time
    sequence_show_time = pygame.time.get_ticks()

    # Move to the screen that shows the sequence to the player
    current_screen = "show_sequence"


def draw_signal_sequence():
    global current_screen, signal_message, boss_health, sequence_show_time
    screen.fill((0, 0, 0))

    title_text = title_font.render("Boss Battle", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    # Adds spaces between the signals for better display
    sequence_dispaly = "   ".join(signal_sequence)
    info = (f"Memorize the sequence: {sequence_dispaly}\n\n"
            f"You have 5 seconds to memorize the sequence")
    render_text_block(info, panel.x + 15, panel.y + 15, panel.width - 30, font)


def begin_attack_input():
    global current_screen, signals_remaining, attack_message

    current_screen = "attack_input"
    signals_remaining = deque(signal_sequence)
    attack_message = "Repeat the sequence by clicking the signals in the correct order."


def draw_attack_input():
    screen.fill((0, 0, 0))

    title_text = title_font.render("Boss Battle", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    # Display the attack message, boss health and score to the player
    info = (f"{attack_message}\n\n Boss Health: {boss_health}\n\n Score: {score}")
    render_text_block(info, panel.x + 15, panel.y + 15,
                      panel.width - 30, font)  # Text placement and font

    direction_buttons = []  # List to store the direction buttons

    # Button layout, row  and column for each direction
    layout = [("UP", 0, 0), ("DOWN", 1, 0), ("LEFT", 0, 1), ("RIGHT", 1, 1)]

    button_width = 100
    button_height = 50
    gap = 20
    start_x = (800 - (2 * button_width + gap)) // 2
    start_y = 400

    for label, row, col in layout:  # Create buttons for each direction
        x = start_x + col * (button_width + gap)
        y = start_y + row * (button_height + gap)
        button = Button(x, y, button_width, button_height, label)
        button.draw(screen)
        direction_buttons.append(button)

    return direction_buttons  # return the buttons so we can check for clicks


def click_direction(direction):
    global boss_health, score, attack_message, current_screen

    # Get the next expected signal from the deque
    expected = signals_remaining[0]

    if direction == expected:
        signals_remaining.popleft()
        attack_message = "Correct! Keep going."

        if not signals_remaining:
            boss_health -= 1
            score += 1
            if boss_health == 0:
                begin_route_map()
            else:
                attack_message = f"You hit the boss! Boss health is now {boss_health}."
                begin_signal_sequence()  # Start a new sequence for the next attack
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

    render_text_block(
        attack_message +
        "\n\nMove to the route challenge",
        panel.x +
        15,
        panel.y +
        15,
        panel.width -
        30,
        font)

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

    # dijkstra's algorithm to find the optimal route
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

    # Build the route from Destination back to Base
    optimal_route = []
    current = "Destination"

    while current is not None:
        optimal_route.append(current)
        current = predecessor[current]

    # Make the reverse of route
    optimal_route.reverse()

    # turn the list into text
    optimal_route = " -> ".join(optimal_route)

    # Total cost of the optimal route
    optimal_cost = distance["Destination"]

    route_map_message = (
        "You need to outrun the Alien King to defeat him and take his ship.")


def draw_route_map():
    screen.fill((0, 0, 0))

    title_text = title_font.render(
        "Route Map Challenge", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 50))
    screen.blit(title_text, title_rect)

    panel = pygame.Rect(50, 90, 700, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)

    map_info = (f"{route_map_message}\n\n"
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
        font)

    route_options_buttons = []

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
    global current_screen, score, current_dialogue, optimal_route, optimal_cost, end_message

    route_choices = {
        "A": "Base -> Moon -> Destination",
        "B": "Base -> Mars -> Jupiter -> Destination",
        "C": "Base -> Mars -> Venus -> Destination",
    }

    chosen_letter = option[0]  # Get the letter from the button text
    # Get the corresponding route text
    chosen_route = route_choices[chosen_letter]

    if chosen_route == optimal_route:
        score += 1

        result = "You chose the optimal route and reached the destination safely! You win!"

        current_dialogue = (
            f"{result}\n\n"
            f"Total fuel cost of the best route: {optimal_cost}\n\n"
            "You defeated the Alien King! You can now take his ship anywhere."
        )
        current_screen = "after_boss"

    else:
        end_message = (
            "You chose a suboptimal route and got caught by space pirates!\n\n"
            " Game over."
        )
        current_screen = "ended_lose"


def draw_police_screen():
    """
    Draw the police checkpoint screen with scan button.

    Shows the police dialogue and the Scan Licence button. The
    actual scan logic (Bloom filter check) runs in the main 
    event loop when the button is clicked.

    """
    screen.fill((0, 0, 0))

    title_text = title_font.render("Police Checkpoint", False, (255, 255, 255))
    title_rect = title_text.get_rect(center=(400, 100))
    screen.blit(title_text, title_rect)  # Draws title text on the rectangle

    panel = pygame.Rect(40, 130, 720, 300)
    pygame.draw.rect(screen, (0, 0, 0), panel)  # Black textbox
    pygame.draw.rect(screen, (255, 255, 255), panel, 2)  # White outline

    text = current_dialogue
    render_text_block(text, panel.x + 15, panel.y + 15,
                      panel.width - 30, font)  # Text placement and font

    # Scan button to process the licence
    scan_button.draw(screen)


# Game state Installation
# These globals are modified throughout the game. Most functions
# that change them use the `global` keyword.
current_screen = "menu"
current_location = starting
movement_history = Stack()
current_dialogue = ""
player_inventory = Inventory()
shop_search_text = ""


# Progression flags
gps_installed = False
end_message = ""


# Boss battle state
boss_health = 3
player_licence = assign_player_licence()
boss_door = 0
search_low = 1
search_high = 15
boss_message = ""
score = 0
attack_message = ""
sequence_show_time = 0
optimal_route = []
optimal_cost = 0
route_map_message = ""

# Static Buttons
# Buttons that appear on multiple screens or have fixed positions.
# Dynamic buttons (route, choice, door) are built each frame in
# the builder functions below.
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


# Dynamic Button Builders
def build_action_buttons(location):
    """


    Build the list of action buttons shown at a given location.

    Decides whether to show the Talk / Search button, the Choose Route
    button, or both. If only one applies, a single centred button is
    returned; if both apply, the static talk_button and travel_button
    are used side by side.

    Args:
        location: The current Location object.

    Returns:
        list[Button]: The action buttons appropriate for this location.



    """
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
    """

    Build the list of dialogue choice buttons for a given location.

    Reads the visible choices for the location (filtered by
    get_visible_choices) and creates a button for each, stacked
    vertically and centred horizontally.

    Args:
        location: The current Location object.

    Returns:
        list[Button]: The choice buttons for this location.


    """
    buttons = []
    choices = get_visible_choices(location)
    # Taking the choices and its index to arrange the buttons
    for i, choice in enumerate(choices):
        x = (800 - 600) // 2
        y = 420 + i * 55
        buttons.append(Button(x, y, 600, 45, choice))
    return buttons


def build_route_buttons(location):
    """

    Build the list of travel route buttons for a given location.

    Reads the visible routes for the location (filtered by
    get_visible_routes) and creates a button for each, formatted as
    "Go to (location name)". The buttons are stacked vertically and
    centred horizontally.

    Args:
        location: The current Location object.

    Returns:
        list[Button]: The route buttons for this location.


    """
    buttons = []
    routes = get_visible_routes(location)
    # Taking the location and its index to arrange the buttons
    for i, route in enumerate(routes):
        x = (800 - 700) // 2
        y = 410 + i * 60
        buttons.append(Button(x, y, 700, 50, f"Go to {route}"))
    return buttons


def travel_to(location):
    """

    Move the player to a new location and trigger associated events.

    Updates the current location, pushes the previous one onto the
    movement history stack, and clears any active dialogue. Then handles
    location specific logic:
        - parade: triggers the boss battle
        - shop: switches to the shop screen with item search
        - garage (from shop with GPS): mechanic installs GPS
        - garage (from shop without GPS): triggers the lose ending
        - police: switches to the licence checkpoint screen
        - destination: shows BFS path to celebration
        - celebration: triggers the win ending

    Args:
        location: The Location object to travel to.

    Side effects:
        Modifies several globals: current_location, current_screen,
        current_dialogue, gps_installed, end_message.


    """
    global current_location, current_screen, current_dialogue
    global gps_installed, end_message

    # Track the previous location so we can detect specific
    # transitions (e.g. shop -> garage triggers the mechanic).
    previous_location = current_location
    movement_history.push(previous_location)
    current_location = location
    current_dialogue = ""

    # Parade: triggers the boss battle
    if current_location == parade:
        begin_find_boss()
        return

    # Shop: switch to the shop screen with item search
    if current_location == shop:
        current_screen = "shop"

        current_dialogue = (
            "Welcome to my humble shop, stranger! "
            "Type the name of an item to search for it.\n"
            # We don't need the small items available box
            "Items available: Raygun, GPS, Cap, Gloop"
        )
        return
    # GAarage: three different outcomes
    if current_location == garage:
        # Win path: came from shop carrying a GPS - mechanic installs it
        if movement_history.peek() == shop and player_inventory.has("GPS"):
            gps_installed = True

            current_dialogue = (
                "Mechanic: GPS installed and working perfectly!\n\n"
                "GPS calculating fastest route...\n"
                "Best path: Garage -> Police Checkpoint -> Destination"
            )
            current_screen = "location"
        # Normal entry: first visit from the starting point
        elif movement_history.peek() == starting:

            current_screen = "location"
        # Fail path: visited shop but didn't pick up GPS - game over
        else:
            end_message = ("You didn't pick up the GPS in the shop.\n"
                           "You had to go back to the diner.\n"
                           "There you got really, really, really drunk.\n"
                           "You were disappointed in yourself.\n"
                           "In your misery you wandered out of the diner.\n"
                           "You got so lost you are still trying to find your way.\n"
                           "THE END")

            current_screen = "ended_lose"

            return
    # Police: switch to licence checkpoint screen
    if current_location == police:
        current_screen = "police"
        current_dialogue = ("POLICE CHECKPOINT\n"
                            "Officer: Show your licence"
                            )

        return
    # Destination: show BFS path to celebration
    if current_location == destination:
        # Convert one-way edges to two-way so BFS can find a path.
        # The graph was built directional for story reasons; for
        # the final pathfinding we need full connectivity.
        make_connections_reciprocal()
        # Run breadth-first search as the main algorithm showcase
        path_to_celebration = bfs(destination, celebration)

        # Format the path for display; fallback if BFS returns None
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
     # Celebration: trigger win ending
    if current_location == celebration:
        end_message = (
            "You made it to the celebration party!\n\n"
            "Promotion confirmed. Drinks on the boss.\n\n"
            "THE END."
        )
        current_screen = "ended_win"
        return
    # Default - just show the new location's main screen
    current_screen = "location"


# Main Game Loop
while running:

    # Rebuild dynamic buttons every frame so they update when
    # the location or game state changes
    action_buttons = build_action_buttons(current_location)
    choice_buttons = build_choice_buttons(current_location)
    route_buttons = build_route_buttons(current_location)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Keyboard Input (shop search bar)
        if event.type == pygame.KEYDOWN and current_screen == "shop":
            if event.key == pygame.K_RETURN:
                # Run search only when something has been typed
                if shop_search_text.strip():
                    current_dialogue = search_shop(
                        shop, shop_search_text.strip(), player_inventory)
                    shop_search_text = ""
            elif event.key == pygame.K_BACKSPACE:
                shop_search_text = shop_search_text[:-1]
            else:
                # Only accept printable characters (filters Ctrl, Shift, etc.).
                # Cap at 24 chars so text fits in the input box visually.
                if event.unicode.isprintable() and len(shop_search_text) < 24:
                    shop_search_text += event.unicode

        # Mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Menu screen: Start Game button
            if current_screen == "menu":
                if start_button.is_clicked(event.pos):
                    current_screen = "intro"
             # Intro story: Continue button
            elif current_screen == "intro":
                if continue_button.is_clicked(event.pos):
                    current_screen = "location"
            # Main location view: branches to Talk or Travel
            elif current_screen == "location":
                for button in action_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Talk / Search":
                            current_screen = "choices"
                        elif button.text == "Choose Route":
                            current_screen = "routes"
                        break
            # Dialogue choices screen
            elif current_screen == "choices":
                for button in choice_buttons:
                    if button.is_clicked(event.pos):
                        if button.text == "Back":
                            current_screen = "location"
                        else:
                            current_dialogue = current_location.choices[button.text]
                            current_screen = "location"
                        break
            # Travel route selection screen
            elif current_screen == "routes":
                # Lookup table: convert button text back into a Location object
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
             # Shop screen: Leave Shop button (search is via keyboard)
            elif current_screen == "shop":
                if leave_shop_button.is_clicked(event.pos):
                    current_screen = "location"
                    current_dialogue = ""
            # Police checkpoint: run Bloom filter scan on the licence
            elif current_screen == "police":

                if scan_button.is_clicked(event.pos):

                    # Use the Bloom Filter instance
                    result = police_scan(player_licence)

                    if result == "Let the driver pass":

                        current_dialogue = (
                            "POLICE CHECKPOINT\n"
                            "Officer: Licence is valid\n"
                            "Let driver pass.\n"
                        )

                        # Let's the player pick the location
                        current_screen = "location"

                    else:
                        end_message = (
                            "POLICE CHECKPOINT\n"
                            "Officer: Invalid licence\n"
                            "GAME OVER\n"
                        )

                        # Terminate the game
                        current_screen = "ended_lose"
            # Boss battle stage 1: door clicks (binary search)
            elif current_screen == "find_boss":
                door_buttons = draw_find_boss()
                for button in door_buttons:
                    if button.is_clicked(event.pos):
                        click_door(int(button.text))
                        break
            # Boss battle stage 2: direction clicks (queue input)
            elif current_screen == "attack_input":
                direction_buttons = draw_attack_input()
                for button in direction_buttons:
                    if button.is_clicked(event.pos):
                        click_direction(button.text)
                        break
            # Stage 2 fail: continue to stage 3
            elif current_screen == "attack_failed":
                if continue_to_route_button.is_clicked(event.pos):
                    begin_route_map()
             # Boss battle stage 3: route option clicks (Dijkstra)
            elif current_screen == "route_map":
                option_buttons = draw_route_map()
                for button in option_buttons:
                    if button.is_clicked(event.pos):
                        click_route_option(button.text)
                        break
             # Boss defeated: continue to destination
            elif current_screen == "after_boss":
                if proceed_button.is_clicked(event.pos):
                    travel_to(destination)
            # Reached destination: continue to celebration
            elif current_screen == "destination_reached":
                if proceed_button.is_clicked(event.pos):
                    travel_to(celebration)
            # Win/lose screens: Play Again button resets the game
            elif current_screen in ("ended_win", "ended_lose"):
                if restart_button.is_clicked(event.pos):

                    # Reset ALL game state to initial values
                    current_screen = "menu"
                    current_location = starting
                    movement_history = Stack()
                    player_inventory = Inventory()
                    current_dialogue = ""
                    shop_search_text = ""
                    gps_installed = False
                    score = 0
                    boss_health = 3
                    player_licence = assign_player_licence()

    # TIMER: auto-advance from sequence display to input
    # After showing the signal sequence for 5 seconds, automatically
    # switch to the input stage. This forces the player to rely on
    # memory rather than reading the sequence as they enter it.
    if current_screen == "show_sequence":
        if pygame.time.get_ticks() - sequence_show_time > 5000:
            begin_attack_input()

    # Draw the current screen
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
