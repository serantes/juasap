#!/usr/bin/env bash

#source .venv/bin/activate

pyinstaller --add-binary './desktop/Juasap.png:.' -F juasap.py

#deactivate
