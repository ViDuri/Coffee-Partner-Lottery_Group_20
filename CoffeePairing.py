import pandas as pd
import csv
import random
import copy
import os
from pathlib import Path

# program name and online form URL, we can change these when we made a decision for the name and made a google forms
PROGRAM_NAME = "Mystery Brew"
FORM_URL = "https://forms.gle/4N1a1LbFNmTovK9cA" 

DELIMITER = ','

def print_instructions():
    instructions = f"""
Welcome to {PROGRAM_NAME}!

Follow these steps to participate in {PROGRAM_NAME}:

1. **Fill Out the Online Form:**
   - Visit our sign-up form at:
       {FORM_URL}
   - Enter your full name and valid email address.
   - Complete any additional fields if required.
   - Submit the form to record your response.

2. **Download the CSV File:**
   - After submitting the form, go to the form responses section.
   - Look for the option to download or export responses.
   - Download the responses as a CSV file.
   - IMPORTANT: Save this file as "Coffee Partner Lottery participants.csv" 
     in the same directory as this script.

3. **Check the CSV File Format:**
   - Ensure the CSV file includes the headers "Your name:" and "Your e-mail:".
   - If there are extra columns, the program will ignore them, but the required columns must be present.

4. **Run the Program:**
   - Once the CSV file is correctly placed and named, run this Python script.
   - The program will read the CSV file, randomly assign you to a group, and display a conversation starter for your meeting.

5. **Enjoy!:**
   - Your group details and a fun conversation starter will be printed on the screen.
   - Follow any further instructions displayed by the program.
"""
    print(instructions)

# call the function for the instructions
print_instructions()
print("Press Enter when you want to start")

# function for reading a txt file with conversation starters
def get_conversation_starter():
    starters_file = "conversation_starters.txt"
    if os.path.exists(starters_file):  # check if the file exists, otherwise return the standard sentence
        with open(starters_file, 'r', encoding="utf8") as file:
            lines = file.read().splitlines()
            starter = random.choice(lines)
            return starter
    return "What's your favorite colour?"  

# function for making a txt file for each group (with conversation starter) - Sandra
def group_messages():
    group_no = 1  # tracking group numbering, initial value 1
    for group in npairs:
        group_list = list(group)  # tuple to list
        # converting emails to participant names
        p_in_group = [formdata[formdata[header_email] == email].iloc[0][header_name] for email in group_list]
        # getting conversation starter for this group
        starter = get_conversation_starter()
        # group message template, PROGRAM_NAME from the 1st branch
        message = f"""
Hello {", ".join(p_in_group)}!
You have been gathered together for a {PROGRAM_NAME}.

To start your meeting: 
{starter}

Enjoy your coffee!
"""
        # saving message to a file
        file_name = f"group_{group_no}.txt"
        Path(file_name).write_text(message, encoding="utf-8")
        print(f"Saved message for Group {group_no}: {file_name}")  # for checking
        group_no += 1  # increase group number

# function for group size input
def group_size_input():
    while True:
        try:
            group_size = int(input("Please enter your preferred group size: "))
            if group_size < 2:
                print("Group size should be at least 2.")
            else:
                return group_size
        except ValueError:
            print("Invalid Input")

# function for splitting into groups
def split_into_groups(participants, group_size):
    participants = participants.copy()  # avoid modifying the original list
    random.shuffle(participants)  # shuffle participants
    n = len(participants)
    num_groups = n // group_size  # number of groups
    remainder = n % group_size  # number of remaining participants
    groups = []
    start = 0
    # loop through groups, distributing extra participants if needed
    for i in range(num_groups):
        extra = 1 if i < remainder else 0
        groups.append(participants[start:start+group_size+extra])
        start += group_size + extra
    if start < n:  # add any remaining participants
        groups.append(participants[start:])
    return groups

# function for loading old groups (avoid redundant matching)
def load_old_groups(filename):
    old_groups = set()  # initialize set
    if os.path.exists(filename):
        with open(filename, "r") as file:
            csvreader = csv.reader(file, delimiter=',')
            for row in csvreader:
                group = sorted([email.strip() for email in row if email.strip()])
                if group:
                    old_groups.add(tuple(group))
    return old_groups

def append_new_groups(filename, groups):
    mode = "a" if os.path.exists(filename) else "w"  # append if file exists, else create new
    with open(filename, mode) as file:
        for group in groups:
            file.write(','.join(group) + "\n")

# path to the CSV file with participant data
participants_csv = "Coffee Partner Lottery participants.csv"
formdata = pd.read_csv(participants_csv, sep=DELIMITER)

# header names in the CSV file (name and e-mail of participants)
header_name = "Your name:"
header_email = "Your e-mail:"

# path to TXT file that stores the pairings of this round
new_pairs_txt = "Coffee Partner Lottery new pairs.txt"

# path to CSV file that stores the pairings of this round
new_pairs_csv = "Coffee Partner Lottery new pairs.csv"

# path to CSV file that stores all pairings (to avoid repetition)
all_pairs_csv = "Coffee Partner Lottery all pairs.csv"

# init set of old pairs
opairs = set()

def main():
    print_instructions()
    input("Press Enter when you want to start...")
    
    # Get the desired group size from the user
    group_size = group_size_input()
    
    # Get a list of participant emails from the CSV file (removing any extra whitespace)
    participants = list(set(formdata[header_email].str.strip()))
    
    # Generate groups using the split_into_groups function
    # We assign the resulting groups to the global variable 'npairs'
    global npairs
    npairs = split_into_groups(participants, group_size)
    
    # Build and print the output string showing the groups on screen
    output_string = "------------------------\n"
    output_string += "Today's coffee partners:\n"
    output_string += "------------------------\n"
    for group in npairs:
        group_list = list(group)
        # Convert each email to "Name (email)" using the CSV data
        names_emails = [f"{formdata[formdata[header_email] == email].iloc[0][header_name]} ({email})" 
                        for email in group_list]
        output_string += "* " + ", ".join(names_emails) + "\n"
    print("\n" + output_string)
    
    round_starter = get_conversation_starter()
    print("Conversation Starter for this round:")
    print(round_starter + "\n")
    # Generate and save group messages for each group
    group_messages()
    
    print("Job done.")

# call main
main()
