# -*- coding: utf-8 -*-
"""Živijó mattermost webhook."""

from webhook import run as zivijo_run


def run() -> bool:
    return zivijo_run()


if __name__ == "__main__":
    run()
