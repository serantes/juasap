#!/usr/bin/env bash

#source .venv/bin/activate

lrelease juasap.pro
pyinstaller \
    --add-binary './desktop/Juasap.png:desktop' \
    --add-binary './i18n/gl_ES.qm:i18n' \
    --add-binary './i18n/en_US.qm:i18n' \
    --add-binary './i18n/es_ES.qm:i18n' \
    -F juasap.py

#deactivate
