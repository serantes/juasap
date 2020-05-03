#!/usr/bin/env bash

#source .venv/bin/activate

pyinstaller \
    --add-binary './desktop/Juasap.png:desktop' \
    --add-binary './locale/en/LC_MESSAGES/messages.mo:locale/en/LC_MESSAGES' \
    --add-binary './locale/es/LC_MESSAGES/messages.mo:locale/es/LC_MESSAGES' \
    --add-binary './locale/gl/LC_MESSAGES/messages.mo:locale/gl/LC_MESSAGES' \
    -F juasap.py

#deactivate
