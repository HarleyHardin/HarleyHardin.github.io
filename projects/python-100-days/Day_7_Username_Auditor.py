# Day 7 - Username Auditor
# This program checks usernames for compliance with predefined rules.
# Flags:
# - No Profanity
# - No Impersonation
## I got lazy... 
import os

print("Username Auditor by Harley Hardin")

profanity = []
with open("wordlists/profanity.txt") as f:
    profanity = f.read().splitlines()
    for word in profanity:
        word = word.strip()
    profanity = [word for word in profanity if word]

impersonation = []
with open("wordlists/impersonation.txt") as f:
    impersonation = f.read().splitlines()
    for word in impersonation:
        word = word.strip()
    impersonation = [word for word in impersonation if word]

while True:
    username = input("Username >> ")
    if username.lower() == "exit":
        break

    if any(word in username.lower() for word in profanity):
        print("Username contains profanity!")
        continue
    elif any(word in username.lower() for word in impersonation):
        print("Username contains impersonation!")
        continue
