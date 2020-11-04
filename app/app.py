from flask import Flask, render_template, request, redirect, url_for
from trello_functions import get_items, add_item_to_list, move_to_done
from viewModel import ViewModel

app = Flask(__name__)

@app.route('/')
def index():
    items = get_items()
    item_view_model = ViewModel(items)
    return render_template('index.html', view_model = item_view_model)

@app.route('/add-item', methods = ['POST'])
def add_item():
    item = request.form.get('item_name')
    add_item_to_list(item, '5efc77d5ce13a25c8b6bf9c1')
    return redirect('/') 

@app.route('/complete-item/<item_id>', methods = ['POST'])
def complete_item(item_id):
    move_to_done(item_id)
    return redirect('/')

if __name__ == '__main__':
    app.run()