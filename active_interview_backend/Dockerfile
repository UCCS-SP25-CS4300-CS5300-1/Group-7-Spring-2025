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

# # Install dependencies required for Chrome and ChromeDriver
# RUN apt-get update && apt-get install -y \
#     wget \
#     unzip \
#     xvfb \
#     libxi6 \
#     libgconf-2-4 \
#     libnss3 \
#     libxss1 \
#     libappindicator1 \
#     libindicator7 \
#     fonts-liberation \
#  && rm -rf /var/lib/apt/lists/*

# # Optionally, install Google Chrome if needed for your tests
# RUN wget -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#  && apt-get update \
#  && apt-get install -y ./google-chrome.deb \
#  && rm google-chrome.deb
# Set ChromeDriver version (adjust to the appropriate version for Chrome 135)
ENV CHROME_VERSION=135.0.7049.52

# Optionally, install Google Chrome if needed for your tests
RUN wget -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
 && apt-get update \
 && apt-get install -y ./google-chrome.deb \
 && rm google-chrome.deb

# # Set ChromeDriver version (adjust as needed)
ENV CHROMEDRIVER_VERSION=135.0.7049.52
# ENV CHROMEDRIVER_VERSION=114.0.5735.90

# Download and install ChromeDriver
RUN wget -O chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip \
 && unzip chromedriver.zip \
 && mv chromedriver /usr/local/bin/chromedriver \
 && chmod +x /usr/local/bin/chromedriver \
 && rm chromedriver.zip

# Setup django
# RUN python manage.py collectstatic --noinput
# RUN python manage.py makemigrations
# RUN python manage.py migrate

# make user
RUN useradd testinguser

RUN chmod +x ./start.sh

EXPOSE 443 
EXPOSE 8000

# Run startup script
CMD ["bash", "./start.sh"]
