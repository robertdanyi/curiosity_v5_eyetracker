# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 08:29:06 2018

@author: danyir@ceu.edu
"""

from __future__ import division

import constants as cons
import math
import numpy as np



def get_pulserange():
    """calculates shrinking/growing range for the flowers/attGetter relative to size constant"""
    pulse = []
    range1 = np.linspace(1, cons.DS[1]/60, 30,endpoint=False).tolist()
    range2 = np.linspace(cons.DS[1]/60, -cons.DS[1]/60, 60,endpoint=False).tolist()
    range3 = np.linspace(-cons.DS[1]/60, 0, 30,endpoint=False).tolist()
    pulse.extend(range1 + range2 + range3 + range1 + range2)

    return pulse


def pythagoras(a,b):

    return math.sqrt(math.pow(a,2) + math.pow(b,2))


def calculate_handPos(spos):
    """calculates the position and angle of the pointing hand depending on the obj position"""

    b = math.fabs(spos[0]) # x
    a = math.fabs(spos[1]) # y
    c = pythagoras(a,b)  # math.sqrt(math.pow(a,2) + math.pow(b,2))
    cosAngle = b / c
    sinAngle = a / c

    handC = c - cons.OCC_SIZE *1.025 #*1.1
    if spos[0] < 0:
        handX = cosAngle * -handC

    else:
        handX = cosAngle * handC
    if spos[1] < 0:
        handY = sinAngle * -handC
    else:
        handY = sinAngle * handC

    angleInRadians = math.atan2(spos[1],spos[0])
    """ degrees = radians * 57.29577951 """
    angle = angleInRadians * 57.29577951

    return handX, handY, angle


def calculate_handShake(angle):
    """calculates the hand movement steps according to the angle"""

    if angle <= -135:
        handShake = (8, (angle+180)/10)
#    elif angle <= -90:
#        handShake = (-8/45*(angle+90), 4.5)
    elif angle <= -45:
        handShake = (-8/45*(angle+90), 4.5)
#    elif angle <= 0:
#        handShake = (-8, -angle/10)
    elif angle <= 45:
        handShake = (-8, -angle/10)
#    elif angle <= 90:
#        handShake = (8/45*(angle-90), -4.5)
    elif angle <= 135:
        handShake = (8/45*(angle-90), -4.5)
    elif angle <= 180:
        handShake = (8, (angle-180)/10)

    shakeX = handShake[0]/10
    shakeY = handShake[1]/10

    return shakeX, shakeY


def calculate_distance(spos1, spos2):
    """calculates the distance between the center spots of the two objects"""

    x1, y1 = spos1
    x2, y2 = spos2
    abs_x1, abs_x2 = math.fabs(x1), math.fabs(x2)
    abs_y1, abs_y2 = math.fabs(y1), math.fabs(y2)

    if x1 >= 0 and x2 >= 0:
        a = (x2 - x1) if x1 < x2 else (x1 - x2)
    elif x1 < 0 and x2 < 0:
        a = (abs_x2 - abs_x1) if abs_x1 < abs_x2 else (abs_x1 - abs_x2)
    else:
        a = abs_x1 + abs_x2

    if y1 >= 0 and y2 >= 0:
        b = (y2 - y1) if y1 < y2 else (y2 - y1)
    elif y1 < 0 and y2 < 0:
        b = (abs_y2 - abs_y1) if abs_y1 < abs_y2 else (abs_y1 - abs_y2)
    else:
        b = abs_y1 + abs_y2

    c = pythagoras(a,b)
    return c
