####
# This is Day 6 of the 100 day coding challenge series.
# The challenge for this day focuses on creating a suspicious process checker.
# disclosure: This code is for educational purposes. I am only giving myself 1 hour to complete these projects.
# there are many things that I could improve in this program, but I am limiting myself to 1 hour for this challenge.
####

####
# Requirements:
# - Have a graphical interface.
# - Let the user type in a process name to check.
# - Have a button that performs the check.
# - Maintain my own collection of at least 8 suspicious process names.
# - Tell the user whether the entered process is Suspicious or Not found in the suspicious list.
# - ignore capitolization when checking process names.
# - Handles blank input without crashing.
# - Have a way to clear/reset the current result.
####

####
# Bonus Objectives:
# - Keep a count of how many processes have been checked.
# - Show a different visual warning for suspicious results.
# - Let the user add a new process name to the suspicious list while the program is running.
# - Add a small investigation/history area showing previously checked processes.
####

####
# This program could be improved using the CISA guidelines for identifying and terminating suspicious processes.
# References:
# - CISA Identify and Terminate Suspicious Processes (CM0023)
####

import tkinter as tk

# colors
SUSPICIOUS_COLOR = "red"
NORMAL_COLOR = "green"

# Global Variables
suspicious_processes = ["process1", "process2", "process3", "process4", "process5", "process6", "process7", "process8"] # Initialize the suspicious process list
history = []                                                                                                        # Initialize the process history list
counter = 0

def check_process():
    process_name = search_entry.get()                                                                               # Get the process name entered by the user
    if not process_name:                                                                                            # Handle blank input
        result_label.config(text="Please enter a process name.")
        return

    process_name = process_name.lower()                                                                             # Ignore capitalization
    global counter
    counter += 1
    history.append(process_name)                                                                                    # Add the checked process to the history
    if process_name in suspicious_processes:
        result_label.config(text=f"{process_name} is Suspicious!", fg=SUSPICIOUS_COLOR)
    else:
        result_label.config(text=f"{process_name} not found in the suspicious list.", fg=NORMAL_COLOR)
    counter_label.config(text=f"Processes checked: {counter}")
    search_entry.delete(0, tk.END)                                                                                  # Clear the entry widget after checking
    search_entry.focus()                                                                                            # Set focus back to the entry widget for convenience

def add_suspicious_process():
    new_process = search_entry.get().lower()
    if new_process and new_process not in suspicious_processes:
        suspicious_processes.append(new_process)
        result_label.config(text=f"{new_process} added to suspicious list.", fg=NORMAL_COLOR)
    search_entry.delete(0, tk.END)
    search_entry.focus()

def process_history():
    history_window = tk.Toplevel(root)
    history_window.title("Process History")
    history_window.geometry("300x200")
    history_listbox = tk.Listbox(history_window)
    history_listbox.pack(fill=tk.BOTH, expand=True)
    for i, process in enumerate(history, start=1):
        history_listbox.insert(tk.END, f"{i}. {process}")
    close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
    close_button.pack()

# Initialize the main application window and its widgets
root = tk.Tk()                                                                                                      # Create the main application window
root.title("Suspicious Process Checker")                                                                            # Set the window title
root.geometry("400x300")                                                                                            # Set the window size
search_entry = tk.Entry(root)                                                                                       # Create an entry widget for the user to type in a process name
search_entry.pack()                                                                                                 # Add the entry widget to the window

check_button = tk.Button(root, text="Check Process", command=check_process)                                         # Create a button to perform the check
add_button = tk.Button(root, text="Add Suspicious Process", command=add_suspicious_process)                         # Create a button to add a new suspicious process
history_button = tk.Button(root, text="Process History")                                                            # Create a button to view process history
clear_button = tk.Button(root, text="Clear Result")                                                                 # Create a button to clear the result
check_button.pack()                                                                                                 # Add the button to the window
add_button.pack()                                                                                                   # Add the add button to the window
history_button.pack()                                                                                               # Add the history button to the window
clear_button.pack()                                                                                                 # Add the clear button to the window
result_label = tk.Label(root, text="", fg=NORMAL_COLOR)                                                             # Create a label to display the result
result_label.pack() # Add the result label to the window
counter_label = tk.Label(root, text="Processes checked: 0")                                                         # Create a label to display the counter
counter_label.pack()                                                                                                # Add the counter label to the window

check_button.config(command=check_process)                                                                          # Link the button to the check_process function
add_button.config(command=add_suspicious_process)                                                                   # Link the add button to the add_suspicious_process function
history_button.config(command=process_history)                                                                      # Link the history button to the process_history function
def clear_result():
    result_label.config(text="", fg=NORMAL_COLOR)
    search_entry.delete(0, tk.END)                                                                                  # Clear the entry widget as well
    search_entry.focus()                                                                                            # Set focus back to the entry widget for convenience
clear_button.config(command=clear_result)                                                                           # Link the clear button to the clear_result function





root.mainloop()                                                                                                     # Start the Tkinter event loop

