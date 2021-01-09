# -*- coding: utf-8 -*-
"""
stimuli animation, labeling and testing functions for 'Curiosity 2.0' experiment
Lab version

test interesting label: random choice
pointing task int side: alternating
"""

from __future__ import division
from __future__ import print_function
import os
import time
import random
from datetime import datetime
from threading import Timer

from psychopy import prefs
prefs.general['audioLib'] = ['pygame', 'sounddevice', 'pyo']
from psychopy import visual, monitors
from psychopy import core, sound, event

import constants as c
import calculations
import occluders_animation as occl_anim
import labeling_objects as labeling


mon = monitors.Monitor("TobiiT60XL", width=52, distance=65) #check width

win = visual.Window(size=c.DS, monitor=mon, screen=0, fullscr=True, units='pix', color=([0.4, 0.4, 0.4]), colorSpace="rgb", winType="pyglet",
                    waitBlanking=False, allowGUI=False)
win.mouseVisible = False

# util
pulse = calculations.get_pulserange()

# image and sound stimuli objects
img = c.Image_stimuli(win)
snd = c.Sound_stimuli(win)

# choose an interesting sound label randomly for labeling new objects
int_label_idx = random.choice([0,1])
int_label_snd = snd.label_sounds[int_label_idx]

# arrange test sounds so that interesting is at index 0
test_lbl_snds = snd.test_label_snds
int_test_snd = test_lbl_snds.pop(int_label_idx)
test_lbl_snds.insert(0,int_test_snd)


def introduce_familiar_objects(tracker, stims, side_order):
    """
    Parameters
    ----------
    tracker : InfantTobiiTracker object
        used for logging.
    stims : list of strings
        two .jpg file paths (apple and banana pics)
    side_order : list of integers
        0 and 1 in random order,
        determines which object to label from stims, and which label sound to play.
        These will be in sync because both the label list and the stim list are randomised the same way.

    Returns
    -------
    None.

    """

    rounds = len(side_order)

    # randomise order of stims and labels the same way
    stim_order = random.sample([0,1], 2)
    first, second = stim_order[0], stim_order[1]
    stims = [stims[first], stims[second]]
    fam_label_sounds = [snd.fam_label_sounds[first], snd.fam_label_sounds[second]]

    for n in range(rounds):

        # for debugging
        print("\nApple and banana, round {0}".format(n+1))

        occluders = _create_occluders(2)

        show_face(tracker)

        # get label
        side = side_order[n]
        fam_label_snd = fam_label_sounds[side]

        objstims = [
                visual.ImageStim(win, image=stims[0], pos=c.start_pos1, size=c.OBJ_SIZE),
                visual.ImageStim(win, image=stims[1], pos=c.start_pos2, size=c.OBJ_SIZE)
                ]

        ## objects for 6 seconds ##
        event.clearEvents()
        tracker.log("familiar_objects_shown")
        show_fam_objects(tracker, objstims)

        ## occluders float down to cover objects ##
        event.clearEvents()
        snd.snd_down.play()
        _move_occluders(occluders, frames=c.occl_lim, positions=[c.rect_pos1, c.rect_pos2],
                        step= -c.down, objs=objstims)
        time.sleep(1)

        ## shuffle ##
        sposs = occl_anim.shuffle_occluders(win, occluders, isFamiliar=True, isVertical=False)

        labeling.label_objects(win, occluders, sposs=sposs, isFamiliar=True, isVertical=False,
                               side=side, label_snd=fam_label_snd, tracker=tracker) #, stims=objstims)

        ## occluders up ##
        objstims[0].setPos(sposs[0])
        objstims[1].setPos(sposs[1])
        tracker.log("labeling_fam_occluders_up")
        snd.snd_up.play()
        _move_occluders(occluders, frames=120, positions=[sposs[0], sposs[1]], step=c.up, objs=objstims)

        tracker.log("Labeling_{0}_ENDS".format("fam_object"))


def introduce_new_objects(tracker, stimpaths):

    videofiles = [os.path.join(path, f) for path in stimpaths for f in os.listdir(path) if f.endswith(".avi")]
    imgfiles = [os.path.join(path, f) for path in stimpaths for f in os.listdir(path) if f.endswith(".png")]

    anim_stims = [visual.MovieStim3(win, filename=videofile, size=c.STIMSIZE, flipVert=False, noAudio=True) for videofile in videofiles]
    img_stims = [visual.ImageStim(win, image=imgfile, size=c.STIMSIZE) for imgfile in imgfiles]

    for n in range(len(anim_stims)):

        occluders = _create_occluders(2)

        # The last test round has "vertical ending"
        isVertical=True if n==len(anim_stims)-1 else False

        int_side = stimpaths[n].split("_")[-2]
        i_first = True if stimpaths[n].split("_")[-1]=="first" else False
        t = 1.0 if i_first else 6.5

        show_face(tracker)

        tracker.log("Familiarisation_anim{0}_{1}{2}".format(str(n+1), int_side, "1" if i_first else "2"))

        # for code debugging
        print("\nFamiliarisation animation {0}".format(n+1))
        print("\tinteresting side:", int_side, "; moves:", " first" if i_first else " second")

        _play_familiarisation_anim(tracker, anim_stims[n], t)
        img_stim = img_stims[n]

        ### occluders float down to cover objects ###
        event.clearEvents()
        tracker.log("occluders_going_down")
        snd.snd_down.play()
        _move_occluders(occluders, frames=c.occl_lim, positions=[c.rect_pos1, c.rect_pos2],
                               step= -c.down, objs=[img_stim])
        time.sleep(1)

        # shuffle
        tracker.log("shuffle_starts")
        sposs = occl_anim.shuffle_occluders(win, occluders, False, isVertical)

        labeling.label_objects(win, occluders, tracker=tracker, isFamiliar=False, isVertical=isVertical,
                               sposs=sposs, side=random.choice([0,1]), label_snd=int_label_snd)

        tracker.log("Labeling_{0}_ENDS".format("test_object"))


def run_test(tracker, test_stimuli_nr):

    occluders = _create_occluders(4)

    int_obj, boring_obj = img.int_obj, img.boring_obj
    fam_obj1, fam_obj2 = img.fam_obj1, img.fam_obj2

    fam_img_pool = random.sample([c.FAM_IMGS[0], c.FAM_IMGS[1]], 2)
    fam_img1 = fam_img_pool[0]
    fam_img2 = fam_img_pool[1]
    fam_pos1 = c.fam_positions[str(test_stimuli_nr)][0]
    fam_pos2 = c.fam_positions[str(test_stimuli_nr)][1]
    # for logging
    fam1_name = os.path.basename(fam_img1).split("_")[0]
    fam1_name_pos = c.fam_log_positions[str(test_stimuli_nr)][0]
    target_shelf = c.log_positions[str(test_stimuli_nr)][0] # target shelf is where the labeled obj is

    # blank for 1 s
    _draw_imgs_on_screen(60)

    for k in (0,1):

        int_pos = c.positions[str(test_stimuli_nr)][k]
        boring_pos = c.positions[str(test_stimuli_nr)][1-k]

        int_obj.setPos(int_pos)
        boring_obj.setPos(boring_pos)

        fam_obj1.setImage(fam_img1)
        fam_obj1.setPos(fam_pos1)
        fam_obj2.setImage(fam_img2)
        fam_obj2.setPos(fam_pos2)

        print("\nTest {0}".format(str(k+1)))

        # for logging:
        label_type = "intLabel" if k==0 else "otherLabel"
        test_word = test_lbl_snds[k].split("_")[-3]
        print("\tlabel: {0}, int pos: {1}, test word: '{2}'".format(label_type, target_shelf, test_word))

        snd_test = sound.Sound(value=test_lbl_snds[k]) # in order
        snd_test.setVolume(0.7)

        _draw_imgs_on_screen(30, imgs=occluders) # occl shown 500 ms

        # lift up occluders
        # baseline starts 40 frames after occluders started to lift
        tracker.log("lifting_occluders")
        bl_start_log = Timer(0.667, tracker.log, ["baseline_starts"])
        bl_start_log.start()

        snd.snd_up.play()
        _move_occluders(occluders, frames=60, size=c.SIZE, positions=c.four_positions, step=c.up,
                        objs=[int_obj, boring_obj, fam_obj1, fam_obj2], tracker=tracker)

        # baseline (started already 20 frames ago when lifting occls)
        _draw_imgs_on_screen(220, imgs=[int_obj, boring_obj, fam_obj1, fam_obj2], tracker=tracker)

        tracker.log("att_gett_starts_baseline_ends")

        snd_test.play()
        _draw_att_getter(160, imgs=[int_obj, boring_obj, fam_obj1, fam_obj2]) # 2.7 s

        tracker.log("test__{0}:{1}:{2}_{3}:{4}_STARTS"
                    .format(label_type, test_word, target_shelf, fam1_name, fam1_name_pos))

        _draw_imgs_on_screen(240, imgs=[int_obj, boring_obj, fam_obj1, fam_obj2], tracker=tracker)

        tracker.log("test__{0}_ENDS".format(label_type))

        _draw_imgs_on_screen(30) #0.5s blank

    tracker.log("Experiment_ended")
    tracker.stop_recording()
    tracker.close()

    # int side to pointing task image alternation
    # at idx 0 is the right_side int image
    img_choice = 0 if test_stimuli_nr%2==0 else 1 # -> right if even nr
#    print("img choice for pointing task:", img_choice)
    run_pointing_task(test_lbl_snds, img_choice)


def run_pointing_task(test_sounds, img_choice):

    # set test img to the same image both times
    # to avoid side bias
    p_test_imgs_list = c.test_imgs
    p_test_img = img.p_test_img
    p_test_img.setImage(p_test_imgs_list[img_choice])

    occluders = _create_occluders(2)

    int_label_string = test_sounds[0].split("_")[-3]
    boring_label_string = test_sounds[1].split("_")[-3]
    labels = [int_label_string, boring_label_string]

    date_stim = visual.TextStim(win, text=datetime.now().strftime("%B %d, %Y, %H:%M"),
                                pos=(300,100), height=60, color="black", bold=True, wrapWidth=1600, alignHoriz="right")
    int_label_stim = visual.TextStim(win, text="Interesting label: {0}".format(int_label_string.upper()),
                                     pos=(300,0), height=80, color="black", bold=True, wrapWidth=1600, alignHoriz="right")
    boring_label_stim = visual.TextStim(win, text="Other label: {0}".format(boring_label_string.upper()),
                                        pos=(300,-100), height=80, color="black", bold=True, wrapWidth=1600, alignHoriz="right")

    print("\n###### Press SPACE to start the pointing task #######")
    print("\tInteresting label: ", int_label_string)

    win.flip()

    event.clearEvents()
    while not _getKeypress():
        pass

    for i in range(2):
        print("\nPointing Test {0}. \n\tMelyik a {1}?".format(str(i+1), labels[i]))

        #attention getter
        snd.attGettSound.play()
        _draw_att_getter(120)

        _draw_imgs_on_screen(30, imgs=occluders)

        # lift up occluders
        snd.snd_up.play()
        _move_occluders(occluders, frames=75, positions=[c.start_pos1, c.start_pos2], step=c.up, objs=[p_test_img])

        while not _getKeypress():
            p_test_img.draw()
            win.flip()

    event.clearEvents()
    while not _getKeypress():

        date_stim.draw()
        int_label_stim.draw()
        boring_label_stim.draw()
        win.flip()

    print("\nDONE! Thanks!\n\n\nINSERT COIN...\n")
    win.close()
    core.quit()


def show_face(tracker):

    _draw_imgs_on_screen(30)

    tracker.log("intro_with_face_start")
    snd.snd_szia.play()
    _draw_imgs_on_screen(150, imgs=[img.face])


def show_fam_objects(tracker, objstims):

    _draw_imgs_on_screen(60, imgs=objstims, tracker=tracker)

    step = 2
    count = 2
    for i in [0,1]:
        snd.snd_fam.play()
        for frameN in range(120):  # 2*2 seconds
            objstims[i].setOri(count)
            for obj in objstims:
                obj.draw()
            win.flip()
            if count == 30:
                step = -2
            elif count == -30:
                step = 2
            count += step

            _getKeypress(tracker=tracker)

    time.sleep(1) # show objects for another 1s


def _draw_imgs_on_screen(frames, imgs = [], tracker=None):

    for f in range(frames):
        for image in imgs:
            image.draw()
        win.flip()

        _getKeypress(tracker=tracker)


def _draw_att_getter(frames, imgs=[]):

    period = int(frames/8)

    for framesN in range(frames):
        for image in imgs:
            image.draw()
        f = framesN%(int(frames/2))
        if f < period:
            img.att_getters[0].draw()
        elif f < 2*period:
            img.att_getters[1].draw()
        elif f < 3*period:
            img.att_getters[2].draw()
        else:
            img.att_getters[3].draw()

        win.flip()

#    for frameN in range(frames):
#        for image in imgs:
#            image.draw()
#        img.att_getter.setSize((c.ATTSIZE+pulse[frameN]*6,c.ATTSIZE+pulse[frameN]*6))
#        img.att_getter.draw()
#        win.flip()


def _move_occluders(occluders, frames=120,  size=c.OCC_SIZE, positions=c.four_positions, step=0, objs=[], tracker=None):
    """Moves occluders from positions with step (step will be negative, if downwards)."""

    for frame in range(frames):

        for obj in objs:
            obj.draw()
        for i in range(len(occluders)):
            occluders[i].setPos(positions[i])
            occluders[i].draw()
        win.flip()

        if len(positions) == 2 :
            positions = [(pos[0], pos[1]+step) for pos in positions]
        else:
            positions = [(pos[0], pos[1]-step) for pos in positions[:2]] + [(pos[0], pos[1]+step) for pos in positions[2:]]

#        if  tracker and (frame==40):
#            tracker.log("baseline_starts") # baseline for 60-40=20 frames


def _play_familiarisation_anim(tracker, anim_stim, t):
    """Plays animation with interesting and boring objects."""

    snd_start = Timer(t, snd.int_sound.play)
    snd_start.start()

    event.clearEvents()
    while anim_stim.status != visual.FINISHED:

        anim_stim.draw()
        win.flip()

        _getKeypress(tracker=tracker)


def _create_occluders(nr):

    if nr == 4:
        return [visual.Rect(win, width=c.SIZE, height=c.SIZE, pos=pos, lineColor='black', fillColor='black')
                for pos in c.four_positions]
    else:
        return [visual.Rect(win, width=c.OCC_SIZE, height=c.OCC_SIZE, pos=pos, lineColor='black', fillColor='black')
                for pos in [c.start_pos1, c.start_pos2]]


def _getKeypress(tracker=None):
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

#############################


