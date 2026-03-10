#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2026-03-10 21:52 
    Name  :     config.py
    Desc  :     
--------------------------------------
"""
import tomllib
from pathlib import Path
CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.toml"


with open(CONFIG_PATH, "rb") as f:
    CONFIG = tomllib.load(f)


def get_config():
    return CONFIG