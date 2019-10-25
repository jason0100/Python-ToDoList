"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, redirect, request
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

@app.route('/todolist')
def todolist():
    return render_template(
        'todolist.html',
        title='To Do List',
        year=datetime.now().year,
        todolists = repository.get_todolists(),
        message='test'
    )

@app.route('/todoitems/<key>', methods=['GET','POST'])
def todoitems(key):
    error_message = ''

    return render_template(
        'todoitems.html',
        title='List',
        todolist=repository.get_todolist(key),
        error_message = error_message
        )

class result:
    def __init__(self):
        self.status=""
        self.msg=''


@app.route('/todolist',methods=['POST'])
def addList():
    #get
    #name=request.args.get('name')
    #post
    data = request.get_json()
    
    res=result()
 
    res = repository.add_list(data['name'])
    jsondata=json.dumps(res)
    print('jsondata= '+str(jsondata))
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
    
