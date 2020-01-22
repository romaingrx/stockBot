#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 17 January 2020
"""

import yfinance as yf

tsla = yf.Ticker("TSLA")

tsla.info
tsla.balance_sheet
