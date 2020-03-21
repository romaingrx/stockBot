#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

import pandas as pd

class Portfolio:

    def __init__(self):
        self.oui = 'oui'
    def push(self, transaction:'Transaction'):
        self.oui = 'non'
