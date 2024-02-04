# -*- coding: utf-8 -*-
"""Testing the __version__ file."""
import __version__ as __version__


def test_version() -> None:
    # the version  has to be in the format x.y.z
    assert __version__.__version__.__contains__(".")
    assert isinstance(__version__.__version__, str)
    assert len(__version__.__version__) > 0
