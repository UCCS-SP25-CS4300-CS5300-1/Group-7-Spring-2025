from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time


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
        chrome_options.add_argument("--use-fake-ui-for-media-stream")
        chrome_options.add_argument("--use-fake-device-for-media-stream") 

        driver = webdriver.Chrome(options=chrome_options)

        return driver

    # if testing in local non-container environment:
    else:
        driver = webdriver.Chrome()

        return driver


def authenticate(test_case, driver):
    # Retrieve or generate E2E user
    user = None
    if not User.objects.filter(username='E2ETester').exists():
        user = User.objects.create_user(
            username="E2ETester",
            password="curlylift77"
        )
    else:
        user = User.objects.get(username='E2ETester')

    # log in on client object
    test_case.user = user
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


def loginSim():
    user = None
    if not User.objects.filter(username = 'test').exists():
        user = User.objects.create_user(
            username="test", 
            password="!QAZxsw2"
        )
    driver = getEnvDriver()
    if settings.PROD == False:
        driver.get('http://127.0.0.1:8000/accounts/login/')
    else:
        driver.get('https://app.activeinterviewservice.me/accounts/login/')
    user_name = driver.find_element(by="id", value="id_username")
    user_password = driver.find_element(by="id", value='id_password')
    submit = driver.find_element(by="id", value="submit")

    user_name.send_keys('test')
    user_password.send_keys('!QAZxsw2')
    submit.send_keys(Keys.RETURN)
    return driver


class TestDriver(StaticLiveServerTestCase):
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

    #From here on you may need to configure the user test to match with the
    #password
    # #As well as match it with the chat number, because that can cause errors
    # #on local machine
    # def testLogin(self):
    #     driver = loginSim()
    #     driver.get('http://127.0.0.1:8000/')
    #     assert len(driver.find_elements(By.ID, "login-button")) == 0

    # def testText2Speech(self):
    #     driver = loginSim()
    #     if settings.PROD == False:
    #         driver.get('http://127.0.0.1:8000/chat/1/')
    #     else:
    #         driver.get('https://app.activeinterviewservice.me/chat/26/')

    #     ai_message = driver.find_element(By.ID, "ai_message").text
    #     text2speech_button = driver.find_element(By.ID, "text2speech_button")
    #     text2speech_button.click()
    #     #print(ai_message)
    #     #Can use anything like the entire message in assert, just did Craig
    #     #because I know for my resume (test) it will say my name
    #     assert "Craig" in ai_message

    # def testCreateChat(self):
    #     driver = loginSim()
    #     if settings.PROD == False:
    #         driver.get('https://127.0.0.1:8000/chat/create')
    #     else:
    #         driver.get('https://app.activeinterviewservice.me/chat/create')
    #     title = driver.find_element(By.ID, "id_title")
    #     title.send_keys('test')
    #     job = driver.find_element(By.ID, "id_listing_choice")
    #     select = Select(job)
    #     select.select_by_index(1)
    #     resume = driver.find_element(By.ID, "id_resume_choice")
    #     select = Select(resume)
    #     select.select_by_index(1)
    #     submit = driver.find_element(By.ID, "create-form-button")
    #     submit.click()
    #     ai_message = driver.find_element(By.ID, "ai_message").text
    #     assert "Craig" in ai_message
















