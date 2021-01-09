from datetime import date, timedelta

from app.item import Item
class ViewModel:

    def __init__(self, items):
        self._items = items

    # Properties

    @property
    def todo_items(self):
        return [item for item in self._items if item.status == 'To Do']

    @property
    def doing_items(self):
        return [item for item in self._items if item.status == 'Doing']

    @property
    def done_items(self):
        return [item for item in self._items if item.status == 'Done']

    @property
    def show_all_done_items(self):
        return len(self.done_items) <= 4

    @property
    def recent_done_items(self):
        return [item for item in self._items if item.status == 'Done' if item.last_modified.date() == date.today()]

    @property
    def older_done_items(self):
        return [item for item in self._items if item.status == 'Done' if item.last_modified.date() <= date.today() + timedelta(days = -1)]

    # Overriding the default class equivalence implementation
    def __eq__(self, other):
        """Overrides the default implementation."""
        if type(self) == type(other):
            return self.items == other.items
        return False