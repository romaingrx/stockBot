#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

from stockBot.utils.types import orderAction, orderType, orderTime

# Order exceptions

class defaultTypeException(Exception):
    def __init__(self, typeClass, notCorrect, *args, **kwargs):
        str = "{typeClass} \'{notCorrect}\' not accepted. Accepted {typeClass} are {values}.".format(typeclass=typeClass, notCorrect=notCorrect, typeClass=typeClass, values = ', '.join([accepted.name for accepted in eval(typeClass)]))
        super().__init__(str, *args, **kwargs)

class OrderActionException(defaultTypeException):
    def __init__(self, notCorrect, *args, **kwargs):
        super().__init__("orderAction", notCorrect, *args, **kwargs)

class OrderTypeException(defaultTypeException):
    def __init__(self, notCorrect, *args, **kwargs):
        super().__init__("orderType", notCorrect, *args, **kwargs)

class OrderTimeException(defaultTypeException):
    def __init__(self, notCorrect, *args, **kwargs):
        super().__init__("orderTime", notCorrect, *args, **kwargs)
