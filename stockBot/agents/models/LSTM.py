#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""

import tensorflow as tf

from stockBot.agents.models import Neural_Network

class naive_LSTM_Network(Neural_Network):
    """
        Simplest LSTM model with one LSTM layer
    """

    def __init__(self, input_shape):
        super().__init__(input_shape)

    def build_model(self):
        """
            Declare the model and compile it
        """
        self.model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(10, input_shape=self.input_shape),
        tf.keras.layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')
