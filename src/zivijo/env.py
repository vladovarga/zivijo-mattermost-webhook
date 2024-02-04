# -*- coding: utf-8 -*-
"""Environment variables."""

import os
import logging

# Constants
ZIVIJO_LOGLEVEL = os.getenv('ZIVIJO_LOGLEVEL', logging.getLevelName(logging.INFO)).upper()

# the URL of the incoming webhook
ZIVIJO_WEBHOOK_URL = os.getenv('ZIVIJO_WEBHOOK_URL')

# channel to post in
ZIVIJO_CHANNEL = os.getenv('ZIVIJO_CHANNEL', 'town-square')

# the path to the CSV file to read
ZIVIJO_BIRTHDAYS_CSV_PATH = os.getenv('ZIVIJO_BIRTHDAYS_CSV_PATH')

# bot appearance
ZIVIJO_BOT_USERNAME = "Živijó"
ZIVIJO_ICON_EMOJI_CSV = os.getenv(
    'ZIVIJO_ICON_EMOJI_CSV',
    # default to some emojis
    ':champagne:,:tada:,:clinking_glasses:,:confetti_ball:,:gift:,:birthday:'
)
