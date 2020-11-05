class Item:

    def __init__(self, id, title, status):
        self.id = id
        self.title = title
        self.status = status
    
    def __eq__(self, other):
        """Overrides the default implementation."""
        if type(self) == type(other):
            return self.__dict__ == other.__dict__
        return False