# Galactic-Delivery-Mishap-

####5740479 

#Graph Node 

#Class Location (code for the nodes) 

class Location: 
	""" Class that will represent each location in the game. 
	Each location has a name, description, connections to other locations, and actions that can be taken at the location."""
	def __init__(self, name: str, description:str): 
        self.name = name 
        self.description = description
        self.connections = {} #Dictionary to hold the connections (edges) 
        self.choices = [] #List of choices at the location 

#Graph that the user will be traversing 

class Graph: 
	""" Class graph to represent the map of locations(nodes) and their connections(edges) in the game. 
	It will have methods to add locations, and connections.""" 
	def __init__(self): 
		self.locations = {} #dictionary to hold the locations 

	def add_location(self, location): 
		"""Method to add a location node to the graph. 
		It takes a location object and checks if is is in the self.locations dictionary. 
		If it doesn't exist location is added to the library"""
		if location.name not in self.locations: # Checks if location is in the library 
			self.locations[location.name] = location # Adds location in the library 
		else: 
			return none # Returns none 

	def add_connection(self, from_location, to_location): 
		""" Method to add a connection(edge) between two locations on the graph.
		It does this by adding to_location to the connections of the from_location"""
		self.locations[location.name].connections[location.name] = to_location 

#Implementation of the Graph 
galaxy = Graph()

#Adding the Nodes 
start = Location( 'Start Point', 'Oooops the GPS broke down') 
garage = Location( 'Garage', 'Shell plc gas station, where people can recharge their vehicles and get their vehicles fixed') 
diner = Location( 'Diner', 'A Diner that offers more food: community') 
shop = Location( 'Antique Shop', 'Every item has its use - find what is useful for you') 
parade = Location( 'Alien Parade', 'Fun like you have never experienced before, join the alien king on his ship')
destination = Location('Roupell Street SE1', 'House of Brad Cooper') 

#Adding Nodes to the Graph 
galaxy.add_location(starting) 
galaxy.add_location(garage) 
galaxy.add_location(diner) 
galaxy.add_location(shop) 
galaxy.add_location(parade) 
galaxy.add_location(destination) 

#Creating the edges 
galaxy.add_connection(starting, garage) 
galaxy.add_connection(starting, diner) 
galaxy.add_connection(garage, diner) 
galaxy.add_connection(diner, shop) 
galaxy.add_connection(diner, parade) 
galaxy.add_connection(shop, garage) 
galaxy.add_connection(parade, destination) 
galaxy.add_connection(garage, destination) 

###5740479 







