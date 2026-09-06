######
# BUGS
# - Passwords are stored in plaintext.
######
import os

Invalid_Usernames = []

ArdyTknUsr = []

with open("Wordlists/impersonation.txt") as f:
    words = f.read().splitlines()
    for word in words:
        Invalid_Usernames.append(word)

with open("Wordlists/profanity.txt") as f:
    words = f.read().splitlines()
    for word in words:
        Invalid_Usernames.append(word)

def update_validity():
    with open("Wordlists/userDB.txt") as f:
        for line in f:
            word = line.split(",", 1)[0].strip()
            if word.lower() not in ArdyTknUsr:
                ArdyTknUsr.append(word.lower())

def choose_username():
    while True:
        username = input("Choose a username: ")
        if len(username) < 4:
            print("Username must be at least 4 characters.")
            continue
        if any(word.lower() in username.lower() for word in Invalid_Usernames):
            print("Invalid username, try again.")
            continue
        if any(word.lower() == username.lower() for word in ArdyTknUsr):
            print("That username is already taken.")
            continue
        return username

def pwStr(password):
    sp_ch = "!@#$%^&*-_=+,.()"
    checks = {
        "Uppercase letter": any(c.isupper() for c in password),
        "Lowercase letter": any(c.islower() for c in password),
        "A number": any(c.isdigit() for c in password),
        "A special character": any(c in sp_ch for c in password),
        "At least 12 characters": len(password) >= 12
    }
    return checks

def choose_password():
    while True:
        password = input("Choose a password: ")
        result = pwStr(password)
        if all(result.values()):
            return password
        else:
            flCh = [check for check, passed in result.items() if not passed]
            if flCh:
                for check in flCh:
                    print(f"- {check.replace('_', ' ').capitalize()}")
            continue


while True:
    update_validity()

    username = choose_username()
    
    password = choose_password()

    with open("Wordlists/userDB.txt", 'a+') as f:
        f.write(f"{username}, {password}\n")

    add_another = input("Add another? (y/n): ")
    if add_another.lower() == "n":
        break
