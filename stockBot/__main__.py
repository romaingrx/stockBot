#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 27 March 2020
"""
import sys, getopt
from config import config

argv = sys.argv[1:]

if len(argv) == 0:
    print('Need at least one argument')
    exit()

opts, arg = getopt.getopt(argv, 'caq',['config','check','alphavantage=','quandl='])

for o, a in opts:
    if o in ('--config'):
        config(argv[1:])
        exit()
    elif o in ('-c', '-a', '-q', '--alphavantage', '--quandl', '--check'):
        print('You must first specify stockBot options.')
