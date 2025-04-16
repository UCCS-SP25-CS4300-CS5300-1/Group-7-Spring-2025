#!/bin/bash

python3 manage.py collectstatic --noinput;
python3 manage.py makemigrations;
python3 manage.py migrate;

gunicorn active_interview_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
