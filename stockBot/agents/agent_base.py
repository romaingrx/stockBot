#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 27 March 2020
"""
import numpy as np
from abc import ABC
import tensorflow as tf
from typing import Optional, List, Text, Dict

from stockBot.neural_networks import Neural_Network, Deep_Q_Learning, DQNTransition, neural_network_graph
from stockBot.reward_strategies import Reward_Strategy, Simple_Reward_Strategy
from stockBot.action_strategies import Action_Strategy, Simple_Action_Strategy
from stockBot.environments import Environment, Continuous_Environment
from stockBot.data import Data_Streamer
from stockBot.brokers import Broker, Fake_Broker
from stockBot.finance import Wallet
from stockBot.renderers import Naive_Plot, Basic_Plot

from tensorboard.plugins.hparams import api as hp

class Agent(ABC):

    def __init__(self, tickers:Text or List[Text]=None, initial_balance=None, broker:Broker=None, wallet:Wallet=None, env:Environment=None, data_streamer:Data_Streamer=None, neural_network:Neural_Network=None, reward_strategy:Reward_Strategy=None, action_strategy:Action_Strategy=None, load_name=None, hyperparams:Dict=None, **kwargs):

        self.hyperparams       = hyperparams
        self._history_capacity = kwargs.get('history_capacity', 30)
        self._random           = kwargs.get('random', False)
        self.features_function = kwargs.get('features_function', 'basic_features')
        self._tickers          = tickers if isinstance(tickers, list) else [tickers]
        self.broker            = broker if isinstance(broker, Broker) else Fake_Broker(Wallet(initial_balance))
        self.data_streamer     = data_streamer or Data_Streamer(tickers, random=self._random, history_capacity=self._history_capacity, features_function=self.features_function)
        self.wallet            = wallet or self.broker.wallet
        self.action_strategy   = action_strategy or Simple_Action_Strategy()
        self.reward_strategy   = reward_strategy or Simple_Reward_Strategy()
        self.renderer          = kwargs.get('renderer', Basic_Plot())
        self.env               = env or Environment(data_streamer=self.data_streamer, broker=self.broker, action_strategy=self.action_strategy, reward_strategy=self.reward_strategy, renderer=self.renderer, history_capacity=self._history_capacity)
        self.neural_network    = neural_network

    def train(self, reward_strategy:Reward_Strategy=None, epochs:int=None, batch_size:int=128, memory_capacity:int=1000, learning_rate:float=0.001, discount_factor:float=0.05, max_steps:Optional=None, update_target_every:int=None) -> List[float]:
        raise NotImplementedError('train not implemented')


    def simulate(self):

        default_ticker_name = self.data_streamer.ticker_names[0]

        done  = False
        state = self.env.reset(default_ticker_name)

        while not done:
            decision = self.neural_network.act(state)

            state, _, done, _ = self.env.step(decision, default_ticker_name)

            self.env.render()
