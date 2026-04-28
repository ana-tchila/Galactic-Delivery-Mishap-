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


#Graph that the user will be moving through 

class Graph: 
	""" Class graph to represent the map of locations(nodes) and their connections(edges) in the game. 
	It will have methods to add locations, and connections.""" 
	def __init__(self): 
		self.locations = {} #dictionary to hold nodes

	def add_location(self, location): 
		"""Method to add a location node to the graph. 
		It takes a location object and adds it to the self.locations dictionary with the location's name as the key."""
		self.locations[location.name] = location # 

	def add_connection(self, from_location, to_location): 
		""" Method to add a connection(edge) between two locations on the graph.
		It does this by adding to_location to the connections of the from_location"""
		self.locations[location.name].connections[location.name] = to_location 

