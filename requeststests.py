import requests

auth_params = {'key' : 'b7ff82f3970592f40825cfb7c771881c', 'token' : 'b3918107d6c9333fcc87a9b0a362b1801db711b71559f152a724b63d5b070b62'}
# Get all cards in the 'To Do' list.

def get_items2():
    todo_cards = requests.get('https://api.trello.com/1/boards/5efc773fd08d053db4ef3c18/cards', params = auth_params).json()
    
    lists = requests.get('https://api.trello.com/1/boards/5efc773fd08d053db4ef3c18/lists', params = auth_params).json()

    items = []
    todo_cards = requests.get('https://api.trello.com/1/boards/5efc773fd08d053db4ef3c18/cards', params = auth_params).json()
    for card in todo_cards:
        for list in lists:
            if card['idList'] == list['id']:
                status = list['name']
                break
        item = {'id': card['id'], 'title': card['name'], 'status': status}
        items.append(item)

    return items


new_card = 'Call Safrina'
todo_list_id = '5efc77d5ce13a25c8b6bf9c1'
params1 = {'key': 'b7ff82f3970592f40825cfb7c771881c', 'token': 'b3918107d6c9333fcc87a9b0a362b1801db711b71559f152a724b63d5b070b62', 'idList': todo_list_id, 'name': new_card}
#requests.post('https://api.trello.com/1/cards/', params = params1)

card_to_move = '5f04caf38d48873dda953ee0'
list_to_move_to = '5efc77d85e465d1006d941b5'
params2 = {'key': 'b7ff82f3970592f40825cfb7c771881c', 'token': 'b3918107d6c9333fcc87a9b0a362b1801db711b71559f152a724b63d5b070b62', 'idList': list_to_move_to}
move_card_base_url = 'https://api.trello.com/1/cards/'
move_card_url = move_card_base_url + card_to_move
#requests.put(move_card_url, params = params2)

'''
fields = ['name']
request_params = {'key' : 'b7ff82f3970592f40825cfb7c771881c', 'token' : 'b3918107d6c9333fcc87a9b0a362b1801db711b71559f152a724b63d5b070b62', 'fields' : fields}

r = requests.get('https://api.trello.com/1/members/me/boards/', params = request_params)

print()
print(type(r.json()))
print(r.json())
'''