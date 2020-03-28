#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Tuesday, 24 March 2020
"""

import numpy as np

from stockBot.types import orderAction, orderType, orderTime
from stockBot.finance import Transaction, Wallet
from stockBot.brokers import Broker

class Fake_Broker(Broker):

    def __init__(self, wallet:Wallet):
        self.wallet = wallet
        pass

    def commit_order(self, transaction:Transaction):
        if transaction.action == orderAction.BUY.value:
            self.buy(transaction)
        elif transaction.action == orderAction.SELL.value:
            self.sell(transaction)

    def buy(self, transaction:Transaction):
        available_amount     = self.wallet.free_balance
        buy_available_amount = min(available_amount, transaction.amount)
        quantity             = int(np.floor(buy_available_amount/transaction.price))
        amount               = transaction.price * quantity
        transaction.quantity = quantity
        transaction.amount   = amount
        bought_price, bought_quantity, fees   = self._real_buy_send(transaction)
        real_transaction     = Transaction(transaction.ticker_name, orderAction.BUY.value, bought_quantity, bought_price, fees, date=transaction.date)
        self.wallet.push(real_transaction)
        return True

    def sell(self, transaction:Transaction):
        portofolio_quantity       = self.wallet._portfolio.get_quantity(transaction.ticker_name)
        sell_quantity             = min(portofolio_quantity, transaction.quantity)
        sell_amount               = transaction.price * sell_quantity
        transaction.quantity      = sell_quantity
        transaction.amount        = sell_amount
        sold_price, sold_quantity, fees = self._real_sell_send(transaction)
        real_transaction     = Transaction(transaction.ticker_name, orderAction.SELL.value, sold_quantity, sold_price, fees, date=transaction.date)
        self.wallet.push(real_transaction)

    def _real_buy_send(self, transaction:Transaction):
        bought_price    = transaction.price
        bought_quantity = transaction.quantity
        fees            = transaction.fees
        return bought_price, bought_quantity, fees

    def _real_sell_send(self, transaction:Transaction):
        sold_price    = transaction.price
        sold_quantity = transaction.quantity
        fees          = transaction.fees
        return sold_price, sold_quantity, fees

    def update(self, ticker_name, step):
        self.wallet.update(ticker_name, step)
