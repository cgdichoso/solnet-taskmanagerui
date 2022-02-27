"""
Login page class module
"""

from selenium.webdriver.common.by import By


class LoginPage:
    USERNAME_FIELD = (By.CSS_SELECTOR, 'input[type="email"]')
    PASSWORD_FIELD = (By.CSS_SELECTOR, 'input[type="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, 'button.login-field')

    def __init__(self, browser):
        self.browser = browser

    def load(self, url='http://localhost:4200/login'):
        self.browser.get(url)

    def set_login(self, user='user', password='user'):
        self.browser.find_element(*self.USERNAME_FIELD).send_keys(user)
        self.browser.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def hit_login(self):
        self.browser.find_element(*self.LOGIN_BUTTON).click()
