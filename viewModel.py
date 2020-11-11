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

    def __eq__(self, other):
        """Overrides the default implementation."""
        if type(self) == type(other):
            return self.items == other.items
        return False


    def get_todo_items(self):
        def is_status_todo(item: Item):
            if item.status == 'To Do':
                return True
            return False
        return list(filter(is_status_todo, self.items))

    def get_doing_items(self):
        def is_status_doing(item: Item):
            if item.status == 'Doing':
                return True
            return False
        return list(filter(is_status_doing, self.items))

    def get_done_items(self):
        def is_status_done(item: Item):
            if item.status == 'Done':
                return True
            return False
        return list(filter(is_status_done, self.items))

    def show_all_done_items_flag(self):
        done_items = self.get_done_items()
        done_items_count = len(done_items)
        if done_items_count <= 4:
            return True
        return False