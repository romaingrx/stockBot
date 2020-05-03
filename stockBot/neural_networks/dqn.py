#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""

import random
import numpy as np
import tensorflow as tf
from collections import namedtuple
from tensorboard.plugins.hparams import api as hp

from stockBot.memory import Memory
from .neural_network_base import Reinforcement_Network
from stockBot.reward_strategies import Reward_Strategy, Simple_Reward_Strategy

DQNTransition = namedtuple('DQNTransition', ['state', 'action', 'reward', 'next_state', 'done'])

class Deep_Q_Learning(Reinforcement_Network):

    def __init__(self, input_shape, hyperparams, load_name=None, output_size=None, Name=None):
        self.output_size = output_size
        self.hyperparams = hyperparams
        super().__init__(input_shape=input_shape, load_name=load_name, Name=Name)
        self.summary_hparams(self.hyperparams)

    def build_model(self, distribution='random_normal', bias='ones'):
        self.input_layer    = tf.keras.Input(shape=self.input_shape, name='input', dtype='float32')
        self.conv1d_1       = tf.keras.layers.Conv1D(filters=self.hyperparams['number_conv_filter'],
                                           kernel_size=self.hyperparams['number_conv_kernel'],
                                           padding='same',
                                           activation='tanh')(self.input_layer)
        self.maxpooling_1   = tf.keras.layers.MaxPooling1D(pool_size=2)(self.conv1d_1)
        self.flatten        = tf.keras.layers.Flatten()(self.maxpooling_1)
        self.feed_layer     = tf.keras.layers.Dense(self.hyperparams['number_dense_units'],
                                           kernel_initializer=distribution,
                                           bias_initializer=bias,
                                           activation='sigmoid',
                                           name='feed')(self.flatten)
        self.decision_layer = tf.keras.layers.Dense(self.output_size,
                                           kernel_initializer=distribution,
                                           bias_initializer=bias,
                                           activation='softmax',
                                           name='decision')(self.feed_layer)
        self.model          = tf.keras.models.Model(inputs=[self.input_layer],
                                          outputs=[self.decision_layer],
                                          name='Policy_Network')


    def old_build_model(self, distribution='random_normal', bias='ones'):
        self.input_layer    = tf.keras.Input(shape=self.input_shape, name='input', dtype='float32')
        self.conv1d_1       = tf.keras.layers.Conv1D(filters=64,
                                           kernel_size=6,
                                           padding='same',
                                           activation='tanh')(self.input_layer)
        self.maxpooling_1   = tf.keras.layers.MaxPooling1D(pool_size=2)(self.conv1d_1)
        self.conv1d_2       = tf.keras.layers.Conv1D(filters=32,
                                           kernel_size=3,
                                           padding='same',
                                           activation='tanh')(self.maxpooling_1)
        self.maxpooling_2   = tf.keras.layers.MaxPooling1D(pool_size=2)(self.conv1d_2)
        self.flatten        = tf.keras.layers.Flatten()(self.maxpooling_2)
        self.feed_layer     = tf.keras.layers.Dense(self.output_size,
                                           kernel_initializer=distribution,
                                           bias_initializer=bias,
                                           activation='sigmoid',
                                           name='feed')(self.flatten)
        self.decision_layer = tf.keras.layers.Dense(self.output_size,
                                           kernel_initializer=distribution,
                                           bias_initializer=bias,
                                           activation='softmax',
                                           name='decision')(self.feed_layer)
        self.model          = tf.keras.models.Model(inputs=[self.input_layer],
                                          outputs=[self.decision_layer],
                                          name='Policy_Network')

    def act(self, state, epsilon=0):
        if epsilon > random.random():
            return np.random.choice(self.output_size)
        else:
            decision = self.predict(np.expand_dims(state, 0))
            return np.argmax(decision)
