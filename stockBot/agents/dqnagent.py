#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Saturday, 21 March 2020
"""
import numpy as np
from typing import Optional, List, Text
from abc import ABC
import tensorflow as tf

from .agent_base import Agent
from stockBot.memory import Memory
from stockBot.reward_strategies import Reward_Strategy
from stockBot.neural_networks import DQNTransition
from stockBot.utils import timer

class DQNAgent(Agent):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_network   = tf.keras.models.clone_model(self.neural_network.model)
        self.target_network.trainable = False

    def train(self, reward_strategy:Reward_Strategy=None, epochs:int=None, batch_size:int=128, memory_capacity:int=1000, learning_rate:float=0.001, discount_factor:float=0.05, max_steps:Optional=None, update_target_every:int=None) -> List[float]:

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

        default_ticker_name = self.data_streamer.ticker_names[0]


        while episode < epochs:
            state = self.env.reset(default_ticker_name)
            self.wallet.reset()
            done = False
            steps = 0
            loss_values = []
            balance_values = []

            while not done:

                epsilon = eps_min + (eps_max - eps_min)*np.exp(-steps/eps_constant)

                decision = self.neural_network.act(state, epsilon=epsilon)

                next_state, reward, done, info = self.env.step(decision, default_ticker_name)

                if steps % 100 == 0:
                    print('episode %d ,step %d'%(episode, steps))
                    print(info)

                memory.push(state, decision, reward, next_state, done)

                state = next_state
                total_reward += reward
                rewards.append(reward)
                balance_values.append(self.wallet.balance)

                steps += 1

                if len(memory) < batch_size:
                    continue

                loss_value = self._fit_memory(memory, batch_size, learning_rate, discount_factor)
                loss_values.append(loss_value)

                if update_target_every % steps == 0:
                    self.target_network.set_weights(self.neural_network.model.get_weights())

                if max_steps and steps > max_steps:
                    done = True

                # self.env.render(episode)

            mean_loss    = np.mean(loss_values)
            mean_balance = np.mean(balance_values)
            mean_reward  = np.mean(rewards)
            self.neural_network.summary_scalar('loss', mean_loss, episode)
            self.neural_network.summary_scalar('balance', mean_balance, episode)
            self.neural_network.summary_scalar('reward', mean_reward, episode)

            print('Epoch %d/%d'%(episode, epochs))
            print('loss %.3f - balance %.2f - reward %.3f'%(mean_loss, mean_balance, mean_reward))

            episode += 1

            if episode == epochs:
                self.neural_network.save_model(episode=self.neural_network.initial_episode + epochs)

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
                self.neural_network.model(state_batch) * tf.one_hot(action_batch, self.env.action_space.n),
                axis=1
            )
            next_state_values = tf.where(
                done_batch,
                tf.zeros(batch_size),
                tf.math.reduce_max(self.target_network(next_state_batch), axis=1)
            )

            expected_state_action_values = reward_batch + (discount_factor * next_state_values)
            loss_value = loss(expected_state_action_values, state_action_values)


        variables = self.neural_network.model.trainable_variables
        gradients = g.gradient(loss_value, variables)
        optimizer.apply_gradients(zip(gradients, variables))

        return loss_value
