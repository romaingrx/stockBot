#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""

class Agent:

    def __init__(self, df, model, money, max_buy, max_sell, look_back):
        """
            df        (pandas.DataFrame)
            model     (model.NeuralNetwork)
            money     (int or float)
            max_buy   (int or float)
            max_sell  (int or float)
            look_back (int)
        """
        self.look_back = look_back
        self.df = df
        self.model = model
        self.initial_money = money
        self.max_buy = max_buy
