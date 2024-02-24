# -*- coding: utf-8 -*-
# mypy: disable_error_code="attr-defined, arg-type, method-assign"
"""Testing main module."""

from typing import Dict, List
import datetime
import pytest
from unittest.mock import patch, mock_open

from webhook import read_and_parse_csv

# constants for further testing
CSV_HEADER = "email,user_id,iso-birth-date,iso-name-date"

USER_1 = {
    "email": "user_1@email.com",
    "user_id": "@user_1_id",
    "iso-birth-date": "2022-01-01",
    "birth_date": datetime.datetime(2022, 1, 1),
    "iso-name-date": "2022-01-02",
    "name_date": datetime.datetime(2022, 1, 2)
}

USER_2 = {
    "email": "user_2@email.com",
    "user_id": "@user_2_id",
    "iso-birth-date": "2022-02-01",
    "birth_date": datetime.datetime(2022, 2, 1),
    "iso-name-date": "2022-02-02",
    "name_date": datetime.datetime(2022, 2, 2)
}


def compose_csv_content(csv_header: str, users: List[Dict]) -> str:
    """Compose the csv content from the users data."""
    csv_content = "{csv_header}\n".format(csv_header=csv_header)

    for user in users:
        csv_content += "{email},{user_id},{iso_birth_date},{iso_name_date}\n".format(
            email=user["email"],
            user_id=user.get("user_id"),
            iso_birth_date=user["iso-birth-date"],
            iso_name_date=user["iso-name-date"]
        )

    return csv_content


def test_read_and_parse_csv() -> None:
    """Test the read_and_parse_csv function with a well formatted csv."""

    csv_content = compose_csv_content(CSV_HEADER, [USER_1, USER_2])

    with patch('builtins.open', mock_open(read_data=csv_content)):
        result = read_and_parse_csv()

    assert len(result) == 2

    # Check the parsed data
    assert result[0]["email"] == USER_1["email"]
    assert result[0]["user_id"] == USER_1["user_id"]
    assert result[0]["iso-birth-date"] == USER_1["iso-birth-date"]
    assert result[0]["birth_date"].year == USER_1["birth_date"].year
    assert result[0]["birth_date"].month == USER_1["birth_date"].month
    assert result[0]["birth_date"].day == USER_1["birth_date"].day
    assert result[0]["iso-name-date"] == USER_1["iso-name-date"]
    assert result[0]["name_date"].year == USER_1["name_date"].year
    assert result[0]["name_date"].month == USER_1["name_date"].month
    assert result[0]["name_date"].day == USER_1["name_date"].day

    assert result[1]["email"] == USER_2["email"]
    assert result[1]["user_id"] == USER_2["user_id"]
    assert result[1]["iso-birth-date"] == USER_2["iso-birth-date"]
    assert result[1]["birth_date"].year == USER_2["birth_date"].year
    assert result[1]["birth_date"].month == USER_2["birth_date"].month
    assert result[1]["birth_date"].day == USER_2["birth_date"].day
    assert result[1]["iso-name-date"] == USER_2["iso-name-date"]
    assert result[1]["name_date"].year == USER_2["name_date"].year
    assert result[1]["name_date"].month == USER_2["name_date"].month
    assert result[1]["name_date"].day == USER_2["name_date"].day


def test_read_and_parse_csv_without_header() -> None:
    """CSV file missing the header."""
    csv_content = compose_csv_content("", [USER_1, USER_2])

    with patch('builtins.open', mock_open(read_data=csv_content)):
        with pytest.raises(KeyError):
            read_and_parse_csv()


def test_read_and_parse_csv_invalid_birth_date() -> None:
    """CSV file with invalid birth date."""
    user_1 = USER_1.copy()
    user_1["iso-birth-date"] = "2022-01-32"

    csv_content = compose_csv_content(CSV_HEADER, [user_1, USER_2])

    with patch('builtins.open', mock_open(read_data=csv_content)):
        result = read_and_parse_csv()

    assert len(result) == 1

    # Check the parsed data
    assert result[0]["email"] == USER_2["email"]
    assert result[0]["user_id"] == USER_2["user_id"]
    assert result[0]["iso-birth-date"] == USER_2["iso-birth-date"]
    assert result[0]["birth_date"].year == USER_2["birth_date"].year
    assert result[0]["birth_date"].month == USER_2["birth_date"].month
    assert result[0]["birth_date"].day == USER_2["birth_date"].day
    assert result[0]["iso-name-date"] == USER_2["iso-name-date"]
    assert result[0]["name_date"].year == USER_2["name_date"].year
    assert result[0]["name_date"].month == USER_2["name_date"].month
    assert result[0]["name_date"].day == USER_2["name_date"].day


def test_read_and_parse_csv_invalid_name_date() -> None:
    """CSV file with invalid name date."""
    user_1 = USER_1.copy()
    user_1["iso-name-date"] = "2022-01-32"

    csv_content = compose_csv_content(CSV_HEADER, [user_1, USER_2])

    with patch('builtins.open', mock_open(read_data=csv_content)):
        result = read_and_parse_csv()

    assert len(result) == 1

    # Check the parsed data
    assert result[0]["email"] == USER_2["email"]
    assert result[0]["user_id"] == USER_2["user_id"]
    assert result[0]["iso-birth-date"] == USER_2["iso-birth-date"]
    assert result[0]["birth_date"].year == USER_2["birth_date"].year
    assert result[0]["birth_date"].month == USER_2["birth_date"].month
    assert result[0]["birth_date"].day == USER_2["birth_date"].day
    assert result[0]["iso-name-date"] == USER_2["iso-name-date"]
    assert result[0]["name_date"].year == USER_2["name_date"].year
    assert result[0]["name_date"].month == USER_2["name_date"].month
    assert result[0]["name_date"].day == USER_2["name_date"].day


def test_read_and_parse_csv_missing_user_id() -> None:
    """CSV file with missing user_id."""

    user_1 = USER_1.copy()
    user_1["user_id"] = ""

    csv_content = compose_csv_content(CSV_HEADER, [user_1, USER_2])

    with patch('builtins.open', mock_open(read_data=csv_content)):
        with patch('webhook.logging') as mock_logging:
            result = read_and_parse_csv()

    assert len(result) == 1

    # assert that the logging.error was called
    assert mock_logging.error.called

    # Check the parsed data
    assert result[0]["email"] == USER_2["email"]
    assert result[0]["user_id"] == USER_2["user_id"]
    assert result[0]["iso-birth-date"] == USER_2["iso-birth-date"]
    assert result[0]["birth_date"].year == USER_2["birth_date"].year
    assert result[0]["birth_date"].month == USER_2["birth_date"].month
    assert result[0]["birth_date"].day == USER_2["birth_date"].day
    assert result[0]["iso-name-date"] == USER_2["iso-name-date"]
    assert result[0]["name_date"].year == USER_2["name_date"].year
    assert result[0]["name_date"].month == USER_2["name_date"].month
    assert result[0]["name_date"].day == USER_2["name_date"].day


def test_read_and_parse_csv_user_id_without_at() -> None:
    """CSV file with user_id without @ at the beginning."""

    user_1 = USER_1.copy()
    user_1["user_id"] = "user_1_id"

    csv_content = compose_csv_content(CSV_HEADER, [user_1, USER_2])

    with patch('builtins.open', mock_open(read_data=csv_content)):
        with patch('webhook.logging') as mock_logging:
            result = read_and_parse_csv()

    assert len(result) == 2

    # assert that the logging.warning was called
    assert mock_logging.warning.called

    # Check the parsed data
    assert result[0]["email"] == USER_1["email"]
    assert result[0]["user_id"] == USER_1["user_id"]
    assert result[0]["iso-birth-date"] == USER_1["iso-birth-date"]
    assert result[0]["birth_date"].year == USER_1["birth_date"].year
    assert result[0]["birth_date"].month == USER_1["birth_date"].month
    assert result[0]["birth_date"].day == USER_1["birth_date"].day
    assert result[0]["iso-name-date"] == USER_1["iso-name-date"]
    assert result[0]["name_date"].year == USER_1["name_date"].year
    assert result[0]["name_date"].month == USER_1["name_date"].month
    assert result[0]["name_date"].day == USER_1["name_date"].day

    assert result[1]["email"] == USER_2["email"]
    assert result[1]["user_id"] == USER_2["user_id"]
    assert result[1]["iso-birth-date"] == USER_2["iso-birth-date"]
    assert result[1]["birth_date"].year == USER_2["birth_date"].year
    assert result[1]["birth_date"].month == USER_2["birth_date"].month
    assert result[1]["birth_date"].day == USER_2["birth_date"].day
    assert result[1]["iso-name-date"] == USER_2["iso-name-date"]
    assert result[1]["name_date"].year == USER_2["name_date"].year
    assert result[1]["name_date"].month == USER_2["name_date"].month
    assert result[1]["name_date"].day == USER_2["name_date"].day
