"""
Home page class module
"""

from selenium.webdriver.common.by import By
from datetime import datetime


class HomePage:
    ACTIVE_SIDE_NAV = (By.CSS_SELECTOR, 'a[class*="selected"]')
    TASK_TITLE_FIELD = (By.CSS_SELECTOR, 'input[name="taskTitle"]')
    TASK_DESCRIPTION_FIELD = (By.CSS_SELECTOR, 'input[name="taskDesc"]')
    CALENDAR_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Open calendar"]')
    SELECT_DATE_BUTTON = (By.CSS_SELECTOR, 'button[aria-label="Choose month and year"]')
    DATE_PICK_TODAY = (By.CSS_SELECTOR, 'div[class*="mat-calendar-body-today"]')
    IMPORTANT_LABEL = (By.CSS_SELECTOR, 'label[for="mat-checkbox-1-input"]')
    IMPORTANT_CHECKBOX = (By.CSS_SELECTOR, 'mat-checkbox[class*="home-checkbox"]')
    ADD_TASK_BUTTON = (By.CSS_SELECTOR, 'button[id="addTask"]')
    TASK_ITEMS = (By.CSS_SELECTOR, 'mat-card[class*="task-card"]')
    REMOVE_TASK_ICONS = (By.CSS_SELECTOR, 'mat-icon[class*="remove-icon"]')
    COMPLETE_CHECKBOXES = (By.CSS_SELECTOR, 'mat-checkbox[class*="complete-checkbox"]')
    HOME_NAV = (By.CSS_SELECTOR, 'a[ng-reflect-router-link="home"]')
    ALL_TASKS_NAV = (By.CSS_SELECTOR, 'a[ng-reflect-router-link="all-tasks"]')
    IMPORTANT_TASKS_NAV = (By.CSS_SELECTOR, 'a[ng-reflect-router-link="important-tasks"]')

    def __init__(self, browser):
        self.browser = browser

    def check_current_url(self):
        return self.browser.current_url

    def get_active_side_nav(self):
        side_nav_list = {'/nav/home': 'My day', '/nav/all-tasks': 'All Tasks',
                         '/nav/important-tasks': 'Important Tasks'}
        href = self.browser.find_element(*self.ACTIVE_SIDE_NAV).get_property('href')
        return side_nav_list[href[href.find('/nav'):]]

    def add_a_task(self, title, description, date, important=False):
        if important:
            self.browser.find_element(*self.IMPORTANT_LABEL).click()
            self.update_to_important()
        self.browser.find_element(*self.TASK_TITLE_FIELD).send_keys(title)
        self.browser.find_element(*self.TASK_DESCRIPTION_FIELD).send_keys(description)
        self.browser.find_element(*self.CALENDAR_BUTTON).click()
        self.select_date(date)
        self.browser.find_element(*self.ADD_TASK_BUTTON).click()

    def select_date(self, date):
        if isinstance(date, str) and date.casefold() == 'today':
            self.browser.find_element(*self.DATE_PICK_TODAY).click()
        else:
            try:
                data_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                print('\nERROR: Incorrect string format')

            year = (By.XPATH, '//div[text()="' + data_date.strftime('%Y') + '"]')
            month = (By.XPATH, '//div[text()="' + data_date.strftime('%b').upper() + '"]')
            day = (By.CSS_SELECTOR, 'td[aria-label="' + data_date.strftime('%B %d, %Y') + '"]')
            self.browser.find_element(*self.SELECT_DATE_BUTTON).click()
            self.browser.find_element(*year).click()
            self.browser.find_element(*month).click()
            self.browser.find_element(*day).click()

    def update_to_important(self):
        important = self.browser.find_element(*self.IMPORTANT_CHECKBOX)
        while not('mat-checkbox-checked' in important.get_attribute('class')):
            important.click()

    def get_task_list(self):
        return self.browser.find_elements(*self.TASK_ITEMS)

    def get_task_index(self, text_value):
        index = 0
        for task_item in self.get_task_list():
            if text_value in task_item.text:
                break
            else:
                index += 1
        return index

    def is_task_in_list(self, text_value):
        task_found = False
        for task_item in self.get_task_list():
            if text_value in task_item.text:
                task_found = True
        return task_found

    def remove_task(self, text_value):
        remove_icons = self.browser.find_elements(*self.REMOVE_TASK_ICONS)
        remove_icons[self.get_task_index(text_value)].click()

    def complete_task(self, text_value, complete=True):
        checkbox = self.browser.find_elements(*self.COMPLETE_CHECKBOXES)[self.get_task_index(text_value)]
        if complete:
            while not(self.is_checkbox_checked(text_value)):
                checkbox.click()
        else:
            while self.is_checkbox_checked(text_value):
                checkbox.click()

    def is_checkbox_checked(self, text_value):
        checkbox = self.browser.find_elements(*self.COMPLETE_CHECKBOXES)[self.get_task_index(text_value)]
        return 'mat-checkbox-checked' in checkbox.get_attribute('class')

    def navigate_to(self, menu):
        if menu == 'home':
            self.browser.find_element(*self.HOME_NAV).click()
        elif menu == 'all-tasks':
            self.browser.find_element(*self.ALL_TASKS_NAV).click()
        elif menu == 'important-tasks':
            self.browser.find_element(*self.IMPORTANT_TASKS_NAV).click()
        else:
            print(f'\nERROR: {menu} is not a valid navigation menu')

    def count_task_list(self):
        return len(self.get_task_list())