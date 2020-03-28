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

transaction1 = Transaction('SPCE', 'buy', 10, 10.14)
transaction2 = Transaction('TSLA', 'buy', 2, 100.14)

class Ledger_Test(unittest.TestCase):

    def test_init(self):
        ledger = Ledger()
        self.assertEqual(len(ledger), 0)

    def test_savage(self):
        n = 999
        ledger = Ledger()
        for _ in range(n):
            ledger.push(transaction1)
        self.assertEqual(len(ledger), n)
        ledger.reset()
        self.assertEqual(len(ledger), 0)

    def test_len(self):
        n = 10
        ledger = Ledger()
        for _ in range(n):
            ledger.push(transaction1)
        self.assertEqual(len(ledger), n)

    def test_reset(self):
        ledger = Ledger()
        ledger.push(transaction1)
        ledger.push(transaction2)
        ledger.reset()
        self.assertEqual(len(ledger), 0)

if __name__ == '__main__':
    unittest.main()
