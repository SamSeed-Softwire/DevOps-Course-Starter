import requests
import os

auth_params_key = os.environ.get('AUTH_PARAMS_KEY')
auth_params_token = os.environ.get('AUTH_PARAMS_TOKEN')
auth_params = {'key' : auth_params_key, 'token' : auth_params_token}


class TrelloData:

    def __init__(self, board_id: str):
    
        self.lists = get_lists(board_id)
        self.cards = get_cards(board_id)


class TrelloIDs:

    def __init__(self, board_id: str):
    
        self.board_id = board_id
        self.idList_todo = get_idList(board_id, "To Do")
        self.idList_doing = get_idList(board_id, "Doing")
        self.idList_done = get_idList(board_id, "Done")


def get_lists(board_id: str):
    return requests.get(f'https://api.trello.com/1/boards/{board_id}/lists', params = auth_params).json()

def get_cards(board_id: str):
    return requests.get(f'https://api.trello.com/1/boards/{board_id}/cards', params = auth_params).json()

def get_idList(board_id: str, name: str):
    lists = get_lists(board_id)
    # QQ: Need test for when multiple lists have the same name.
    for list in lists:
        if list["name"] == name:
            return list["id"]
    raise ValueError(f'No list exists with the name "{name}".')