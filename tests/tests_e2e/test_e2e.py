from dotenv import load_dotenv, find_dotenv
import os
import pymongo
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from webdriver_manager.chrome import ChromeDriverManager

import application.app as app
from application.user import User


@pytest.fixture(scope='module')
def test_app():

    # Load the environment variables.
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # Override environment variables.
    temp_db = "temp_db"
    os.environ['COSMOS_TODO_APP_DATABASE'] = temp_db
    os.environ['LOGIN_DISABLED'] = "False"

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
    COSMOS_USERNAME = os.environ.get('COSMOS_USERNAME')
    COSMOS_PASSWORD = os.environ.get('COSMOS_PASSWORD')
    COSMOS_HOST = os.environ.get('COSMOS_HOST')
    COSMOS_PORT = os.environ.get('COSMOS_PORT')
    client = pymongo.MongoClient(f"""mongodb://{COSMOS_USERNAME}:{COSMOS_PASSWORD}@{COSMOS_HOST}:{COSMOS_PORT}/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@{COSMOS_USERNAME}@""")
    client.drop_database(db)

@pytest.fixture(scope='module')
def driver():
    chrome_driver_path = ChromeDriverManager().install()
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    with webdriver.Chrome(chrome_driver_path, options=opts) as driver:
        yield driver

# Explictly set the user role when making requests to the Flask app. This may be useful if I introduce test journeys for other roles e.g. reader, admin.
@pytest.fixture(scope='module')
def writer_user(test_app):
    @test_app.login_manager.request_loader
    def load_user_from_request(request):
        writer_user_id = "0"
        return User(writer_user_id, "writer")

# TODO: Add more journeys.

def test_task_journey(driver, test_app, writer_user):

    driver.get('http://localhost:5000/')

    assert driver.title == 'To-Do App'

    def find_items(list):
        items = driver.find_elements(By.XPATH, f'''//div[@name='{list}']//ul//li''')
        return items

    def count_items(list):
        items = find_items(list)
        return len(items)

    def check_item_name_and_count(list):

        # Check there's now 1 item in the specified list
        assert count_items(list) == 1

        # Check the new item has the correct name.
        list_items = find_items(list)
        list_item_name = list_items[0].text
        assert list_item_name == initial_item_name


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