from bson.objectid import ObjectId
from datetime import datetime
import os
import pymongo

from application.item import Item
from application.user import User

class MongoClient:

    def __init__(self):

        self.MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
        self.MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
        self.MONGO_HOST = os.environ.get('MONGO_HOST')
        self.MONGO_TODO_APP_DATABASE = os.environ.get('MONGO_TODO_APP_DATABASE')
        self.client = pymongo.MongoClient(f"mongodb+srv://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}/?retryWrites=true&w=majority")
        self.db = self.client[self.MONGO_TODO_APP_DATABASE]

    # User management.

    @property
    def users(self):
        users = []
        raw_users = self.db['users'].find()
        for raw_user in raw_users:
            user = User(raw_user['_id'], raw_user['role'])
            users.append(user)
        return users

    def user_exists(self, github_id):
        github_id = int(github_id)
        return self.db['users'].count_documents({'_id': github_id}) > 0

    def get_user(self, github_id):
        github_id = int(github_id)
        if self.user_exists(github_id):
            raw_user = self.db['users'].find_one({'_id': github_id})
            return User(raw_user['_id'], raw_user['role'])
        else:
            ## TODO: Work out a more sensible return type/functionality.
            return None

    def add_user(self, github_id, role = "reader"):
        github_id = int(github_id)
        if self.user_exists(github_id):
            message = f"""User '{github_id}' already exists in database. Use the edit_user_role method if you want to change their role."""
        else:
            user = User(github_id, role) # To check the validity of the role being assigned.
            self.db['users'].insert_one({'_id': github_id, 'role': role})
            message = f"""User '{github_id}' successfully added and assigned the role of {role}."""
        return message

    def edit_user_role(self, github_id, new_role):
        github_id = int(github_id)
        user = User(github_id, new_role) # To check the validity of the role being assigned.
        if not self.user_exists(github_id):
            message = "User '{github_id}' doesn't exist in database. Use the add_user method if you want to add a user."
        else:
            self.db['users'].update_one({'_id': github_id}, {'$set': {'_id': github_id, 'role': new_role}})
            message = f"""User '{github_id}' successfully assigned the role of {new_role}."""
        return message

    def delete_user(self, github_id):
        github_id = int(github_id)
        if not self.user_exists(github_id):
            message = f"""User '{github_id}' doesn't exist in database. Are you sure this is the user you wanted to delete?"""
        else:
            self.db['users'].delete_one({'_id': github_id})
            message = f"""User '{github_id}' successfully deleted."""
        return message


    # Item management.

    @property
    def items(self):
        items = []
        lists = self.db.list_collection_names()
        for list in lists:
            raw_items = self.db[list].find()
            for raw_item in raw_items:
                item = Item(str(raw_item['_id']), raw_item['title'], list, raw_item['last_modified'])
                items.append(item)
        return items

    def add_item(self, title, list):
        result = self.db[list].insert_one({'title': title, 'last_modified': datetime.now()})
        return result.inserted_id

    def delete_item(self, id, list):
        self.db[list].delete_one({'_id': ObjectId(id)})

    def move_item(self, id, from_list, to_list):
        item = self.db[from_list].find_one({'_id': ObjectId(id)})
        new_id = self.add_item(item['title'], to_list)
        self.delete_item(id, from_list)
        return new_id

    def delete_all_items(self):
        for list in self.lists:
            self.db[list].delete_many({})