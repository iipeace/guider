import sys
import json


from flask_socketio import emit


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


def communicate_with_guider(timestamp, targetAddr):
    import os
    curDir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, '%s/../../guider' % curDir)
    from guider import NetworkManager

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
            except (json.decoder.JSONDecodeError, KeyError):
                line = '-' * 50
                print("%s\n%s\n%s" % (line, len(str_pipe), line))
        else:
            print('[%s] %s' % (data_type, str_pipe))

    print('request_finished')


def disconnect_with_guider(target_timestamp):
    print("request_stop")
    if RequestManager.get_requestStatus(target_timestamp):
        RequestManager.disable_request(target_timestamp)
        emit('request_stop_result', 'stop success : ' + target_timestamp)
    else:
        emit('request_stop_result', 'stop failed : ' + target_timestamp)
