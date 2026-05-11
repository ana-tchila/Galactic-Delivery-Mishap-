# Galactic-Delivery-Mishap-

####5740479 

#Graph Node 

#Class Location (code for the nodes) 

class Location: 
	"""Represents each location in the game. 
	
	Stores name, description, connections to other locations, 
	and available actions."""
	def __init__(self, name: str, description:str): 
		self.name = name 
		self.description = description
		self.connections = {} #Dictionary to hold the connections (edges) 
		self.choices = [] #List of choices at the location 

	def add_choice(self, choice): 
		"""Method to add choices to the location's chocie list """
		self.choices.append(choice) #appends the list of choices 
		
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
garage = Location( 'Garage', 'Shell plc gas station, where people can recharge their vehicles and get their vehicles fixed') 
diner = Location( 'Diner', 'A Diner that offers more food: community') 
shop = Location( 'Antique Shop', 'Every item has its use - find what is useful for you') 
parade = Location( 'Alien Parade', 'Fun like you have never experienced before, join the alien king on his ship')
destination = Location( 'Roupell Street SE1', 'House of Brad Cooper') 
celebration = Location( 'Celebration', 'You made it to Brad Copper on time. Time for a promotion and well deserved party')


#Adding Nodes to the Graph 
galaxy.add_location(starting) 
galaxy.add_location(garage) 
galaxy.add_location(diner) 
galaxy.add_location(shop) 

#Adding choices to the nodes inside 
#shop.add_choice("Talk to the Shopkeeper")
#shop.add_choice("GPS")
#shop.add_choice("Raygun")

galaxy.add_location(parade) 
galaxy.add_location(destination) 
galaxy.add_location(celebration) 

#Creating the edges 
galaxy.add_connection(starting, garage, False) #One way connection only 
galaxy.add_connection(starting, diner) 
galaxy.add_connection(garage, diner) 
galaxy.add_connection(diner, shop) 
galaxy.add_connection(diner, parade) 
galaxy.add_connection(shop, garage) 
galaxy.add_connection(parade, destination) 
galaxy.add_connection(garage, destination) 
#galaxy.add_connection(starting, celebration) 
#galaxy.add_connection(shop, celebration) 
# Add connection later when the player gets to the destination 

#5740479 
#Breadth first Search 

from collections import deque #import the deque class for the queue 

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

current_location = starting #Starting point 

# User input to start the game and decide if the player wants to play or not 

while True: #Loop for user input 
	
	response = input(
	"You are an intergalactic space delivery driver.\n"
	"You have just received an urgent food order to Roupell Street SE1.\n"  
	"Are you ready to start the delivery? (yes/no)" 
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

while game_running: 
	
	print(f"Current location:{current_location.name}") #print the current location name
	print(current_location.description) #prints the current location description

	if current_location.choices: #Check if there are choices at the current location 
		print("Available choices:")
		for choice in current_location.choices: 
			print(f"- {choice}") #Print the choices at the current location
	
	print(list(current_location.connections.keys())) #prints the available connections from the current location 
	
	user_input = input("Where do you want to go?").strip() # Get user input for the next location 
	if user_input in current_location.connections:
		current_location = current_location.connections[user_input] # Move to the next location 
	else: 
		print("Invalid location, please try again.")


