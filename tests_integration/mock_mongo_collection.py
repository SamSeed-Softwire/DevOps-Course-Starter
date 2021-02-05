from datetime import datetime

class MockMongoCollection:

    def __init__(self, list):
        self.list = list


    def find(self):
        if self.list == 'todo-items':
            return [
                {'_id': 'todo_1', 'title': 'ItemInToDo', 'last_modified': datetime(1, 1, 1)}
            ]
        elif self.list == 'doing-items':
            return [
                {'_id': 'doing_1', 'title': 'ItemInDoing', 'last_modified': datetime(1, 1, 1)}
            ]
        elif self.list == 'done-items':
            return [
                {'_id': 'done_1', 'title': 'ItemInDone', 'last_modified': datetime(1, 1, 1)}
            ]
        else:
            return None