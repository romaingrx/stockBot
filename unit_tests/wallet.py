#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Thursday, 26 March 2020
"""

from __init__ import PROJECTPATH, sys
sys.path.append(PROJECTPATH)

from stockBot.finance import Wallet, Transaction
import unittest
import pandas as pd
import numpy as np

initial_balance = 1000

class Wallet_Test(unittest.TestCase):

    def test_initialisation(self):
        wallet = Wallet(initial_balance)
        self.assertEqual(wallet.initial_balance, initial_balance)
        self.assertEqual(wallet.balance, initial_balance)


    def test_reset(self):
        wallet = Wallet(initial_balance)
        transaction1 = Transaction('SPCE', 'buy', 10, 10.14)
        wallet.push(transaction1)
        transaction2 = Transaction('TSLA', 'buy', 2, 100.14)
        wallet.push(transaction2)
        wallet.reset()
        self.assertEqual(initial_balance, wallet.balance)
        self.assertTrue(len(wallet._portfolio) == 0)
        self.assertTrue(len(wallet._ledger) == 0)
    def test_contenu_ledger(self):
        wallet = Wallet(initial_balance)
        transaction1 = Transaction('SPCE', 'buy', 10, 10.00)
        wallet.push(transaction1)
        transaction2 = Transaction('TSLA', 'buy', 2, 100.00)
        wallet.push(transaction2)
        transaction3 = Transaction('TSLA', 'sell', 1, 200.00)
        wallet.push(transaction3)
        df=wallet._ledger.as_frame()
        self.assertTrue(True)
        self.assertTrue(df['ticker_name'].values[0] == 'SPCE')
        self.assertTrue(df['ticker_name'].values[1]=='TSLA')
        self.assertTrue(wallet._portfolio._portfolio[0].quantity == 10)
        self.assertTrue(wallet._portfolio._portfolio[1].quantity == 1)


if __name__=='__main__':
    unittest.main()
