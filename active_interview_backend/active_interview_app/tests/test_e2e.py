from django.conf import settings
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# === Helper Fucntions ===
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


def generateExampleUser():
    user = User.objects.create_user(
        username="example", 
        password="goodray31"
    )

    return user


def authenticate(test_case, driver):
    # Generate user and log in on client object
    test_case.user = generateExampleUser()
    test_case.client.force_login(test_case.user)

    # Get session cookie from Django test client
    session_cookie = test_case.client.cookies['sessionid']
    
    # Navigate Selenium to the live server domain to set the cookie
    driver.get(test_case.live_server_url)
    
    # Add the session cookie to Selenium
    driver.add_cookie({
        'name': 'sessionid',
        'value': session_cookie.value,
        'path': '/',
        'domain': 'localhost',  # Adjust if needed for your live_server_url
    })

    # Refresh the page after adding the cookie
    driver.get(test_case.live_server_url)



class TestDriver(LiveServerTestCase):
    def testE2EDriver(self):
        # Init chrome driver
        driver = getEnvDriver()

        # Stop chrome driver
        driver.quit()

    
    def testE2EAuth(self):
        # Init chrome driver
        driver = getEnvDriver()
        
        authenticate(self, driver)

        # Assert that uesr is logged in through user authentication buttons
        assert len(driver.find_elements(By.ID, "profile-dropdown")) > 0
        assert len(driver.find_elements(By.ID, "login-button")) == 0

        # Stop chrome driver
        driver.quit()
