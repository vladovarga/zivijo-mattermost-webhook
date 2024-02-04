# -*- coding: utf-8 -*-
"""Testing main module."""
# mock env variables are set in setup.cfg
from env import (
    ZIVIJO_ICON_EMOJI_CSV
)


def test_default_emojis() -> None:
    """Test if the default emojis are present."""
    result = ZIVIJO_ICON_EMOJI_CSV

    assert isinstance(result, str)

    assert (len(result.split(',')) > 0)
