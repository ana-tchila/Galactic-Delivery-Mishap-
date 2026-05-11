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


shop_item_description = {"shopkeeper" : ("Welcome to my humble shop, starngar!", "You can find things from all around the universe here!"),
"GPS": ( "Is this what you are looking for?", "Luckily, some guy sold me his old bike scraps, and this is one of the parts which are in good condition", "It looks rusty and old, but I assure you, it works like it is brand new!"), 
"Raygun": ("A buddy from your planet with a funny accent called Richtofen sold me this weapon", "He told me it is one of his best creations or something....", "Yeah, it looks as weird as him") }

def search_shop(shop_choices, item_wanted, player_inventory):
    index = search(shop_choices.choices, item_wanted)
    offered_item = shop_choices.choices[index]
    item_wanted = "GPS"
    descriptions = shop_item_description.get(offered_item, "Woah buddy, you wish!")
    if offered_item == "shopkeeper":
        return descriptions
     
    if player_inventory.has(item_wanted):
        return f"n/ you found the GPS part!"
    else:
        return f" This is not helpful."

    
