from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Make a context-dependent driver for the environment
def getEnvDriver():
    # if testing in production container environment:
    if settings.PROD:
        # Configure chrome options
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chrome_options)

        return driver
    
    # if testing in local non-container environment:
    else:
        driver = webdriver.Chrome()

        return driver



class TestHost(LiveServerTestCase):
    def test0010(self):
        # Init chrome driver
        driver = getEnvDriver()

        driver.quit()
