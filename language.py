# This Python file uses the following encoding: utf-8

import gettext
import os

from tools import _PR2A

lang = os.getenv('LANGUAGE')[0:2].lower()
if (lang not in ('es', 'gl')):
    lang = 'en'
translations = gettext.translation(
    'messages',
    localedir=_PR2A('locale'),
    languages=[lang]
)
translations.install()
_ = translations.gettext

if __name__ == "__main__":
    pass
