#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""
import numpy as np
import pandas as pd
from typing import Text

from .transactions import Transaction
from stockBot.types import orderAction, orderTime, orderType
from stockBot.data import get_step_data

# TODO: créer des attributs cohérents pour contenir les transactions avec le prix actuel de l'action
# TODO: implémenter la fonction push pour qu'il ajoute une transaction (ACHAT)
# TODO: implémenter la fonction pop pour qu'il retire une transaction (VENTE)
# TODO: implémenter la fonction update qui met à jour le prix des actions
# TODO: implémenter la fonction reset qui remet tout à zéro
class Stonk:

    def __init__(self, ticker_name:Text, quantity:int, price:float):
        self.ticker_name = ticker_name
        self.quantity    = quantity
        self.price       = price

    def as_dict(self)->dict:
        return dict({'ticker_name':self.ticker_name, 'quantity':self.quantity})

    def __contains__(self, o):
        return self.ticker_name == o.ticker_name

    def __str__(self):
        return "<%s-quantity:%d-price:%.2f>"%(self.ticker_name, self.quantity, self.price)

    def __repr__(self):
        return self.__str__()

class Portfolio:

    def __init__(self):
        self.current_balance  = 0.0
        self._portfolio = []

    def find_ticker(self, ticker_name):
        """
            return the index of the ticker if it exists, else return None
        """
        index = -1
        for i, stonk in enumerate(self._portfolio):
            if stonk.ticker_name == ticker_name:
                index = i
        return index

    def get_quantity(self, ticker_name):
        index = self.find_ticker(ticker_name)
        return self._portfolio[index].quantity if index != -1 else 0

    def push(self, transaction:Transaction):
        """
            Met à jour les attributs en fonctions du orderAction (BUY, SELL) de la transaction
        """
        index = self.find_ticker(transaction.ticker_name)

        if index == -1:
            index = len(self._portfolio)
            self._portfolio.append(Stonk(transaction.ticker_name, 0, 0))

        if transaction.action == orderAction.BUY.value:
            last_price    = self._portfolio[index].price
            last_quantity = self._portfolio[index].quantity

            PRU = (last_price*last_quantity + transaction.price*transaction.quantity)/(last_quantity + transaction.quantity)

            self._portfolio[index].quantity += transaction.quantity
            self._portfolio[index].price     = PRU
            self.current_balance            += transaction.amount

        elif transaction.action == orderAction.SELL.value:
            self.current_balance            -= transaction.quantity * self._portfolio[index].price
            self._portfolio[index].quantity -= transaction.quantity
            if self._portfolio[index].quantity == 0:
                del self._portfolio[index]

    def as_frame(self) -> pd.DataFrame:
        return pd.DataFrame([stock.as_dict() for stock in self._portfolio])

    def __str__(self) -> str:
        string  = "\n--- PORTFOLIO ---\n"
        string += self.as_frame().to_string(index=False)
        string += "\n"
        return string

    def update(self, ticker_name, date:int=None):
        iter = self.find_ticker(ticker_name)
        if iter != -1:
            stonk = self._portfolio[iter]
            # if stonk.quantity == 0:
            #     del self._portfolio[iter]
            last_price = stonk.price
            stonk.price = get_step_data(stonk.ticker_name, date)
            self.current_balance += (stonk.price-last_price)*stonk.quantity

    def __len__(self):
        return len(self._portfolio)

    def reset(self):
        del self._portfolio
        self.current_balance  = 0.0
        self._portfolio = []
