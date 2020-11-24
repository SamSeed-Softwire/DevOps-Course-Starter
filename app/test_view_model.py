from datetime import datetime
from view_model import ViewModel
from item import Item

dummy_id = 'id'
dummy_title = 'title'
dummy_status = 'status'
dummy_last_modified = datetime(1, 1, 1)

def test_get_todo_items():
    
    items = [
         Item(dummy_id, dummy_title, 'To Do', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Status is not "To Do"', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'To Do', dummy_last_modified)
    ]
    item_view_model = ViewModel(items)
    todo_items = item_view_model.todo_items
    assert todo_items == [
         Item(dummy_id, dummy_title, 'To Do', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'To Do', dummy_last_modified)
    ]

    empty_items = []
    empty_item_view_model = ViewModel(empty_items)
    empty_todo_items = empty_item_view_model.todo_items
    assert empty_todo_items == []

def test_get_doing_items():
    
    items = [
         Item(dummy_id, dummy_title, 'Doing', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Status is not "Doing"', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Doing', dummy_last_modified)
    ]
    item_view_model = ViewModel(items)
    doing_items = item_view_model.doing_items
    assert doing_items == [
         Item(dummy_id, dummy_title, 'Doing', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Doing', dummy_last_modified)
    ]

    empty_items = []
    empty_item_view_model = ViewModel(empty_items)
    empty_doing_items = empty_item_view_model.doing_items
    assert empty_doing_items == []
    

def test_get_done_items():
    
    items = [
         Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Status is not "Done"', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
    ]
    item_view_model = ViewModel(items)
    done_items = item_view_model.done_items
    assert done_items == [
         Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
    ]

    empty_items = []
    empty_item_view_model = ViewModel(empty_items)
    empty_done_items = empty_item_view_model.done_items
    assert empty_done_items == []


def test_show_all_done_items_flag():

    items_x4 = [
         Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)        
    ]
    item_view_model_x4 = ViewModel(items_x4)
    assert item_view_model_x4.show_all_done_items_flag() == True

    items_x5 = [
         Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)        
        ,Item(dummy_id, dummy_title, 'Done', dummy_last_modified)
    ]
    item_view_model_x5 = ViewModel(items_x5)
    assert item_view_model_x5.show_all_done_items_flag() == False