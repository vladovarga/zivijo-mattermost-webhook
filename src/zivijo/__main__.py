# -*- coding: utf-8 -*-
"""Živijó mattermost webhook."""

import csv
import random
import os
import datetime
from typing import Dict, List
import logging

import requests

# Constants
ZIVIJO_LOGLEVEL = os.getenv('ZIVIJO_LOGLEVEL', logging.getLevelName(logging.INFO)).upper()

logging.basicConfig(level=ZIVIJO_LOGLEVEL)

# the URL of the incoming webhook
ZIVIJO_WEBHOOK_URL = os.environ['ZIVIJO_WEBHOOK_URL']

# channel to post in
ZIVIJO_CHANNEL = os.getenv('ZIVIJO_CHANNEL', 'town-square')

# the path to the CSV file to read
ZIVIJO_BIRTHDAYS_CSV_PATH = os.environ['ZIVIJO_BIRTHDAYS_CSV_PATH']

# bot appearance
ZIVIJO_BOT_USERNAME = "Živijó"
ZIVIJO_ICON_EMOJI_CSV = os.getenv(
    'ZIVIJO_ICON_EMOJI_CSV',
    # default to some emojis
    ':champagne:,:tada:,:clinking_glasses:,:confetti_ball:,:gift:,:birthday:'
)

logging.info("Starting Živijó Mattermost webhook")
logging.info(f"ZIVIJO_WEBHOOK_URL: {ZIVIJO_WEBHOOK_URL}")
logging.info(f"ZIVIJO_CHANNEL: {ZIVIJO_CHANNEL}")
logging.info(f"ZIVIJO_BIRTHDAYS_CSV_PATH: {ZIVIJO_BIRTHDAYS_CSV_PATH}")
logging.info(f"ZIVIJO_BOT_USERNAME: {ZIVIJO_BOT_USERNAME}")
logging.info(f"ZIVIJO_ICON_EMOJI_CSV: {ZIVIJO_ICON_EMOJI_CSV}")


# Functions
def read_birthdays() -> List[Dict]:
    """Read the birthdays csv line by line and parse data into a dictionary."""

    result: List[Dict] = []

    with open(ZIVIJO_BIRTHDAYS_CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            # convert iso date to datetime object

            try:
                row["birth_date"] = datetime.datetime.strptime(row['iso-birth-date'], '%Y-%m-%d')
            except ValueError:
                logging.error(f"Failed to parse date {row['iso-birth-date']} for user {row['user_id']}. Skipping.")
                continue

            result.append(row)

    logging.info(f"Read {len(result)} birthdays from {ZIVIJO_BIRTHDAYS_CSV_PATH}")

    return result


def post_message(birthday_boys_ids: List[str]) -> bool:
    """Post a message to the webhook."""

    if (len(birthday_boys_ids) == 0):
        # wtf?
        logging.error("This should not happen. How come there are not birthday boys?")
        return False

    # prepare the random icon emoji from the list
    bot_icon_emoji = random.choice(ZIVIJO_ICON_EMOJI_CSV.split(','))  # nosec B311

    # prepare the message
    colleague_wording = "colleague" if (len(birthday_boys_ids) == 1) else "colleagues"

    colleague_id_list = ", ".join(birthday_boys_ids)

    message = "Today is the birthday of our beloved {colleague_wording} {colleague_id_list}. All the best and many more years to come! :)".format(  # noqa: E501
        colleague_wording=colleague_wording,
        colleague_id_list=colleague_id_list
    )

    # prepare the payload
    payload = {
        "channel": ZIVIJO_CHANNEL,
        "username": ZIVIJO_BOT_USERNAME,
        "icon_emoji": bot_icon_emoji,
        "text": message,
        # "props": {
        #     "card": "Salesforce Opportunity Information:\n\n [Opportunity](https://salesforce.com/OPPORTUNITY_ID)"
        # }
    }

    headers = {"Content-Type": "application/json"}

    # post the message
    response = requests.post(ZIVIJO_WEBHOOK_URL, headers=headers, json=payload, timeout=5)

    if response.status_code != 200:
        raise Exception(f"Failed to send notification to Mattermost: {response.text}")

    logging.info(f"Posted message to Mattermost: {message}")

    # everything went fine
    return True


def run() -> bool:
    """Run the bot."""

    # read the birthdays
    birthdays = read_birthdays()

    if (len(birthdays) == 0):
        logging.info(f"No birthdays read? {ZIVIJO_BIRTHDAYS_CSV_PATH} is empty?")
        return True

    # get today's date
    today = datetime.datetime.today()

    # filter out the birthdays that match today's date
    birthday_boys_ids = [b["user_id"] for b in birthdays if b["birth_date"].month == today.month and b["birth_date"].day == today.day]  # noqa: E501

    if (len(birthday_boys_ids) == 0):
        logging.info("No birthdays today :(")
        return True

    logging.info(f"We have some birthdays today! {birthday_boys_ids}")

    # post the message
    post_message(birthday_boys_ids)

    # everything went fine
    return True


if __name__ == "__main__":
    run()
