#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

import pandas as pd
from typing import List, Text

from .transactions import Transaction

class Ledger:

    def __init__(self):
        self._transactions = []

    def push(self, transaction:Transaction):
        self._transactions += [transaction]

    def transactions(self) -> List[Transaction]:
        return self._transactions

    def reset(self):
        del self._transactions
        self._transactions = []

    def as_frame(self) -> pd.DataFrame:
        dtf = pd.DataFrame([transaction.as_dict() for transaction in self._transactions])
        dtf.index_col='date'
        return dtf
    def __str__(self) -> Text:
        return str(self.as_frame()) if len(self._transactions) > 0 else "No transactions yet."
