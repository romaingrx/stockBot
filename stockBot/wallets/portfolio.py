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


class Portfolio:

    def __init__(self):
        self.current_balance  = 0.0
        pass

    def push(self, transaction:Transaction):
        """
            Met à jour les attributs en fonctions du orderAction (BUY, SELL) de la transaction
        """
        self.current_balance += transaction.amount if transaction.action == orderAction.BUY.value else -transaction.amount

    def update(self):
        pass

    def reset(self):
        pass
