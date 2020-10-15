from datetime import datetime

class Item:

    def __init__(self, id, title, status, last_modified: datetime):
        self.id = id
        self.title = title
        self.status = status
        self.last_modified = last_modified

    def __eq__(self, other):
        """Overrides the default implementation."""
        if type(self) == type(other):
            return self.__dict__ == other.__dict__
        return False