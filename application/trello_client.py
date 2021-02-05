from bson.objectid import ObjectId
from datetime import datetime
import os
import pymongo

from application.item import Item

class TrelloClient:

    def __init__(self):

        self.MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
        self.MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
        self.MONGO_HOST = os.environ.get('MONGO_HOST')
        self.MONGO_TODO_APP_DATABASE = os.environ.get('MONGO_TODO_APP_DATABASE')
        self.client = pymongo.MongoClient(f"mongodb+srv://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}/?retryWrites=true&w=majority")
        self.db = self.client[self.MONGO_TODO_APP_DATABASE]

        self.refresh_lists()
        self.refresh_items()


    def refresh_lists(self):
        self.lists = self.db.list_collection_names()

    def refresh_items(self):
        self.refresh_lists()
        items = []
        for list in self.lists:
            raw_items = self.db[list].find()
            for raw_item in raw_items:
                item = Item(str(raw_item['_id']), raw_item['title'], list, raw_item['last_modified'])
                items.append(item)
        self.items = items

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