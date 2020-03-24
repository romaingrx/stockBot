#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""
from enum import Enum


class Enumarate(Enum):

    @classmethod
    def names(cls):
        return [attr.name for attr in cls]

    @classmethod
    def values(cls):
        return [attr.value for attr in cls]

# ORDER

class orderAction(Enumarate):
    BUY  = 'buy'
    SELL = 'sell'

class orderType(Enumarate):
    LIMITED     = 'limited'
    MARKET      = 'market'
    STOPLOSS    = 'stopLoss'
    STOPLIMITED = 'stopLimited'

class orderTime(Enumarate):
    DAY       = 'day'
    PERMANENT = 'permanent'


# STREAMER

class streamerSource(Enumarate):
    YFINANCE      = 'yfinance'
    ALPHA_VANTAGE = 'alpha_vantage'
    QUANDL        = 'quandl'
