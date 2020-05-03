# This Python file uses the following encoding: utf-8

import os
import subprocess
import sys

ROOT_DIR = sys._MEIPASS \
    if hasattr(sys, '_MEIPASS') \
    else os.path.dirname(os.path.realpath(__file__))

EXTERNAL_URL_OPEN_BIN = 'xdg-open'


# Converts relative path to application real path.
def _PR2A(d):
    return os.path.join(ROOT_DIR, d)


# External open url.
def _EOU(url):
    subprocess.call([EXTERNAL_URL_OPEN_BIN, url])


if __name__ == "__main__":
    pass
