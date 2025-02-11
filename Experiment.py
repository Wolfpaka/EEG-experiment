# -*- coding: utf-8 -*-
"""
A PsychoPy script for a self-paced reading experiment.
Participants read a story one word at a time.
They press the SPACE key to advance to the next word.
The reaction time for each word is recorded and saved to a CSV file.
Additionally, participant's name, age, gender (selected from a drop-down)
and a file number (to prevent overwriting previous files) are collected.
"""

from psychopy import visual, core, event, gui, data
import os

# --------------------------
# Collect Participant Information via Dialog Box
# --------------------------
# For a drop-down, provide a list as the default for "Gender".
participant_info = {
    "Name": "",
    "Age": "",
    "Gender": ["Male", "Female", "Other"],
    "FileNumber": "1"  # enter a number to append to the file name
}

dlg = gui.DlgFromDict(participant_info, title="Participant Information")
if not dlg.OK:
    core.quit()  # Exit if the dialog is cancelled

# --------------------------
# Create a Unique CSV File Name
# --------------------------
# Get the current date/time string (a safe format for filenames)
dateStr = data.getDateStr()  
# Create a filename using participant's name, date, and file number.
fileName = f"{participant_info['Name']}_{dateStr}_{participant_info['FileNumber']}"
csvFileName = fileName + ".csv"

# (Optional) Check if the file exists already, and if so, warn or modify the file name.
if os.path.exists(csvFileName):
    print(f"Warning: {csvFileName} already exists. It will be overwritten.")

# Open the CSV file for writing
data_file = open(csvFileName, "w")
data_file.write("Name,Age,Gender,Word,RT\n")  # Write header row

# --------------------------
# Set Up the PsychoPy Window
# --------------------------
win = visual.Window(size=(800, 600), color='black', units='norm')

# --------------------------
# Display Instructions
# --------------------------
instructions = visual.TextStim(
    win,
    text=(
        "You will read a story one word at a time.\n"
        "Press the SPACE key to see the next word.\n\n"
        "Press any key to begin."
    ),
    color='white',
    height=0.07
)
instructions.draw()
win.flip()
event.waitKeys()  # Wait for any key press to start

# --------------------------
# Define the Story and Split it into Words
# --------------------------
story_text = (
    "Once upon a time there was a brave knight who fought dragons and saved the kingdom."
)
words = story_text.split()  # Create a list of words

# --------------------------
# Create a Clock to Measure Reaction Times
# --------------------------
clock = core.Clock()

# --------------------------
# Loop Through Each Word in the Story
# --------------------------
for word in words:
    # Create and display the word stimulus
    word_stim = visual.TextStim(win, text=word, color='white', height=0.1)
    word_stim.draw()
    win.flip()
    
    # Reset the clock when the word is shown
    clock.reset()
    
    # Wait for the SPACE key and record the reaction time (RT)
    keys = event.waitKeys(keyList=['space'], timeStamped=clock)
    rt = keys[0][1]  # Extract the reaction time
    
    # Write the participant info, word, and RT to the CSV file
    # (The Gender field will be set to the selected value from the drop-down.)
    data_file.write(f"{participant_info['Name']},{participant_info['Age']},{participant_info['Gender']},{word},{rt}\n")

# --------------------------
# Cleanup: Close File, Window, and Quit
# --------------------------
data_file.close()
win.close()
core.quit()
