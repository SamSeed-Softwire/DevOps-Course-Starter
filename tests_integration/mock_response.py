class MockResponse:

    def __init__(self, json):
        self._json = json

    def json(self):
        return self._json