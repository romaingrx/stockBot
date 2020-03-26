#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Tuesday, 24 March 2020
"""

from typing import Text
from stockBot import TENSORBOARDPATH
from stockBot.wallets import Wallet
from .renderer_base import Renderer

class File_Renderer(Renderer):

    def __init__(self, file_path:Text=None):
        self.file = file_path or TENSORBOARDPATH%"../renderer.txt"
        self.fd = open(self.file, 'w')
        self.fd.truncate(0)

    def render(self, wallet:Wallet):
        update_str = str(wallet)
        self.fd.write(update_str)

    def reset(self):
        pass
