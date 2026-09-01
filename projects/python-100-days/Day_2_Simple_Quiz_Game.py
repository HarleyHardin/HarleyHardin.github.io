# Rules :
# 1. The player has to answer 5 questions.
# 2. Each question has one correct answer.
# 3. Tell the player if their answer is correct or incorrect after each question.
# 4. Keep track of how many questions the player answered correctly.
# 5. At the end of the game, display the player's score out of 5 and their percentage score.
# 6. Answers should not be case sensitive.

from datetime import datetime, timedelta                                                # import random module to generate a random number
import calendar                                                                         # import calendar module to get the number of days in a month


totalQuestions = 5                                                                      # Set the total number of questions in the quiz
correctAnswers = 0                                                                      # Initialize a counter for the number of correct answers

while True:                                                                             # Start an infinite loop to allow the user to play the quiz multiple times
    print("Welcome to the Quiz Game!")                                                  # Print a welcome message to the player
    print("You will be asked 5 simple questions. Try to answer them correctly!")        # Print instructions for the player
    input("Press Enter to start the quiz...")                                           # Wait for the player to press Enter before starting the quiz

    print("\nQuestion 1: What month is it?")                                            # Print the first question to the player
    answer = input("Your answer: ").strip().lower()                                     # Prompt the player for their answer and convert it to lowercase
    if answer == datetime.now().strftime("%B").lower():                                 # Check if the player's answer matches the current month (case insensitive)
        print("Correct!")                                                               # Print a message indicating the answer is correct
        correctAnswers += 1                                                             # Add 1 to the correct answers counter
    else:
        print(f"Incorrect! The correct answer is {datetime.now().strftime('%B')}.")     # Print a message indicating the answer is incorrect and show the correct answer
    input("Press Enter to continue to the next question...")                            # Wait for the player to press Enter before moving on to the next question

    print("\nQuestion 2: What is the short form of the current month?")                 # Print the second question to the player
    answer = input("Your answer: ").strip().lower()
    if answer == datetime.now().strftime("%b").lower():                                 # Check if the player's answer matches the short form of the current month (case insensitive)
        print("Correct!")
        correctAnswers += 1
    else:
        print(f"Incorrect! The correct answer is {datetime.now().strftime('%b')}.")
    input("Press Enter to continue to the next question...")

    print("\nQuestion 3: How many days are in the current month?")
    answer = input("Your answer: ").strip()
    if answer.isdigit() and int(answer) == calendar.monthrange(datetime.now().year, datetime.now().month)[1]:  # Check if the player's answer is a digit and matches the number of days in the current month
        print("Correct!")
        correctAnswers += 1
    else:
        print(f"Incorrect! The correct answer is {calendar.monthrange(datetime.now().year, datetime.now().month)[1]}.")
    input("Press Enter to continue to the next question...")

    print("\nQuestion 4: What weekday is it today?")
    answer = input("Your answer: ").strip().lower()
    if answer == datetime.now().strftime("%A").lower():
        print("Correct!")
        correctAnswers += 1
    else:
        print(f"Incorrect! The correct answer is {datetime.now().strftime('%A')}.")
    input("Press Enter to continue to the next question...")

    print("\nQuestion 5: What is the short form of the current weekday?")
    answer = input("Your answer: ").strip().lower()
    if answer == datetime.now().strftime("%a").lower():
        print("Correct!")
        correctAnswers += 1
    else:
        print(f"Incorrect! The correct answer is {datetime.now().strftime('%a')}.")
    input("Press Enter to view your results...")
    print(f"\nYou answered {correctAnswers} out of {totalQuestions} questions correctly.") # Print the number of correct answers out of the total number of questions
    percentage = (correctAnswers / totalQuestions) * 100                                   # Calculate the percentage score based on the number of correct answers and total questions
    print(f"Your score is {percentage:.2f}%.")                                             # Print the percentage score with two decimal places
    break                                                                                  # Exit the loop after displaying the results