#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import essential packages #
try:
    import os
    import sys
    import json
    import re
    import logging

    from threading import Lock
    from flask import Flask, render_template, request, jsonify
    from flask_socketio import SocketIO, send, emit
except ImportError:
    err = sys.exc_info()[1]
    print("[Error] Fail to import python default packages: %s" % err.args[0])
    sys.exit(0)


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
        return cls.requests.get(request_id)

    @classmethod
    def clear_request(cls):
        cls.requests.clear()


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        # Default is '{{' but Vue.js uses '{{' / '}}'
        variable_start_string='%%',
        # Default is '}}' but Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


def createApp(config_filename=None):
    # define flask object #
    app = CustomFlask(__name__,
                      template_folder='./static',
                      static_url_path='',
                      static_folder='./static')
    if config_filename:
        app.config.from_pyfile(config_filename)

    # app.config['SECRET_KEY'] = 'XXXX'
    socketio = SocketIO(app)

    # add Guider path here #
    curDir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, '%s/../guider' % curDir)

    # import NetworkManger form Guider #
    from guider import NetworkManager

    @app.route('/')
    def index():
        print("route /")

        return render_template('index.html', server_addr=request.host_url)

    @socketio.on('connect')
    def connected():
        print("connect")

    @socketio.on('disconnect')
    def disconnected():
        print("disconnect")

        RequestManager.clear_request()

    @socketio.on('request_start')
    def request_start(timestamp, targetAddr):
        print('request_start')

        # set addresses #
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

        # build message #
        msg = {}
        msg['timestamp'] = timestamp
        RequestManager.add_request(timestamp)

        '''
        # for multi-thread feautre #
        global thread
        with thread_lock:
        if thread is None:
        thread = socketio.start_background_task(thread_task)
        '''

        while RequestManager.get_requestStatus(timestamp):
            # read data from Guider #
            str_pipe = pipe.getData()
            if not str_pipe:
                break

            print('got a message from Guider at %s' % timestamp)

            data_type = pipe.getDataType(str_pipe)
            if data_type == 'JSON':
                try:
                    # convert string to JSON #
                    json_pipe = json.loads(str_pipe)

                    # split stats #
                    msg['cpu_pipe'] = json.dumps(json_pipe["cpu"])
                    msg['mem_pipe'] = json.dumps(json_pipe["mem"])
                    msg['proc_pipe'] = json.dumps(json_pipe["process"])
                    msg['length_pipe'] = str(len(str_pipe))

                    emit('server_response', msg)
                except:
                    line = '-' * 50
                    print("%s\n%s\n%s" % (line, len(str_pipe), line))
            else:
                print('[%s] %s' % (data_type, str_pipe))

        print('request_finished')

    @socketio.on('custom_connect')  # this is custom one
    def custom_connect(msg):
        print("custom_connect")

        emit('server_response', {'data': msg})

    @socketio.on('request_stop')
    def request_stop(target_timestamp):
        print("request_stop")

        if RequestManager.get_requestStatus(target_timestamp) == True:
            RequestManager.disable_request(target_timestamp)
            emit('request_stop_result', 'stop success : ' + target_timestamp)
        else:
            emit('request_stop_result', 'stop failed : ' + target_timestamp)
        return

    return app, socketio


if __name__ == '__main__':
    # set log level #
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # create flask app #
    app, socketio = createApp()

    # define default address #
    DEFIP = '0.0.0.0'
    DEFPORT = 5000

    # parse address for binding #
    if len(sys.argv) > 1:
        addrList = sys.argv[1].split(':')
        if len(addrList) == 2:
            ip, port = addrList
        elif len(addrList) == 1:
            if '.' in addrList[0]:
                ip = addrList[0]
                port = DEFPORT
            else:
                ip = DEFIP
                port = addrList[0]
        else:
            print('input IP:PORT')
            sys.exit(0)
    else:
        ip = DEFIP
        port = DEFPORT

    # run app #
    socketio.run(app, host=ip, port=port)
