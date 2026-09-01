import random                                                                               # import random module to generate a random number

# Color codes for terminal output
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

answer = random.randint(1, 100)                                                             # Generate a random number between 1 and 100
tries = 1                                                                                   # Initialize a counter for the number of tries

while True:                                                                                 # Start an infinite loop to allow the user to guess multiple times
    guess = input("What is your guess: ")                                                   # Prompt the user for their guess

    if not guess.isdigit():                                                                 # Check if the input is a valid number
        print(RED + "Please enter a valid number." + RESET)                                 # Print an error message in red if the input is not a number
        continue                                                                            # Skip the rest of the loop and prompt for input again
    
    if int(guess) > 100 or int(guess) < 1:                                                  # Check if the guess is within the valid range
        print(RED + "Please enter a number between 1 and 100." + RESET)                     # Print an error message in red if the guess is out of range
        continue                                                                            # Skip the rest of the loop and prompt for input again

    if answer == int(guess):                                                                # Check if the user's guess is correct
        print(GREEN + "CORRECT!" + RESET)                                                   # Print a success message in green
        print(GREEN + "The answer was: " + str(answer) + RESET)                             # Print the correct answer in green
        print(GREEN + "You found the answer in " + str(tries) + " tries!" + RESET)          # Print the number of tries it took to guess correctly
        break                                                                               # Exit the loop if the guess is correct
    else:                                                                                   # If the guess is incorrect, provide feedback
        if answer > int(guess):                                                             # Check if the answer is greater than the guess
            print(YELLOW + "TOO LOW!" + RESET)                                              # Print a message indicating the guess is too low in yellow
        else:                                                                               # If the answer is less than the guess
            print(BLUE + "TOO HIGH!" + RESET)                                               # Print a message indicating the guess is too high in blue
        print(RED + "BETTER LUCK NEXT TIME :(" + RESET)                                     # Print a failure message in RED
        tries += 1                                                                          # Increment the number of tries