#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""
from enum import Enum

class orderAction(Enum):
    BUY  = 'buy'
    SELL = 'sell'

class orderType(Enum):
    LIMITED     = 'limited'
    MARKET      = 'market'
    STOPLOSS    = 'stopLoss'
    STOPLIMITED = 'stopLimited'

class orderTime(Enum):
    DAY       = 'day'
    PERMANENT = 'permanent'
