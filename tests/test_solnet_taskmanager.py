"""
Test module for SolNet Task Manager UI
"""

from pages.login import LoginPage
from pages.home import HomePage


def login_to_taskmanager(browser):
    login_page = LoginPage(browser)

    # Given the login page is displayed
    login_page.load()

    # And username and password is keyed-in
    login_page.set_login()

    # When the login button is clicked
    login_page.hit_login()


def test_login_taskmanager(browser):
    home_page = HomePage(browser)
    login_to_taskmanager(browser)

    # Then the homepage is displayed
    assert '/nav/home' in home_page.check_current_url()
    assert 'My day' == home_page.get_active_side_nav()


def test_add_remove_task(browser):
    home_page = HomePage(browser)
    login_to_taskmanager(browser)

    # When a task is added in the home page
    home_page.add_a_task('new task', 'description', 'today')

    # Then a task should be listed
    assert home_page.is_task_in_list('new task')

    # When the task is removed in the home page
    home_page.remove_task('new task')

    # The task should no longer be listed
    assert not(home_page.is_task_in_list('new task'))


def test_mark_unmark_task(browser):
    home_page = HomePage(browser)
    login_to_taskmanager(browser)

    # When a task is added in the home page
    home_page.add_a_task('marking task', 'description', 'today')

    # When a task is marked as completed
    home_page.complete_task('marking task')

    # Then the task is updated to completed
    assert home_page.is_checkbox_checked('marking task')

    # When a task is unmarked
    home_page.complete_task('marking task', complete=False)

    # Then the task is updated to marked and NOT completed
    assert not home_page.is_checkbox_checked('marking task')


def test_navigate_all_tasks_and_favorites(browser):
    home_page = HomePage(browser)
    login_to_taskmanager(browser)

    # When a couple of tasks are added in the home page
    home_page.add_a_task('important task', 'description', 'today', True)
    home_page.add_a_task('less important task', 'description', 'today')

    # When user navigates to all tasks
    home_page.navigate_to('all-tasks')

    # Then the homepage is displayed
    assert '/nav/all-tasks' in home_page.check_current_url()
    assert 'All Tasks' == home_page.get_active_side_nav()
    assert home_page.count_task_list() >= 2

    # When user navigates to all tasks
    home_page.navigate_to('important-tasks')

    # Then the homepage is displayed
    assert '/nav/important-tasks' in home_page.check_current_url()
    assert 'Important Tasks' == home_page.get_active_side_nav()
    assert home_page.count_task_list() >= 1