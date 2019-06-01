'''
$ cd guider
$ export FLASK_APP=agent
$ flask run
'''

import os
import sys
import json

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit

class RequestManager(object):
    requests = {}

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(RequestManager, self).__new__(self)
            return self.instance

    @classmethod
    def add_request(cls, request_id):
        cls.requests[request_id] = True

    @classmethod
    def disable_request(cls, request_id):
        cls.requests[request_id] = False

    @classmethod
    def get_request(cls, request_id):
        return cls.requests.get(request_id)

    @classmethod
    def clear_request(cls):
        cls.requests.clear()

SERVER_ADDR = "http://0.0.0.0:5000" # default Server ip/port (local)

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        # Default is '{{' but Vue.js uses '{{' / '}}'
        variable_start_string='%%',
        # Default is '}}' but Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__, template_folder='./templates')

# app.config['SECRET_KEY'] = 'XXXX'
socketio = SocketIO(app)

# add guider path here
curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../guider' % curDir)

from guider import NetworkManager

NetworkManager.prepareServerConn(None, None)

# get connection with server #
conn = NetworkManager.getServerConn()
if not conn:
    print('\nFail to get connection with server')
    sys.exit(0)

# request command #
pipe = NetworkManager.getCmdPipe(conn, 'GUIDER top -a -J')
if not pipe:
    print('\nFail to get command pipe')
    sys.exit(0)

@app.route('/')
def index():
    return render_template('index_vue.html', server_addr=SERVER_ADDR)

@socketio.on('connect')
def connected():
    print("This is real-connect message") # this works naturally

@socketio.on('disconnect') # Not Custom
def disconnected():
    RequestManager.clear_request()
#    print("Client is disconnected")

@socketio.on('custom_connect') # this is custom one
def custom_connect(msg):
#    print("This Customed-connected_event!")
    emit('server_response', {'data': msg})

@socketio.on('request_start')
def request_start(timestamp, msg):
    msg['timestamp'] = timestamp
    RequestManager.add_request(timestamp)
    is_connected = RequestManager.get_request(timestamp)
    while (is_connected==True):
        str_pipe = pipe.getData() # str type with json contents
        length_pipe = len(str_pipe)
        msg['length_pipe'] = str(length_pipe)
        msg['str_pipe'] = str_pipe
        print('Emit length : ', msg['length_pipe'])
        emit('server_response', msg)
        is_connected = RequestManager.get_request(timestamp)
    #connected(msg)

@socketio.on('request_stop')
def request_stop(target_timestamp):
    if RequestManager.get_request(target_timestamp) == True:
        RequestManager.disable_request(target_timestamp)
        emit('request_stop_result', 'stop success : ' + target_timestamp)
    else:
        emit('request_stop_result', 'stop failed : ' + target_timestamp )
    return

if __name__ == '__main__':
    app.logger.info("Flask is running on {0}".format(str(SERVER_ADDR)))
    request_manager = RequestManager()
    socketio.run(app, host='0.0.0.0', port=5000)

#@app.route('/')
#def hello_world():
#    return pipe.getData()
