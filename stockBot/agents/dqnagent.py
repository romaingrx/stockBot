#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""
import numpy as np
from typing import Optional, List, Text, Dict
from abc import ABC
import tensorflow as tf
import keras

from stockBot.neural_networks import Neural_Network, Deep_Q_Learning, DQNTransition, neural_network_graph
from stockBot.reward_strategies import Reward_Strategy, Simple_Reward_Strategy, Sortino
from stockBot.action_strategies import Action_Strategy, Simple_Action_Strategy
from stockBot.environments import Environment, Continuous_Environment
from stockBot.data import Data_Streamer
from stockBot.brokers import Broker, Fake_Broker
from stockBot.finance import Wallet
from stockBot.renderers import Naive_Plot, Basic_Plot
from .agent_base import Agent
from stockBot.memory import Memory
from stockBot.utils import timer
from numba import jit

class DQNAgent(Agent):

    def __init__(self, tickers:Text or List[Text]=None, initial_balance=None, broker:Broker=None, wallet:Wallet=None, env:Environment=None, data_streamer:Data_Streamer=None, neural_network:Neural_Network=None, reward_strategy:Reward_Strategy=None, action_strategy:Action_Strategy=None, load_name=None, hyperparams:Dict=None, Name:Text=None, **kwargs):

        self.hyperparams       = hyperparams
        self._history_capacity = kwargs.get('history_capacity', 30)
        self._random           = kwargs.get('random', False)
        self.features_function = kwargs.get('features_function', 'basic_features')
        self._tickers          = tickers if isinstance(tickers, list) else [tickers]
        self.broker            = broker if isinstance(broker, Broker) else Fake_Broker(Wallet(initial_balance))
        self.data_streamer     = data_streamer or Data_Streamer(tickers, random=self._random, history_capacity=self._history_capacity, features_function=self.features_function)
        self.wallet            = wallet or self.broker.wallet
        self.action_strategy   = Simple_Action_Strategy()
        self.reward_strategy   = Simple_Reward_Strategy()
        self.renderer          = kwargs.get('renderer', Basic_Plot())
        self.env               = env or Environment(data_streamer=self.data_streamer, broker=self.broker, action_strategy=self.action_strategy, reward_strategy=self.reward_strategy, renderer=self.renderer, history_capacity=self._history_capacity)
        self.neural_network    = Deep_Q_Learning(input_shape=self.env.observation_space.shape, output_size=self.env.action_space.n, load_name=kwargs.get('load_name',None), hyperparams=hyperparams, Name=Name)

    def train(self, epochs:int=None, batch_size:int=128, memory_capacity:int=1000, learning_rate:float=0.0001, discount_factor:float=0.9999, max_steps:Optional=None) -> List[float]:
        self.optimizer = tf.optimizers.Adam(lr=learning_rate)
        memory = Memory(memory_capacity, DQNTransition)
        reward_strategy = self.reward_strategy
        max_steps = max_steps or np.iinfo(np.int32).max
        epochs = epochs or 25

        eps_max = 0.9
        eps_min = 0.05
        eps_constant = 750

        episode = 0
        total_reward = 0
        rewards = []

        default_ticker_name = self.data_streamer.ticker_names[0]

        while episode < epochs:
            state = self.env.reset(default_ticker_name)
            done = False
            steps = 0
            loss_values = []
            balance_values = []

            while not done:

                epsilon = eps_min + (eps_max - eps_min)*np.exp(-steps/eps_constant)

                decision = self.neural_network.act(state, epsilon=epsilon)

                next_state, reward, done, info = self.env.step(decision, default_ticker_name)

                # self.env.render()

                if steps % 100 == 0:
                    print('episode %d ,step %d'%(episode, steps))
                    info['epsilon'] = epsilon
                    print(info)

                memory.push(state, decision, reward, next_state, done)

                state = next_state
                total_reward += reward
                rewards.append(reward)
                balance_values.append(self.wallet.balance)

                steps += 1

                if len(memory) < batch_size:
                    continue

                loss_value = self._fit_memory(memory, batch_size, discount_factor)
                loss_values.append(loss_value)

                if max_steps and steps > max_steps:
                    done = True

            episode += 1

            mean_loss    = np.mean(loss_values)
            mean_balance = np.mean(balance_values)
            mean_reward  = np.mean(rewards)
            self.neural_network.summary_scalar('loss', mean_loss, episode)
            self.neural_network.summary_scalar('balance', mean_balance, episode)
            self.neural_network.summary_scalar('reward', mean_reward, episode)
            self.neural_network.summary_weights_biases_histogram(episode)

            print('Epoch %d/%d'%(episode, epochs))
            print('loss %.3f - balance %.2f - reward %.3f'%(mean_loss, mean_balance, mean_reward))

            if episode == epochs:
                self.neural_network.save_model(episode=self.neural_network.initial_episode + epochs)

        return rewards


    def _fit_memory(self, memory:Memory, batch_size:int, discount_factor:float):
        transitions = memory.sample(batch_size)
        batch = DQNTransition(*zip(*transitions))

        state_batch = tf.convert_to_tensor(batch.state)
        action_batch = tf.convert_to_tensor(batch.action)
        reward_batch = tf.convert_to_tensor(batch.reward)
        next_state_batch = tf.convert_to_tensor(batch.next_state)
        done_batch = tf.convert_to_tensor(batch.done)

        variables = self.neural_network.model.trainable_variables

        q_next_states = self.neural_network.model(next_state_batch)
        q_target = tf.where(done_batch, reward_batch, reward_batch + discount_factor * tf.math.reduce_max(q_next_states, axis=1))

        with tf.GradientTape() as tape:
            tape.watch(variables)

            q_states = self.neural_network.model(state_batch)

            action_one_hot = tf.one_hot(action_batch, depth=self.env.action_space.n)
            q_values_actions = tf.math.reduce_sum(tf.multiply(q_states, action_one_hot) , axis=1)

            loss = tf.reduce_mean(tf.square(q_values_actions - q_target))


        gradients = tape.gradient(loss, variables)
        self.optimizer.apply_gradients(zip(gradients, variables))

        return loss
