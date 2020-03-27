#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@author : Romain Graux
@date : Friday, 27 March 2020
"""
from pathlib import Path

def get_project_root() -> Path:
    """Returns project root folder."""""
    return Path(__file__).parent.parent.parent
