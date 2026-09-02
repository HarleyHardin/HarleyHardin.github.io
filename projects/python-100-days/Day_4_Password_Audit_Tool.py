# Password Audit Tool
# This script is designed to audit passwords for security compliance. It checks for common vulnerabilities such as weak passwords, reused passwords, and passwords that do not meet complexity requirements.
# passwords are scored between 0 and 100, with 0 being the weakest and 100 being the strongest. The score is based on the following criteria:
# - Length: Passwords must be at least 12 characters long. If the password is shorter than 12 characters, this results in a score of 0 for the password.
# - Uppercase letters: Passwords must contain at least one uppercase letter. This is worth 20 points.
# - Lowercase letters: Passwords must contain at least one lowercase letter. This is worth 20 points.
# - Digits: Passwords must contain at least one digit. This is worth 20 points.
# - Special characters: Passwords must contain at least one special character. This is worth 20 points.
# - Repeated characters: Passwords must not contain the same character repeated consecutively more than twice. This is worth 20 points.
# - Common passwords: Passwords must not be in the list of the 10k most common passwords. This results in a score of 0 for the password.
# enter q to quit the audit session.
# After audit session completion an average score is provided to the user. User is prompted to press enter to close the program.

import os

def load_common_passwords(): # loads the 10k-most-common.txt worldlist from the wordlists dir.
    common_passwords = set()
    with open("wordlists/10k-most-common.txt") as f:
        for line in f:
            common_passwords.add(line.strip())
    return common_passwords
common_passwords = load_common_passwords()

def average(scores):
    if not scores:
        return 0
    return sum(scores) / len(scores)
scores = []

def up_case_check(password):
    return any(c.isupper() for c in password)

def low_case_check(password):
    return any(c.islower() for c in password)

def digit_check(password):
    return any(c.isdigit() for c in password)

def special_char_check(password):
    special_characters = "!@#$%^&*()"
    return any(c in special_characters for c in password)

def repeated_char_check(password):
    for c in range(len(password) - 2):
        if password[c] == password[c + 1] == password[c + 2]:
            return False
    return True

def get_score_ranking(score): # returns a whole number ranking based on the score
    for key in sorted(score_ranking.keys(), reverse=True):
        if score >= key:
            return score_ranking[key]
    return "Unknown"


score_ranking = {
    100: "Very Strong",
    80: "Strong",
    60: "Average",
    40: "Weak",
    20: "Very Weak",
    0: "Very Weak"
}

vs = 0
s = 0
a = 0
w = 0
vw = 0


# Welcome massage
print("Welcome to the Password Audit Tool!")
print("Enter 'q' to quit the audit session at any time.")

while True:
    password = input("password: ")
    if password.lower() == "q":
        average_score = average(scores)
        print(f"Very Strong passwords: {vs}")
        print(f"Strong passwords: {s}")
        print(f"Average passwords: {a}")
        print(f"Weak passwords: {w}")
        print(f"Very Weak passwords: {vw}")
        print(average_score)
        print(f"Average password ranking: {get_score_ranking(average_score)}") # returns a whole word ranking based on the average score
        input("Press Enter to close the program.")
        break
    
    score = 0

    if up_case_check(password):
        print("Uppercase check passed.")
        score += 20
    else:
        print("Uppercase check failed.")

    if low_case_check(password):
        print("Lowercase check passed.")
        score += 20
    else:
        print("Lowercase check failed.")

    if digit_check(password):
        print("Digit check passed.")
        score += 20
    else:
        print("Digit check failed.")

    if special_char_check(password):
        print("Special character check passed.")
        score += 20
    else:
        print("Special character check failed.")

    if not repeated_char_check(password):
        print("Repeated character check failed.")
    else:
        print("Repeated character check passed.")
        score += 20

    if len(password) >= 12:
        print("Length check passed.")
    else:
        print("Length check failed.")
        score = 0

    if password in common_passwords:
        print("Common password check failed.")
        score = 0
    else:
        print("Common password check passed.")

    scores.append(score)
    print(f"Password score: {score}")
    print(f"Password ranking: {get_score_ranking(score)}")
    
    if score == 100:
        vs += 1
    elif score >= 80:
        s += 1
    elif score >= 60:
        a += 1
    elif score >= 40:
        w += 1
    else:
        vw += 1