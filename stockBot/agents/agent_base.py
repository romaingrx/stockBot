#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 27 March 2020
"""
import numpy as np
from abc import ABC
import tensorflow as tf
from typing import Optional, List, Text

from stockBot.neural_networks import Neural_Network, Deep_Q_Learning, DQNTransition, neural_network_graph
from stockBot.reward_strategies import Reward_Strategy, Simple_Reward_Strategy
from stockBot.action_strategies import Action_Strategy, Simple_Action_Strategy
from stockBot.environments import Environment
from stockBot.data import Data_Streamer
from stockBot.brokers import Broker, Fake_Broker
from stockBot.finance import Wallet

class Agent(ABC):

    def __init__(self, tickers:Text or List[Text]=None, initial_balance=None, broker:Broker=None, wallet:Wallet=None, env:Environment=None, data_streamer:Data_Streamer=None, neural_network:Neural_Network=None, reward_strategy:Reward_Strategy=None, action_strategy:Action_Strategy=None):
        self._tickers         = tickers if isinstance(tickers, list) else [tickers]
        self._initial_balance = initial_balance
        self.broker           = broker if isinstance(broker, Broker) else Fake_Broker(Wallet(self._initial_balance))
        self.data_streamer    = data_streamer or Data_Streamer(tickers)
        self.wallet           = wallet or self.broker.wallet
        self.action_strategy  = action_strategy or Simple_Action_Strategy()
        self.reward_strategy  = reward_strategy or Simple_Reward_Strategy()
        self.env              = env or Environment(data_streamer=self.data_streamer, broker=self.broker, action_strategy=self.action_strategy, reward_strategy=self.reward_strategy)
        self.neural_network   = neural_network if isinstance(neural_network, Neural_Network) else Deep_Q_Learning(self.env.observation_space.shape)

    def train(self, reward_strategy:Reward_Strategy=None, epochs:int=None, batch_size:int=128, memory_capacity:int=1000, learning_rate:float=0.001, discount_factor:float=0.05, max_steps:Optional=None, update_target_every:int=None) -> List[float]:
        raise NotImplementedError('train not implemented')
