#!/usr/bin/env bash

#source .venv/bin/activate

pyinstaller \
    --add-binary './desktop/Juasap.png:desktop' \
    --add-binary './locales/en/LC_MESSAGES/messages.mo:locales/en/LC_MESSAGES' \
    --add-binary './locales/es/LC_MESSAGES/messages.mo:locales/es/LC_MESSAGES' \
    --add-binary './locales/gl/LC_MESSAGES/messages.mo:locales/gl/LC_MESSAGES' \
    -F juasap.py

#deactivate
