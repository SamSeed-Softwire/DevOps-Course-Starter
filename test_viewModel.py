from viewModel import ViewModel
from item import Item


def test_get_todo_items():
    items = [
         Item('id', 'title', 'To Do')
        ,Item('id', 'title', 'Status is not "To Do"')
        ,Item('id', 'title', 'To Do')
    ]
    item_view_model = ViewModel(items)
    todo_items = item_view_model.get_todo_items()
    assert todo_items == [
         Item('id', 'title', 'To Do')
        ,Item('id', 'title', 'To Do')
    ]

def test_get_doing_items():
    items = [
         Item('id', 'title', 'Doing')
        ,Item('id', 'title', 'Status is not "Doing"')
        ,Item('id', 'title', 'Doing')
    ]
    item_view_model = ViewModel(items)
    doing_items = item_view_model.get_doing_items()
    assert doing_items == [
         Item('id', 'title', 'Doing')
        ,Item('id', 'title', 'Doing')
    ]

def test_get_done_items():
    items = [
         Item('id', 'title', 'Done')
        ,Item('id', 'title', 'Status is not "Done"')
        ,Item('id', 'title', 'Done')
    ]
    item_view_model = ViewModel(items)
    done_items = item_view_model.get_done_items()
    assert done_items == [
         Item('id', 'title', 'Done')
        ,Item('id', 'title', 'Done')
    ]