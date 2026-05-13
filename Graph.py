# Galactic-Delivery-Mishap-

####5740479 

from collections import deque
import random
import time
import os
from boss_game import find_boss, space_boss_battle, route_map_challenge
from shop_system import inventory, search_shop 

#Graph Node 

#Class Location (code for the nodes) 

class Location: 
	"""Represents each location in the game. 
	
	Stores name, description, connections to other locations, 
	and available actions."""
	def __init__(self, name: str, description:str, items: str = None): 
		self.name = name 
		self.description = description
		self.connections = {} #Dictionary to hold the connections (edges)
		self.choices = {} #Dictionary to hold the choices 
		self.items = {} #Items that can be found at the Antique Shop 
		

	def add_choice(self, choice:str, response:str): 
		"""Adds a player interaction choice to the location"""
		self.choices[choice] = response #adds the choice and its response to the dictionary
	
	def add_item(self, item: str, description:str): 
		"Adds a item and description to the location"
		self.items[item] = description # adds the items and its description to the dictionary 
		
#Graph that the user will be traversing 

class Graph: 
	"""Graph of locations connected by directed or undirected edges.  
	
	Stores location objects indexed by name and has 
	methods to add locations, create connections, and find the locations""" 
	def __init__(self): 
		self.locations = {} #dictionary to hold the locations 

	def add_location(self, location): 
		"""Adds a location node.
		
		It takes a location object, checks it in the self.locations dictionary. 
		If it is nonexistent location is added"""
		if location.name not in self.locations: # Checks location in the library 
			self.locations[location.name] = location # Adds location to the library 
		else: 
			return None # Returns none 

	def add_connection(self, from_location, to_location, two_way = True): 
		"""Adds a connection (edge) between two locations. 
		
		It adds to_location to the connections of the from_location
		If two_way = True then connection is undirected."""

		if from_location.name not in self.locations or to_location.name not in self.locations: #Checks library 
			return None 
		self.locations[from_location.name].connections[to_location.name] = to_location # Adds connection 
		if two_way: 
			self.locations[to_location.name].connections[from_location.name] = from_location #Makes connection undirected 

	def find_location(self, location_n): 
		"""Finds the location in the dictionary
		
		Checks self.locations and returns the object""" 
		if location_n in self.locations: # Checks location in the library 
			return self.locations[location_n] # Returns the location object 
		else: 
			return None # Returns None  

#Implementation of the Graph 
galaxy = Graph()

#Adding the Nodes 
starting = Location( 'Start Point', 'You look around and see empty space') 
garage = Location( 'Garage', 'Shell plc gas station, where people can refuel and get their vehicles fixed') 
police = Location( 'Police check point', 'A checkpoint is ahead - you need to show your driver license to pass through') 
diner = Location( 'Diner', 'A Diner that offers more food: community') 
shop = Location( 'Antique Shop', 'Every item has its use - find what is useful for you') 
parade = Location( 'Alien Parade', 'The Alien Parade')
destination = Location( 'Roupell Street SE1', 'House of Brad Cooper') 
celebration = Location( 'Celebration', 'You made it to Brad Copper on time. Time for a promotion and well deserved party')

#Adding choices to the nodes inside 
diner.add_choice("Talk to the Bartender", "Bartender: Do I look like a GPS system to you? \n" 
"Go to the parade, you will fit right in with the crowd there.")
diner.add_choice("Talk to the old man at the counter", "OLD MAN: You younger generation, always dependent on technology.\n"
"In the old days we used our brains. Go to the Antique shop, you might find a map. If you can even read it.") 
garage.add_choice("Talk to the Mechanic", "I am sorry,\n"
"but we do not have the parts to fix your GPS system. You might want to rest at the diner.")
shop.add_choice("Talk to the Shopkeeper", "Welcome to my humble shop, stranger! \n" 
"You can find the GPS you are searching for somewhere in my shop")

#Adding the items 
shop.add_item("GPS", "It looks old and rusty, but it works like it is new")
shop.add_item("Raygun", "A buddy from your planet with a funny accent sold me this weapon.\n" 
"He told me it is one of his best creations.") 
shop.add_item("Cap", "This is such an antique, back from the time when people lived on Earth.")
shop.add_item("Gloop", "Do not shake it")

#Adding Nodes to the Graph 
galaxy.add_location(starting) 
galaxy.add_location(garage) 
galaxy.add_location(diner) 
galaxy.add_location(shop) 
galaxy.add_location(police) 
galaxy.add_location(parade) 
galaxy.add_location(destination) 
galaxy.add_location(celebration) 

#Creating the edges 
galaxy.add_connection(starting, garage, False) #One way connection only 
galaxy.add_connection(starting, diner, False) 
galaxy.add_connection(garage, diner, False) 
galaxy.add_connection(diner, shop, False) 
galaxy.add_connection(diner, parade, False) 
galaxy.add_connection(shop, garage, False)
galaxy.add_connection(parade, destination, False) 
galaxy.add_connection(police, destination, False)

def make_connections_reciprocal(): 
	""" Makes the connections between the locations reciprocal for BFS usage.""" 

	galaxy.add_connection(starting, garage) #One way connection only 
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
	
#5740479 
#Breadth first Search 

def bfs(start, goal): 
	""" Breadth-First Search algorithm to find the shortest path

	Args: 
		start: starting location object.  
		goal: destination location object. """

	visited = {start} # Set to keep track of visited nodes 
	queue = deque([[start]]) # Queue to hold the paths to explore 

	while queue: 

		path = queue.popleft() # Get the first path from the queue 
		
		current_location = path[-1] #Get the last location in the path 
		if current_location == goal:
			return path # Return the path to reach the goal 

		for neighbor in current_location.connections.values(): # loops throught the connections of the current_location 
			if neighbor not in visited: # Check if the neighbor has not been visited 

				visited.add(neighbor) # Mark the current location as visited 

				new_path = list(path) # Create a new path with the neighbor 
				new_path.append(neighbor) 
				queue.append(new_path) # Add the new path to the queue

	return None # Return None if no path is found 
#5740479 


#5740479 

#Stack 
class Stack: 
	""" Stack data Structure """ 
	def __init__(self): 
		self.stack = [] # List to hold the stack elements 

	def push(self, item): 
		"""Adds an item to the top of the stack."""
		return self.stack.append(item) # returns item to the stack 

	def is_empty(self): 
		"""Checks if the stack is empty."""
		return len(self.stack) == 0 # Returns true if the stack is empty, false otherwise 

	def pop(self): 
		"""Removes and returns the item at the top of the stack."""
		if not self.is_empty(): #Check if the stack is not empty 
			return self.stack.pop() # Returns the item at the top of the stack
		else: 
			return None # Returns None if the stack is empty 
	
	def peek(self): 
		"""Returns the item at the top of the stack without removing it.""" 
		if not self.is_empty(): # Check if the stack is not empty 
			return self.stack[-1] #Returns the item a the top without removing it 
		else: 
			return None #Returns None if the stack is empty 

#5740479 


#5740479 

# User input to start the game and decide if the player wants to play or not 

if __name__ == "__main__": # For the GUI to work 

	while True: #Loop for user input 
	
		response = input(
		"You are an intergalactic space delivery driver.\n"
		"You have just received an urgent food order to Roupell Street SE1.\n"  
		"Are you ready to start the delivery? (yes/no) " 
		) # Get user input 
	
		if response.lower().strip() == "yes": # make user input lowercase and remove space 
			game_running = True 
			print(
				"Great! You have accepted the delivery.\n" 
				"Your GPS is calculating the fastest route.. . .  .\n"
				"ERROR: GPS CONNECTION LOST.\n" 
				"You must navigate through the galaxy on your own." 
			) 
			break #Exit the loop to start the game 
		
		elif response.lower().strip() == "no": 
			game_running = False 
			print("The delivery has been assigned to another driver.")
			break # Exit the loop to end the game
		
		else: 
			print("Invalid input, please enter yes or no.") 


# Actual game loop 
#5740479 

	current_location = starting # Set the current location to the starting point 
	movement_history = Stack() #Stack to keep track of the movement history 
	player_inventory = inventory() #creates an instance of Inventory Class

	while game_running: 

		print(f"Current Loccation: {current_location.description}")

		# Enter special locations with unique interactions here 
		if current_location == shop: 
			item_wanted = input("What are you looking for in the shop? ").strip() # Asks what the user is looking for 
			result = search_shop(current_location, item_wanted, player_inventory)
			print(result) 

		elif current_location == parade: 
			print("You see a large ship in the sky.\n"
			"You know the model of the ship and know it has GPS.\n"
			"You decide to defeat the Alien king and take the ship\n") 

			find_boss() # Call the function to find the boss 
			space_boss_battle() # Call the function for the space boss battle
			route_map_challenge() # Call the function for the route map challenge 

			print("You have defeated the Alien King")
			print("You know can now take the ship anywhere you want")
	
		elif current_location == garage and movement_history.peek() == shop: 
			if police not in current_location.connections.values(): #Check if the police checkpoint is already connected 
				galaxy.add_connection(garage, police, False) # One way connection from garage to police checkpoint 
				print("Mechanic installed the GPS and it is now working!")
				print("GPS calculating the fastest route to the destination . . .")
				print("Shortest Route --> Garage -> Police Checkpooint --> Destination")
	
		elif current_location == police: 
			pass
		
		elif current_location == destination: 
			print("Congratulations! You have successfully delivered the package to Brad Cooper on time.")
			print("Notification Alert: A message from Boss")
			print("Boss: Great job on the delivery! You earned a promotion.")
			print("Boss: I am throwing a party to celebrate our success, you are invited!")
			print("Boss: See you at the celebration!")
    		
			make_connections_reciprocal() # Make the connections reciprocal for BFS 
			shortest_path = bfs(destination, celebration) # Find the shortest path to the celebration 

			print("GPS is calculating the fastest route to the celebration .  .  .")
			print("Shortest path to the celebration:")

			for location in shortest_path: 
				print(location.name) # Print the names of the locations in the shortest path 
		
			break 
		
		#Normal connections 
		elif current_location.choices: #Check if there are choices at the current location 
			print("Available choices:")
			for choice in current_location.choices.keys(): 
				print(f"- {choice}") #Print the choices at the current location
			user_choice = input("What do you want to do? ").strip() # Get user input for the choice
			if user_choice in current_location.choices: 
				print(current_location.choices[user_choice]) # Print the response for the chosen action 
			else: 
				print("Invalid choice, please type the choice exactly as shown.") # Print an error message for invalid choice 
				continue # Skip the rest of the loop and ask for input again 
		
		print(f"Available routes: {list(current_location.connections.keys())}") # Print the available routes from the current location 
	
		user_input = input("Where do you want to go? ").strip() # Get user input for the next location 
		if user_input in current_location.connections:
			movement_history.push(current_location) # Push the new location to the stack 
			current_location = current_location.connections[user_input] # Move to the next location 
		else: 
			print("Invalid location, please try again.")
	
#5740479 
