#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Wednesday, 15 April 2020
"""

from stockBot.agents import DQNAgent
from stockBot.action_strategies import Simple_Action_Strategy
from stockBot.reward_strategies import Simple_Reward_Strategy, Sortino

from tensorboard.plugins.hparams import api as hp
import tensorflow as tf


# hyper parameters configuration

HP_LEARNING_RATE       = hp.HParam('learning_rate', hp.Discrete([0.0001, 0.001, 0.01, 0.1]))
HP_NUM_DENSE_UNITS     = hp.HParam('number_dense_units', hp.Discrete([128, 256, 512]))
HP_NUM_CONV_FILTER     = hp.HParam('number_conv_filter', hp.Discrete([16, 32, 64]))
HP_NUM_CONV_KERNEL     = hp.HParam('number_conv_kernel', hp.Discrete([16, 32, 64]))

METRIC_BALANCE = hp.Metric('balance', display_name='balance')
METRIC_LOSS    = hp.Metric('loss', display_name='loss')
METRIC_REWARD  = hp.Metric('reward', display_name='reward')

hparams = [HP_LEARNING_RATE, HP_NUM_DENSE_UNITS, HP_NUM_CONV_FILTER, HP_NUM_CONV_KERNEL]
metrics = [METRIC_BALANCE, METRIC_LOSS, METRIC_REWARD]

with tf.summary.create_file_writer('res/tensorboards').as_default():
    hp.hparams_config(
    hparams=hparams,
    metrics=metrics,
  )

def get_name_hparams(hparams):
    string = "DQN"
    for key, val in hparams.items():
     string += "*%s=%s"%(str(key), str(val))
    return string

# training
tickers = ['TSLA']

for learning_rate in [0.01]:
    # for num_dense_units in HP_NUM_DENSE_UNITS.domain.values:
    #     for num_conv_filter in HP_NUM_CONV_FILTER.domain.values:
    #         for num_conv_kernel in HP_NUM_CONV_KERNEL.domain.values:
    hparams = {
        HP_LEARNING_RATE.name:learning_rate,
        HP_NUM_DENSE_UNITS.name:256,
        HP_NUM_CONV_FILTER.name:64,
        HP_NUM_CONV_KERNEL.name:6,
    }
    Agent  = DQNAgent(tickers, 10000, random=False, features_function='stat', Name=get_name_hparams(hparams), hyperparams=hparams)
    Agent.train(learning_rate=learning_rate)
