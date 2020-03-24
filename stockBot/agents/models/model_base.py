#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Thursday, 19 March 2020
"""

import os
import logging
import tensorflow as tf
from abc import ABC, ABCMeta, abstractmethod
from typing import Text

from stockBot.__init__ import MODELPATH, TENSORBOARDPATH, DEFAULT_TENSORBOARDPATH
from stockBot.agents.rewards import Reward_Strategy

class Neural_Network(ABC):
    """
        The skeleton of all neural networks with basics functions.
    """

    def __init__(self, input_shape, save_model_path:Text=None, save_tensorboard_path:Text=None):
        self._save_model_path = save_model_path or MODELPATH
        self._save_tensorboard_path = save_tensorboard_path or TENSORBOARDPATH
        self.input_shape = input_shape
        self.model_name = None
        self.model = None
        self.build_model()
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

    def save_model(self, episode=None):
        """
            Save the model to .h5 format in ./res/models/
        """
        if not self.model_name:
            raise NotImplementedError('Model not implemented')
        extension = ".h5" if not episode else "_%d.h5"%episode
        self.model.save(self._save_model_path%(self.model_name+extension))
        return None

    def load_model(self):
        """
            Load the model from .h5 format in ./res/models/
        """
        if not self.model_name:
            raise NotImplementedError('Model not implemented')
        self.model = tf.keras.models.load_model(self._save_model_path%(self.model_name+".h5"))
        return None

    @abstractmethod
    def build_model(self):
        raise NotImplementedError('build_model not implemented')

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
            raise NotImplementedError('Model not implemented')
        # os.system("rm -r \"%s\""%(TENSORBOARDPATH%self.model_name))
        self.tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir = self._save_tensorboard_path%self.model_name, histogram_freq=1)

    def __str__(self):
        """
            The string representation of the model
        """
        if not self.model:
            raise NotImplementedError("Model not implemented")
        stringlist = []
        self.model.summary(print_fn=lambda x: stringlist.append(x))
        return "\n".join(stringlist)


class Reinforcement_Network(Neural_Network):

    def __init__(self, input_shape, layer_size):
        self.layer_size = layer_size
        super().__init__(input_shape)

    @abstractmethod
    def act(self, state, epsilon, **kwargs):
        raise NotImplementedError('act not implemented')
