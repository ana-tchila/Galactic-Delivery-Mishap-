from collections import deque
import random
import time
import os

score = 0

def show_status():
    print("Score:", score)


def find_boss():
    global score

    print("\nSTAGE 1: FIND THE BOSS")
    print("You enter a corridor with 15 locked doors.")
    print("The boss is hiding behind one of them.")
    print("Your scanner can split the door zone in half.")
    print("Pick the middle door for better optimisation.")

    boss_door = random.randint(1, 15)

    low = 1
    high = 15

    while low <= high:
        show_status()

        middle = (low + high) // 2

        print("\nCurrent door zone:")

        for door in range(low, high + 1):
            print("Door", door, end="  ")

        print()

        if low == high:
            print("Only one door left. Scan this door.")
        else:
            print("Pick the middle door for better optimisation.")

        try:
            guess = int(input("Enter the door number to scan: "))

        except ValueError:
            print("Invalid input. Please enter a door number.")
            continue

        if guess != middle:
            print("Unstable scan. The scanner can only optimise properly from the middle door.")
            print("Try again without losing a life or attempt.")
            continue

        if guess == boss_door:
            print("\nCorrect! You found the boss behind Door", boss_door)
            score += 1
            return True

        elif guess < boss_door:
            print("Boss signal detected behind a higher-numbered door.")
            low = guess + 1

        else:
            print("Boss signal detected behind a lower-numbered door.")
            high = guess - 1

    return False


def space_boss_battle():
    global score

    print("\nSTAGE 2: SPACE BOSS BATTLE")

    directions = ["LEFT", "RIGHT", "UP", "DOWN"]
    signals = deque()

    for i in range(3):
        random_signal = random.choice(directions)
        signals.append(random_signal)

    boss_health = 3

    print("SPACE BOSS BATTLE")
    print("Memorise the GPS attack route:")

    for signal in signals:
        print(signal)

    time.sleep(5)

    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print("Enter the GPS attack route to hit the boss.")

    while signals:
        correct_signal = signals.popleft()
        answer = input("Enter signal: ").upper().strip()

        if answer == correct_signal:
            print("Correct hit!")
            boss_health -= 1
            score += 1
        else:
            print("Wrong route!")
            print("The boss blocked your attack.")
            break

    print("\nBoss health:", boss_health)
    print("Score:", score)

    if boss_health == 0:
        print("You defeated the Space Boss!")
    else:
        print("The Space Boss survived.")


def route_map_challenge():
    global score

    print("\nSTAGE 3: ROUTE MAP CHALLENGE")

    image_path = r"/Users/eman/Desktop/Space_Path (1).png"

    if os.path.exists(image_path):
        os.system("open " + "'" + image_path + "'")
    else:
        print("Image not found. Please check the image name and location.")
        print("\nDo not worry. You can still continue the game using the text map below.")
        print("\nTEXT ROUTE MAP:")
        print("Base -> Moon = 4")
        print("Base -> Mars = 5")
        print("Moon -> Destination = Base -> Mars plus 3")
        print("Mars -> Jupiter = Half of Mars -> Venus")
        print("Mars -> Venus = 6")
        print("Venus -> Destination = Same as Base -> Moon")
        print("Jupiter -> Destination = missing fuel cost")
        print("\nClue: The best route total fuel cost is 10.")

    graph = {
        "Base": {"Moon": 4, "Mars": 5},
        "Moon": {"Destination": 8},
        "Mars": {"Jupiter": 3, "Venus": 6},
        "Jupiter": {"Destination": 2},
        "Venus": {"Destination": 4},
        "Destination": {}
    }

    costs = {}
    previous = {}
    unvisited = []

    for place in graph:
        costs[place] = float("inf")
        previous[place] = None
        unvisited.append(place)

    costs["Base"] = 0

    while unvisited:
        current = min(unvisited, key=lambda place: costs[place])
        unvisited.remove(current)

        for neighbour in graph[current]:
            new_cost = costs[current] + graph[current][neighbour]

            if new_cost < costs[neighbour]:
                costs[neighbour] = new_cost
                previous[neighbour] = current

    best_route = []
    current = "Destination"

    while current is not None:
        best_route.insert(0, current)
        current = previous[current]

    route_options = {
        "A": ["Base", "Moon", "Destination"],
        "B": ["Base", "Mars", "Jupiter", "Destination"],
        "C": ["Base", "Mars", "Venus", "Destination"]
    }

    print("\nRoute Map Challenge")
    print("Look at the image map if it opened.")
    print("If the image did not open, use the text route map shown above.")
    print("Choose the route with the lowest fuel cost.")

    print("\nA. Base -> Moon -> Destination")
    print("B. Base -> Mars -> Jupiter -> Destination")
    print("C. Base -> Mars -> Venus -> Destination")

    answer = input("\nEnter A, B, or C: ").upper().strip()

    if answer in route_options:
        user_route = route_options[answer]

        if user_route == best_route:
            score += 1
            print("\nCorrect! You chose the best route.")
            print("You gained 1 point.")
        else:
            print("\nWrong answer.")
            print("The best route is:", " -> ".join(best_route))
    else:
        print("\nInvalid choice. Please enter A, B, or C.")

    print("\nBest route:", " -> ".join(best_route))
    print("Fuel cost:", costs["Destination"])
    print("Final Score:", score)


def main():
    find_boss()
    space_boss_battle()
    route_map_challenge()

