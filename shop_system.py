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
    print("\nSearching for:", item)

    unordered_list_size = len(unordered_list)

    for element in range(unordered_list_size):
        print("Checking item:", unordered_list[element])

        if item == unordered_list[element]:
            print("Item found!")
            return element

    print("Item not found.")
    return None 


#this class represents the player's inventory and provides methods to add, remove, and check for items. It uses the search function to check if an item is in the inventory.

class Inventory:
    """
    Represents the player's collected items during the game.

    The inventory is implemented as a list because items can be added
    and removed dynamically as the player progresses, and the data is
    inherently unordered. Membership checks use the linear search 
    function defined above.

    Attributes:
        items (list): The current list of item names held by the player.
    
    """
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        print("\nAdding item to inventory:", item)
        self.items.append(item)
        print("Current inventory:", self.items)
        

    def has(self, item):
        print("\nChecking if you already have:", item)
        return search(self.items, item) is not None


# Searching the system 

def search_shop(shop_choices, item_wanted, player_inventory):
    """
   Search the shop for a requested item and add it to the inventory.

    Wraps the linear search algorithm with additional logic:
        - Handles empty or whitespace-only input gracefully
        - Performs a case-insensitive match so 'gps', 'GPS', and 'Gps'
          all find the same item
        - Tells the player what items are available if their search fails
        - Prevents duplicate items from being added to the inventory

    Args:
        shop_choices: A Location object representing the shop.
            Its `items` attribute is a dictionary mapping item names
            to their descriptions.
        item_wanted: The string the player typed into the search bar.
        player_inventory: The player's Inventory object, modified
            in-place if a match is found.

    Returns:
        str: A message to display to the player. Could be:
            - A prompt to type a name (if input was empty)
            - A "not found" message listing available items
            - The item's description plus "You take the {item}" (success)
            - The item's description plus "You already have {item}"
              (if the item is a duplicate)

   """


    # Handle empty input
    if not item_wanted or not item_wanted.strip():
        return "Type the name of an item to search for it."
    
    shop_items = list(shop_choices.items.keys())
    
    # Make search case-insensitive by matching against lowercase versions
    item_wanted_lower = item_wanted.lower().strip()
    matched_index = None
    
    for i in range(len(shop_items)):
        if shop_items[i].lower() == item_wanted_lower:
            matched_index = i
            break
    
    if matched_index is None:
        available = ", ".join(shop_items)
        return (
            f"Sorry, '{item_wanted}' is not for sale in this shop.\n"
            f"Available items: {available}."
        )
    
    offered_item = shop_items[matched_index]
    print("The shopkeeper found:", offered_item)
    
    descriptions = shop_choices.items.get(offered_item, "Woah buddy, you wish!")
    
    if player_inventory.has(offered_item):
        return f"{descriptions}\n\nYou already have {offered_item}."
    
    player_inventory.add_item(offered_item)
    return f"{descriptions}\n\nYou take the {offered_item}."
    

#5752030