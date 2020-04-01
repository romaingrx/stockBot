#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Monday, 30 March 2020
"""

import matplotlib.pyplot as plt
from collections import deque

from stockBot.finance import Wallet
from .renderer_base import Renderer

class Naive_Plot(Renderer):

    def __init__(self, window_size=50):
        self.fig = plt.figure()
        self.ax  = plt.subplot(211)
        self.axargs = plt.subplot(212)
        self.iter = 0
        self.window_size = window_size
        self.x = deque(maxlen=self.window_size)
        self.y = deque(maxlen=self.window_size)
        self.args = deque(maxlen=self.window_size)

    def render(self, wallet:Wallet, *args):
        self.ax.clear()
        self.axargs.clear()
        self.ax.set_title('Balance du wallet')
        self.ax.set_xlabel('Steps')
        self.ax.set_ylabel('balance')
        self.ax.grid(True)

        plt.setp([self.ax, self.axargs], xlim=(max(0, self.iter-self.window_size), self.iter+self.window_size))
        # plt.xlim(max(0, self.iter-self.window_size), self.iter+self.window_size)

        self.iter += 1
        self.x.append(self.iter)
        self.y.append(wallet.balance)
        self.args.append(*args)

        self.ax.axhline(wallet.initial_balance, color='blue', ls='--', label='initial balance')
        self.axargs.plot(self.x, self.args, color='red', label='args')
        self.ax.plot(self.x, self.y, linestyle='-', color='purple', label='balance')
        plt.legend()
        self.fig.canvas.draw()
        plt.pause(0.001)

    def reset(self):
        del self.x
        del self.y
        del self.args
        self.ax.clear()
        self.iter = 0
        self.x = deque(maxlen=self.window_size)
        self.y = deque(maxlen=self.window_size)
        self.args = deque(maxlen=self.window_size)
