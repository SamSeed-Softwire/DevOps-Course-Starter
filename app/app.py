from flask import Flask, render_template, request, redirect

from app.trello_client import TrelloClient
from app.view_model import ViewModel

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
        trello_client.add_item_to_todo(item)
        return redirect('/')

    @app.route('/start-item/<item_id>', methods = ['POST'])
    def start_item(item_id):
        trello_client.move_to_doing(item_id)
        return redirect('/')

    @app.route('/complete-item/<item_id>', methods = ['POST'])
    def complete_item(item_id):
        trello_client.move_to_done(item_id)
        return redirect('/')

    @app.route('/delete-all-items', methods = ['POST'])
    def delete_items():
        trello_client.delete_all_items()
        return redirect('/')

    return app