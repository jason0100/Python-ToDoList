
"""
Settings for the polls application.

You can set values of REPOSITORY_NAME and REPOSITORY_SETTINGS in
environment variables, or set the default values in code here.
"""

from os import environ

REPOSITORY_NAME = environ.get('REPOSITORY_NAME', 'mongodb')

if REPOSITORY_NAME == 'azuretablestorage':
    REPOSITORY_SETTINGS = {
        'STORAGE_NAME': environ.get('STORAGE_NAME', ''),
        'STORAGE_KEY': environ.get('STORAGE_KEY', ''),
        'STORAGE_TABLE_POLL': environ.get('STORAGE_TABLE_POLL', 'todolists'),
        'STORAGE_TABLE_CHOICE': environ.get('STORAGE_TABLE_CHOICE', 'todoitems'),
    }
elif REPOSITORY_NAME == 'mongodb':
    REPOSITORY_SETTINGS = {
        'MONGODB_HOST': environ.get('MONGODB_HOST', 'localhost:27017'),
        'MONGODB_DATABASE': environ.get('MONGODB_DATABASE', 'ToDoList'),
        'MONGODB_COLLECTION': environ.get('MONGODB_COLLECTION', 'lists'),
    }
elif REPOSITORY_NAME == 'memory':
    REPOSITORY_SETTINGS = {}
else:
    raise ValueError('Unknown repository.')
