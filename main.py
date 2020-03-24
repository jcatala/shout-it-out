#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import configparser
from pathlib import Path

config = configparser.ConfigParser()

home_dir = str(Path.home())
config.read("{}/.SIO.conf".format(home_dir))

bot_api_key = config['DEFAULT']['apikey']