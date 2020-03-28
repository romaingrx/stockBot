#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 23 March 2020
"""

from .streamer_base import Streamer
from .alpha_vantage import Alpha_Vantage_Streamer
from .quandl import Quandl_Streamer
from .yfinance import Yfinance_Streamer

streamer_mapper = {'yfinance':Yfinance_Streamer,
                   'alpha_vantage':Alpha_Vantage_Streamer,
                   'quandl':Quandl_Streamer}
