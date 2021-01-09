# -*- coding: utf-8 -*-
"""
Labeling objects for Curiosity
"""

import random
from psychopy import prefs
prefs.general['audioLib'] = ['pygame', 'sounddevice', 'pyo']
from psychopy import visual, sound, event, core
from PIL import Image, ImageOps

import constants as c
import calculations


hand_img_obj = Image.open(c.hand_img_file).resize((c.HANDSIZE, int(c.HANDSIZE/3)))

snd_up = sound.Sound(value=c.occl_up)
snd_up.setVolume(0.6)


def label_objects(win, occluders, sposs, isFamiliar, isVertical, side, label_snd, tracker=None):

    hand_img = hand_img_obj
    hand = visual.ImageStim(win)

    for i in range(2):
        occluders[i].setPos(sposs[i])

    # randomise or select positions:
    sposLabeled = sposs[side] if side != None else None
    occluderLabeled = occluders[side] if side != None else None
    sndLabel = sound.Sound(value=label_snd)
    sndLabel.setVolume(0.8)

    if isVertical: # in vertical positioning of occluders
        handX = random.choice([-c.OCC_SIZE, c.OCC_SIZE])
        handY = sposLabeled[1]

        angle = 0
        if handX > 0:
            hand_img = ImageOps.flip(hand_img)
            angle = 180

    else:
        handX, handY, angle = calculations.calculate_handPos(sposLabeled)
        if sposLabeled[0] < 0:
            hand_img = ImageOps.flip(hand_img)

    # calculate handshake steps
    shakeX, shakeY = calculations.calculate_handShake(angle)
    # rotate hand image with angle
    hand_img = hand_img.rotate(angle, expand=True)

    hand = visual.ImageStim(win, hand_img)

    occluderLabeled.lineColor = "red"
    occluderLabeled.lineWidth = 3

    event.clearEvents()

    if tracker:
        tracker.log("Labeling_{0}_STARTS".format("fam_object" if isFamiliar else "test_object"))

    frames = 420 if isFamiliar else 480
    for frameN in range(frames):

        occluders[0].draw()
        occluders[1].draw()

        # play labeling voice
        if frameN == 75:
            pass
            sndLabel.play()

        # pointing hand
        if frameN > 50:
            m = frameN%50
            if m < 25:
                hand.setPos((handX + shakeX*m, handY + shakeY*m))
                hand.draw()
            else:
                hand.setPos((handX + shakeX*(50-m), handY + shakeY*(50-m)))
                hand.draw()

        win.flip()

        _getKeypress(win, tracker=tracker)


def _getKeypress(win, tracker=None):
    """Quits if escape, returns True if space, returns False if nothing is pressed."""

    keys = event.getKeys(keyList=["space", "escape"])
    if keys and keys[0] == "escape":
        print("\nSTOPPED!\n\n\nINSERT COIN...\n")
        if tracker:
           tracker.log("experiment_was_stopped!")
        win.close()
        core.quit()
    elif keys and keys[0] == "space":
        return True
    else:
        return False


