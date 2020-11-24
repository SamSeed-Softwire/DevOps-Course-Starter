from item import Item
class ViewModel:

    def __init__(self, items):
        self.items = items
        self.todo_items = self.get_todo_items()
        self.doing_items = self.get_doing_items()
        self.done_items = self.get_done_items()

    # Properties

    @property
    def items(self):
        return self._items
    
    @items.setter
    def items(self, items):
        check_type(items)
        self._items = items

    @property
    def todo_items(self):
        return self._todo_items

    @todo_items.setter
    def todo_items(self, todo_items):
        check_type(todo_items)
        self._todo_items = todo_items

    @property
    def doing_items(self):
        return self._doing_items

    @doing_items.setter
    def doing_items(self, doing_items):
        check_type(doing_items)
        self._doing_items = doing_items

    @property
    def done_items(self):
        return self._done_items

    @done_items.setter
    def done_items(self, done_items):
        check_type(done_items)
        self._done_items = done_items
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

# QQ Couldn't get this to work as a class method
def check_type(items):
    items_type_error_message = 'Error: the collection of items used to initialise this ViewModel instance must be a *list*, where each element in the list is of type Item.'
    if type(items) != list:
        raise TypeError(items_type_error_message)
    for item in items:
        if type(item) != Item:
            raise TypeError(items_type_error_message)