import requests

class TrelloIDs:

    def __init__(self, board_id: str, auth_params):

        self.board_id = board_id
        self.idList_todo = get_idList(board_id, "To Do", auth_params)
        self.idList_doing = get_idList(board_id, "Doing", auth_params)
        self.idList_done = get_idList(board_id, "Done", auth_params)


def get_lists(board_id: str, auth_params):
    return requests.get(f'https://api.trello.com/1/boards/{board_id}/lists', params = auth_params).json()

def get_idList(board_id: str, name: str, auth_params):
    lists = get_lists(board_id, auth_params)
    # QQ: Need test for when multiple lists have the same name.
    for list in lists:
        if list["name"] == name:
            return list["id"]
    raise ValueError(f'No list exists with the name "{name}".')