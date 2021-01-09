# -*- coding: utf-8 -*-


import random
import constants as c
from psychopy import visual, sound, event, core
import steps_positions as stp


def shuffle_occluders(win, occluders, isFamiliar, isVertical):
    """Makes occluders move, bounce off walls, change trajectories when collide, and move to labeling position """

    song = sound.Sound(value=c.shuffle_song)
    song.setVolume(0.3)

    # starting positions
    spos1 = c.start_pos1
    spos2 = c.start_pos2
    # starter steps before the random movements
    step1 = c.step1
    step2 = c.step2

    max1, max2 = False, False
    choice = random.choice([1,2])
    side = random.choice([1,2])
    div = 60
    topCircle = visual.Circle(win, radius=1, pos=c.top)
    bottomCircle = visual.Circle(win, radius=1, pos=c.bottom)
    # choice determines correlation of left and right ending positions
    leftEnd = c.top_left if choice == 1 else c.bottom_left
    rightEnd = c.bottom_right if choice == 1 else c.top_right
    leftCircle = visual.Circle(win, radius=1, pos=leftEnd)
    rightCircle = visual.Circle(win, radius=1, pos=rightEnd)
    possible_steps = c.AllSteps
    first_collision = True

    song.play(loops=10) # play theme during animation

    event.clearEvents()

    # random shuffle
    for frameN in range(541):

            # when occluders collide
            if spos1 == spos2:

                # change tracjectories
                if first_collision:
                # first collision: from horizontal to vertical
                    vert_steps = [(0, c.STPX), (0, -c.STPX)] # horizontal steps used
                    random.shuffle(vert_steps)
                    step1, step2 = vert_steps
                    spos1 = (spos1[0] + step1[0], spos1[1] + step1[1])
                    spos2 = (spos2[0] + step2[0], spos2[1] + step2[1])
                    first_collision = False

                else:

                    spos1, spos2, step1, step2, possible_steps = stp.changeTrajectories(spos1, spos2, step1, step2, possible_steps)

            # default behaviour
            else:
                spos1, step1 = stp.get_next_rect_pos(spos1, step1)
                spos2, step2 = stp.get_next_rect_pos(spos2, step2)

            occluders[0].setPos(spos1)
            occluders[1].setPos(spos2)
            occluders[0].draw()
            occluders[1].draw()

            win.flip()

            if _getKeypress(win):
                break

    song.fadeOut(1000)

    sposs = [spos1,spos2] if side == 1 else [spos2, spos1]

    # arrange to labeling pos
    for frameN in range(61):

        div = div-1 if div > 1 else div

        if isVertical:

            sposs = stp.arrange_vertical(sposs, c.top, c.bottom, div)
            if topCircle.contains(sposs[0]):
                max1 = True
            if bottomCircle.contains(sposs[1]):
                max2 = True

        else:

            sposs = stp.arrange_horizontal(sposs, leftEnd, rightEnd, div)
            if leftCircle.contains(sposs[0]):
                    max1 = True
            if rightCircle.contains(sposs[1]):
                    max2 = True

        spos1 = sposs[0] if side == 1 else sposs[1]
        spos2 = sposs[1] if side == 1 else sposs[0]
        occluders[0].setPos(spos1)
        occluders[1].setPos(spos2)
        occluders[0].draw()
        occluders[1].draw()

        win.flip()

        if max1 and max2:
            break

    return [spos1, spos2]


def _getKeypress(win):
    keys = event.getKeys(keyList=["space", "escape"])
    if keys and keys[0] == "escape":
        win.close()
        core.quit()
    elif keys and keys[0] == "space":
        return True
    else:
        return False

