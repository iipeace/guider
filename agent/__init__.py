'''
$ cd guider
$ export FLASK_APP=agent
$ flask run
'''
import os
import sys
import json

from flask import Flask
app = Flask(__name__)

#add guider path here
curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../guider' % curDir)

from guider import NetworkManager

NetworkManager.prepareServerConn('127:0.0.1:5555', None)

# get connection with server #
conn = NetworkManager.getServerConn()
if not conn:
    print('\nFail to get connection with server')
    sys.exit(0)

# request command #
pipe = NetworkManager.getCmdPipe(conn, 'GUIDER top -a -j')
if not pipe:
    print('\nFail to get command pipe')
    sys.exit(0)

@app.route('/')
def hello_world():
    return pipe.getData() 