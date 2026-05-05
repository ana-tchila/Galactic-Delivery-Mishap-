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
			return none # Returns none 

	def add_connection(self, from_location, to_location, two_way = True): 
		"""Adds a connection (edge) between two locations. 
		
		It adds to_location to the connections of the from_location
		If two_way = True then connection is undirected."""

		if from_location not in self.locations or to_locations not in self.location: #Checks library 
			return None 
		self.location[from_location.name].connections[to_location.name] = to_location # Adds connection 
		if two_way: 
			self.location[to_location.name].connection[from_location.name] = from_location #Makes connection undirected 

	def find_location(self, location_n) 
		"""Finds the location in the dictionary
		
		Checks self.locations and returns the object""" 
		if location_n in self.locations: # Checks location in the library 
			return self.locations[location_n] # Returns the location object 
		else: 
			return None # Returns None  

#Implementation of the Graph 
galaxy = Graph()

#Adding the Nodes 
start = Location( 'Start Point', 'Oooops the GPS broke down') 
garage = Location( 'Garage', 'Shell plc gas station, where people can recharge their vehicles and get their vehicles fixed') 
diner = Location( 'Diner', 'A Diner that offers more food: community') 
shop = Location( 'Antique Shop', 'Every item has its use - find what is useful for you') 
##5752030
##shopkeeper = location( "shoopkeeper", "Welcome to my humble shop, starngar!", "You can find things from all around the universe here!")
##gps = location( "GPS", "Is this what you are looking for?", "Luckily, some guy sold me his old bike scraps, and this is one of the parts which are in good condition", "It looks rusty and old, but I assure you, it works like it is brand new!")
##raygun = location( "Raygun", "A buddy from your planet with a funny accent called Richtofen sold me this weapon", "He told me it is one of his best creations or something....", "Yeah, it looks as weird as him")
#5752030
parade = Location( 'Alien Parade', 'Fun like you have never experienced before, join the alien king on his ship')
destination = Location( 'Roupell Street SE1', 'House of Brad Cooper') 
Celebration = Location( 'Celebration', 'You made it to Brad Copper on time. Time for a promotion and well deserved party') 

#Adding Nodes to the Graph 
galaxy.add_location(starting) 
galaxy.add_location(garage) 
galaxy.add_location(diner) 
galaxy.add_location(shop) 
#galaxy.add_location(shopkeeper)
#galaxy.add_location(gps)
#galaxy.add_location(raygun)
galaxy.add_location(parade) 
galaxy.add_location(destination) 
galaxy.add_location(celebration) 

#Creating the edges 
galaxy.add_connection(starting, garage, False) #One way connection only 
galaxy.add_connection(starting, diner) 
galaxy.add_connection(garage, diner) 
galaxy.add_connection(diner, shop) 
###5752030
##galaxy.add_connection(shop, shopkeeper)
##galaxy.add_connection(shop, gps)
##galaxy.add_connection(shop, raygun)
##5752030
galaxy.add_connection(diner, parade) 
galaxy.add_connection(shop, garage) 
galaxy.add_connection(parade, destination) 
galaxy.add_connection(garage, destination) 
galaxy.add_connection(start, celebration) 
galaxy.add_connection(shop, celebration) 

###5740479 

#User input and game loop 
current_location = starting #Starting point 

while True: #Loop for user input 
	
	response = input(
	"You have just received a new order, you need to go to Roupell Street SE1\n" 
	"and deliver the food on time.\n" 
	"Are you ready to start the delivery? (yes/no)" 
	) # Get user input 
	
	if response.lower().strip() == "yes": # make user input lowercase and remove space 
		game_running = True 
		print(
			"Great! You have accepted the delivery, you are now at the starting point.\n" 
			"Your GPS is now calculating the best route.\n"
			"Something is not working. The GPS is broken.\n" 
			"You need to find your way to Roupell Street on your own." 
		) 
	
	elif response.lower().strip() == "no": 
		game_running = False 
		print("The delivery has been assigned to another driver.")

	else: 
		print("Invalid input, please enter yer or not.") 

### When the game is running 

while game_running
	pass # pass for now 
	







