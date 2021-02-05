from flask import Flask, render_template, request, redirect

from application.mongo_client import MongoClient
from application.view_model import ViewModel


def create_app():

    app = Flask(__name__)
    mongo_client = MongoClient()

    @app.route('/')
    def index():
        mongo_client.refresh_items()
        items = mongo_client.items
        view_model = ViewModel(items)
        return render_template('index.html', view_model = view_model)

    @app.route('/add-item', methods = ['POST'])
    def add_item():
        item_name = request.form.get('item_name')
        mongo_client.add_item(item_name, 'todo-items')
        return redirect('/')

    @app.route('/start-item/<item_id>', methods = ['POST'])
    def start_item(item_id):
        mongo_client.move_item(item_id, 'todo-items', 'doing-items')
        return redirect('/')

    @app.route('/complete-item/<item_id>', methods = ['POST'])
    def complete_item(item_id):
        mongo_client.move_item(item_id, 'doing-items', 'done-items')
        return redirect('/')

    @app.route('/uncomplete-item/<item_id>', methods = ['POST'])
    def uncomplete_item(item_id):
        mongo_client.move_item(item_id, 'done-items', 'doing-items')
        return redirect('/')

    @app.route('/delete-all-items', methods = ['POST'])
    def delete_items():
        mongo_client.delete_all_items()
        return redirect('/')

    return app