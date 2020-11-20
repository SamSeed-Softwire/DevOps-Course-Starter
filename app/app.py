import os
from flask import Flask, render_template, request, redirect, url_for
from trello_functions import get_items, add_item_to_list, move_to_doing, move_to_done
from view_model import ViewModel
from trello_info import TrelloIDs

board_id = os.environ.get('BOARD_ID')

trello_ids = TrelloIDs(board_id)
idList_todo = trello_ids.idList_todo

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    items = get_items()
    view_model = ViewModel(items)
    return render_template('index.html', view_model = view_model)

@app.route('/add-item', methods = ['POST'])
def add_item():
    item = request.form.get('item_name')
    add_item_to_list(item, idList_todo)
    return redirect('/') 

@app.route('/start-item/<item_id>', methods = ['POST'])
def start_item(item_id):
    move_to_doing(item_id)
    return redirect('/')

@app.route('/complete-item/<item_id>', methods = ['POST'])
def complete_item(item_id):
    move_to_done(item_id)
    return redirect('/')

if __name__ == '__main__':
    app.run()