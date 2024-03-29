"""
This script runs the Python_toToList application using a development server.
"""

from os import environ
from Python_toDoList import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
   
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    #PORT = 5555
    #print('running port:'+str(PORT))
    #app.run(HOST, PORT)
    app.run(HOST, PORT, debug=True)
