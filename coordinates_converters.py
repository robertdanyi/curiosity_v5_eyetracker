# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 10:52:57 2018
"""

from constants import CONTROL_DISPSIZE



def tobii_norm_2_psy_px(normalized_point):

    """
    Function to convert
        tobii norm point coordinates (top left: (0,0), center: (0.5, 0.5))
        into psychopy pixel screen coordinates (top left: (-dispsize[0]/2, dispsize[1]/2), center: (0,0))
    """
    dispsize = CONTROL_DISPSIZE

    return ((round((normalized_point[0] - 0.5) * dispsize[0], 0)),
                 (round((1 - 2 * normalized_point[1]) * 0.5 * dispsize[1], 0)))



def pygaze_px_2_psy_px(coordinate):

    """
    Function to convert
        pygaze pixel coordinates (top left: (0,0), center: (dispsize[0] / 2, dispsize[1] / 2))
        into psychopy pixel screen coordinates (top left: (-dispsize[0]/2, dispsize[1]/2), center: (0,0))
    """
    dispsize = CONTROL_DISPSIZE

    return ((round(coordinate[0] - dispsize[0]/2, 0)),
                 (round(-coordinate[1] + dispsize[1]/2, 0)))

