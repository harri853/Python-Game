# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 13:49:02 2020

@author: Peggy
"""
# Import libraries and modules
import pygame


# Import individual contribuutions
import utils.alex as FuncAlex
import utils.harri as FuncHarri
import utils.hongyuan as FuncHongyuan

# Mute function used to change mute values between true and false 
# Returns mute value for use 
def Mute(mute):
    if mute == True:
        mute = False
    elif mute == False:
        mute = True
    return mute
    
