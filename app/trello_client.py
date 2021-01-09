from datetime import datetime
import requests
import os

from app.item import Item
from app.trello_data import TrelloData
from app.trello_ids import TrelloIDs

class TrelloClient:

    def __init__(self):

        self.board_id = os.environ.get('BOARD_ID')        
        self.auth_params_key = os.environ.get('AUTH_PARAMS_KEY')
        self.auth_params_token = os.environ.get('AUTH_PARAMS_TOKEN')
        self.auth_params = {'key': self.auth_params_key, 'token': self.auth_params_token}
        
        self.idList_todo = ''
        self.idList_doing = ''
        self.idList_done = ''

        self.cards = []
        self.lists = []
        self.items = []

        self.refresh_items()
        self.refresh_ids()


    def refresh_items(self):
        
        trello_data = TrelloData(self.board_id, self.auth_params)
        self.cards = trello_data.cards
        self.lists = trello_data.lists

        # Retrieve relevant info on all to do items
        self.items = []
        for card in self.cards:
            for list in self.lists:
                if card['idList'] == list['id']:
                    # The 'status' of the card is the name of the list it's in.
                    status = list['name']
                    break
            last_modified = datetime.strptime(card['dateLastActivity'][:-1] + '000', '%Y-%m-%dT%H:%M:%S.%f')
            item = Item(card['id'], card['name'], status, last_modified)
            self.items.append(item)

    def refresh_ids(self):
       
        trello_ids = TrelloIDs(self.board_id, self.auth_params)
        self.idList_todo = trello_ids.idList_todo
        self.idList_doing = trello_ids.idList_doing
        self.idList_done = trello_ids.idList_done


    def add_item_to_list(self, name, idList):
        add_item_params = {'key': self.auth_params_key, 'token': self.auth_params_token, 'name': name, 'idList': idList}
        requests.post('https://api.trello.com/1/cards/', params = add_item_params)

    def add_item_to_todo(self, name):
        self.add_item_to_list(name, self.idList_todo)

    def move_to_doing(self, idCard):
        move_item_to_doing_params = {'key': self.auth_params_key, 'token': self.auth_params_token, 'idList': self.idList_doing}
        requests.put(f'https://api.trello.com/1/cards/{idCard}/', params = move_item_to_doing_params)

    def move_to_done(self, idCard):
        move_item_to_done_params = {'key': self.auth_params_key, 'token': self.auth_params_token, 'idList': self.idList_done}
        requests.put(f'https://api.trello.com/1/cards/{idCard}/', params = move_item_to_done_params)

    def delete(self, idCard):
        requests.delete(f'https://api.trello.com/1/cards/{idCard}/', params = self.auth_params)


    def delete_all_items(self):
        self.refresh_items()
        for card in self.cards:
            self.delete(card['id'])