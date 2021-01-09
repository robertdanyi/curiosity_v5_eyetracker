# -*- coding: utf-8 -*-
"""
CURIOSITY - Subject_class
GUI for experimenter
Created on Fri Sep 21 16:37:11 2018
"""

import os
import datetime
import tkinter as tk

import constants as c


class Subject(object):

    subjectsLog = os.path.join(c.LOGDIR, "subjects_log.txt")
    if not os.path.exists(subjectsLog):
        with open(subjectsLog, "w") as slog:
            slog.write("\n")

    def __init__(self):

        self.datetime_of_exp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    # create GUI
    def showGui(self):

        tobii_disp = c.DS
        font = ("Helvetica", 16)
        gui = tk.Tk()
        gui.title("Experiment and Subject data")
        gui.geometry("600x400")
        gui.grid_rowconfigure(0, weight=1)
        gui.grid_rowconfigure(8, weight=1)
        gui.grid_columnconfigure(0, weight=1)

        # frames
        fsettings = tk.Frame(gui, width=600)
        fdata = tk.Frame(gui)
        fExitbutton = tk.Frame(gui, width=600)

        # layout
        fsettings.grid(sticky="ew", columnspan=2)
        fdata.grid(sticky="w")
        fExitbutton.grid(row=13, column=1, sticky="nsew")


        # widgets
        tk.Label(fsettings, text="'CURIOSITY' EXPERIMENT", font=("Arial", 18), fg="blue").grid(row=1, sticky="w")
        tk.Label(fsettings, text="Date and time: {}".format(datetime.datetime.now().strftime("%Y-%m-%d  %I:%M %p")), font=font).grid(row=2, sticky="w")
        tk.Label(fsettings, text="Display resolution of Tobii monitor: {}".format(tobii_disp), font=font).grid(row=3, sticky="w")

        tk.Label(fsettings, text="").grid(row=4, sticky="w")

        tk.Label(fdata, text="Age of subject (MMDD): ", anchor="nw", font=font).grid(row=5, sticky=tk.W)
        age = tk.Entry(fdata,width=4, font=font)
        age.grid(column=1, row=5, sticky=tk.W)

        tk.Label(fdata, text="Gender of subject (f or m): ", anchor="nw", font=font).grid(row=6, sticky=tk.W)
        gender = tk.Entry(fdata,width=4, font=font)
        gender.grid(column=1, row=6, sticky=tk.W)

        tk.Label(fdata, text="Initials of subject: ", anchor="nw", font=font).grid(row=7, sticky=tk.W)
        initials = tk.Entry(fdata,width=4, font=font)
        initials.grid(column=1, row=7, sticky=tk.W)

        # gap column
        tk.Label(fdata, text="", anchor="nw", font=font).grid(row=5, column=2, rowspan=4, sticky=tk.W)

        # invalidity message
        validityline = tk.Label(gui, text="", anchor="nw", font=font, fg="red")
        validityline.grid(row=9, sticky=tk.W)

        # submit button
        tk.Button(fdata, font=font, bg='green', text = "SUBMIT", cursor="arrow",
                  command = lambda: self._onSubmitButton(gui, age, gender, initials, validityline)).grid(row=7, column=3, rowspan=3, pady=5,sticky="w")

        # exit button
        tk.Button(fExitbutton, font=font, bg='red', text = "EXIT",
                  command = lambda: self._onExitButton(gui)).grid(sticky="s")

        gui.config(cursor="")

        gui.mainloop()


    def _onSubmitButton(self, gui, age, gender, initials, validityline):

        ### validation ###
        # age
        if self._checkIfInputIsInt(age.get()) == False:
            validityline.config(text = "Age > Please enter two digits for months, two for days.")
        elif len(str(age.get())) < 3:
            validityline.config(text = "Age > Please enter two digits for months, two for days.")
        # gender
        elif gender.get() not in ["f", "m"]:
            validityline.config(text = "Invalid gender. Please enter 'f' for female, or 'm' for male.")
        # initials
        elif len(str(initials.get())) < 2:
            validityline.config(text = "Please enter initials of subject (2-4 letters).")

        else:
            self.subject_age = age.get()
            self.subject_code = str(initials.get()).upper() +"_" + str(gender.get())
            self._writeSubjectLog(str(initials.get()).lower())
            gui.destroy()


    def _onExitButton(self, gui):
        gui.destroy()


    def _writeSubjectLog(self, initials):
        with open(Subject.subjectsLog, "a+") as slog:
            data = slog.readlines()
            if len(data) > 1:
                self.subject_number = int(data[-1]) + 1
                print( "subject nr: ", self.subject_number)
            else:
                self.subject_number = 1

            if initials != "test":
                slog.write("\n\nTime of experiment: {0}\nSubject nr: {1}\nSubject code: {2}\nSubject age: {3}\n{1}"
                           .format(self.datetime_of_exp, self.subject_number, self.subject_code, self.subject_age))


    def _checkIfInputIsInt(self, number):
        try:
            int(number)
        except ValueError:
            return False
        return True


#    def _get_subject_number():
#        with open(Subject.subjectsLog, "a+") as slog:
#            data = slog.readlines()
#            if len(data) > 1:
#                nr = int(data[-1]) + 1
#            else:
#                nr = 1
#
#            print( "subject nr: ", nr)
#            return nr




