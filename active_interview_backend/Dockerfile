FROM python:3.9

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

# Install app
COPY . /app

# Setup django
# RUN python manage.py collectstatic --noinput
# RUN python manage.py makemigrations
# RUN python manage.py migrate

EXPOSE 8000

# Run startup script
CMD ["./start.sh"]
