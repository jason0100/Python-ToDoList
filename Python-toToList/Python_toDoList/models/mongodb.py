
"""
Repository of polls that stores data in a MongoDB database.
"""

from bson.objectid import ObjectId, InvalidId
from pymongo import MongoClient
from flask import jsonify

from . import toDoItem, toDoList, toDoNotFound

import json
import uuid


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
        docs = self.collection.find().sort([['_id',-1]])
        print('MONGODB_COLLECTION='+str(self.collection))
        print('get_todolists='+str(docs.count()))
        #處理objectid
        lists = [_todolist_from_doc(doc) for doc in docs]
        return lists

    def get_todolist(self, todolist_name):
        result =['status', 'msg']
        print('mongodb.py='+todolist_name)
        doc = self.collection.find_one({'name':todolist_name})
        print('doc='+str(doc))
        list = _todolist_from_doc(doc)
        
        #jsondocs=json.dumps(_todolist_from_doc)
        #print('docs='+str(_todolist_from_doc))
        #print('list='+json.dumps(list))
        #return jsonify(docs)
        #return str(_todolist_from_doc)
        return list



    def add_list(self, name):
        result =['status', 'msg']
        print('mongodb.py >>>add_list(self, name):='+str(name))
        doc = self.collection.find_one({'name':name})
        if doc is not None:
            result[0]='error'
            result[1]='List Duplicated.'
            
           
        else:
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

    def edit_list(self,key,name):
        result =['status', 'msg']
        print('mongodb.py >>>edit_list(self, key)='+str(key)+'/'+str(name))
        doc = self.collection.find_one({'_id':ObjectId(key)})
        if doc is None:
            result[0]='error'
            result[1]='List is not exist.'
        else:
            result[0]='success'
            result[1]='Edit list success.'
            self.collection.update(doc,{"$set":{"name":name}})
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

    def add_item(self, todolist_name, todoitem_name):
        result =['status', 'msg']
        print('add_item >>>='+str(todolist_name)+ str(todoitem_name))
        doc = self.collection.find_one({'name':todolist_name})
        itemsList = doc['items']
        for index,item in enumerate(itemsList):
            print(index)
            print(item)
        if doc is  None:
            result[0]='error'
            result[1]='List not exist.'
            print('if doc is  None:')
        else:
            print('==========if doc is  Not None:')
            #query = []
            query = self.collection.find_one({'name':todolist_name,"items":{"$elemMatch":{"name":todoitem_name}}})
            print(str(query))
            if query is None:
                try:
                    item_doc = {
                            'id':uuid.uuid1(),
                            #'id':query['items'].count(),
                            'name':todoitem_name,
                            }
                    #push object to an array in collection

                    print('item_doc='+str(item_doc['id']))
                    self.collection.update(doc,{'$push':{"items":item_doc}})
                    print('test')
                    result[0]='success'
                    result[1]='Add Item success.'
                except:
                    result[0]='error'
                    result[1]='DB error.'
            else:
                result[0]='error'
                result[1]='Item exist.'
                
        print(str(result))
        return result

    def edit_item(self,todolist_name, id, newName):
        result =['status', 'msg']
        print('mongodb.py >>>edit_item(self,todolist_namem id, newName)='+str(todolist_name)+'/'+str(id)+'/'+str(newName))
        doc = self.collection.find_one({'name':todolist_name})
        query_oldName = self.collection.find_one({'name':todolist_name,"items.id":uuid.UUID(id)})
        query_newName = self.collection.find_one({'name':todolist_name,"items.name":newName})
        #print('query='+str(query_newName))
        if doc is None:
            result[0]='error'
            result[1]='List is not exist.'
        elif query_oldName is None:
            result[0]='error'
            result[1]='Item is not exist.'
        elif query_newName is not None:
            result[0]='error'
            result[1]='New name duplicate.'
          
        else:
            itemsList = doc['items']
            for i in itemsList:
                print(i['id'])
            if query_oldName is not None:
                self.collection.update({'name':todolist_name,"items.id":uuid.UUID(id)},{"$set":{"items.$.name":newName}})
                result[0]='success'
                result[1]='Edit item success.'
            else:
                result[0]='error'
                result[1]='Item not exist.'
        return result

    def del_item(self, todolist_name, todoitem_name):
       result =['status', 'msg']
       print('Mongodb=>>>>>>todolist_name={list},totoitem_name={item}'.format(list=str(todolist_name),item=str(todoitem_name)))
       doc = self.collection.find_one({'name':todolist_name})
       if doc is  None:
            result[0]='error'
            result[1]='List not exist.'
            print('if doc is  None:')
       else:
           itemsList = doc['items']
           print('doc='+str(doc))
           #query = self.collection.find_one({"items":{"$elemMatch":{"name":todoitem_name}}})
           query = self.collection.find_one({"items.name":todoitem_name})
           print('query='+str(query))
           if query is not None:
             self.collection.update(doc,{"$pull":{"items":{"name":todoitem_name}}})
             result[0]='success'
             result[1]='Delete item success.'
     
           else:
                result[0]='error'
                result[1]='Item not exist.'
        
           print(str(result))
       return result
        
   