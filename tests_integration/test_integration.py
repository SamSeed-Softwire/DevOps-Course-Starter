from dotenv import load_dotenv, find_dotenv
import os
import pymongo
import pytest
from unittest.mock import patch, Mock

import application.app as app
from tests_integration.mock_mongo_db import MockMongoDatabase


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
    monkeypatch.setattr(pymongo, "MongoClient", mock_mongo_client)

def mock_mongo_client(*args, **kwargs):
    MONGO_TODO_APP_DATABASE = os.environ.get('MONGO_TODO_APP_DATABASE')
    return {MONGO_TODO_APP_DATABASE: MockMongoDatabase()}

def test_index_page(mock_response, client):
    response = client.get('/')
    content = response.data.decode('utf8')
    assert 'ItemInToDo' in content
    assert 'ItemInDoing' in content
    assert 'ItemInDone' in content