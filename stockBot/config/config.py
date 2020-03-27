# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 27 March 2020
"""
import quandl, alpha_vantage
from datetime import datetime
import warnings
import getopt
import json
import sys
import os

import os, sys
cwd = os.path.abspath(os.getcwd())
sys.path.append(cwd)

from stockBot import CONFIG_FILE
from stockBot.exceptions import KeyNotConfiguredError, AlphaVantageKeyNotConfiguredError, QuandlKeyNotConfiguredError


def parse_api_keys(argv):
    ALPHAVANTAGE_API_KEY, QUANDL_KEY = None, None
    opt, arg = getopt.getopt(argv,'a:q:c',['alphavantage=','quandl=','check'])
    for o, a in opt:
        if o in ('--alphavantage', '-a'):
            ALPHAVANTAGE_API_KEY = a
        if o in ('--quandl', '-q'):
            QUANDL_KEY = a
        if o in ('--check', '-c'):
            check()
            exit()
    return ALPHAVANTAGE_API_KEY, QUANDL_KEY

def config(argv):
    ALPHAVANTAGE_API_KEY, QUANDL_KEY = parse_api_keys(argv)
    if not ALPHAVANTAGE_API_KEY:
        warnings.warn("AlphaVantage API Key not given.")
    if not QUANDL_KEY:
        warnings.warn("Quandl API Key not given.")
    envALPHAVANTAGE_API_KEY, envQUANDL_KEY = getenv()
    files = ['~/.bashrc', '~/.bash_profile']
    if ALPHAVANTAGE_API_KEY:
        # os.environ.update({'ALPHAVANTAGE_API_KEY':ALPHAVANTAGE_API_KEY})
        for file in files:
            file = os.path.expanduser(file)
            if os.path.exists(file):
                if not envALPHAVANTAGE_API_KEY:
                    with open(file, 'a+') as fd:
                        fd.write("# AlphaVantage key added by StockBot on %s\n"%(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        fd.write('export %s=\"%s\"\n'%('ALPHAVANTAGE_API_KEY', ALPHAVANTAGE_API_KEY))
                else:
                    print("RYETYFUGHTDRTFYGUHGFYRTF")
                    print("Change AlphaVantage key from %s to %s"%(envALPHAVANTAGE_API_KEY, ALPHAVANTAGE_API_KEY))
                    with open(file, 'r') as fd:
                        data = fd.readlines()
                        for i, line in enumerate(data):
                            split = line.split('=')
                            if split[0] == 'export ALPHAVANTAGE_API_KEY':
                                data[i] = 'export %s=\"%s\"\n'%('ALPHAVANTAGE_API_KEY', ALPHAVANTAGE_API_KEY)
                    with open(file, 'w') as fd:
                        fd.writelines(data)
        print('AlphaVantage Key set!')
    if QUANDL_KEY:
        # os.environ.update({'QUANDL_KEY':QUANDL_KEY})
        for file in files:
            file = os.path.expanduser(file)
            if os.path.exists(file):
                if not envQUANDL_KEY:
                    with open(file, 'a+') as fd:
                        fd.write("# Quandl key added by StockBot on %s\n"%(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                        fd.write('export %s=\"%s\"\n'%('QUANDL_KEY', QUANDL_KEY))
                else:
                    print("Change Quandl key from %s to %s"%(envQUANDL_KEY, QUANDL_KEY))
                    with open(file, 'r') as fd:
                        data = fd.readlines()
                        for i, line in enumerate(data):
                            split = line.split('=')
                            if split[0] == 'export QUANDL_KEY':
                                data[i] = 'export %s=\"%s\"\n'%('QUANDL_KEY', QUANDL_KEY)
                    with open(file, 'w') as fd:
                        fd.writelines(data)
        print('Quandl Key set!')
    return

def getenv():
    ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
    QUANDL_KEY           = os.getenv('QUANDL_KEY')
    return ALPHAVANTAGE_API_KEY, QUANDL_KEY

def check():
    ALPHAVANTAGE_API_KEY, QUANDL_KEY = getenv()
    if not ALPHAVANTAGE_API_KEY:
        print('AlphaVantage key not configured yet.')
    if not QUANDL_KEY:
        print('Quandl key not configured yet.')
    if ALPHAVANTAGE_API_KEY and QUANDL_KEY:
        print('All keys configured.')
