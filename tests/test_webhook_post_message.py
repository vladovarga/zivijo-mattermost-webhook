# -*- coding: utf-8 -*-
"""Testing main module."""

import datetime
from unittest.mock import patch

from webhook import post_message

# constants for further testing

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


def test_post_message() -> None:
    """Test the post_message function with a well formatted csv."""

    with patch('webhook.logging') as mock_logging:
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            result = post_message(["@user_1_id"], ["@user_2_id"])

    assert result is True
    assert mock_logging.info.called
