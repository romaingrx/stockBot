#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Thursday, 26 March 2020
"""

import sys
sys.path.append('../stockBot')
from stockBot.wallets import Wallet, Transaction
import unittest

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


if __name__=='__main__':
    unittest.main()
