import random

#colors
green = "\033[92m"          # Green
blue = "\033[94m"           # Blue
magenta = "\033[95m"        # Magenta
red = "\033[91m"            # Red
yellow = "\033[93m"         # Yellow
reset_color = "\033[0m"     # Reset

choices = ["rock", "paper", "scissors"]                                                                                 # List of choices for the game
wins = 0                                                                                                                # Initialize a counter for the number of wins
losses = 0                                                                                                              # Initialize a counter for the number of losses
ties = 0                                                                                                                # Initialize a counter for the number of ties

print(f"{green}Welcome to Rock, Paper, Scissors!{reset_color}")                                                         # Print a welcome message to the player
print(f"{blue}You will be playing against the computer. Try to beat it!{reset_color}")                                  # Print instructions for the player
input(f"{yellow}Press Enter to start the game...{reset_color}")                                                         # Wait for the player to press Enter before starting the game

while True:

    player_choice = input(f"{magenta}Enter your choice (rock, paper, or scissors): {reset_color}").strip().lower()      # Prompt the player for their choice and convert it to lowercase
    if player_choice not in choices:                                                                                    # Check if the player's choice is valid
        print(f"{red}Invalid choice! Please choose rock, paper, or scissors.{reset_color}")                             # Print an error message for invalid choice
        continue                                                                                                        # Restart the loop to allow the player to choose again

    computer_choice = random.choice(choices)                                                                            # Generate a random choice for the computer
    print(f"You chose {green}{player_choice}{reset_color}. The computer chose {blue}{computer_choice}{reset_color}.")   # Print both choices

    # Determine the winner
    if player_choice == computer_choice:
        print(f"{yellow}It's a tie!{reset_color}")
        ties += 1
    elif (player_choice == "rock" and computer_choice == "scissors") or \
         (player_choice == "paper" and computer_choice == "rock") or \
         (player_choice == "scissors" and computer_choice == "paper"):
        print(f"{green}You win!{reset_color}")
        wins += 1
    else:
        print(f"{red}You lose!{reset_color}")
        losses += 1

    play_again = input(f"{yellow}Do you want to play again? (yes/no): {reset_color}").strip().lower()                   # Prompt the player to play again
    if play_again != "yes":                                                                                             # Check if the player wants to play again
        print(f"{blue}\nFinal Score: {wins} Wins, {losses} Losses, {ties} Ties{reset_color}")                           # Print the final score
        print(f"{green}Thanks for playing! Goodbye!{reset_color}")                                                      # Print a goodbye message
        break                                                                                                           # Exit the loop and end the game
