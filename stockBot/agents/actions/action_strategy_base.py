#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 25 March 2020
"""

from abc import ABC, abstractmethod

class Action_Strategy(ABC):

    def __init__(self):
        self.low   = None
        self.high   = None
        self.shape = None
        self.dtype = None


    @abstractmethod
    def get_order(self, action):
        raise NotImplementedError()
