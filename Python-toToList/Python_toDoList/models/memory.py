from . import toDoItem, toDoList, toDoNotFound
from . import _load_samples_json

class Repository(object):
    def __init__(self, setting):
        self.name = 'In-Memory'
        self.index = {}

    def get_todolists(self):
        return self.index.values()

    def get_todolist(self, todolist_key):
        print('todolist_key='+str(todolist_key))
        todolist = self.index.get(todolist_key)
        if todolist is None:
            raise toDoNotFound()
        return todolist

    def add_sample_todolist(self):
        todolist_key = 0
        todoitem_key = 0
       
        for sample_todolist in  _load_samples_json():
            todolist = toDoList(str(todolist_key), sample_todolist['text'])
            print('todolist_key='+str(todolist_key))
            for sample_todoitem in sample_todolist['todoitems']:
                todolist.toDoItems.append(toDoItem(str(todoitem_key), sample_todoitem))
                todoitem_key +=1
                print('todoitem_key='+str(todoitem_key))

            self.index[str(todolist_key)] = todolist
            todolist_key += 1