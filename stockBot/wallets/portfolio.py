#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

import pandas as pd
from .transactions import Transaction
from stockBot.types import orderAction, orderTime, orderType

# TODO: créer des attributs cohérents pour contenir les transactions avec le prix actuel de l'action
# TODO: implémenter la fonction push pour qu'il ajoute une transaction (ACHAT)
# TODO: implémenter la fonction pop pour qu'il retire une transaction (VENTE)
# TODO: implémenter la fonction update qui met à jour le prix des actions
# TODO: implémenter la fonction reset qui remet tout à zéro
class Stonk:
    def __init__(self, ticker_name, quantity:int):
        self.ticker_name = ticker_name
        self.quantity = quantity
    def as_dict(self)->dict:
        return dict({'ticker_name':self.ticker_name, 'quantity':self.quantity})

class Portfolio:

    def __init__(self):
        self.current_balance  = 0.0
        self._portfolio = []
        pass

    def findticker(self,ticker_name):
        if(len(self._portfolio)) == 0:
            s = Stonk(ticker_name,0)
            self._portfolio += [s]
            return 0
        else:
            i = 0
            while(self._portfolio[i].ticker_name != ticker_name):
                i = i+1
            return i

    def push(self, transaction:Transaction):
        """
            Met à jour les attributs en fonctions du orderAction (BUY, SELL) de la transaction
        """
        i = self.findticker(transaction.ticker_name)
        self._portfolio[i].quantity = self._portfolio[i].quantity + transaction.quantity
        self.current_balance += transaction.amount if transaction.action == orderAction.BUY.value else -transaction.amount

    def as_frame(self) -> pd.DataFrame:
        return pd.DataFrame([stock.as_dict() for stock in self._portfolio])
    def update(self):
        pass

    def reset(self):
        pass
