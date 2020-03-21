#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Thursday, 19 March 2020
"""
import os
import subprocess
import numpy as np
import tensorflow as tf

from stockBot.__init__ import MODELPATH, TENSORBOARDPATH, DEFAULT_TENSORBOARDPATH

class Neural_Network(object):
    """
        The skeleton of all neural networks with basics functions.
    """

    def __init__(self, input_shape):
        self.input_shape = input_shape
        self.model_name = None
        self.model = None
        self._build_model()
        self._get_name_model()
        self._launch_tensorboard()

    def fit(self, *args, **kwargs):
        """
            Same as tf.keras.models.Sequential.fit but force callbacks to the tensorboard.
        """
        if not self.model:
            raise NotImplementedError("Model not implemented")
        return self.model.fit(*args, **kwargs, verbose=1, callbacks=[self.tensorboard_callback])

    def predict(self, *args, **kwargs):
        """
            Same as tf.keras.models.Sequential.predict but force callbacks to the tensorboard.
        """
        if not self.model:
            raise NotImplementedError("Model not implemented")
        return self.model.predict(*args, **kwargs, callbacks=[self.tensorboard_callback])

    def save_model(self):
        """
            Save the model to .h5 format in ./res/models/
        """
        if not self.model_name:
            raise NotImplementedError('Model not implemented')
        self.model.save(MODELPATH%(self.model_name+".h5"))
        return None

    def load_model(self):
        """
            Load the model from .h5 format in ./res/models/
        """
        if not self.model_name:
            raise NotImplementedError('Model not implemented')
        self.model = tf.keras.models.load_model(MODELPATH%(self.model_name+".h5"))
        return None

    def _build_model(self):
        raise NotImplementedError('_build_model not implemented')

    def _get_name_model(self):
        """
            Compute the template name of the model
        """
        if not self.model:
            raise NotImplementedError('Model not implemented')
        self.model_name = "%s-"%(self.__class__.__name__.upper())
        for layer in self.model.layers:
            self.model_name += '(%s)'%','.join(map(str, layer.input_shape))
            self.model_name += '%s->'%(layer.name.upper())
        self.model_name += '(%s)'%','.join(map(str,self.model.layers[-1].output_shape))

    def _launch_tensorboard(self):
        """
            Declare the TensorBoard
        """
        if not self.model_name:
            self.tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir = DEFAULT_TENSORBOARDPATH, histogram_freq=1, write_images=True)
        else:
            # os.system("rm -r \"%s\""%(TENSORBOARDPATH%self.model_name))
            self.tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir = TENSORBOARDPATH%self.model_name, histogram_freq=1, write_images=True)

    def __str__(self):
        """
            The string representation of the model
        """
        if not self.model:
            raise NotImplementedError("Model not implemented")
        stringlist = []
        self.model.summary(print_fn=lambda x: stringlist.append(x))
        return "\n".join(stringlist)


class naive_LSTM_Network(Neural_Network):
    """
        Simplest LSTM model with one LSTM layer
    """

    def __init__(self, input_shape):
        super().__init__(input_shape)

    def _build_model(self):
        """
            Declare the model and compile it
        """
        self.model = tf.keras.models.Sequential([
        tf.keras.layers.LSTM(10, input_shape=self.input_shape),
        tf.keras.layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')

class Reinforcement_Network(Neural_Network):

    def __init__(self, input_shape, layer_size, decision_size=3):
        self.layer_size = layer_size
        self.decision_size = decision_size
        super().__init__(input_shape)

    def _build_model(self, distribution='random_normal', bias='zeros'):
        self.input_layer    = tf.keras.Input(shape=self.input_shape, name='input')
        self.feed_layer     = tf.keras.layers.Dense(self.layer_size,
                                           kernel_initializer=distribution,
                                           bias_initializer=bias,
                                           name='feed')(self.input_layer)
        self.decision_layer = tf.keras.layers.Dense(self.decision_size,
                                           kernel_initializer=distribution,
                                           bias_initializer=bias,
                                           name='decision')(self.feed_layer)
        self.buy_layer      = tf.keras.layers.Dense(1,
                                           kernel_initializer=distribution,
                                           bias_initializer=bias,
                                           name='buy')(self.feed_layer)
        # self.forecast_layer = tf.keras.layers.Dense(1, name='forecast')(self.feed_layer)
        self.model          = tf.keras.models.Model(inputs=[self.input_layer],
                                          outputs=[self.decision_layer,
                                                   self.buy_layer
                                                   # self.forecast_layer
                                                   ])
    def act(self, state):
        assert state.shape == self.input_shape

        decision, buy = self.predict(np.expand_dims(state, 0))
        return np.argmax(decision), int(buy)

    def get_state(series, t):
        raise NotImplementedError('get_state not implemented')
