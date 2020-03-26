#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Thursday, 26 March 2020
"""

from timeit import default_timer

class timer():
    """
        Used in with statement to get the time of 'sentence' in ms
    """
    def __init__(self, sentence):
        self.sentence = sentence
    def __enter__(self):
        self.start = default_timer()
    def __exit__(self, type, value, traceback):
        print("--- timer : %s -> %.2f ms"%(self.sentence, (1000)*(default_timer()-self.start)))
