# -*- coding: utf-8 -*-
"""Živijó mattermost webhook."""

import csv
import random
import datetime
from typing import Dict, List
import logging

import requests

from env import (
    ZIVIJO_LOGLEVEL,
    ZIVIJO_WEBHOOK_URL,
    ZIVIJO_CHANNEL,
    ZIVIJO_BIRTHDAYS_CSV_PATH,
    ZIVIJO_BOT_USERNAME,
    ZIVIJO_ICON_EMOJI_CSV
)

logging.basicConfig(level=ZIVIJO_LOGLEVEL)

logging.info("Starting Živijó Mattermost webhook")
logging.info(f"ZIVIJO_WEBHOOK_URL: {ZIVIJO_WEBHOOK_URL}")
logging.info(f"ZIVIJO_CHANNEL: {ZIVIJO_CHANNEL}")
logging.info(f"ZIVIJO_BIRTHDAYS_CSV_PATH: {ZIVIJO_BIRTHDAYS_CSV_PATH}")
logging.info(f"ZIVIJO_BOT_USERNAME: {ZIVIJO_BOT_USERNAME}")
logging.info(f"ZIVIJO_ICON_EMOJI_CSV: {ZIVIJO_ICON_EMOJI_CSV}")


def get_random_emoji() -> str:
    """Returns randomly one of the emojis defined in ZIVIJO_ICON_EMOJI_CSV."""
    return random.choice(ZIVIJO_ICON_EMOJI_CSV.split(','))  # nosec B311


def get_random_positive_message() -> str:
    """Returns randomly one of the messages."""
    messages = ["All the best and many more years to come.",
                "Your presence brightens our workplace.",
                "We're grateful to have you as part of our team.",
                "We're truly appreciative to have you contributing to our team.",
                "Wishing you continued success and prosperity in the years ahead.",
                "Here's to your ongoing achievements and a future filled with happiness.",
                "Sending you wishes for a lifetime of joy, fulfillment, and memorable experiences.",
                "May each passing year bring you closer to your dreams and aspirations.",
                "Here's to a future brimming with excitement, prosperity, and fulfillment.",
                "May the coming years be even more fulfilling and rewarding than the ones before."
                ]
    return random.choice(messages)  # nosec B311


def read_and_parse_csv() -> List[Dict]:
    """Read the csv line by line and parse data into a dictionary."""

    result: List[Dict] = []

    with open(ZIVIJO_BIRTHDAYS_CSV_PATH) as csvfile:
        # check if the csv has a header
        # has_header = csv.Sniffer().has_header(csvfile.read(1024))

        # if (not has_header):
        #     logging.error(f"CSV file {ZIVIJO_BIRTHDAYS_CSV_PATH} does not have a header. Please add correct header.")
        #     return result

        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            # convert ISO date to datetime object
            try:
                if (row['iso-birth-date']):
                    row["birth_date"] = datetime.datetime.strptime(row['iso-birth-date'], '%Y-%m-%d')
            except ValueError:
                logging.error(f"Failed to parse birth date {row['iso-birth-date']} for user {row['user_id']}. Skipping.")  # noqa: E501
                continue

            try:
                if (row['iso-name-date']):
                    row["name_date"] = datetime.datetime.strptime(row['iso-name-date'], '%Y-%m-%d')
            except ValueError:
                logging.error(f"Failed to parse name date {row['iso-name-date']} for user {row['user_id']}. Skipping.")
                continue

            # check if user_id is present
            if (not row.get("user_id")):
                logging.error(f"User ID is missing for user {row}. Skipping.")
                continue

            # check if user_id begins with @
            if (not row["user_id"].startswith("@")):
                # add @ to the user_id
                row["user_id"] = f"@{row['user_id']}"
                logging.warning(f"User ID {row['user_id']} does not start with @. Adding @.")

            result.append(row)

    logging.info(f"Read {len(result)} birthdays from {ZIVIJO_BIRTHDAYS_CSV_PATH}")

    return result


def post_message(birthday_people_ids: List[str], nameday_people_ids: List[str]) -> bool:
    """Post a message to the webhook."""

    if ((len(birthday_people_ids) == 0) and (len(nameday_people_ids) == 0)):
        # wtf?
        message = "This should not happen. How come there are no birthdays or namedays?"
        logging.error(message)
        raise Exception(message)

    if (len(birthday_people_ids) > 0):
        # prepare the birthday message
        birthday_colleague_wording = "colleague" if (len(birthday_people_ids) == 1) else "colleagues"

        birthday_colleague_id_list = ", ".join(birthday_people_ids)

        birthday_message = "### {emoji} Happy Birthday! {emoji} \nToday is the birthday of our beloved {colleague_wording} {colleague_id_list}. {random_message} :)".format(  # noqa: E501
            emoji=get_random_emoji(),
            colleague_wording=birthday_colleague_wording,
            colleague_id_list=birthday_colleague_id_list,
            random_message=get_random_positive_message()
        )

    if (len(nameday_people_ids) > 0):
        # prepare the nameday message
        nameday_colleague_wording = "colleague" if (len(nameday_people_ids) == 1) else "colleagues"

        nameday_colleague_id_list = ", ".join(nameday_people_ids)

        nameday_message = "### {emoji} Happy Nameday! {emoji} \nThe day has come to celebrate the nameday of our dearest {colleague_wording} {colleague_id_list}. {random_message} :)".format(  # noqa: E501
            emoji=get_random_emoji(),
            colleague_wording=nameday_colleague_wording,
            colleague_id_list=nameday_colleague_id_list,
            random_message=get_random_positive_message()
        )

    # final message
    message = "\n\n".join([birthday_message, nameday_message])

    # prepare the payload
    payload = {
        "channel": ZIVIJO_CHANNEL,
        "username": ZIVIJO_BOT_USERNAME,
        "icon_emoji": get_random_emoji(),
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

    # read the csv
    parsed_csv = read_and_parse_csv()

    if (len(parsed_csv) == 0):
        logging.info(f"No data read? {ZIVIJO_BIRTHDAYS_CSV_PATH} is empty?")
        return False

    # get today's date
    today = datetime.datetime.today()

    # filter out the birthdays that match today's date
    birthday_people_ids = [b["user_id"] for b in parsed_csv if b.get("birth_date") and b["birth_date"].month == today.month and b["birth_date"].day == today.day]  # noqa: E501

    # filter out the namedays that match today's date
    nameday_people_ids = [b["user_id"] for b in parsed_csv if b.get("name_date") and b["name_date"].month == today.month and b["name_date"].day == today.day]  # noqa: E501

    if (len(birthday_people_ids) == 0):
        logging.info("No birthdays today :(")
    else:
        logging.info(f"We have some birthdays today! {birthday_people_ids}")

    if (len(nameday_people_ids) == 0):
        logging.info("No namedays today :(")
    else:
        logging.info(f"We have some namedays today! {nameday_people_ids}")

    if ((len(birthday_people_ids) == 0) and (len(nameday_people_ids) == 0)):
        return True

    # post the message
    return post_message(birthday_people_ids, nameday_people_ids)
