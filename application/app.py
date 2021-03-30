from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, current_user, AnonymousUserMixin
from flask_login.utils import login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
import os
import requests

from application.mongo_client import MongoClient
from application.view_model import ViewModel


def create_app():

    app = Flask(__name__)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    if os.environ.get('LOGIN_DISABLED') == "True":
        login_disabled = True
    else:
        login_disabled = False
    app.config['LOGIN_DISABLED'] = login_disabled

    mongo_client = MongoClient()

    # Handle authentication & authorisation.

    login_manager = LoginManager()
    login_manager.init_app(app)

    client = WebApplicationClient(os.environ.get('GITHUB_CLIENT_ID'))


    @login_manager.unauthorized_handler
    def unauthenticated():
        # state = os.urandom(16)
        uri = client.prepare_request_uri("https://github.com/login/oauth/authorize")#, state = state)
        return redirect(uri)

    @login_manager.user_loader
    def load_user(user_id):
        if mongo_client.user_exists(user_id):
            return mongo_client.get_user(user_id)
        else:
            # Is returning AnonymousUserMixin sensible here?
            return AnonymousUserMixin()

    @app.route('/login/callback/', methods = ['GET'])
    def process_callback():

        # Get information from authorisation request response.
        authorization_response_url = request.url
        authorization_response_code = request.args.get('code')
        # authorization_response_state = request.args.get('state')

        # Construct token request.
        client_secret = os.environ.get('GITHUB_CLIENT_SECRET')
        token_request_base_url = "https://github.com/login/oauth/access_token"
        token_request_url, token_request_headers, token_request_body = client.prepare_token_request(
            token_request_base_url,
            authorization_response=authorization_response_url,
            code=authorization_response_code,
            client_secret = client_secret#,
            # state = authorization_response_state
        )

        # Get an access token.
        token_request_response = requests.post(
            token_request_url,
            headers = token_request_headers,
            data = token_request_body
        )
        client.parse_request_body_response(token_request_response.text)

        # Get user details.
        user_request_base_uri = "https://api.github.com/user"
        user_request_uri, user_request_headers, user_request_body = client.add_token(
            user_request_base_uri
        )
        user_info = requests.get(
            user_request_uri,
            headers = user_request_headers,
            data = user_request_body
        ).json()

        # Create user object and log user in.
        user_id = user_info['id']
        user = User(user_id, "reader")
        users = mongo_client.users
        # Assign the first user to be an admin.
        if len(users) == 0:
            user.role = "admin"
        mongo_client.add_user(user_id, user.role)
        login_user(user)

        # Return to the main page.
        return redirect('/')

    # Login/logout/authorisation screens.

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect('/login')

    @app.route('/forbidden')
    def forbidden():
        return render_template('forbidden.html')

    @app.route('/')
    def index():
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