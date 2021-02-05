from dotenv import load_dotenv, find_dotenv
import os
import pymongo
import pytest
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from webdriver_manager.chrome import ChromeDriverManager

import application.app as app


@pytest.fixture(scope='module')
def test_app():

    # Load the environment variables.
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    temp_db = "temp_db"
    os.environ['MONGO_TODO_APP_DATABASE'] = temp_db

    # Create app instance using newly created board.
    application  = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target = lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear down.
    thread.join(1)
    drop_database(temp_db)

def drop_database(db):
    MONGO_USER_NAME = os.environ.get('MONGO_USER_NAME')
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    MONGO_HOST = os.environ.get('MONGO_HOST')
    client = pymongo.MongoClient(f"mongodb+srv://{MONGO_USER_NAME}:{MONGO_PASSWORD}@{MONGO_HOST}/?retryWrites=true&w=majority")
    client.drop_database(db)

@pytest.fixture(scope='module')
def driver():
    chrome_driver_path = ChromeDriverManager().install()
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    with webdriver.Chrome(chrome_driver_path, options=opts) as driver:
        yield driver

def test_task_journey(driver, test_app):
    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

    def find_items(list):
        items = driver.find_elements(By.XPATH, f'''//div[@name='{list}']//ul//li''')
        return items

    def count_items(list):
        items = find_items(list)
        return len(items)

    def check_item_name(actual_name, expected_name_without_root):
        root_pattern = r'.+\s-\s'
        full_name_pattern = root_pattern + expected_name_without_root
        name_matcher = re.compile(full_name_pattern)
        match_result = name_matcher.fullmatch(actual_name)
        return bool(match_result)

    def check_item_name_and_count(list):

        # Check there's now 1 item in the specified list
        assert count_items(list) == 1

        # Check the new item has the correct name.
        list_items = find_items(list)
        list_item_name = list_items[0].text
        assert check_item_name(list_item_name, initial_item_name) == True

    # Check no items in lists at start.
    assert count_items('todo') == 0
    assert count_items('doing') == 0
    assert count_items('done') == 0

    # Create new item.
    initial_item_name = 'Test item'
    new_item_form = driver.find_element(By.XPATH, '''//form[@action='/add-item']//input[@name='item_name']''')
    new_item_form.send_keys(initial_item_name)
    new_item_form.submit()
    driver.implicitly_wait(10)

    # Check item is now in the todo list as expected.
    check_item_name_and_count('todo')

    # Start the item.
    start_item_button = driver.find_element(By.XPATH, '''//div[@name='todo']//ul//li//input[@value='Start']''')
    start_item_button.click()

    # Check item is now in the doing list as expected.
    check_item_name_and_count('doing')

    # Complete the item.
    complete_item_button = driver.find_element(By.XPATH, '''//div[@name='doing']//ul//li//input[@value='Complete']''')
    complete_item_button.click()

    # Check item is now in the done list as expected.
    check_item_name_and_count('done')

    # Uncomplete the item.
    uncomplete_item_button = driver.find_element(By.XPATH, '''//div[@name='done']//ul//li//input[@value='Uncomplete']''')
    uncomplete_item_button.click()

    # Check item is now back in the doing list as expected.
    check_item_name_and_count('doing')