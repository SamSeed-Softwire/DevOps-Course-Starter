from flask import Flask, render_template, request, redirect

from application.trello_client import TrelloClient
from application.view_model import ViewModel


def create_app():

    app = Flask(__name__)
    trello_client = TrelloClient()

    @app.route('/')
    def index():
        trello_client.refresh_items()
        items = trello_client.items
        view_model = ViewModel(items)
        return render_template('index.html', view_model = view_model)

    @app.route('/add-item', methods = ['POST'])
    def add_item():
        item = request.form.get('item_name')
        trello_client.add_item(item, 'todo-items')
        return redirect('/')

    @app.route('/start-item/<item_id>', methods = ['POST'])
    def start_item(item_id):
        trello_client.move_item(item_id, 'todo-items', 'doing-items')
        return redirect('/')

    @app.route('/complete-item/<item_id>', methods = ['POST'])
    def complete_item(item_id):
        trello_client.move_item(item_id, 'doing-items', 'done-items')
        return redirect('/')

    @app.route('/uncomplete-item/<item_id>', methods = ['POST'])
    def uncomplete_item(item_id):
        trello_client.move_item(item_id, 'done-items', 'doing-items')
        return redirect('/')

    @app.route('/delete-all-items', methods = ['POST'])
    def delete_items():
        trello_client.delete_all_items()
        return redirect('/')

    return app