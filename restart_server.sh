#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
python3 add_challenges.py
flask run
