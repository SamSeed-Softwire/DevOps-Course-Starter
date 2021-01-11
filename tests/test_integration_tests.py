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
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = app.create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

@pytest.fixture
def mock_response(monkeypatch):
    monkeypatch.setattr(requests, "get", mock_get)

def mock_get(url, *args, **kwargs):
    board_id = os.environ.get('BOARD_ID')

    if url == f'https://api.trello.com/1/boards/{board_id}/lists':
        samples_trello_lists_response = [
            {'id': '5efc77d5ce13a25c8b6bf9c1', 'name': 'To Do', 'closed': False, 'pos': 65535, 'softLimit': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'subscribed': False},
            {'id': '5efc77d79bdbfe8a63d420c2', 'name': 'Doing', 'closed': False, 'pos': 131071, 'softLimit': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'subscribed': False},
            {'id': '5efc77d85e465d1006d941b5', 'name': 'Done', 'closed': False, 'pos': 196607, 'softLimit': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'subscribed': False}
        ]
        return MockResponse(samples_trello_lists_response)

    if url == f'https://api.trello.com/1/boards/{board_id}/cards':
        samples_trello_cards_response = [
                {'id': '5ffc57387b09283ffcbad149', 'checkItemStates': None, 'closed': False, 'dateLastActivity': '2021-01-11T13:48:40.748Z', 'desc': '', 'descData': None, 'dueReminder': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'idList': '5efc77d5ce13a25c8b6bf9c1', 'idMembersVoted': [], 'idShort': 122, 'idAttachmentCover': None, 'idLabels': [], 'manualCoverAttachment': False, 'name': 'ItemInToDo', 'pos': 65535, 'shortLink': 'BqFhR7rv', 'isTemplate': False, 'cardRole': None, 'badges': {'attachmentsByType': {'trello': {'board': 0, 'card': 0}}, 'location': False, 'votes': 0, 'viewingMemberVoted': False, 'subscribed': False, 'fogbugz': '', 'checkItems': 0, 'checkItemsChecked': 0, 'checkItemsEarliestDue': None, 'comments': 0, 'attachments': 0, 'description': False, 'due': None, 'dueComplete': False, 'start': None}, 'dueComplete': False, 'due': None, 'idChecklists': [], 'idMembers': [], 'labels': [], 'shortUrl': 'https://trello.com/c/BqFhR7rv', 'start': None, 'subscribed': False, 'url': 'https://trello.com/c/BqFhR7rv/122-itemintodo', 'cover': {'idAttachment': None, 'color': None, 'idUploadedBackground': None, 'size': 'normal', 'brightness': 'light'}},
                {'id': '5ffc57409465f37f024185c0', 'checkItemStates': None, 'closed': False, 'dateLastActivity': '2021-01-11T13:48:53.020Z', 'desc': '', 'descData': None, 'dueReminder': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'idList': '5efc77d79bdbfe8a63d420c2', 'idMembersVoted': [], 'idShort': 123, 'idAttachmentCover': None, 'idLabels': [], 'manualCoverAttachment': False, 'name': 'ItemInDoing', 'pos': 65535, 'shortLink': 'PnFSuhAg', 'isTemplate': False, 'cardRole': None, 'badges': {'attachmentsByType': {'trello': {'board': 0, 'card': 0}}, 'location': False, 'votes': 0, 'viewingMemberVoted': False, 'subscribed': False, 'fogbugz': '', 'checkItems': 0, 'checkItemsChecked': 0, 'checkItemsEarliestDue': None, 'comments': 0, 'attachments': 0, 'description': False, 'due': None, 'dueComplete': False, 'start': None}, 'dueComplete': False, 'due': None, 'idChecklists': [], 'idMembers': [], 'labels': [], 'shortUrl': 'https://trello.com/c/PnFSuhAg', 'start': None, 'subscribed': False, 'url': 'https://trello.com/c/PnFSuhAg/123-itemindoing', 'cover': {'idAttachment': None, 'color': None, 'idUploadedBackground': None, 'size': 'normal', 'brightness': 'light'}},
                {'id': '5ffc57487f2b918eb98eb0bf', 'checkItemStates': None, 'closed': False, 'dateLastActivity': '2021-01-11T13:48:56.845Z', 'desc': '', 'descData': None, 'dueReminder': None, 'idBoard': '5efc773fd08d053db4ef3c18', 'idList': '5efc77d85e465d1006d941b5', 'idMembersVoted': [], 'idShort': 124, 'idAttachmentCover': None, 'idLabels': [], 'manualCoverAttachment': False, 'name': 'ItemInDone', 'pos': 65535, 'shortLink': 'RPlcZanE', 'isTemplate': False, 'cardRole': None, 'badges': {'attachmentsByType': {'trello': {'board': 0, 'card': 0}}, 'location': False, 'votes': 0, 'viewingMemberVoted': False, 'subscribed': False, 'fogbugz': '', 'checkItems': 0, 'checkItemsChecked': 0, 'checkItemsEarliestDue': None, 'comments': 0, 'attachments': 0, 'description': False, 'due': None, 'dueComplete': False, 'start': None}, 'dueComplete': False, 'due': None, 'idChecklists': [], 'idMembers': [], 'labels': [], 'shortUrl': 'https://trello.com/c/RPlcZanE', 'start': None, 'subscribed': False, 'url': 'https://trello.com/c/RPlcZanE/124-itemindone', 'cover': {'idAttachment': None, 'color': None, 'idUploadedBackground': None, 'size': 'normal', 'brightness': 'light'}}
            ]
        return MockResponse(samples_trello_cards_response)

    return None

def test_index_page(mock_response, client):
    response = client.get('/')
    content = response.data.decode('utf8')
    assert 'ItemInToDo' in content
    assert 'ItemInDoing' in content
    assert 'ItemInDone' in content