#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Thursday, 19 March 2020
"""
import os
import subprocess
import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.callbacks import TensorBoard

from settings import MODELPATH, TENSORBOARDPATH, DEFAULT_TENSORBOARDPATH

class NeuralNetwork(object):
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
        self.model = load_model(MODELPATH%(self.model_name+".h5"))
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
            self.tensorboard_callback = TensorBoard(log_dir = DEFAULT_TENSORBOARDPATH, histogram_freq=1, write_images=True)
        else:
            self.tensorboard_callback = TensorBoard(log_dir = TENSORBOARDPATH%self.model_name, histogram_freq=1, write_images=True)

    def __str__(self):
        """
            The string representation of the model
        """
        if not self.model:
            raise NotImplementedError("Model not implemented")
        stringlist = []
        self.model.summary(print_fn=lambda x: stringlist.append(x))
        return "\n".join(stringlist)


class naive_LSTM(NeuralNetwork):
    """
        Simplest LSTM model with one LSTM layer
    """

    def __init__(self, input_shape):
        super().__init__(input_shape)

    def _build_model(self):
        """
            Declare the model and compile it
        """
        self.model = Sequential([
        layers.LSTM(10, input_shape=self.input_shape),
        layers.Dense(1)
        ])
        self.model.compile(optimizer='adam', loss='mse')

if __name__=='__main__':
    LSTM = naive_LSTM((10,1))
    print(LSTM)
