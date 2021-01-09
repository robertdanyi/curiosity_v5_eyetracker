
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 12:17:20 2018

functions providing the next positions and steps for the occluders animation

NOTE: If the screen is refreshing at 60Hz, it means 16.7ms per frame
"""

import random
import numpy as np
import constants as c


def get_rand_flower_pos(): # NOT USED
    """gets  24 random flower positions within a 6*4 grid on the screen"""

    # horizontal: width of screen shortened by 1.5 x flower size (0.75 on each side);  6 slots with 5 gaps between them -> 11 slots
    hSlot = (c.DS[0]-int(c.FSIZE*1.5))/11 # 103; if c.FSIZE*1.5 -> 96

    # vertical: height of screen shortened by 1.5 x flower size (0.75 on each side) 4 slots with 3 gaps between them -> 7 slots
    vSlot = (c.DS[1]-int(c.FSIZE*1.5))/7 # 82; if *1.5 -> 72

    # 4 random samples from each of the 6 horizontal slots
    fXpoints = []
    for x in (-5.5,-3.5,-1.5, 0.5, 2.5, 4.5):
        fXpoints.append(random.sample(np.arange(int(hSlot*x), int(hSlot*x)+hSlot),4))
        # @ -5.5 ->  -566 -> (-566,-463) OR if c.FSIZE*1.5 -> -528, (-528,-432)
        # @ -3.5 ->  -360 -> (-360,-257) OR if c.FSIZE*1.5 -> -336, (-336,-240)
        # @ -1.5 ->  -154 -> (-154, -51) OR if c.FSIZE*1.5 -> -144, (-144,-48)

    # 6 random samples from each of the 4 vertical slots
    fYpoints = []
    for y in (-3.5,-1.5, 0.5, 2.5):
        fYpoints.append(random.sample(range(int(vSlot*y), int(vSlot*y)+vSlot),6))
        # @ -3.5 -> -287 -> (-287,-205)
        # @ -1.5 -> -123 -> (-123,-41)

    fpositions = []
    for m in range(6):
        for n in range(4):
            fpositions.append((fXpoints[m][n], fYpoints[n][m]))

    return fpositions


def get_next_rect_pos(spos, step):
    """gets rectangle positions and steps across different conditions"""

    # check if rect hits left or right borders of screen
    if spos[0] <= -(c.X - (c.OCC_SIZE/2)) or spos[0] >= (c.X - (c.OCC_SIZE/2)):
        step = (-step[0], step[1])
    # check if rect hits bottom or top of screen
    if spos[1] <= -(c.Y-(c.OCC_SIZE/2)) or spos[1] >= (c.Y-(c.OCC_SIZE/2)):
        step = (step[0],-step[1])

    spos = ((spos[0] + step[0], spos[1] + step[1]))

    return spos, step


def getClosingPos(spos1, spos2):
    """calculates the next positions of rectangles when they close up"""

    if spos1[0] > spos2[0]:
        step1X = -c.STPX/2
        step2X = c.STPX/2
    elif spos1[0] < spos2[0]:
        step1X = c.STPX/2
        step2X = -c.STPX/2
    else:
        step1X = 0
        step2X = 0

    if spos1[1] > spos2[1]:
        step1Y = -c.STPY/2
        step2Y = c.STPY/2
    elif spos1[1] < spos2[1]:
        step1Y = c.STPY/2
        step2Y = -c.STPY/2
    else:
        step1Y = 0
        step2Y = 0

    step1 = (step1X, step1Y)
    step2 = (step2X, step2Y)

    spos1 = ((spos1[0] + step1[0], spos1[1] + step1[1]))
    spos2 = ((spos2[0] + step2[0], spos2[1] + step2[1]))

    return spos1, spos2


def changeTrajectories(spos1, spos2, step1, step2, possible_steps):
    """provides new trajectories, 45 or 135 degrees to the previous ones, expecting already used ones"""

    stepss = [stp for stp in possible_steps if stp not in ((step1, step2), (step2, step1))]

    steps = random.choice(stepss)

    step1 = steps[0]
    step2 = steps[1]
    possible_steps = [stp for stp in possible_steps if stp not in ((step1, step2), (step2, step1))]

    spos1 = (spos1[0] + step1[0], spos1[1] + step1[1])
    spos2 = (spos2[0] + step2[0], spos2[1] + step2[1])

    return spos1, spos2, step1, step2, possible_steps


def getFinalSteps(endpos, spos, div):
    """provides the next step when arranging rectangle to its final position """
    stepX = (endpos[0] - spos[0])/div
    stepY = (endpos[1] - spos[1])/div

    return (stepX, stepY)

def arrange_vertical(sposs, top, bottom, div):
    """arranges rectangles to the top and to the bottom of the vertical middle line"""

    top_pos = sposs[0]
    bottom_pos = sposs[1]
    topStep = getFinalSteps(top,top_pos, div)
    top_pos = (top_pos[0] + topStep[0], top_pos[1] + topStep[1])

    bottomStep = getFinalSteps(bottom, bottom_pos, div)
    bottom_pos = (bottom_pos[0] + bottomStep[0], bottom_pos[1] + bottomStep[1])

    return [top_pos, bottom_pos]


def arrange_horizontal(sposs, leftEnd, rightEnd, div):
    """arranges rectangles to (left-up and right-down) or (left-down and right-up) positions"""

    left_pos = sposs[0]
    right_pos = sposs[1]
    step1 = getFinalSteps(leftEnd,left_pos, div)
    left_pos = (left_pos[0] + step1[0], left_pos[1] + step1[1])

    step2 = getFinalSteps(rightEnd,right_pos, div)
    right_pos = (right_pos[0] + step2[0], right_pos[1] + step2[1])

    return [left_pos, right_pos]














