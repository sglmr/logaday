#!/bin/bash

# Go to the correct directory
cd /home/happy/recordmyday

# Pull git changes
git pull

# Activate virtual environment
source venv/bin/activate

# pip commands
pip install --upgrade pip | grep -v 'already satisfied'
pip install -r requirements.txt | grep -v 'already satisfied'
pip install -r requirements.txt --upgrade | grep -v 'already satisfied'

# Django commands
python manage.py migrate
python manage.py collectstatic --noinput --clear | grep -v 'Deleting'


# Refresh nginx & gunicorn
echo "Restarting gunicorn & nginx..."
sudo systemctl daemon-reload
sudo systemctl restart recordmyday
sudo systemctl restart nginx
echo "Done!"

# Django deploy check
python manage.py check --deploy

# pip dependecy check
pip list --outdated

# Deactivate virtual environment
deactivate