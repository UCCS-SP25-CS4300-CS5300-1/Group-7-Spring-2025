FROM python:3.9

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install requirements
COPY django-requirements.txt ./
RUN pip install -r django-requirements.txt --no-cache-dir

# Install app
COPY . /app
# ENTRYPOINT ["python3"]
# EXPOSE 3000
# CMD ["manage.py", "runserver", "0.0.0.0:3000"]
