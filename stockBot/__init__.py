#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

# from . import agents, models, rewards, preprocess, evaluate, visualizer

import os, datetime, matplotlib.pyplot as plt

# # # # # # #
# VARIABLES #
# # # # # # #

TESTSIZE     = 0.2 # Size of seperation between train and validation data

# # # # # # # # # #
# FIXED VARIABLES #
# # # # # # # # # #

PROJECTPATH              = os.path.abspath(os.path.dirname(__file__))
MODELPATH                = PROJECTPATH + "/../res/models/%s"
TENSORBOARDPATH          = PROJECTPATH + "/../res/tensorboards/%s"
DEFAULT_TENSORBOARDPATH  = PROJECTPATH + "/../res/tensorboards/" + datetime.datetime.now().strftime("%Y/%m/%d-%H.%M.%S")


# # # # # # #
# SETTINGS  #
# # # # # # #

# Background in white
plt.rcParams['figure.facecolor'] = '#FFFFFF'
plt.rcParams['axes.facecolor']   = '#FFFFFF'

# Background in grey
# plt.rcParams['figure.facecolor'] = '#A9A9A9'
# plt.rcParams['axes.facecolor']   = '#A9A9A9'
