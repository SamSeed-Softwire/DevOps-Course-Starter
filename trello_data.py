import requests

class TrelloData:

    def __init__(self, board_id: str, auth_params):

        self.lists = get_lists(board_id, auth_params)
        self.cards = get_cards(board_id, auth_params)


def get_lists(board_id: str, auth_params):
    return requests.get(f'https://api.trello.com/1/boards/{board_id}/lists', params = auth_params).json()

def get_cards(board_id: str, auth_params):
    return requests.get(f'https://api.trello.com/1/boards/{board_id}/cards', params = auth_params).json()