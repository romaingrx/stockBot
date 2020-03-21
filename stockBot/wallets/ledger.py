#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

import pandas as pd
from typing import List
from collections import namedtuple
from .transactions import Transaction

class Ledger:

    def __init__(self):
        self._transactions = []

    def push(self, transaction:'Transaction'):
        self._transactions += [transaction]

    def transactions(self) -> List['Transaction']:
        return self._transactions

    def as_frame(self) -> pd.DataFrame:
        return pd.DataFrame(self.transactions)
