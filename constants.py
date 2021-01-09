# -*- coding: utf-8 -*-
"""
constants for "Curiosity" exp
"""

from __future__ import division
import os
# from psychopy import prefs
# prefs.general['audioLib'] = ['pygame', 'sounddevice', 'pyo']
from psychopy import visual, sound


# EYETRACKER settings
TRACKERTYPE = 'tobii'
DUMMYMODE = False
# unused:
SACCVELTHRESH = 35 # degrees per second, saccade velocity threshold
SACCACCTHRESH = 9500 # degrees per second, saccade acceleration threshold
BLINKTHRESH = 150 # milliseconds, blink detection threshold used in PyGaze method
EVENTDETECTION = 'pygaze' # Tobii offers no native method


# DISPLAY keyword arguments
MOUSEVISIBLE = False
DISPTYPE = 'psychopy'
TOBII_DISPSIZE = (1920,1200) # Tobii t60xl: (1920 x 1200) screen ratio: 16/10
CONTROL_DISPSIZE = (1024, 768) #(2048, 1152) #?
FULLSCREEN = True
SCREENSIZE = (51.7, 32.31) # physical Tobii screen size in cm. (52.7, 29.6) are for the Dell monitor
SCREENDIST = 65.0 # centimeters; avg distance between screen and participant's eyes

# Foreground colour set to white
FGC = (255, 255, 255)
# Background colour set to black
BGC = (0, 0, 0)

###################

DS = (1920,1200) # Tobii t60xl: (1920 x 1200) screen ratio: 16/10...
X = DS[0]/2    # Tobii: 960
Y = DS[1]/2    # Tobii: 600

# size of the objects and squares
STIMSIZE = (1920,1080)
SIZE = int(DS[0]/4) # - Tobii: 1920/4 -> 480; notracker = 1600/4=400
OBJ_SIZE = (SIZE, SIZE)
OCC_SIZE = SIZE+30 # Tobii: 510, notracker: 430 1920/3.75 = 512
# test object sizes:
boring_size = (SIZE-int(Y*0.056), SIZE-int(Y*0.056)) # Tobii: 447,
interesting_size = (SIZE+int(Y*0.1), SIZE+int(Y*0.1)) # Tobii: 540
fam_size = (SIZE-Y*0.15, SIZE-Y*0.15) # Tobbi: 510
HANDSIZE = int(DS[1]/3) # 1920x1200 -> 400
ATTSIZE = int(DS[1]/6)


#############
### PATHS ###

# Path to the current file's parent folder
DIR = os.path.dirname(os.path.abspath(__file__))

# folder for logfile
LOGDIR = os.path.join(DIR, "Logfiles")
# FileExistError only exists on python3
#try:
#    os.mkdir(LOGDIR)
#except FileExistsError:
#    pass

# Calibration
CALIBDIR = os.path.join(DIR, "calibrationfiles")
CALIBSOUNDFILE = os.path.join(CALIBDIR, "cen_4.wav")
CALIBIMG = os.path.join(CALIBDIR, "glowing-star-180x180.png")
CALIBVIDEO = os.path.join(CALIBDIR, '--- cal_movie_1.mov')
ATT_IMG = os.path.join(CALIBDIR, 'att_03.png')

# Stimuli dirs
IMGSDIR = os.path.join(DIR, "imgs") # imgs folder
# apple and banana
FAM_IMGS_DIR = os.path.join(IMGSDIR, "familiarImages")
FAM_IMGS = [os.path.join(FAM_IMGS_DIR, img) for img in os.listdir(FAM_IMGS_DIR)]

SNDDIR = os.path.join(DIR, "sounds")
TEST_SND_DIR = os.path.join(SNDDIR, "test_sounds")
INT_SOUND = os.path.join(SNDDIR, "test_sounds", "interesting_sound.wav")
FAMILIARSNDDIR = os.path.join(SNDDIR, "familiarSounds")
FAM_SNDS = [os.path.join(FAMILIARSNDDIR, s) for s in os.listdir(FAMILIARSNDDIR)]

# Stimuli sound files
szia_baba = os.path.join(SNDDIR, "szia_baba_szia_fam_noiseless.wav")
newLabelSoundFile1 = os.path.join(TEST_SND_DIR, "egy_bitye_egy_bitye_noiseless.wav")
newLabelSoundFile2 = os.path.join(TEST_SND_DIR, "egy_tacok_egy_tacok_noiseless.wav")
testLabelSoundFile1 = os.path.join(TEST_SND_DIR, "nezd_hol_van_a_bitye_bitye_pt1_2.62s.wav")
testLabelSoundFile2 = os.path.join(TEST_SND_DIR, "nezd_hol_van_a_tacok_tacok_pt1_2.68s.wav")
fam_moving_snd = os.path.join(SNDDIR, "rattle-toy.wav")
occl_down = os.path.join(SNDDIR, "occluders_donw_magic_mallett.wav")
occl_up = os.path.join(SNDDIR, "occluders_up_sfx-magic.wav")
shuffle_song = os.path.join(SNDDIR, "birdfish-happy-loop.wav")
attGettSoundFile = os.path.join(TEST_SND_DIR, "cen_4_short.wav")

# Stimuli image files
face_img = os.path.join(IMGSDIR, "Paula_round_no_bg.png")
test_imgs = [os.path.join(IMGSDIR, "test_imgs", img) for img in os.listdir(os.path.join(IMGSDIR, "test_imgs"))]
#test_imgs_dir = os.path.join(IMGSDIR, "test_imgs")
INT_IMG = os.path.join(IMGSDIR, "interesting_obj_no_bg_714x714.png")
BORING_IMG = os.path.join(IMGSDIR, "grey_obj_no_bg_714x714.png")

hand_img_file = os.path.join(IMGSDIR, "hand.png")
attGetterImg = os.path.join(IMGSDIR, "att_02.png") # att getter after calibr
att_gett_imgs_dir = os.path.join(IMGSDIR, "att_gett") # att getter in test
att_gett_imgs = [os.path.join(att_gett_imgs_dir, png) for png in os.listdir(att_gett_imgs_dir)]

STIM_DIR = os.path.join(DIR, "anims")
STIM_FOLDERS = os.listdir(STIM_DIR)
list.sort(STIM_FOLDERS)

# create the the list of stimuli folders containing all 4 in left-right-left or right-left-right order
# folders: 1,2,3,4
v1 = STIM_FOLDERS[0] # right1
v2 = STIM_FOLDERS[1] # left1
v3 = STIM_FOLDERS[2] # left2
v4 = STIM_FOLDERS[3] # right2
# left_right_left_orders = [[v2,v1,v3], [v2,v4,v3], [v3,v1,v2], [v3,v4,v2]]
# right_left_right_orders = [[v1,v2,v4], [v1,v3,v4], [v4,v2,v1], [v4,v3,v1]]
order_dict = {"left":[[v2,v1,v3,v4], [v2,v4,v3,v1], [v3,v1,v2,v4], [v3,v4,v2,v1]],  #lrlr_orders
              "right":[[v1,v2,v4,v3], [v1,v3,v4,v2], [v4,v2,v1,v3], [v4,v3,v1,v2]]} #rlrl_orders


#################
### ANIMATION ###

# steps for moving objects
STPX = 8
STPY = 5 # Tobii t60xl: 5

#start_pos1 = (-X*0.5, 0)
#start_pos2 = (X*0.5, -0)
#rect_pos1 = (-X*0.5, Y+SIZE/2) # y:Tobii: 600+240 = 840
#rect_pos2 = (X*0.5, Y+SIZE/2)

start_pos1 = (-X*0.5-(SIZE*0.2), 0) # Tobii: -960*0,5-(480*0,2) = -480-96=526
start_pos2 = (X*0.5+(SIZE*0.2), -0)
rect_pos1 = (-X*0.5-(SIZE*0.2), Y+SIZE/2) # y:Tobii: 600+240 = 840 (just above the screen)
rect_pos2 = (X*0.5+(SIZE*0.2), Y+SIZE/2)
step1 = (STPX,0)
step2 = (-STPX,0)

top = (0,Y-SIZE*0.6)
bottom = (0,-Y+SIZE*0.6)

top_left = X*-0.5, Y*0.5
bottom_left = X*-0.5, Y*-0.5
top_right = X*0.5, Y*0.5
bottom_right = X*0.5, Y*-0.5
four_positions = [bottom_left, bottom_right, top_left, top_right]

positions = {"1":[bottom_left, top_right], "2":[bottom_right, top_left],
                 "3":[top_left, bottom_right], "0":[top_right, bottom_left]}

fam_positions = {"1":[top_left, bottom_right], "2":[top_right, bottom_left],
                 "3":[bottom_left, top_right], "0":[bottom_right, top_left]}

log_positions = {"1":["bottom-left", "top-right"], "2":["bottom-right", "top-left"],
                 "3":["top-left", "bottom-right"], "0":["top-right", "bottom-left"]}

fam_log_positions = {"1":["top-left", "bottom-right"], "2":["top-right", "bottom-left"],
                     "3":["bottom-left", "top-right"], "0":["bottom-right", "top-left"]}

# moving occluders
up = down = Y/50 # Tobii-> 12 px/round, notracker: 10
occl_lim = int((Y+SIZE/2)/down) + 1 # make it slower? (Tobii: 70+1)


AllSteps = [((0,STPY), (STPX, -STPY)), ((0,STPY), (-STPX, -STPY)),  # (up, right-down), (up,left-down)
            ((0,-STPY), (-STPX, STPY)), ((0,-STPY), (STPX, STPY)), # (down, left-up), (down, right-up)
            ((STPX,0), (-STPX,-STPY)), ((STPX,0), (-STPX,STPY)), # (right, left-down), (right, left-up)
            ((-STPX,0), (STPX,-STPY)), ((-STPX,0), (STPX,STPY)), # (left, right-down), (left, right-up)
            ((STPX,STPY), (-STPX,0)), ((STPX,STPY), (0,-STPY)), # (right-up, left), (right-up, down)
            ((-STPX,STPY), (STPX,0)), ((-STPX,STPY), (0,-STPY)), # (left-up, right), (left-up, down)
            ((STPX,-STPY), (0,STPY)), ((STPX,-STPY), (-STPX,0)), # (right-down, up), (right-down, left)
            ((-STPX,-STPY), (STPX,0)), ((-STPX,-STPY), (0,STPY)), # (left-down, right), (left-down, up)
            ]



class Image_stimuli(object):

    def __init__(self, win):

        self.face = visual.ImageStim(win, face_img, size=STIMSIZE)
#        self.att_getter = visual.ImageStim(win, attGetterImg, size=ATTSIZE)
        self.att_getters = [visual.ImageStim(win, att_gett) for att_gett in att_gett_imgs]
        self.hand = visual.ImageStim(win)
        self.int_obj = visual.ImageStim(win, INT_IMG, size=interesting_size)
        self.boring_obj = visual.ImageStim(win, BORING_IMG, size=boring_size)
        self.fam_obj1 = visual.ImageStim(win, size=fam_size)
        self.fam_obj2 = visual.ImageStim(win, size=fam_size)
        self.p_test_img = visual.ImageStim(win, size=STIMSIZE)


class Sound_stimuli(object):

    def __init__(self, win):

        self.snd_szia = sound.Sound(value=szia_baba)
        self.snd_szia.setVolume(0.7)
        self.snd_fam = sound.Sound(value=fam_moving_snd)
        self.snd_fam.setVolume(0.8)
        self.snd_down = sound.Sound(value=occl_down)
        self.snd_down.setVolume(0.6)
        self.snd_up = sound.Sound(value=occl_up)
        self.snd_up.setVolume(0.6)
        self.int_sound = sound.Sound(value=INT_SOUND)
        self.int_sound.setVolume(0.35)
        self.attGettSound = sound.Sound(value=attGettSoundFile)
        self.attGettSound.setVolume(0.8)
        self.label_sounds = [newLabelSoundFile1, newLabelSoundFile2]
        self.fam_label_sounds = FAM_SNDS
        self.test_label_snds = [testLabelSoundFile1, testLabelSoundFile2]




