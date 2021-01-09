# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 17:32:49 2021

@author: SMC
"""


import unittest
import random
import math
import calculations as calc
import constants as cons



class TestCalculations(unittest.TestCase):

    def test_get_pulserange(self):
        self.assertAlmostEqual(len(calc.get_pulserange()), 210)
        self.assertGreater(calc.get_pulserange()[-1], -20)
        self.assertLess(calc.get_pulserange()[-1], -18) # ends arount -19


    def test_pythagoras(self):
        self.assertAlmostEqual(calc.pythagoras(3,4),5)


    def test_calculate_handPos(self):
        # generate random coordinates on psychopy (0,0 in center) pixel coordinates
        # cons.DS = display size
        spos = (random.randint(-cons.DS[0]/2, cons.DS[0]/2),
                random.randint(-cons.DS[1]/2, cons.DS[1]/2))

        # handPos must be closer to center than spos
        self.assertLess(math.fabs(calc.calculate_handPos(spos)[0]), math.fabs(spos[0]))
        self.assertLess(math.fabs(calc.calculate_handPos(spos)[1]), math.fabs(spos[1]))


    def test_calculate_distance(self):

        positions = [[(542, 233), (43, 412)], # a=499, b=179, c=530.1339
                     [(-542, -233), (-43, -412)], # a=499, b=179, c=530.1339
                     [(542, 233), (-43, -412)]] # a=585, b=645, c=870.775
        distances = [530,530,870]
        for (pos1, pos2), d in zip(positions, distances):
            self.assertAlmostEqual(int(calc.calculate_distance(pos1,pos2)), d)


