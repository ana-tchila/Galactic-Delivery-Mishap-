# Galactic-Delivery-Mishap-

####5740479 

from collections import deque
import random
import time
import os
from boss_game import find_boss, space_boss_battle, route_map_challenge
from shop_system import Inventory, search_shop 
from shop_system import Inventory, search_shop 
from police_station import police_scan, assign_player_licence


class Location:
    """Represents each location in the game
    
    Stores name, description, connections to other locations, 
    and available actions"""
    def __init__(self, name: str, description: str, items: str=None):
        self.name = name
        self.description = description
        self.connections = {}
        self.choices = {}
        self.items = {}
        
    def add_choice(self, choice: str, response: str):
        """Adds a player interaction choice to the location"""
        self.choices[choice] = response

    def add_item(self, item: str, description: str):
        """Adds a item and description to the location"""
        self.items[item] = description


class Graph: 
    """Stores location objects indexed by name 

    Methods: 
        add_location()
         create_connections()
        find_location()
    """ 
    def __init__(self):
        self.locations = {}

    def add_location(self, location): 
        """Checks locations and adds it to the dictionary"""
        if location.name not in self.locations: 
            self.locations[location.name] = location
        else: 
            return None

    def add_connection(self, from_location, to_location, two_way=True):
        """Adds a connection between two locations
        
        Keyword arguments:
        two_ways (bool): makes connection reciprocal 
        """
        if from_location.name not in self.locations or to_location.name not in self.locations:
            return None
        self.locations[from_location.name].connections[to_location.name] = to_location
        if two_way:
            self.locations[to_location.name].connections[from_location.name] = from_location

    def find_location(self, location_n):
        """Finds the location in the dictionary"""
        if location_n in self.locations:
            return self.locations[location_n]
        else:
            return None

# Creating graph instance 
galaxy = Graph()

# Creating locations 
starting = Location( 'Start Point', 'You look around and see empty space') 
garage = Location( 'Garage', 'Shell plc gas station, where people can refuel and get their vehicles fixed') 
police = Location( 'Police check point', 'A checkpoint is ahead - you need to show your driver license to pass through') 
diner = Location( 'Diner', 'A Diner that offers more than food: community') 
shop = Location( 'Antique Shop', 'Every item has its use - find what is useful for you') 
parade = Location( 'Alien Parade', 'The Alien Parade')
destination = Location( 'Roupell Street SE1', 'House of Brad Cooper') 
celebration = Location( 'Celebration', 'You made it to Brad Copper on time. Time for a promotion and well deserved party')

# Adding choices 
diner.add_choice("Talk to the Bartender", "Bartender: Do I look like a GPS system to you? \n" 
"Go to the parade, you will fit right in with the crowd there.")
diner.add_choice("Talk to the old man at the counter", "OLD MAN: You younger generation, always dependent on technology.\n"
"In the old days we used our brains. Go to the Antique shop, you might find a map. If you can even read it.") 
garage.add_choice("Talk to the Mechanic", "I am sorry,\n"
"but we do not have the parts to fix your GPS system. You might want to rest at the diner.")
shop.add_choice("Talk to the Shopkeeper", "Welcome to my humble shop, stranger! \n" 
"You can find the GPS you are searching for somewhere in my shop")

# Adding items 
shop.add_item("GPS", "It looks old and rusty, but it works like it is new")
shop.add_item("Raygun", "A buddy from your planet with a funny accent sold me this weapon.\n" 
"He told me it is one of his best creations.") 
shop.add_item("Cap", "This is such an antique, back from the time when people lived on Earth.")
shop.add_item("Gloop", "Do not shake it")

# Adding locations to the graph 
galaxy.add_location(starting) 
galaxy.add_location(garage) 
galaxy.add_location(diner) 
galaxy.add_location(shop) 
galaxy.add_location(police) 
galaxy.add_location(parade) 
galaxy.add_location(destination) 
galaxy.add_location(celebration) 

# Creating the edges 
galaxy.add_connection(starting, garage, False)
galaxy.add_connection(starting, diner, False) 
galaxy.add_connection(garage, diner, False) 
galaxy.add_connection(diner, shop, False) 
galaxy.add_connection(diner, parade, False) 
galaxy.add_connection(shop, garage, False)
galaxy.add_connection(parade, destination, False) 
galaxy.add_connection(police, destination, False)

# For BFS use 
def make_connections_reciprocal(): 
    """ Makes the connections between the locations reciprocal""" 
    galaxy.add_connection(starting, garage) 
    galaxy.add_connection(starting, diner) 
    galaxy.add_connection(garage, diner) 
    galaxy.add_connection(diner, shop) 
    galaxy.add_connection(diner, parade) 
    galaxy.add_connection(shop, garage)
    galaxy.add_connection(parade, destination) 
    galaxy.add_connection(police, destination)
    galaxy.add_connection(shop, celebration) 
    galaxy.add_connection(starting, celebration)
    galaxy.add_connection(diner, celebration) 
    
def bfs(start, goal):
    """ Breadth-First Search algorithm to find the shortest path"""
    visited = {start}
    queue = deque([[start]])

    while queue:

        path = queue.popleft()
        
        current_location = path[-1]
        if current_location == goal:
            return path

        for neighbor in current_location.connections.values():
            if neighbor not in visited:
                visited.add(neighbor)
                
                new_path = list(path)
                new_path.append(neighbor)
                
                queue.append(new_path)

    return None


class Stack:
    """Implements a first in last out data structure""" 
    def __init__(self):
        self.stack = []

    def push(self, item):
        """Adds an item to the top of the stack"""
        return self.stack.append(item)

    def is_empty(self):
        """Checks if the stack is empty"""
        return len(self.stack) == 0

    def pop(self):
        """Removes and returns the item at the top of the stack"""
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None
    
    def peek(self):
        """Returns the item at the top of the stack without removing it""" 
        if not self.is_empty():
            return self.stack[-1]
        else:
            return None

# User input to start the game and decide if the player wants to play or not 

if __name__ == "__main__": # For the GUI to work 

# User input to start the game and decide if the player wants to play or not 
    while True:
        response = input(
        "You are an intergalactic space delivery driver.\n"
        "You have just received an urgent food order to Roupell Street SE1.\n"  
        "Are you ready to start the delivery? (yes/no) " 
        ) 
        # make user input lowercase and remove space 
        if response.lower().strip() == "yes":
            game_running = True
            print(
            "Great! You have accepted the delivery.\n" 
            "Your GPS is calculating the fastest route.. . .  .\n"
            "ERROR: GPS CONNECTION LOST.\n" 
            "You must navigate through the galaxy on your own." 
            ) 
            break
        
        elif response.lower().strip() == "no":
            game_running = False
            print("The delivery has been assigned to another driver.")
            break 
        
        else: 
            print("Invalid input, please enter yes or no.") 


# Actual game loop 
    current_location = starting
    movement_history = Stack() # Stack to keep track of the movement history 
    player_inventory = Inventory()
    player_licence = assign_player_licence()

    while game_running: 

        print(f"Current Loccation: {current_location.description}")

        # Special locations
        if current_location == shop: 
            item_wanted = input("What are you looking for in the shop? ").strip() 
            result = search_shop(current_location, item_wanted, player_inventory)
            print(result) 

        elif current_location == parade: 
            print("You see a large ship in the sky.\n"
            "You know the model of the ship and know it has GPS.\n"
            "You decide to defeat the Alien king and take the ship\n") 

            find_boss() 
            space_boss_battle()
            route_map_challenge() 

            print("You have defeated the Alien King")
            print("You know can now take the ship anywhere you want")
    
        elif current_location == garage and movement_history.peek() == shop: 
            if police not in current_location.connections.values(): 
                galaxy.add_connection(garage, police, False) 
                print("Mechanic installed the GPS and it is now working!")
                print("GPS calculating the fastest route to the destination . . .")
                print("Shortest Route --> Garage -> Police Checkpooint --> Destination")

                current_location = police 
                continue 

        elif current_location == police: 
            print("POLICE CHECKPOINT")
            print("Officer: Show your licence")

            print(f"Here is my licence: {player_licence}")
            result = police_scan(player_licence)

            if result == "Access Denied": 
                print("GAME OVER")
                print("You were arrested for using and invalid licence")
                break  

            else: 
                print("Access Granted to pass")

        elif current_location == destination: 
            print("Congratulations! You have successfully delivered the package to Brad Cooper on time.")
            print("Notification Alert: A message from Boss")
            print("Boss: Great job on the delivery! You earned a promotion.")
            print("Boss: I am throwing a party to celebrate our success, you are invited!")
            print("Boss: See you at the celebration!")
            
            make_connections_reciprocal()
            shortest_path = bfs(destination, celebration) 

            print("GPS is calculating the fastest route to the celebration .  .  .")
            print("Shortest path to the celebration:")

            for location in shortest_path: 
                print(location.name) 

            break
        
        # Normal connections/ displaying choices 
        elif current_location.choices:
            print("Available choices:")

            for choice in current_location.choices.keys(): 
                print(f"- {choice}") 
            user_choice = input("What do you want to do? ").strip() 
            if user_choice in current_location.choices: 
                print(current_location.choices[user_choice]) 
            else: 
                print("Invalid choice, please type the choice exactly as shown.")  
                continue 
        
        # Changing the location 
        print(f"Available routes: {list(current_location.connections.keys())}") 
        user_input = input("Where do you want to go? ").strip() 

        if user_input in current_location.connections:
            movement_history.push(current_location) 
            current_location = current_location.connections[user_input] 
        else: 
            print("Invalid location, please try again.")

#5740479 
