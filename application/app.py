from flask import Flask, abort, render_template, request, redirect
from flask_login import LoginManager, login_required, current_user
from flask_login.utils import login_user, logout_user
from functools import wraps
from oauthlib.oauth2 import WebApplicationClient
import os
import requests

from application.mongo_client import MongoClient
from application.item_view_model import ItemViewModel
from application.user import User
from application.user_view_model import UserViewModel


def create_app():

    # Initialise app.
    app = Flask(__name__)
    app.secret_key = os.environ.get('FLASK_SECRET_KEY')

    app.config['LOGIN_DISABLED'] = os.environ.get('LOGIN_DISABLED') == "True"

    # Initialise database client.
    mongo_client = MongoClient()

    # Handle authentication & authorisation.

    login_manager = LoginManager()
    login_manager.init_app(app)

    client = WebApplicationClient(os.environ.get('GITHUB_CLIENT_ID'))


    @login_manager.unauthorized_handler
    def unauthenticated():
        uri = client.prepare_request_uri("https://github.com/login/oauth/authorize")
        return redirect(uri)

    @login_manager.user_loader
    def load_user(user_id):
        return mongo_client.get_user(user_id)

    @app.route('/login/callback/', methods = ['GET'])
    def process_callback():

        # Get information from authorisation request response.
        authorization_response_url = request.url
        authorization_response_code = request.args.get('code')

        # Construct token request.
        client_secret = os.environ.get('GITHUB_CLIENT_SECRET')
        token_request_base_url = "https://github.com/login/oauth/access_token"
        token_request_url, token_request_headers, token_request_body = client.prepare_token_request(
            token_request_base_url,
            authorization_response=authorization_response_url,
            code=authorization_response_code,
            client_secret = client_secret
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

    def admins_only(view_function):
        @wraps(view_function)
        def wrapper(*args, **kwargs):
            if current_user.role == 'admin':
                return view_function(*args, **kwargs)
            else:
                abort(403)
        return wrapper

    def admins_and_writers_only(view_function):
        @wraps(view_function)
        def wrapper(*args, **kwargs):
            if current_user.role in ('admin', 'writer'):
                return view_function(*args, **kwargs)
            else:
                abort(403)
        return wrapper

    def login_disabled_manager(view_function):
        @wraps(view_function)
        def wrapper(*args, **kwargs):
            if app.config['LOGIN_DISABLED'] == True:
                logout_user()
                user = User(0, os.environ.get('ROLE_FOR_DEV_PURPOSES'))
                login_user(user)
            return view_function(*args, **kwargs)
        return wrapper

    # Login/logout/authorisation screens.

    @app.route('/login')
    def login():
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect('/login')

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('forbidden.html'), 403


    # Main page.

    @app.route('/')
    @login_disabled_manager
    @login_required
    def index():
        items = mongo_client.items
        item_view_model = ItemViewModel(items)
        role = current_user.role
        return render_template('index.html', item_view_model = item_view_model, role = role)


    # Actions.

    @app.route('/add-item', methods = ['POST'])
    @login_disabled_manager
    @login_required
    @admins_and_writers_only
    def add_item():
        item_name = request.form.get('item_name')
        mongo_client.add_item(item_name, 'todo-items')
        return redirect('/')

    @app.route('/start-item/<item_id>', methods = ['POST'])
    @login_disabled_manager
    @login_required
    @admins_and_writers_only
    def start_item(item_id):
        mongo_client.move_item(item_id, 'todo-items', 'doing-items')
        return redirect('/')

    @app.route('/complete-item/<item_id>', methods = ['POST'])
    @login_disabled_manager
    @login_required
    @admins_and_writers_only
    def complete_item(item_id):
        mongo_client.move_item(item_id, 'doing-items', 'done-items')
        return redirect('/')

    @app.route('/uncomplete-item/<item_id>', methods = ['POST'])
    @login_disabled_manager
    @login_required
    @admins_and_writers_only
    def uncomplete_item(item_id):
        mongo_client.move_item(item_id, 'done-items', 'doing-items')
        return redirect('/')

    @app.route('/delete-all-items', methods = ['POST'])
    @login_disabled_manager
    @login_required
    @admins_and_writers_only
    def delete_items():
        mongo_client.delete_all_items()
        return redirect('/')

    @app.route('/manage-users', methods = ['GET'])
    @login_disabled_manager
    @login_required
    @admins_only
    def manage_users():
        users = mongo_client.users
        user_view_model = UserViewModel(users)
        return render_template('manage-users.html', user_view_model = user_view_model)

    @app.route('/edit-user-role', methods = ['POST'])
    @login_disabled_manager
    @login_required
    @admins_only
    def edit_user_role():
        github_id = request.form.get('github_id')
        new_role = request.form.get('new_role')
        mongo_client.edit_user_role(github_id, new_role)
        users = mongo_client.users
        user_view_model = UserViewModel(users)
        return render_template('manage-users.html', user_view_model = user_view_model)

    @app.route('/delete-user', methods = ['POST'])
    @login_disabled_manager
    @login_required
    @admins_only
    def delete_user():
        github_id = request.form.get('github_id')
        mongo_client.delete_user(github_id)
        users = mongo_client.users
        user_view_model = UserViewModel(users)
        return render_template('manage-users.html', user_view_model = user_view_model)

    return app