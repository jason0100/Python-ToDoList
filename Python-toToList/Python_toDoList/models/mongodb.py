
"""
Repository of polls that stores data in a MongoDB database.
"""

from bson.objectid import ObjectId, InvalidId
from pymongo import MongoClient

from . import toDoItem, toDoList, toDoNotFound

import json


def _todolist_from_doc(doc):
    """Creates a poll object from the MongoDB poll document."""
    return toDoList(str(doc['_id']), doc['name'], doc['items'])

def _todoitem_from_doc(doc):
    """Creates a choice object from the MongoDB choice subdocument."""
    return toDoItem(str(doc['id']), doc['name'], doc['date'])

class Repository(object):
    """MongoDB repository."""
    def __init__(self, settings):
        """Initializes the repository with the specified settings dict.
        Required settings are:
         - MONGODB_HOST
         - MONGODB_DATABASE
         - MONGODB_COLLECTION
        """
        self.name = 'MongoDB'
        self.host = settings['MONGODB_HOST']
        self.client = MongoClient(self.host)
        self.database = self.client[settings['MONGODB_DATABASE']]
        self.collection = self.database[settings['MONGODB_COLLECTION']]

    def get_todolists(self):
        """Returns all  from the repository."""
        docs = self.collection.find()
        print('MONGODB_COLLECTION='+str(self.collection))
        print('get_todolists='+str(docs.count()))
        lists = [_todolist_from_doc(doc) for doc in docs]
        return lists

    

    def add_list(self, name):
        result =['status', 'msg']
        print('mongodb.py >>>add_list(self, name):='+str(name))
        doc = self.collection.find_one({'name':name})
        #if doc is not None:
        #    result[0]='error'
        #    result[1]='List Duplicated.'
            
           
        #else:
        list_doc = {
            'name': name,
            'items':[]
        }
        addResult = self.collection.insert(list_doc)
        print('addResult='+str(addResult))

        if addResult!='':
            result[0]='success'
            result[1]='Add list success.'
        else:
            result[0]='error'
            result[1]='DB error'
        
        print(str(result))
        
        return result

    def del_list(self, key):
        result =['status', 'msg']
        print('mongodb.py >>>del_list(self, key)='+str(key))
       
        delResult = self.collection.remove({'_id':ObjectId(key)})
        print('delResult='+str(delResult))
        if delResult['ok']==1.0:
            result[0]='success'
            result[1]='Delete list success.'
        else:
            result[0]='error'
            result[1]='List not exist.'
        
        print(str(result))
        
        return result