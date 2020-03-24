#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Sunday, 22 March 2020
"""

from abc import abstractmethod
from collections import namedtuple, deque
import random

Memory_State = namedtuple('Memory_State', ['state', 'action', 'reward', 'next_state', 'done'])

class Memory:

    def __init__(self, capacity:int, memory_state:namedtuple=Memory_State):
        self.capacity = capacity
        self.memory_state = memory_state
        self.memory = deque([], maxlen=self.capacity)

    def push(self, *args):
        self.memory.append(Memory_State(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
