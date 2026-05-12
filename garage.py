import random
import time
import os

def garage_gps_game():
  lives = 3
  score = 0 
  attempts = 3
  result = "Lost in Garage"

  gps_code = str(random.randint(100, 999)) #generate threee didgit num randomly

  print("GPS code:", gps_code)
  time.sleep(3)

  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")
  # I HAVE CHANGED THIS IF STATEMENT FROM THIS print("\n"* 100}
  # THEY ARE BOTH TO CLEAR EVERYTHING FROM THE SCREEN 
  # THE ONE I STUCK WITH IS MORE OFFICIAL - BY CHECKING THE COMPUTER'S OS SYSTEM - nt = windows
  # THE PRINT STATEMENT IS JUST PRNTING EMPTY LINES 100 TIMES


garage_gps_game()

  
