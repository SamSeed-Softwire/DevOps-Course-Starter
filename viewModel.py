class ViewModel:

    def __init__(self, items):
        self.items = items

    @property
    def items(self):
        return self._items
    
    @items.setter
    def items(self, items):
        self._items = items
    
    def get_to_do_items(self):
        to_do_items = []
        for item in self.items:
                if self.items.status == "To Do":
                    to_do_items.append(item)
                else:
                    continue
            