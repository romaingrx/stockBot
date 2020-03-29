#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 28 March 2020
"""

from __init__ import PROJECTPATH, sys
sys.path.append(PROJECTPATH)

from stockBot.finance import Wallet, Portfolio, Ledger, Transaction
import unittest

initial_balance = 1000
transaction1 = Transaction('SPCE', 'buy', 10, 10.14)
transaction2 = Transaction('TSLA', 'buy', 2, 100.14)
buy_transaction  = Transaction('TSLA', 'buy' , 1, 100)
sell_transaction = Transaction('TSLA', 'sell', 1, 110)


class Portfolio_Test(unittest.TestCase):

    def test_init(self):
        portfolio = Portfolio()
        self.assertEqual(len(portfolio), 0)
        self.assertEqual(portfolio.current_balance, 0)

    def test_buy_sell_len(self):
        portfolio = Portfolio()
        portfolio.push(buy_transaction)
        portfolio.push(sell_transaction)
        self.assertEqual(len(portfolio), 0)

    def test_buy_sell_balance(self):
        portfolio = Portfolio()
        portfolio.push(buy_transaction)
        portfolio.push(sell_transaction)
        self.assertEqual(portfolio.current_balance, 0)
        portfolio.push(buy_transaction)
        portfolio.push(buy_transaction)
        portfolio.push(sell_transaction)
        self.assertEqual(portfolio.current_balance, 100)

    def test_savage(self):
        n = 999
        portfolio = Portfolio()
        for _ in range(n):
            portfolio.push(transaction1)
        self.assertEqual(len(portfolio), 1)
        portfolio.reset()
        for _ in range(n):
            portfolio.push(Transaction('Ticker n°%d'%_, 'buy', 10, 10.12))
        self.assertEqual(len(portfolio), n)

    def test_len(self):
        n = 10
        portfolio = Portfolio()
        for _ in range(n):
            portfolio.push(transaction1)
        self.assertEqual(len(portfolio), 1)
        for _ in range(n):
            portfolio.push(transaction2)
        self.assertEqual(len(portfolio), 2)

    def test_reset(self):
        portfolio = Portfolio()
        portfolio.push(transaction1)
        portfolio.push(transaction2)
        portfolio.reset()
        self.assertEqual(len(portfolio), 0)
        self.assertEqual(portfolio.current_balance, 0)

if __name__=='__main__':
    unittest.main()
