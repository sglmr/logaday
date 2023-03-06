#!/bin/bash

# Go to the correct directory
cd /home/happy/recordaday

# Pull git changes
git pull

# pip commands
python -m pip install --upgrade pip | grep -v 'already satisfied'
python -m pip install -r requirements.txt | grep -v 'already satisfied'
python -m pip install -r requirements.txt --upgrade | grep -v 'already satisfied'

# Django commands
python manage.py migrate
python manage.py collectstatic --noinput --clear | grep -v 'Deleting'


# Refresh nginx & gunicorn
echo "Restarting gunicorn & nginx..."
sudo systemctl restart recordaday
sudo systemctl restart caddy
sudo systemctl daemon-reload
echo "Done!"

# Django deploy check
python manage.py check --deploy

# pip dependecy check
python -m pip list --outdated