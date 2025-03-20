FROM python:3.9

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install requirements
COPY django-requirements.txt ./
RUN pip install -r django-requirements.txt --no-cache-dir

# Install app
COPY . /app

# Setup django
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000

# Start Gunicorn, binding to 0.0.0.0:8000 with 3 worker processes.
CMD ["gunicorn", "active_interview_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
