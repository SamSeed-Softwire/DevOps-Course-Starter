from datetime import datetime, timedelta
from application.item_view_model import ItemViewModel
from application.item import Item


dummy_id = 'id'
dummy_title = 'title'
dummy_status = 'status'
dummy_last_modified = datetime(1, 1, 1)


def test_todo_items():

    items = [
         Item(dummy_id, dummy_title, 'todo-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Status is not "todo-items"', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'todo-items', dummy_last_modified)
    ]
    item_view_model = ItemViewModel(items)
    todo_items = item_view_model.todo_items
    assert todo_items == [
         Item(dummy_id, dummy_title, 'todo-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'todo-items', dummy_last_modified)
    ]

    empty_items = []
    empty_item_view_model = ItemViewModel(empty_items)
    empty_todo_items = empty_item_view_model.todo_items
    assert empty_todo_items == []


def test_doing_items():

    items = [
         Item(dummy_id, dummy_title, 'doing-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Status is not "doing-items"', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'doing-items', dummy_last_modified)
    ]
    item_view_model = ItemViewModel(items)
    doing_items = item_view_model.doing_items
    assert doing_items == [
         Item(dummy_id, dummy_title, 'doing-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'doing-items', dummy_last_modified)
    ]

    empty_items = []
    empty_item_view_model = ItemViewModel(empty_items)
    empty_doing_items = empty_item_view_model.doing_items
    assert empty_doing_items == []


def test_done_items():

    items = [
         Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Status is not "done-items"', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
    ]
    item_view_model = ItemViewModel(items)
    done_items = item_view_model.done_items
    assert done_items == [
         Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
    ]

    empty_items = []
    empty_item_view_model = ItemViewModel(empty_items)
    empty_done_items = empty_item_view_model.done_items
    assert empty_done_items == []


def test_show_all_done_items():

    items_x4 = [
         Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
    ]
    item_view_model_x4 = ItemViewModel(items_x4)
    assert item_view_model_x4.show_all_done_items == True

    items_x5 = [
         Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'done-items', dummy_last_modified)
    ]
    item_view_model_x5 = ItemViewModel(items_x5)
    assert item_view_model_x5.show_all_done_items == False


def test_recent_done_items():
    today = datetime.today()
    items = [
         Item(dummy_id, dummy_title, 'done-items', today + timedelta(days = -1))
        ,Item(dummy_id, dummy_title, 'done-items', today)
        ,Item(dummy_id, dummy_title, 'Status is not "done-items"', today)
        ,Item(dummy_id, dummy_title, 'done-items', today + timedelta(days = +1))
    ]
    item_view_model = ItemViewModel(items)
    recent_done_items = item_view_model.recent_done_items
    assert recent_done_items == [
         Item(dummy_id, dummy_title, 'done-items', today)
    ]


def test_older_done_items():
    today = datetime.today()
    items = [
         Item(dummy_id, dummy_title, 'done-items', today + timedelta(days = -1))
        ,Item(dummy_id, dummy_title, 'Status is not "done-items"', today + timedelta(days = -1))
        ,Item(dummy_id, dummy_title, 'done-items', today)
    ]
    item_view_model = ItemViewModel(items)
    older_done_items = item_view_model.older_done_items
    assert older_done_items == [
         Item(dummy_id, dummy_title, 'done-items', today + timedelta(days = -1))
    ]