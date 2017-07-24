#!/usr/bin/env bash

PROJECT_DIR=$(readlink -f $(dirname $(readlink -f "$0"))/..)

cd $PROJECT_DIR
pyside-uic germaniumsb/MainWindow.ui > germaniumsb/MainWindow.py

