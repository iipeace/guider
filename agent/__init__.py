'''
$ cd guider
$ export FLASK_APP=agent
$ flask run
'''
import os
import sys
import json
import re

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, send, emit

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

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
    def get_requestStatus(cls, request_id):
        print(cls.requests)
        return cls.requests.get(request_id)

    @classmethod
    def clear_request(cls):
        cls.requests.clear()

SERVER_ADDR = "http://localhost:5000" # default Server ip/port (local)

class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        # Default is '{{' but Vue.js uses '{{' / '}}'
        variable_start_string='%%',
        # Default is '}}' but Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))

app = CustomFlask(__name__, 
        template_folder='templates',
        static_folder='../guider-vue/static')

# app.config['SECRET_KEY'] = 'XXXX'
socketio = SocketIO(app)

#add guider path here
curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../guider' % curDir)

from guider import NetworkManager
@app.route('/')
def index():
    return render_template('index.html', server_addr=request.host_url)

@socketio.on('connect')
def connected():
    print("Connected") 

@socketio.on('disconnect')
def disconnected():
    RequestManager.clear_request()

@socketio.on('request_start')
def request_start(timestamp, targetAddr):
     
    NetworkManager.prepareServerConn(None, targetAddr)
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

    print('Requested ----- ')
    msg = {}
    msg['timestamp'] = timestamp
    RequestManager.add_request(timestamp)
    is_connected = RequestManager.get_requestStatus(timestamp)
    cntGetData = -1
    while (is_connected != False):
        str_pipe = pipe.getData() # str type with json contents
        cntGetData = cntGetData + 1
        if pipe.getDataType(str_pipe) == 'JSON':
            try: 
                json_pipe = json.loads(str_pipe)
                msg['cpu_pipe'] = json.dumps(json_pipe["cpu"])
                msg['mem_pipe'] = json.dumps(json_pipe["mem"])
                msg['proc_pipe'] = json.dumps(json_pipe["process"])
                length_pipe = len(str_pipe)
                msg['length_pipe'] = str(length_pipe)
                emit('server_response', msg)
            except:
                print("[" + str(cntGetData) + "]----------------Json parsing error----------------")
        is_connected = RequestManager.get_requestStatus(timestamp)
        print("is_connected : " + str(is_connected) + " / timestamp : " + timestamp)
        # time.sleep should not be used for its blocking thread or something.
        # (related articles are found over stackoverflow or somewhere else)


@socketio.on('request_stop')
def request_stop(target_timestamp):
    if RequestManager.get_requestStatus(target_timestamp) == True:
        RequestManager.disable_request(target_timestamp)
        emit('request_stop_result', 'stop success : ' + target_timestamp)
    else:
        emit('request_stop_result', 'stop failed : ' + target_timestamp )
    return

if __name__ == '__main__':
    app.logger.info("Flask is running on {0}".format(str(SERVER_ADDR)))
    request_manager = RequestManager()
    socketio.run(app, host='0.0.0.0', port=5000)

