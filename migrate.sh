#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
export FLASK_APP=create_migration.py
flask db migrate -m "Add EcoChallenge model and user_challenges association"
flask db upgrade
deactivate
