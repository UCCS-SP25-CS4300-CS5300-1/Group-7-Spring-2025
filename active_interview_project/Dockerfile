FROM python:3

WORKDIR /app

# Install requirements
COPY web-requirements.txt ./
RUN pip install -r web-requirements.txt --no-cache-dir

# Install app and run
COPY . /app
ENTRYPOINT ["python3"]
EXPOSE 3000
CMD ["manage.py", "runserver", "0.0.0.0:3000"]
