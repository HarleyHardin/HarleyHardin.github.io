import random

cash = 100

def roll():
    result = random.randint(1, 13)
    return result

def placeBet():
    while True:
        bet = input("Your bet >> ")
        if not bet.isdigit():
            print(bet + "is not a valid number.")
            continue
        elif int(bet) > int(cash):
            print("Not enough cash")
            continue
        return bet

while True:
    number = roll()
    print("The number is " + str(number))
    bet = placeBet()
    choice = input("higher or lower >> ")
    result = roll()
    if choice == "higher":
        if result > number:
            cash += int(bet)
            print("You won!")

        elif result == number:
            print("It's a tie.")
            
        else:
            print("Better luck next time...")
            cash = cash - int(bet)
            
    else:
        if result < number:
            cash += int(bet)
            print("You won!")
            
        elif result == number:
            print("It's a tie.")
            
        else:
            print("Better luck next time...")
            cash = cash - int(bet)
            
    print("You have $" + str(cash))
    if cash <= 0:
        print("Game Over!")
        break
