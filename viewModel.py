from item import Item
class ViewModel:

    def __init__(self, items):
        self.items = items

    @property
    def items(self):
        return self._items
    
    @items.setter
    def items(self, items):
        items_type_error_message = 'Error: the collection of items used to initialise this ViewModel instance must be a *list*, where each element in the list is of type Item.'
        if type(items) != list:
            raise TypeError(items_type_error_message)
        for item in items:
            if type(item) != Item:
                raise TypeError(items_type_error_message)
        self._items = items
    
    def get_to_do_items(self):
        to_do_items = []
        for item in self.items:
                if self.items.status == "To Do":
                    to_do_items.append(item)
                else:
                    continue
            
    def __eq__(self, other):
        """Overrides the default implementation."""
        if type(self) == type(other):
            return self.items == other.items
        return False