import unittest
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

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
        driver.implicitly_wait(7)
        driver.find_element_by_name('searchButton').click()

    def top_search(self, query):
        driver = self.driver
        driver.find_element_by_name('query').send_keys(query)
        driver.find_element_by_name('popular').click()
        driver.implicitly_wait(7)
        driver.find_element_by_name('searchButton').click()

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
        self.login(False, 'selenium', 'selenium')
        self.relevant_search('corsair')
        self.driver.implicitly_wait(7)
        result_title = self.driver.find_element_by_name('resultTitle')
        assert result_title.text == 'Search Results'

    def test_search_top(self):
        self.login(False, 'selenium', 'selenium')
        self.top_search('corsair')
        self.driver.implicitly_wait(7)
        result_title = self.driver.find_element_by_name('resultTitle')
        assert result_title.text == 'Search Results'

    def test_search_relevant_none(self):
        self.login(False, 'selenium', 'selenium')
        self.relevant_search('notgonnafindthisnosir')
        self.driver.implicitly_wait(7)
        result_title = self.driver.find_element_by_name('resultTitle')
        assert result_title.text == 'No Results Found'

    def test_search_top_none(self):
        self.login(False, 'selenium', 'selenium')
        self.top_search('notgonnafindthisnosir')
        self.driver.implicitly_wait(7)
        result_title = self.driver.find_element_by_name('resultTitle')
        assert result_title.text == 'No Results Found'

    def test_product_details(self):
        self.login(True, 'selenium_man', 'selenium_man')
        self.create_listing()
        assert self.driver.find_element_by_name('prodName').text == 'selenium'

    def test_new_product_relevant_search(self):
        self.login(True, 'selenium_man', 'selenium_man')
        self.create_listing()
        self.driver.get('http://frontend:8000/home')
        self.relevant_search('selenium')
        self.driver.implicitly_wait(7)
        assert self.driver.find_element_by_name('resultTitle').text == 'Search Results'

    def test_new_product_top_search(self):
        self.login(True, 'selenium_man', 'selenium_man')
        self.create_listing()
        self.driver.get('http://frontend:8000/home')
        self.top_search('selenium')
        self.driver.implicitly_wait(7)
        assert self.driver.find_element_by_name('resultTitle').text == 'Search Results'
        
    def tearDown(self):
        requests.get('http://services:8000/selenium')
        self.driver.close()

if __name__ == "__main__":
    # time.sleep(30)
    unittest.main()
