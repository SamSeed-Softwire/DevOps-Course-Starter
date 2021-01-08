from flask import Flask, render_template, request, redirect
from app.trello_functions import get_items, add_item_to_todo, move_to_doing, move_to_done, delete_all_items
from app.view_model import ViewModel

def create_app():

    app = Flask(__name__)

    @app.route('/')
    def index():
        items = get_items()
        view_model = ViewModel(items)
        return render_template('index.html', view_model = view_model)

    @app.route('/add-item', methods = ['POST'])
    def add_item():
        item = request.form.get('item_name')
        add_item_to_todo(item)
        return redirect('/')

    @app.route('/start-item/<item_id>', methods = ['POST'])
    def start_item(item_id):
        move_to_doing(item_id)
        return redirect('/')

    @app.route('/complete-item/<item_id>', methods = ['POST'])
    def complete_item(item_id):
        move_to_done(item_id)
        return redirect('/')

    @app.route('/delete-all-items', methods = ['POST'])
    def delete_items():
        delete_all_items()
        return redirect('/')

    return app

app = create_app()
if __name__ == '__main__':
    app.run()