FROM python:3.9

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

# Install app
COPY . /app

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# # Set ChromeDriver version (adjust to the appropriate version for Chrome 135)
# ENV CHROME_VERSION=135.0.7049.52-1

# # Optionally, install Google Chrome if needed for your tests
# RUN wget -O google-chrome.deb https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}_amd64.deb \
#  && apt-get update \
#  && apt-get install -y ./google-chrome.deb \
#  && rm google-chrome.deb

# # # Set ChromeDriver version (adjust as needed)
# ENV CHROMEDRIVER_VERSION=135.0.7049.52

# # Download and install ChromeDriver
# RUN wget -O chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip \
#  && unzip chromedriver.zip \
#  && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
#  && chmod +x /usr/local/bin/chromedriver \
#  && rm chromedriver.zip

# Setup django
# RUN python manage.py collectstatic --noinput
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# # make user
# RUN useradd testinguser

RUN chmod +x ./start.sh

EXPOSE 443 
EXPOSE 8000

# Run startup script
CMD ["bash", "./start.sh"]
