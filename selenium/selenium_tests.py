import unittest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        requests.get('http://services:8000/selenium')
        self.driver = webdriver.Remote(
           command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME)
        self.man_signup()
        self.user_signup()

    def login(self, is_man, user, pw):
        driver = self.driver
        driver.get('http://frontend:8000')
        if is_man:
            check = driver.find_element_by_id('id_is_man')
            check.click()
        driver.find_element_by_id('id_username').send_keys(user)
        password = driver.find_element_by_id('id_password')
        password.send_keys(pw)
        password.send_keys(Keys.RETURN)
        return driver.current_url == 'http://frontend:8000/home'

    def user_signup(self):
        driver = self.driver
        driver.get('http://frontend:8000/create-user')
        driver.find_element_by_id('id_username').send_keys('selenium')
        driver.find_element_by_id('id_password').send_keys('selenium')
        driver.find_element_by_id('id_email').send_keys('selenium@email.com')
        driver.find_element_by_id('id_phone_number').send_keys('1234567890')
        driver.find_element_by_id('id_first_name').send_keys('selenium')
        driver.find_element_by_id('id_last_name').send_keys('tests')
        driver.find_element_by_name('createUser').submit()

    def man_signup(self):
        driver = self.driver
        driver.get('http://frontend:8000/create-manufacturer')
        driver.find_element_by_id('id_man_name').send_keys('selenium_man')
        driver.find_element_by_id('id_password').send_keys('selenium_man')
        driver.find_element_by_id('id_email').send_keys('selenium_man@email.com')
        driver.find_element_by_id('id_phone_number').send_keys('098764321')
        driver.find_element_by_id('id_web_url').send_keys('selenium.com')
        driver.find_element_by_name('createMan').submit()

    def relevant_search(self, query):
        driver = self.driver
        driver.find_element_by_name('query').send_keys(query)
        driver.find_element_by_name('searchButton').click()
        title = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'resultTitle')))
        print('Clicked relevant search, current url:', driver.current_url)
        return title


    def top_search(self, query):
        driver = self.driver
        driver.find_element_by_name('query').send_keys(query)
        driver.find_element_by_name('popular').click()
        driver.find_element_by_name('searchButton').click()
        title = WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'resultTitle')))
        print('Clicked relevant search, current url:', driver.current_url)
        return title

    def create_listing(self):
        driver = self.driver
        driver.get('http://frontend:8000/create-listing')
        driver.find_element_by_id('id_name').send_keys('selenium')
        driver.find_element_by_id('id_type').send_keys('selenium')
        driver.find_element_by_id('id_description').send_keys('selenium')
        driver.find_element_by_id('id_price').send_keys('123')
        driver.find_element_by_id('id_warranty').send_keys('selenium')
        driver.find_element_by_id('id_img_url').send_keys('selenium')
        driver.find_element_by_name('createListing').submit()

    def test_user_login_error(self):
        assert not self.login(False, 'wrong', 'wrong')

    def test_man_login_error(self):
        assert not self.login(True, 'wrong', 'wrong')

    def test_create_user(self):
        assert self.login(False, 'selenium', 'selenium')

    def test_create_man(self):
        assert self.login(True, 'selenium_man', 'selenium_man')

    def test_search_relevant(self):
        if not self.login(False, 'selenium', 'selenium'):
            assert False
        self.driver.implicitly_wait(10)
        result_title = self.relevant_search('corsair')
        assert result_title.text == 'Search Results'

    def test_search_top(self):
        if not self.login(False, 'selenium', 'selenium'):
            assert False
        self.driver.implicitly_wait(10)
        result_title = self.top_search('corsair')
        assert result_title.text == 'Search Results'

    def test_search_relevant_none(self):
        if not self.login(False, 'selenium', 'selenium'):
            assert False
        self.driver.implicitly_wait(10)
        result_title = self.relevant_search('pear')
        assert result_title.text == 'No Results Found'

    def test_search_top_none(self):
        if not self.login(False, 'selenium', 'selenium'):
            assert False
        self.driver.implicitly_wait(10)
        result_title = self.top_search('pear')
        assert result_title.text == 'No Results Found'

    def test_product_details(self):
        self.login(True, 'selenium_man', 'selenium_man')
        self.driver.implicitly_wait(10)
        self.create_listing()
        assert self.driver.find_element_by_name('prodName').text == 'selenium'

    def test_new_product_relevant_search(self):
        self.login(True, 'selenium_man', 'selenium_man')
        self.driver.implicitly_wait(10)
        self.create_listing()
        self.driver.implicitly_wait(10)
        self.driver.get('http://frontend:8000/home')
        result_title = self.relevant_search('selenium')
        assert result_title.text == 'Search Results'

    def test_new_product_top_search(self):
        self.login(True, 'selenium_man', 'selenium_man')
        self.driver.implicitly_wait(10)
        self.create_listing()
        self.driver.implicitly_wait(10)
        self.driver.get('http://frontend:8000/home')
        result_title = self.top_search('selenium')
        assert result_title.text == 'Search Results'

    def tearDown(self):
        requests.get('http://services:8000/selenium')
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
