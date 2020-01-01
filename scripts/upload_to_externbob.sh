#!/usr/bin/env bash
"""
    Uploads this to externbob, s.t. this continuously runs
"""

rsync -rPz -e 'ssh -p 2223' --exclude 'venv/' --exclude 'analysis/' --exclude '.env' --progress /Users/david/xtractor/ david@77.59.149.134:/home/david/xtractor/
