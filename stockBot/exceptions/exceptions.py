#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

from stockBot.types import orderAction, orderType, orderTime
from stockBot.types import streamerSource

# Type exception

class defaultTypeError(KeyError):
    def __init__(self, typeClass, notCorrect, *args, **kwargs):
        str = "{typeClass} \'{notCorrect}\' not accepted. Accepted {typeClass} are {values}.".format(typeclass=typeClass, notCorrect=notCorrect, typeClass=typeClass, values = ', '.join(["%s.%s : '%s'"%(typeClass, accepted.name, accepted.value) for accepted in eval(typeClass)]))
        super().__init__(str, *args, **kwargs)

# Order exceptions

class OrderActionError(defaultTypeError):
    def __init__(self, notCorrect, *args, **kwargs):
        super().__init__("orderAction", notCorrect, *args, **kwargs)

class OrderTypeError(defaultTypeError):
    def __init__(self, notCorrect, *args, **kwargs):
        super().__init__("orderType", notCorrect, *args, **kwargs)

class OrderTimeError(defaultTypeError):
    def __init__(self, notCorrect, *args, **kwargs):
        super().__init__("orderTime", notCorrect, *args, **kwargs)

class NotEnoughBalanceError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(self, "Not enough money in the balance.", *args, **kwargs)

# Streamer exceptions

class StreamerSourceError(defaultTypeError):
    def __init__(self, notCorrect, *args, **kwargs):
        super().__init__("streamerSource", notCorrect, *args, **kwargs)

# Config
class KeyNotConfiguredError(Exception):
    def __init__(self, string, *args, **kwargs):
        string = string or "for Quandl or AlphaVantage"
        super.__init__("API Key %s not configured, instructions for setting keys are in the README."%(string), *args, **kwargs)

class AlphaVantageKeyNotConfiguredError(KeyNotConfiguredError):
    def __init__(self, *args, **kwargs):
        super().__init__('AlphaVantage'*args, **kwargs)

class QuandlKeyNotConfiguredError(KeyNotConfiguredError):
    def __init__(self, *args, **kwargs):
        super().__init__('AlphaVantage'*args, **kwargs)
