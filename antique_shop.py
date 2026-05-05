antique_items = {
"old vase": "empty",
"vintage ring box": "empty",
"dusty map": "GPS part",
"persian rug": "empty"
}

bag = []

print{"You have entered the antique shop.")
print("You need to find the missing GPS part.")

while "GPS part" not in bag:
  print("\nChoose an item to search:")

  for item in antique_items:
    print("-", item)
  elif antique_items[choice] == "GPS part":
    print("You searched the", choice)
    print("You found the GPS part!")
    bag.append("GPS part")

  else:
    print("You searched the", choice)
    print("Nothing useful here, try another item.")
    del antique_items[choice]

print("Now return to the garage.")
print("Bag", bag)

