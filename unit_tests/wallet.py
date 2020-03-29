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
import random

BUY_tr  = Transaction('SPCE', 'buy', 1, 10.14)
SELL_tr = Transaction('SPCE', 'sell', 1, 11.14)


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

    def test_profit(self):
        wallet = Wallet(initial_balance)
        wallet.push(BUY_tr)
        wallet.push(SELL_tr)
        self.assertEqual(wallet.balance, initial_balance+1)
        wallet.reset()
        wallet.push(BUY_tr)
        wallet.push(BUY_tr)
        wallet.push(SELL_tr)
        self.assertEqual(wallet.balance, initial_balance+1)

    def test_groupement_portfolio(self):
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
        wallet.push(transaction3)
        self.assertEqual(len(wallet._portfolio._portfolio),1)

    def test_balances(self):
        wallet = Wallet(initial_balance)
        tickers = ['SPCE','TSLA','BCART','AA','AAA']
        for t in tickers:
            i = random.uniform(0.00, 25.00)
            wallet.push(Transaction(t, 'buy', 10, i))
            self.assertEqual(wallet.balance, wallet.free_balance+wallet.locked_balance)
            # print(wallet)
        self.assertTrue(len(wallet._ledger._transactions) == len(tickers))

        self.assertTrue(wallet.balance == wallet.free_balance + wallet.locked_balance)

        #Checking whether quantities are right whilst selling higher
        i = 0
        for t in tickers:
            n = random.uniform(25.00,50.00)
            wallet.push(Transaction(t, 'sell', 5, n))
            self.assertEqual(wallet._portfolio._portfolio[i].quantity, 5)
            i+= 1
        self.assertTrue(wallet.balance >= initial_balance)




if __name__=='__main__':
    unittest.main()
