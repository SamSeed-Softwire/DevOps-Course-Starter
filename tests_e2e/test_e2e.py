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