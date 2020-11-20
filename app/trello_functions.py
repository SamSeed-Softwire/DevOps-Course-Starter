import requests
from trello_config import AUTH_PARAMS_KEY, AUTH_PARAMS_TOKEN
from item import Item
from trello_info import TrelloData, TrelloIDs
import os
from datetime import datetime

AUTH_PARAMS_KEY = os.environ.get('AUTH_PARAMS_KEY')
AUTH_PARAMS_TOKEN = os.environ.get('AUTH_PARAMS_TOKEN')
board_id = os.environ.get('BOARD_ID')

trello_ids = TrelloIDs(board_id)
idList_todo = trello_ids.idList_todo
idList_doing = trello_ids.idList_doing
idList_done = trello_ids.idList_done

# Get all cards in the 'To Do' list.

def get_items():

    cards = TrelloData(board_id).cards
    lists = TrelloData(board_id).lists

    # Retrieve relevant info on all to do items
    items = []
    for card in cards:
        for list in lists:
            if card['idList'] == list['id']:
                # The 'status' of the card is the name of the list it's in.
                status = list['name']
                break
        last_modified = datetime.strptime(card['dateLastActivity'][:-1] + '000', '%Y-%m-%dT%H:%M:%S.%f')
        item = Item(card['id'], card['name'], status, last_modified)
        items.append(item)

    return items

def add_item_to_list(name, idList):
    add_item_params = {'key': AUTH_PARAMS_KEY, 'token': AUTH_PARAMS_TOKEN, 'name': name, 'idList': idList}
    requests.post('https://api.trello.com/1/cards/', params = add_item_params)

def move_to_doing(idCard):
    move_item_to_doing_params = {'key': AUTH_PARAMS_KEY, 'token': AUTH_PARAMS_TOKEN, 'idList': idList_doing}
    requests.put(f'https://api.trello.com/1/cards/{idCard}/', params = move_item_to_doing_params)

def move_to_done(idCard):
    move_item_to_done_params = {'key': AUTH_PARAMS_KEY, 'token': AUTH_PARAMS_TOKEN, 'idList': idList_done}
    requests.put(f'https://api.trello.com/1/cards/{idCard}/', params = move_item_to_done_params)

def delete(idCard):
    delete_item_params = {'key': AUTH_PARAMS_KEY, 'token': AUTH_PARAMS_TOKEN}
    requests.delete(f'https://api.trello.com/1/cards/{idCard}/', params = delete_item_params)

def delete_all_items():
    trello_data = TrelloData(board_id)
    cards = trello_data.cards
    for card in cards:
        delete(card['id'])