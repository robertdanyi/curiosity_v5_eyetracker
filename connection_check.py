# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 12:37:24 2018

@author: Tobii
"""

import tobii_research as tr
import sys


def check_connection():

    eyetrackers = tr.find_all_eyetrackers()

    if eyetrackers:
        eyetracker = eyetrackers[0]
    else:
        print("\nWARNING! libtobii.TobiiProTracker.__init__: no eye trackers found!\n")
        sys.exit()

    print("\nEye tracker OK!\n")
    print("Address: " + eyetracker.address)
    print("Model: " + eyetracker.model)
    print("Serial number: " + eyetracker.serial_number)

