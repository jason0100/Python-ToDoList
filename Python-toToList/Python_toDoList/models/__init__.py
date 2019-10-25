from os import path
import json
import pymongo
from pymongo import MongoClient


conn = MongoClient('localhost', 27017)
db = conn.ToDoList
collection = db.lists
collection_count=collection.count()
print('count='+str(collection_count))
if collection_count==0:
    list = {
        'name':'testList',
        'items':[
            {
              'name':'item1',
             'date':'2019-10-23'
             }
            ]
        }

    result = collection.insert_one(list)
    print('result='+str(result))

class toDoItem(object):
    def __init__(self, key=u'',text=u''):
        """Initializes thie toDoItem"""
        self.key = key
        self.text = text

class toDoList(object):
    def __init__(self, key = u'', text=u'', todoitems=u''):
        """Initializes thie toDoList"""
        self.key = key
        self.text = text
        self.toDoItems = todoitems

class toDoNotFound(Exception):
    """Exception raised when a toDoItem/toDoList object couldn't be retrieved from
    the repository."""
    pass

def _load_samples_json():
    samples_path = path.join(path.dirname(__file__), 'samples.json')
    with open(samples_path, 'r') as samples_file:
        return json.load(samples_file)