#ID: 5752030
# This function performs a linear search on the unordered list to find if the player has the item in their inventory. It returns the index of the item if found, otherwise it returns None.
def search(unordered_list, item):
    """
    preform a linear on an unordered list.
    
    Args:
        unordered_list: a list of items in the player's inventory.
        item: the item to search for in the inventory.
        
    Returns:
        The index of the item if found, otherwise None.
       
    """
    unordered_list_size = len(unordered_list)
    for element in range(unordered_list_size):
        if item == unordered_list[element]:
            return element
    return None 


#this class represents the player's inventory and provides methods to add, remove, and check for items. It uses the search function to check if an item is in the inventory.

class Inventory:
    def __init__(self):
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def has(self, item):
        return search(self.items, item) is not None
player_invetory = Inventory()
