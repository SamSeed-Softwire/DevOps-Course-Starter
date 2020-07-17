import requests

auth_params = {'key' : 'b7ff82f3970592f40825cfb7c771881c', 'token' : 'b3918107d6c9333fcc87a9b0a362b1801db711b71559f152a724b63d5b070b62'}
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

def add_item(name, idList):
    add_item_params = {'key': 'b7ff82f3970592f40825cfb7c771881c', 'token': 'b3918107d6c9333fcc87a9b0a362b1801db711b71559f152a724b63d5b070b62', 'name': name, 'idList': idList}
    requests.post('https://api.trello.com/1/cards/', params = add_item_params)


'''
card_to_move = '5f04caf38d48873dda953ee0'
list_to_move_to = '5efc77d85e465d1006d941b5'
params2 = {'key': 'b7ff82f3970592f40825cfb7c771881c', 'token': 'b3918107d6c9333fcc87a9b0a362b1801db711b71559f152a724b63d5b070b62', 'idList': list_to_move_to}
move_card_base_url = 'https://api.trello.com/1/cards/'
move_card_url = move_card_base_url + card_to_move
#requests.put(move_card_url, params = params2)
'''