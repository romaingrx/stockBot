#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 23 March 2020
"""

from stockBot.data.streamer.streamer import Streamer
from stockBot.data.streamer.yfinance.streamer import Yfinance_Streamer
from stockBot.data.streamer.alpha_vantage.streamer import Alpha_Vantage_Streamer
from stockBot.data.streamer.quandl.streamer import Quandl_Streamer

streamer_mapper = {'yfinance':Yfinance_Streamer,
                   'alpha_vantage':Alpha_Vantage_Streamer,
                   'quandl':Quandl_Streamer}
