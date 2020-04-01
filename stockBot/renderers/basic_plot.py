#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 30 March 2020
"""

import matplotlib.pyplot as plt
from collections import deque
import seaborn as sns
import numpy as np

from stockBot.finance import Wallet
from .renderer_base import Renderer

class Basic_Plot(Renderer):

    def __init__(self, window_size=50):
        sns.set()
        self.fig = plt.figure()
        gs = self.fig.add_gridspec(3, 3)

        sub_shapes = (gs[0, :2], gs[0, 2:], gs[1:, :])

        self.axis = [None]*len(sub_shapes)

        for shape, ax in zip(sub_shapes, range(3)):
            self.axis[ax] = self.fig.add_subplot(shape)
            self.axis[ax].grid(True)

        (self.ax_percentage, self.ax_histogram, self.ax_balance) = self.axis

        plt.subplots_adjust(hspace=0.25)
        self.window_size = window_size
        self.bought, self.sold, self.keep, self.last_length_trans = 0, 0, 0, 0

    def _render_balance(self, wallet):
        self.ax_balance = sns.lineplot(x='date', y= 'balance',data=wallet.info[-self.length:], ls='-', color='purple', label='Balance')
        self.ax_balance.legend(loc='upper left')
        self.ax_balance.set_title('Balance')

    def _render_percentage_invest(self, wallet):
        invested = 100*(
            1 -
            wallet.info['free_balance'][-self.length:] /
            wallet.info['balance'][-self.length:]
        )
        sns.lineplot(x='date', y=invested, data=wallet.info[-self.length:], color='black', ax=self.ax_percentage)
        self.ax_percentage.set_title('Blocked balance percentage')
        self.ax_percentage.set_ylim(-1, 101)

    def _render_histogram(self, wallet):
        if len(wallet._ledger) > self.last_length_trans:
            self.last_length_trans += 1
            last_action_trans = wallet._ledger.as_frame()['action'].values[-1]
            if last_action_trans == 'buy':
                self.bought += 1
            elif last_action_trans == 'sell':
                self.sold += 1
        self.keep = len(wallet.info.index) - self.bought - self.sold
        values = [self.bought, self.sold, self.keep]
        values /= np.linalg.norm(values)
        self.ax_histogram.bar(x=['buy', 'sell', 'keep'], height=values, color='Purple')
        self.ax_histogram.set_title('Actions histogram')
        self.ax_histogram.set_ylim(0, 1)

    def render(self, wallet:Wallet, *args):
        for ax in self.axis:
            ax.clear()

        self.length = min(len(wallet.info.index), self.window_size)
        self.max_date = wallet.info['date'].iloc[-1] - wallet.info['date'][-self.length:].diff().sum()

        self._render_balance(wallet)
        self._render_percentage_invest(wallet)
        self._render_histogram(wallet)

        self.fig.canvas.draw()
        plt.pause(0.00001)

    def reset(self):
        for ax in self.axis:
            ax.clear()
        self.bought, self.sold, self.keep, self.last_length_trans = 0, 0, 0, 0
