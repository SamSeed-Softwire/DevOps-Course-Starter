from dotenv import load_dotenv, find_dotenv
import requests
import os
import pytest
from unittest.mock import patch, Mock

import app.app as app
from tests.mock_response import MockResponse


@pytest.fixture
def client():
    # Use our test integration config instead of the 'real' version.
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

@pytest.fixture
def mock_response(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_get_data)

def mock_get_data(url, *args, **kwargs):
    board_id = os.environ.get('BOARD_ID')

    if url == f'https://api.trello.com/1/boards/{board_id}/lists':
        samples_trello_lists_response = [
            {'id': '5efc77d5ce13a25c8b6bf9c1', 'name': 'To Do', 'closed': False, 'pos': 65535, 'softLimit': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'subscribed': False}, {'id': '5efc77d79bdbfe8a63d420c2', 'name': 'Doing', 'closed': False, 'pos': 131071, 'softLimit': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'subscribed': False}, {'id': '5efc77d85e465d1006d941b5', 'name': 'Done', 'closed': False, 'pos': 196607, 'softLimit': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'subscribed': False}
        ]
        return MockResponse(samples_trello_lists_response)
    if url == f'https://api.trello.com/1/boards/{board_id}/cards':
        samples_trello_cards_response = [
            {'id': '5ff99f06a123e77d1211c9fd', 'checkItemStates': None, 'closed': False, 'dateLastActivity': '2021-01-09T12:18:28.900Z', 'desc': '', 'descData': None, 'dueReminder': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'idList': '5efc77d79bdbfe8a63d420c2', 
            'idMembersVoted': [], 'idShort': 121, 'idAttachmentCover': None, 'idLabels': [], 'manualCoverAttachment': False, 'name': "Do an hour's work on apprenticeship", 'pos': 16384, 'shortLink': '8Px1eNgP', 'isTemplate': False, 'cardRole': None, 'badges': {'attachmentsByType': {'trello': {'board': 0, 'card': 0}}, 'location': False, 'votes': 0, 'viewingMemberVoted': False, 'subscribed': 
            False, 'fogbugz': '', 'checkItems': 0, 'checkItemsChecked': 0, 'checkItemsEarliestDue': None, 'comments': 0, 'attachments': 0, 
            'description': False, 'due': None, 'dueComplete': False, 'start': None}, 'dueComplete': False, 'due': None, 'idChecklists': [], 'idMembers': [], 'labels': [], 'shortUrl': 'https://trello.com/c/8Px1eNgP', 'start': None, 'subscribed': False, 'url': 'https://trello.com/c/8Px1eNgP/121-do-an-hours-work-on-apprenticeship', 'cover': {'idAttachment': None, 'color': None, 'idUploadedBackground': None, 'size': 'normal', 'brightness': 'light'}}
        ]
        return MockResponse(samples_trello_cards_response)

    return None

def test_index_page(mock_response, client):
    response = client.get('/')