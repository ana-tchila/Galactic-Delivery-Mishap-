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

class inventory:
    def __init__(self):
        self.items = []
        
    def add_item(self, item):
        print("\nAdding item to inventory:", item)
        self.items.append(item)
        print("Current inventory:", self.items)
        
    def remove_item(self, item):
        print("\nTrying to remove item:", item)

        if item in self.items:
            self.items.remove(item)
            print(item, "removed from inventory.")
            print("Current inventory:", self.items)
        else:
            print(item, "is not in your inventory.")

    def has(self, item):
        print("\nChecking if you already have:", item)
        return search(self.items, item) is not None




# Searching the system 

def search_shop(shop_choices, item_wanted, player_inventory):
    print("Searching the shop choices...")

    shop_items = list(shop_choices.items.keys())

    index = search(shop_items, item_wanted)

    if index is None:
        print("The item was not found in the shop.")
        return f" You need to look for the '{item_wanted}'"

    offered_item = shop_items[index]
    print("The shopkeeper found:", offered_item)

    descriptions = shop_choices.items.get(offered_item, "Woah buddy, you wish!")

    if player_inventory.has(offered_item):
        print("You already have this item.")
        return f"{descriptions}\nYou already have {offered_item}."

    print("You do not have this item yet.")
    player_inventory.add_item(offered_item)

    return f"{descriptions}\n\nYou take the {offered_item}."

    
   

