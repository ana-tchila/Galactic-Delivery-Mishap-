#ID: 5752030

def create_shop_system():

    print("Creating shop system...")
    print("Shop system is loading inventory, search, and shop items.")

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
        def __init__(self):
            self.items = []
            print("\nInventory created.")
            print("Your inventory is currently empty.")
        
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


    shop_item_description = {
        "Shopkeeper" : ("Welcome to my humble shop, starngar!" "You can find things from all around the universe here!"),
        "GPS": ( "Is this what you are looking for?" "Luckily, some guy sold me his old bike scraps, and this is one of the parts which are in good condition" "It looks rusty and old, but I assure you, it works like it is brand new!"), 
        "Raygun": ("A buddy from your planet with a funny accent called Richtofen sold me this weapon" "He told me it is one of his best creations or something...." "Yeah, it looks as weird as him")
    }

    print("\nShop items loaded.")
    print("Available shop items:", list(shop_item_description.keys()))


    def search_shop(shop_choices, item_wanted, player_inventory):
        print("\nYou entered the shop.")
        print("You are looking for:", item_wanted)
        print("Searching the shop choices...")

        index = search(shop_choices.choices, item_wanted)

        if index is None:
             print("The item was not found in the shop.")
             return f" You need to look for the '{item_wanted}'"

        offered_item = shop_choices.choices[index]
        print("The shopkeeper found:", offered_item)

        descriptions = shop_item_description.get(offered_item, "Woah buddy, you wish!")

        if offered_item == "Shopkeeper":
            print("You are talking to the shopkeeper.")
            return descriptions

        if player_inventory.has(item_wanted):
            print("You already have this item.")
            return f"{descriptions}\nYou don't need {offered_item}."

        print("You do not have this item yet.")
        player_inventory.add_item(offered_item)

        return f"{descriptions}\n\nYou take the {offered_item}."

    
    print("\nShop system is ready.")
    return Inventory, search_shop
  


### 5758609 -- Inventory, search_shop = create_shop_system()

### player_inventory = Inventory()

### calling the function 

### Print statements to test the function + user guidence
