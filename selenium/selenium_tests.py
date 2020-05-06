import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
           command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME)

    def test_login_error(self):
        driver = self.driver
        driver.get('http://frontend:8000')
        username = driver.find_element_by_id('id_username')
        username.send_keys('wrong')
        password = driver.find_element_by_id('id_password')
        password.send_keys('wrong')
        password.send_keys(Keys.RETURN)
        error = driver.find_element_by_name('error')
        assert error.is_displayed()

    def test_create_user(self):
        driver = self.driver
        driver.get('http://frontend:8000/create-user')
        driver.implicitly_wait(10)
        username = driver.find_element_by_id('id_username')
        username.send_keys('selenium')
        password = driver.find_element_by_id('id_password')
        password.send_keys('selenium')
        email = driver.find_element_by_id('id_email')
        email.send_keys('selenium@email.com')
        phone = driver.find_element_by_id('id_phone_number')
        phone.send_keys('1234567890')
        first_name = driver.find_element_by_id('id_first_name')
        first_name.send_keys('selenium')
        last_name = driver.find_element_by_id('id_last_name')
        last_name.send_keys('tests')
        submit = driver.find_element_by_name('createUser')
        submit.submit()
        time.sleep(5)
        print('current URL:', driver.current_url)
        assert driver.current_url == 'http://frontend:8000'

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    time.sleep(15)
    unittest.main()
