import requests
from trello_config import AUTH_PARAMS_KEY, AUTH_PARAMS_TOKEN

auth_params = {'key' : AUTH_PARAMS_KEY, 'token' : AUTH_PARAMS_TOKEN}
board_id = '5efc773fd08d053db4ef3c18'

# Get all cards in the 'To Do' list.

def get_items():
    
    cards = requests.get(f'https://api.trello.com/1/boards/{board_id}/cards', params = auth_params).json()
    lists = requests.get(f'https://api.trello.com/1/boards/{board_id}/lists', params = auth_params).json()

    # Retrieve relevant info on all to do items
    items = []
    for card in cards:
        for list in lists:
            if card['idList'] == list['id']:
                # The 'status' of the card is the name of the list it's in.
                status = list['name']
                break
        item = {'id': card['id'], 'title': card['name'], 'status': status}
        items.append(item)

    return items

def add_item_to_list(name, idList):
    add_item_params = {'key': AUTH_PARAMS_KEY, 'token': AUTH_PARAMS_TOKEN, 'name': name, 'idList': idList}
    requests.post('https://api.trello.com/1/cards/', params = add_item_params)

def move_to_done(idCard):
    idList_todo = '5efc77d85e465d1006d941b5'
    move_item_to_done_params = {'key': AUTH_PARAMS_KEY, 'token': AUTH_PARAMS_TOKEN, 'idList': idList_todo}
    requests.put(f'https://api.trello.com/1/cards/{idCard}/', params = move_item_to_done_params)
