import sqlite3

rooms = {
    "callcenter": {
        "department": "IT",
        "access_level": ["L1", "L2", "TL", "SEC"]
    },

    "security_suite": {
        "department": "security",
        "access_level": ["SEC"]
    },

    "kitchen": {
        "department": "kitchen",
        "access_level": ["KIT", "SEC"]
    },

    "server_room": {
        "department": "IT",
        "access_level": ["L2", "TL"]
    }
}


def getAccLvl():
    while True:
        username = input("Username >> ")

        connection = sqlite3.connect("databases/employees.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT access FROM employees WHERE username = ?",
            (username,)
        )
        result = cursor.fetchone()
        connection.close()

        if result is None:
            print("Invalid username.")
            print("\n")
            continue
        else:
            acl = result[0]
            return acl, username


def getRmKy():
    while True:
        choice = input("Room # >> ")

        if choice == "1":
            key = rooms["callcenter"]["access_level"]
            return choice, key
        elif choice == "2":
            key = rooms["security_suite"]["access_level"]
            return choice, key
        elif choice == "3":
            key = rooms["kitchen"]["access_level"]
            return choice, key
        elif choice == "4":
            key = rooms["server_room"]["access_level"]
            return choice, key
        else:
            print("Please enter a valid room number.")
            print("\n")
            continue


def menu():
    print("\n")
    print("===============")
    print("=Choose a room=")
    print("===============")
    print("1. Callcenter")
    print("2. Security Suite")
    print("3. Kitchen")
    print("4. Server Room")
    print("\n")


while True:
    menu()
    room, key = getRmKy()
    acl, user = getAccLvl()

    if acl == None:
        continue
    elif acl in key:
        print("Access granted.")
        with open("logs/access_logs.txt", 'a+') as f:
            f.write(f"{user}, {room}, GRANTED\n")
    else:
        print("Access denied.")
        with open("logs/access_logs.txt", 'a+') as f:
            f.write(f"{user}, {room}, DENIED\n")

    agn = input("Want to access another room? y/n >> ")
    if agn == "n" or agn == "no":
        break
