# -*- coding: utf-8 -*-
"""Testing main module."""

from webhook import get_random_emoji, get_random_positive_message

from env import (
    ZIVIJO_ICON_EMOJI_CSV
)


def test_random_emoji() -> None:
    """Test the get_random_emoji function."""
    result = get_random_emoji()

    assert isinstance(result, str)
    assert len(result) > 2
    assert result[0] == ":"
    assert result[-1] == ":"
    assert result in ZIVIJO_ICON_EMOJI_CSV


def test_random_positive_message() -> None:
    """Test the get_random_positive_message function."""
    result = get_random_positive_message()

    assert isinstance(result, str)
    assert len(result) > 0
    assert result[-1] == "."
    assert result[0].isupper()
