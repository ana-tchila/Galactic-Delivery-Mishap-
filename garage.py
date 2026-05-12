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


<<<<<<< HEAD
  #while attempts > 0  and lives > 0:
  #  answer = input("Enter GPS code: ").strip()  #strip = strips the answer only, without any spaces = so one python compares thr generated num and the inputted text there is no error 

   # if answer == gps_code:
      #score = score + 1
      #3
      #result = "Congratulations, You Won the Game!"
     # break
    #else:
    #  lives = lives - 1
   #   attempts = attempts -1  

   #   if lives == 0:
  #      result = "Lost in Garage"
 #       break

  # FOR OTHER CODE SECTIONS 
  # if attempts ==0 and lives > 0:
  #   result = "Lost in Garage"

 # print(result)
  #print("Score:", score)
  #print("Lives:", lives)

=======
      if lives == 0:
        result = "Lost in Garage"
        break
>>>>>>> 795cea2d78c7649b2e27b58abd4e37f0f257d292



  
