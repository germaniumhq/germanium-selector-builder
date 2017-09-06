#!/usr/bin/env bash

PROJECT_DIR=$(readlink -f $(dirname $(readlink -f "$0"))/..)

flr -o \
    ts/ -e "tsc --out js/main.js ts/main.ts" \
    germaniumsb/MainWindow.ui -e "germaniumsb/MainWindow.ui > germaniumsb/MainWindow.py" \
    germaniumsb/browserStateMachine.yml -e "cd germaniumsb; state-machine-generator python browserStateMachine.yml"
