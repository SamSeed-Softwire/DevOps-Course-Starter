from dotenv import load_dotenv, find_dotenv
import os
import pytest
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread

import app.app as app


trello_test_organization_id = '5ffd97c7f80c3b13867165e0'

@pytest.fixture(scope='module')
def test_app():

    # Load the environment variables.
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # Create the new board & update the board id environment variable.
    board_id = create_trello_board('test_board')
    os.environ['BOARD_ID'] = board_id


    # Create app instance using newly created board.
    application  = app.create_app()

    # Start the app in its own thread.
    thread = Thread(target = lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear down.
    thread.join(1)
    delete_trello_board(board_id)


def create_trello_board(name):
    create_board_params = {'key': os.environ.get('AUTH_PARAMS_KEY'), 'token': os.environ.get('AUTH_PARAMS_TOKEN'), 'name': name, 'idOrganization': trello_test_organization_id}
    response = requests.post(f'https://api.trello.com/1/boards', params = create_board_params).json()
    return response['id']

def delete_trello_board(id):
    delete_board_params = {'key': os.environ.get('AUTH_PARAMS_KEY'), 'token': os.environ.get('AUTH_PARAMS_TOKEN')}
    response = requests.delete(f'https://api.trello.com/1/boards/{id}', params = delete_board_params).json()
    return response


@pytest.fixture(scope='module')
def driver():
    with webdriver.Firefox() as driver:
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


    # Check no items in todo list at start.
    assert count_items('todo') == 0

    # Create new item.
    item_name = 'Test item'
    new_item_form = driver.find_element(By.ID, 'item_name')
    new_item_form.send_keys(item_name)
    new_item_form.submit()
    driver.implicitly_wait(10)

    # Check there's now 1 item in the todo list.
    assert count_items('todo') == 1

    # Check the new item has the correct name.
    todo_items = find_items('todo')
    full_item_name = todo_items[0].text

    full_item_name_root_pattern = r'.+\s-\s'
    full_item_name_pattern = full_item_name_root_pattern + item_name
    name_matcher = re.compile(full_item_name_pattern)
    match_result = name_matcher.fullmatch(full_item_name)

    assert bool(match_result) == True