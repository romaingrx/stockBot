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
        self._transactions = pd.DataFrame()

    def push(self, transaction:Transaction):
        self._transactions = self._transactions.append(transaction.as_dict(), ignore_index=True)

    def transactions(self) -> List[Transaction]:
        return self._transactions

    def reset(self):
        del self._transactions
        self._transactions = pd.DataFrame()

    def as_frame(self) -> pd.DataFrame:
        return self._transactions

    def __len__(self):
        return len(self._transactions.index)

    def __str__(self) -> Text:
        string  = "\n--- LEDGER ---\n"
        string += self.as_frame().to_string(index=False) if len(self._transactions) > 0 else "No transactions yet."
        string += "\n"
        return string
