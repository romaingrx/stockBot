#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 28 March 2020
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from collections import deque
import pandas as pd
import random
import seaborn as sns

class Wallet:

    def __init__(self, n=1):
        bal = np.random.rand(n)
        self.info = pd.DataFrame({'date':pd.date_range(pd.datetime.today(), periods=n).to_pydatetime().tolist(), 'balance':bal, 'free_balance':bal/np.random.rand(n)})

class Plot_Renderer:

    def __init__(self, n=50):
        self.history_capacity = n
        sns.set()
        self.shape = (2, 1)
        f, self.axes = plt.subplots(*self.shape, sharex=True)
        self.ax_ledger, self.ax_balance = self.axes[0], self.axes[1]

    def _render_balance(self, subdf):
        pass

    def render(self, wallet):
        subdf = wallet.info.iloc[-min(len(wallet.info.index), self.history_capacity):]
        self.axes[0].clear()
        self.axes[1].clear()
        sns.barplot(x='date', y='free_balance', data=subdf, ax=self.axes[0])
        sns.lineplot('date', 'balance', data=subdf, ax=self.axes[1])
        plt.draw()
        plt.pause(0.001)
    def reset(self):
        pass

wallet = Wallet()
plotter = Plot_Renderer()

n = 100
bal = np.random.rand(n)
date = pd.date_range(pd.datetime.today(), periods=n).to_pydatetime().tolist()
balance = bal
free_balance = np.arange(n)
for i in range(n):
    wallet.info = wallet.info.append({'date':date[i], 'balance':bal[i], 'free_balance':free_balance[i]}, ignore_index=True)
    plotter.render(wallet)

# import altair as alt
# from vega_datasets import data
#
# df = data.cars()
#
# alt.renderers.enable('mimetype')
#
# alt.Chart(df).mark_circle().encode(
#     x='Horsepower',
#     y='Miles_per_Gallon'
# ).interactive()
