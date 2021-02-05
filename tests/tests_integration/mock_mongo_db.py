from tests.tests_integration.mock_mongo_collection import MockMongoCollection

class MockMongoDatabase(dict):

    def __init__(self):
        self['todo-items'] = MockMongoCollection('todo-items')
        self['doing-items'] = MockMongoCollection('doing-items')
        self['done-items'] = MockMongoCollection('done-items')


    def list_collection_names(self):
        return ['todo-items', 'doing-items', 'done-items']