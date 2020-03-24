#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""
import numpy as np
from typing import Optional, List
from abc import ABC
import tensorflow as tf

from stockBot.wallets import Portfolio
from .models import Neural_Network, Deep_Q_Learning, DQNTransition
from .rewards import Reward_Strategy, Simple_Reward_Strategy
from .memory import Memory
from stockBot.data import Data_Streamer
from stockBot.wallets import Wallet
from stockBot.brokers import Broker, Fake_Broker
from stockBot.environment import Environment

class Agent():

    def __init__(self, wallet:Wallet, env:Environment=None, data_streamer:Data_Streamer=None, neural_network:Neural_Network=None, reward_strategy:Reward_Strategy=None, broker:Broker=None):
        self.wallet          = wallet
        self.env             = env or Environment(wallet)
        self.data_streamer   = data_streamer or Data_Streamer('SPCE')
        self.neural_network  = neural_network or Deep_Q_Learning(self.env.observation_shape)
        self.target_network = tf.keras.models.clone_model(self.neural_network.model)
        self.target_network.trainable = False
        print(dir(self.target_network))
        self.reward_strategy = reward_strategy or Simple_Reward_Strategy()
        self.broker          = broker or Fake_Broker()

        # A REMPLACER EN PREMIER

        self.action_space = (3,)
        self.n_actions = len(self.action_space)



    def train(self, data=None, reward_strategy:Reward_Strategy=None, epochs:int=None, batch_size:int=128, memory_capacity:int=1000, learning_rate:float=0.001, max_steps:Optional=None, update_target_every:int=None) -> List[float]:

        memory = Memory(memory_capacity, DQNTransition)
        reward_strategy = self.reward_strategy
        max_steps = max_steps or np.iinfo(np.int32).max
        epochs = epochs or 25
        update_target_every = update_target_every or 1000

        eps_max = 0.9
        eps_min = 0.05
        eps_constant = 200

        episode = 0
        total_reward = 0
        rewards = []

        while episode < epochs:
            state = self.env.reset()
            done = False
            steps = 0

            while not done:
                epsilon = eps_min + (eps_max - eps_min)*np.exp(-steps/eps_constant)

                decision, buy = self.neural_network.act(state, epsilon=epsilon, max_buy=5)

                next_state, reward, done, info = self.env.step()

                memory.push(state, decision, reward, next_state, done)

                state = next_state
                total_reward += reward
                rewards.append(reward)

                steps += 1

                if len(memory) < batch_size:
                    continue

                # self._fit_memory(memory, batch_size, learning_rate)

                # if update_target_every % steps == 0:
                #     self.target_network = tf.keras.models.clone_model(self.neural_network.model)
                #     self.target_network.trainable = False

                if max_steps and steps > max_steps:
                    done = True

                # self.env.render(episode)
            if episode == epochs - 1:
                self.neural_network.save(episode)

            episode += 1

        return rewards


    def _fit_memory(self, memory:Memory, batch_size:int, learning_rate:float, discount_factor:float):
        optimizer = tf.keras.optimizers.Adam(learning_rate)
        loss = tf.keras.losses.Huber()

        transitions = memory.sample(batch_size)
        batch = DQNTransition(*zip(*transitions))

        state_batch = tf.convert_to_tensor(batch.state)
        action_batch = tf.convert_to_tensor(batch.action)
        reward_batch = tf.convert_to_tensor(batch.reward)
        next_state_batch = tf.convert_to_tensor(batch.next_state)
        done_batch = tf.convert_to_tensor(batch.done)

        with tf.GradientTape() as g:
            state_action_values = tf.math.reduce_sum(
                self.neural_network(state_batch) * tf.one_hot(action_batch, self.n_actions),
                axis=1
            )
            next_state_values = tf.where(
                done_batch,
                tf.zeros(batch_size),
                tf.math.reduce_max(self.target_network(next_state_batch), axis=1)
            )

            expected_state_action_values = reward_batch + (discount_factor * next_state_values)
            loss_value = loss(expected_state_action_values, state_action_values)

        variables = self.neural_network.trainable_variables
        gradients = g.gradient(loss_value, variables)
        optimizer.apply_gradient(zip(gradients, variables))
