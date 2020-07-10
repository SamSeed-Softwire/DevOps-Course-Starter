from flask import Flask, render_template, request, redirect, url_for
import session_items as session
from session_items import add_item
from trello_functions import get_items

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items = items)

@app.route('/add-item', methods = ['POST'])
def add_item_to_list():
    item = request.form.get('item_name')
    add_item(item)
    return redirect('/')

if __name__ == '__main__':
    app.run()