# Ask user for the path to a directory they want to monitor
# find all regular files inside the directory
# Calculate a SHA-256 hash for each file
# save teh filename/path and sha-256 hash to a file called baseline.txt
# two operating modes; create baseline.txt and check integrity
# check integrity by comparing current file hashes with the baseline
# report files that are unchanged, modified, new, or deleted
# print a final summary of how many files were unchanged, modified, new, or deleted
# Rules for challenge:
# Use pythons built in hashlib module
# program continues to run until the user chooses to exit
# no hard coding of file paths or directory paths
# Program checks every 10 seconds for changes in the monitored directory and reports them. 
# only use the file name instead of the full path when checking integrity

# theres a lot of bugs, ill circle back to these projects after the 100 day challenge and clean them up. 
# the core elements of the program are in place.



import os
import hashlib
import time
import keyboard

# colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"

options = ["1", "2", "3"]

monitored_directory = input("Enter the directory to monitor: ")

prompt = "File Integrity Checker\nChoose an option:\n1. Create baseline\n2. Check integrity\n3. Exit\nEnter your choice: "

# Functions:

# Creates an empty baseline.txt file if it doesn't exist
def create_baseline_file():
    if not os.path.exists("baseline.txt"):
        with open("baseline.txt", "w") as f:
            pass

# Calculates the SHA-256 hash of a file
def calculate_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

# Scans a directory and returns a dictionary of file paths and their SHA-256 hashes
def scan_directory(directory):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                file_hashes[os.path.basename(file_path)] = calculate_file_hash(file_path)
    return file_hashes

# appends the current file hashes to the baseline.txt file
def append_to_baseline(file_hashes):
    with open("baseline.txt", "a") as f:
        for file_path, file_hash in file_hashes.items():
            f.write(f"\"{file_path}\" \"{file_hash}\"\n")

# Reads the baseline.txt file and returns a dictionary of file paths and their SHA-256 hashes
def read_baseline():
    file_hashes = {}
    if os.path.exists("baseline.txt"):
        with open("baseline.txt", "r") as f:
            for line in f:
                parts = line.strip().split("\" \"")
                if len(parts) == 2:
                    file_path = parts[0].strip("\"")
                    file_hash = parts[1].strip("\"")
                    file_hashes[file_path] = file_hash
    return file_hashes

# Compares the current file hashes with the baseline and returns a summary of changes
def check_integrity(current_hashes, baseline_hashes):
    unchanged = []
    modified = []
    new = []
    deleted = []

    for file_path, file_hash in current_hashes.items():
        if file_path in baseline_hashes:
            if file_hash == baseline_hashes[file_path]:
                unchanged.append(file_path)
            else:
                modified.append(file_path)
        else:
            new.append(file_path)

    for file_path in baseline_hashes:
        if file_path not in current_hashes:
            deleted.append(file_path)

    return unchanged, modified, new, deleted

while True:
    choice = input(prompt)
    if choice not in options:
        print(RED + "Invalid choice. Please try again." + RESET)
        continue

    if choice == "1":
        create_baseline_file()
        file_hashes = scan_directory(monitored_directory)
        append_to_baseline(file_hashes)
        print(GREEN + "Baseline created successfully." + RESET)
    elif choice == "2":
        exit_flag = False
        current_hashes = scan_directory(monitored_directory)
        baseline_hashes = read_baseline()
        unchanged, modified, new, deleted = check_integrity(current_hashes, baseline_hashes)
        print(BLUE + "Unchanged files:" + RESET, unchanged)
        print(YELLOW + "Modified files:" + RESET, modified)
        print(GREEN + "New files:" + RESET, new)
        print(RED + "Deleted files:" + RESET, deleted)

    elif choice == "3":
        break
    else:
        print(RED + "Invalid choice. Please try again." + RESET)
        continue