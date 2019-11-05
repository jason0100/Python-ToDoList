"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request, jsonify
from Python_toDoList import app
from Python_toDoList.models import toDoNotFound
from Python_toDoList.models.factory import create_repository
from Python_toDoList.settings import REPOSITORY_NAME, REPOSITORY_SETTINGS

import json
repository = create_repository(REPOSITORY_NAME, REPOSITORY_SETTINGS)
print('REPOSITORY_SETTINGS='+str(REPOSITORY_SETTINGS))


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/seed', methods=['POST'])
def seed():
    """Seeds the database with sample polls."""
    repository.add_sample_todolist()
    return redirect('/todolist')

@app.route('/todolists/all', methods=['GET'])
def todolists_all():
    return render_template(
        'todolists.html',
        title='To Do List',
        year=datetime.now().year,
        todolists = repository.get_todolists(),
        message='test'
    )


@app.route('/todolist', methods=['GET'])
def todolist_name():
    print('Here is def todolist_name(): function')
    if 'todolist_name' in request.args:
        todolist_name = request.args['todolist_name']
        print('todolist_name='+todolist_name)
    else:
        return 'Error:No ToDoList provided. Please specify a ToDoList name.'
    
    list = repository.get_todolist(todolist_name)
    print('list='+str(list))
    #return jsonify(list)
    #return list
    return render_template(
        'todolist.html',
        title=list.text,
        year=datetime.now().year,
        todolist = list,
        message = str(list),
    
    )


class result:
    def __init__(self):
        self.status=""
        self.msg=''


@app.route('/todolist',methods=['POST'])
def addList():
    
    data = request.get_json()#from body
    print('view data = '+str(data))
    res=result()
 
    res = repository.add_list(data['name'])
    jsondata=json.dumps(res)
    print('jsondata= '+str(jsondata))
    return jsondata

@app.route('/todolist/<key>', methods=['PUT'])
def editList(key):
    print('ok')
    data = request.get_json()#from body
    print('name='+str(data))
    res=result()
    print('key={key},name={name}'.format(key=str(key),name=str(data['name'])))
    print('PUT')
    res = repository.edit_list(key,data['name']) 
    jsondata=json.dumps(res)
    return jsondata

@app.route('/todolist/<key>', methods=['DELETE'])
def delList(key):
    res=result()
    print('key='+str(key))
    print('delete')
    res = repository.del_list(key) 
    jsondata=json.dumps(res)
    print('jsondata= '+jsondata)
    return jsondata
    
#######ToDo Item#######
@app.route('/todoitem',methods=['POST'])
def addItem():
    todolist_name = request.args['todolist_name']

    print('todolist_name='+todolist_name)
    
    data = request.get_json()
    print(' str(data[name]).strip()='+ str(data['name']).strip()+"*")
    if str(data['name']).strip()=='':#後端防空白字串
        print('empty')
        jsondata=['error','ItemName is empty.']
        jsondata=json.dumps(jsondata)
    else:
        print('data='+ str(data))
        res = result()
        res=repository.add_item(todolist_name, data['name'])
        jsondata=json.dumps(res)
        print('jsondata= '+jsondata)
    return jsondata

 
@app.route('/todoitem',methods=['PUT'])
def editItem():
   
    data = request.get_json()
    print('data='+ str(data))
    res = result()
    res=repository.edit_item(data['todolist_name'], data['id'],data['newName'])
    jsondata=json.dumps(res)
    print('jsondata= '+jsondata)
    return jsondata


@app.route('/todoitem/', methods=['DELETE'])
def delItem():
    todolist_name = request.args['todolist_name']
    
    todoitem_name = request.args['todoitem_name']
    print('todolist_name={list},todoitem_name={item}'.format(list=str(todolist_name),item=str(todoitem_name)))
    
    res=result()
    
    print('delete')
    res = repository.del_item(todolist_name,todoitem_name) 
    jsondata=json.dumps(res)
    print('jsondata= '+jsondata)
    return jsondata
