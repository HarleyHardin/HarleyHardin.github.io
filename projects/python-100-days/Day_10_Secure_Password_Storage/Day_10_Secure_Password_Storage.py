# Create and account *
# Store account persistently *
# User proper password storage *
# Login *
# Handle bad input *
# Include a menu *




import sqlite3
import bcrypt




def menu():
    print("\n")
    print("=========================")
    print("= SECURE ACCOUNT SYSTEM =")
    print("=========================")
    print("1. Register Account")
    print("2. Login")
    print("3. Exit")
    print("\n")
    nav = input(" >> ")
    return nav




def navigate(nav):
    if nav == "1":
        register()
    elif nav == "2":
        login()
    elif nav == "3":
        exit()




def createpw():
    while True:
        print("\n")
        print("Choose a password.")
        pw1 = input(" >> ")

        check = strength(pw1)
        if all(check.values()):
            print("\n")
            print("Confirm your password.")
            pw2 = input(" >> ")

            if pw1 == pw2:
                return pw1
            else:
                print("\n")
                print("Passwords did not match.")
                continue
        else:
            print("\n")
            print("Pick a stronger password.")
            continue




def strength(password):
    special = "!@#$%^&*-"
    rule = {
        "Uppercase letter": any(c.isupper() for c in password),
        "Lowercase letter": any(c.islower() for c in password),
        "A number": any(c.isdigit() for c in password),
        "A special character": any(c in special for c in password),
        "At least 12 characters": len(password) >= 12
    }
    return rule




def naming(name):
    rule = {
        "2 characters": len(name) >= 2,
        "All letter, accepts - and '": all(char.isalpha() or char in "'-" for char in name),
        "Must contain atleast one letter": any(char.isalpha() for char in name)
    }
    return rule



def encryptpw(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed




def verifypw(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)




def createuser():
    while True:
        print("\n")
        print("Enter your first name.")
        firstname = input(" >> ")

        check = naming(firstname)

        if all(check.values()):
            print("\n")
            print("Enter your last name.")
            lastname = input(" >> ")

            check = naming(lastname)

            if all(check.values()):
                name = lastname + ", " + firstname
                username = firstname + "." + lastname

                connection = sqlite3.connect("Day_10_Secure_Password_Storage/databases/users.db")
                cursor = connection.cursor()

                cursor.execute(
                    "SELECT name FROM users WHERE name = ?",
                    (name,)
                )

                result = cursor.fetchone()

                connection.close()

                if result is None:
                    return name, username
                else:
                    print("Account already exists")
                    return None, None
            else:
                print("\n")
                print("Name must have at least two characters and NO spaces.")
                continue
        else:
            print("\n")
            print("Name must have at least two characters and NO spaces.")
            continue




def register():
    while True:
        name, username = createuser()
        if name is None:
            break
        else:
            password = encryptpw(createpw())
        

        connection = sqlite3.connect("Day_10_Secure_Password_Storage/databases/users.db")
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO users (name, username, password_hash) VALUES (?, ?, ?)",
            (name, username, password)
        )

        connection.commit()
        connection.close()

        print("\n")
        print("Account created")
        print("\n")
        print("Welcome, " + username + "!")
        break




def getHash(username):
    connection = sqlite3.connect("Day_10_Secure_Password_Storage/databases/users.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    connection.close()
    return result[0]




def validateUsername(username):
    connection = sqlite3.connect("Day_10_Secure_Password_Storage/databases/users.db")
    cursor = connection.cursor()
    cursor.execute(
        "SELECT username FROM users WHERE username = ?",
        (username,)
    )

    result = cursor.fetchone()
    connection.close()
    return result




def login():
    print("\n")
    username = input("Username >> ")

    print("\n")
    password = input("Password >> ")

    valid = validateUsername(username)
    if valid is None:
        print("\n")
        print("Invalid")
    else:
        hashed = getHash(username)
        if verifypw(password, hashed):
            with open("Day_10_Secure_Password_Storage/logs/login_logs.txt", 'a+') as f:
                f.write(f"{username}, SUCCESS\n")
            print("\n")
            print("Logged in as " + username)
        else:
            with open("Day_10_Secure_Password_Storage/logs/login_logs.txt", 'a+') as f:
                f.write(f"{username}, FAILED\n")
            print("\n")
            print("Invalid")




while True:
    
    navigate(menu())