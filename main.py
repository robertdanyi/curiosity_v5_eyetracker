# -*- coding: utf-8 -*-
"""
main file for "Curiosity" exp
"""

from __future__ import print_function
import datetime
import os
import random
from pygaze.display import Display
from pygaze.keyboard import Keyboard
from pygaze.time import Time
from pygaze.logfile import Logfile
from Subject_class import Subject
from InfantTobiiEyeTracker_class import InfantTobiiTracker
from connection_check import check_connection
import constants as c



# initialize a pygaze keyboard
kb = Keyboard(keylist=['space'],timeout=None)

### check screen size in constants
assert (c.DS[0] == 1920) and (c.DS[1] == 1200), "Set display size (DS in constants) to (1920x1200) to use the code with Tobii T60XL"

### check if Tobii device is connected
check_connection()

# new subject object
newSubject = Subject()
newSubject.showGui()

# nr derived from subject nr will determine the placement of new objects in test phase
test_stimuli_nr = newSubject.subject_number%4

# stimuli order for familiarisation of new objects
start_side = random.choice(["left", "right"])
chosen_folders = random.choice(c.order_dict[start_side])
test_shelves = c.log_positions[str(test_stimuli_nr)]
stim_folder_paths = [os.path.join(c.STIM_DIR, folder) for folder in chosen_folders] # list of folderpaths
print("stimuli folders:", chosen_folders)

# familiar stimuli folders
famstimuli = c.FAM_IMGS

# Tobii output logfile folder path and filename format
fulltimenow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
datenow = datetime.datetime.now().strftime("%Y-%m-%d")
subjectNumber = "0" + str(newSubject.subject_number) if len(str(newSubject.subject_number)) < 2 else str(newSubject.subject_number)

logfolderpath = os.path.join(c.LOGDIR, "{0}_{1}_{2}".format(subjectNumber, newSubject.subject_code, fulltimenow))
if not os.path.exists(logfolderpath):
    os.makedirs(logfolderpath)
logfilepath = os.path.join(logfolderpath, "s{0}_{1}_{2}".format(subjectNumber, newSubject.subject_code, datenow))

# initialize a Timer
timer = Time()

# initialize the display for stimuli
disp = Display(disptype="psychopy", dispsize=c.TOBII_DISPSIZE, screennr=0, bgc = "grey")

# initialize a tobiitracker
tracker = InfantTobiiTracker(disp, logfilepath)

# create a new logfile (for TESTing purposes only)
eventlog = Logfile(filename="{0}\subj{1}_caliblog_{2}".format(logfolderpath, subjectNumber, datenow))
eventlog.write(["\nDate and time of experiment: {0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))])
eventlog.write(["Subject number: {0}".format(subjectNumber)])
eventlog.write(["Test positions: 1. interesting: {0}, 2. interesting: {1}".format(test_shelves[0], test_shelves[1])])
eventlog.write(["Subject code: {0}".format(newSubject.subject_code)])
eventlog.write(["Subject's age: {0} months and {1} days\n".format(newSubject.subject_age[:2], newSubject.subject_age[2:])])
eventlog.write(["\nEVENT", "TIME"])

### calibration
print("\n\tInfant calibration module.\n\t-> Press 'space' to start!\n")

# wait for space pressed
kb.get_key(keylist=['space'], timeout=None, flush=True)

# call preCalibrate() function
while tracker.preCalibrate() != True:
    tracker.preCalibrate()

print("\n\tStarting calibration\n")
tracker.calibrate(eventlog)

### play animations
import animation_screen as anim
tracker.start_recording() # subscribes to tobii gaze data stream, and writes the .tsv file header
# FAMILIAR phase
rounds=2
side_order = random.choice([[0,1,0], [1,0,1]])[:rounds]
anim.introduce_familiar_objects(tracker, famstimuli, side_order)

# TEACHING phase
rounds=3
anim.introduce_new_objects(tracker, stim_folder_paths[:rounds])

# TEST phase
anim.run_test(tracker, test_stimuli_nr)

### shut down experiment
print("\tExperiment ended.")
eventlog.write(["Experiment closed ", timer.get_time()])

timer.expend()

