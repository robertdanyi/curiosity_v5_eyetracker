# -*- coding: utf-8 -*-
"""
code for demoing curiosity exp for parents
"""

from __future__ import division
from __future__ import print_function
import os
import time
import random
from threading import Timer

from psychopy import prefs
prefs.hardware['audioLib'] = ['pygame', 'PTB', 'sounddevice', 'pyo']
from psychopy import visual
from psychopy import core, sound, event

#from PIL import Image, ImageOps

import constants as c
# import calculations
import occluders_animation as occl_anim
import labeling_objects as labeling

print('audio backend', sound.Sound)


#disp_size=(1920,1080)
# psychopy window instance
win = visual.Window(size=c.DS, screen=0, fullscr=False, units='pix', color=([0.4, 0.4, 0.4]), colorSpace="rgb", winType="pyglet")
win.mouseVisible = False
sound_choice = random.choice([0,1])
new_obj_label = [c.newLabelSoundFile1, c.newLabelSoundFile2][sound_choice]


def demo_main():

    fam_stims = c.FAM_IMGS
    side = random.choice([0,1]) # side to label
    demo_introduce_familar_objects(fam_stims, side)

    new_stims = [os.path.join(c.STIM_DIR, folder) for folder in os.listdir(c.STIM_DIR)]
    demo_introduce_new_objects(new_stims)
    # call test
    run_test()


def demo_introduce_familar_objects(stims, side):

    occluders = _create_occluders(2)

    show_face()

    fam_label_sounds = c.FAM_SNDS # to pass on to labeling

    objStim1 = visual.ImageStim(win, stims[0], pos=c.start_pos1, size=c.OBJ_SIZE)
    objStim2 = visual.ImageStim(win, stims[1], pos=c.start_pos2, size=c.OBJ_SIZE)
    objstims = [objStim1, objStim2]

    ## show objects for 6 seconds ##
    event.clearEvents()
    show_fam_objects(objstims)

    ### occluders float down to cover objects ###
    event.clearEvents()
    snd_down = sound.Sound(value=c.occl_down)
    snd_down.setVolume(0.6)
    snd_down.play()
    _move_occluders(occluders, frames=c.occl_lim, positions=[c.rect_pos1, c.rect_pos2],
                    step= -c.down, objs=[objStim1, objStim2])

    time.sleep(1)

    # call shuffle
    sposs = occl_anim.shuffle_occluders(win, occluders, True, False)

    # call labeling
    labeling.label_objects(win, occluders, sposs=sposs, isFamiliar=True, isVertical=False, side=side, label_snd=fam_label_sounds[side])

    ## occluders up ##
    objstims[0].setPos(sposs[0])
    objstims[1].setPos(sposs[1])
    snd_up = sound.Sound(value=c.occl_up)
    snd_up.setVolume(0.6)
    snd_up.play()
    _move_occluders(occluders, frames=120, positions=[sposs[0], sposs[1]], step=c.up, objs=objstims)


def demo_introduce_new_objects(stims): # soundsList=None,

    occluders = _create_occluders(2)

    isVertical=False

    show_face()

    n = random.choice([0,1,2,3])

#    print("\nFamiliarisation round {0}".format(n+1))
    img_stim = _play_familiarisation_anim(stims[n])

    ### occluders float down to cover objects ###
    snd_down = sound.Sound(value=c.occl_down)
    snd_down.setVolume(0.6)
    event.clearEvents()
    snd_down.play()
    _move_occluders(occluders, frames=c.occl_lim, positions=[c.rect_pos1, c.rect_pos2],
                           step= -c.down, objs=[img_stim])

    time.sleep(1)

    # call shuffle
    sposs = occl_anim.shuffle_occluders(win, occluders, False, isVertical)

    # call labeling
    labeling.label_objects(win, occluders, isFamiliar=False, isVertical=False, sposs=sposs, side=random.choice([0,1]), label_snd=new_obj_label)


def run_test():

    test_stimuli_nr = random.choice([0,1,2,3])

    test_sounds = [c.testLabelSoundFile1, c.testLabelSoundFile2]

    # arrange test sounds so that interesting is at index 0
    int_sound = test_sounds.pop(sound_choice)
    test_sounds.insert(0,int_sound)

    int_img = c.INT_IMG
    boring_img = c.BORING_IMG

    int_obj = visual.ImageStim(win, int_img, size=c.interesting_size)
    boring_obj = visual.ImageStim(win, boring_img, size=c.boring_size)

    fam_img_pool = random.sample([c.FAM_IMGS[0], c.FAM_IMGS[1]], 2)
    fam_img1 = fam_img_pool[0]
    fam_img2 = fam_img_pool[1]
    fam_pos1 = c.fam_positions[str(test_stimuli_nr)][0]
    fam_pos2 = c.fam_positions[str(test_stimuli_nr)][1]

    snd_up = sound.Sound(value=c.occl_up)
    snd_up.setVolume(0.6)

    # blank for 1 s
    _draw_imgs_on_screen(60)

    # pause for 1 s
    time.sleep(1)
    for k in (0,1):

        int_pos = c.positions[str(test_stimuli_nr)][k]
        boring_pos = c.positions[str(test_stimuli_nr)][1-k]

        int_obj.setPos(int_pos)
        boring_obj.setPos(boring_pos)

        fam_obj1 = visual.ImageStim(win, fam_img1, size=c.fam_size, pos=fam_pos1)
        fam_obj2 = visual.ImageStim(win, fam_img2, size=c.fam_size, pos=fam_pos2)

        occluders = [visual.Rect(win, width=c.SIZE, height=c.SIZE, pos=pos, lineColor='black', fillColor='black')
            for pos in c.four_positions]

        snd_test = sound.Sound(value=test_sounds[k]) # in order
        snd_test.setVolume(0.7)

        _draw_imgs_on_screen(30, imgs=occluders) # occl shown 500 ms

        # lift up occluders
        snd_up.play()
        _move_occluders(occluders, frames=60, positions=c.four_positions, step=c.up,
                        objs=[int_obj, boring_obj, fam_obj1, fam_obj2])

        _draw_imgs_on_screen(240, imgs=[int_obj, boring_obj, fam_obj1, fam_obj2])

        snd_test.play()
        _draw_att_getter(160, imgs=[int_obj, boring_obj, fam_obj1, fam_obj2]) # 2.7 s

        _draw_imgs_on_screen(240, imgs=[int_obj, boring_obj, fam_obj1, fam_obj2])
        _draw_imgs_on_screen(30) #0.5s blank

    win.close()
    core.quit()


def show_fam_objects(objstims):

    snd = sound.Sound(value=c.fam_moving_snd)
    snd.setVolume(0.8)

    _draw_imgs_on_screen(60, imgs=objstims)

    step = 2
    count = 2
    for i in [0,1]:
        snd.play()
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

            if _getKeypress():
                objstims[i].setOri(0)
                snd.stop()
                break

    time.sleep(1) # show objects for another 1s


def _draw_imgs_on_screen(frames, imgs = [], snd=None, test=None):

    for f in range(frames):
        for img in imgs:
            img.draw()
        win.flip()

        if _getKeypress():
            if snd:
                snd.stop()
            break


def _draw_att_getter(frames, imgs=[]):

    att_getters = [visual.ImageStim(win, ag) for ag in c.att_gett_imgs]

    period = int(frames/8)

    for framesN in range(frames):
        for image in imgs:
            image.draw()
        f = framesN%(int(frames/2))
        if f < period:
            att_getters[0].draw()
        elif f < 2*period:
            att_getters[1].draw()
        elif f < 3*period:
            att_getters[2].draw()
        else:
            att_getters[3].draw()

        win.flip()


def _move_occluders(occluders, frames=120,  positions=c.four_positions, step=0, objs=[]):
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


def _play_familiarisation_anim(stim_dir):
    """Plays animation with interesting and boring objects. Returns the ending screenshot."""

    videofile = next((os.path.join(stim_dir, f) for f in os.listdir(stim_dir) if f.endswith(".avi")), None)
    imgfile = next((os.path.join(stim_dir, f) for f in os.listdir(stim_dir) if f.endswith(".png")), None)

    anim_stim = visual.MovieStim3(win, videofile, size=(1920,1080), flipVert=False)
    img_stim = visual.ImageStim(win, imgfile, size=(1920,1080))
#    print("\tanimation:", os.path.basename(videofile))

    int_sound = sound.Sound(value=c.INT_SOUND)
    int_sound.setVolume(0.35)

#    int_side = "left" if imgfile.endswith("0.png") else "right" # interesting side be determined from the name of imagefile -> to pass on to labeling
    i_first = True if videofile.split(".")[0].endswith("1") else False
#    print("\tanimation int_side:", int_side)
#    print("\ti_first:", i_first)

    t = 1.0 if i_first else 6.5
    snd_start = Timer(t, int_sound.play)
    snd_start.start()

    event.clearEvents()
    while anim_stim.status != visual.FINISHED:

        anim_stim.draw()
        win.flip()

        if _getKeypress():
            snd_start.cancel()
            int_sound.stop()
            break

    return img_stim


def show_face():

    _draw_imgs_on_screen(30)

    face = visual.ImageStim(win, c.face_img, size=c.STIMSIZE)
    snd = sound.Sound(value=c.szia_baba)
    snd.setVolume(0.7)

    snd.play()
    _draw_imgs_on_screen(150, imgs=[face], snd=snd)


def _create_occluders(nr):

    if nr == 4:
        return [visual.Rect(win, width=c.SIZE, height=c.SIZE, pos=pos, lineColor='black', fillColor='black')
                for pos in c.four_positions]
    else:
        return [visual.Rect(win, width=c.OCC_SIZE, height=c.OCC_SIZE, pos=pos, lineColor='black', fillColor='black')
                for pos in [c.start_pos1, c.start_pos2]]


def _getKeypress():
    keys = event.getKeys(keyList=["space", "escape"])
    if keys and keys[0] == "escape":
        win.close()
        core.quit()
    elif keys and keys[0] == "space":
        return True
    else:
        return False


if __name__ == "__main__":
    demo_main()



