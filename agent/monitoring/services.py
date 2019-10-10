import sys
import json

from flask_socketio import emit
from models import CPU, Memory, Storage, Network, Data

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

def save_database(msg):
    cpu = Cpu(kernel=msg['cpu']['kernel'],
                        user=msg['cpu']['user'],
                        irq=msg['cpu']['irq'],
                        nrCore=msg['cpu']['nrCore'],
                        total=msg['cpu']['total'])

    memory = Memory(kernel=msg['memory']['kernel'],
                            cache=msg['memory']['cache'],
                            free=msg['memory']['free'],
                            anon=msg['memory']['anon'],
                            total=msg['memory']['total'])

    network = Network(inbound=msg['network']['inbound'], outbound=msg['network']['outbound'])

    storage = Storage(free=msg['storage']['free'],
                            usage=msg['storage']['usage'],
                            total=msg['storage']['total'])

    data = Data(cpu=cpu, memory=memory, network=network, storage=storage)
    data.save()

    print('database saved in mongodb!')

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

                msg = dict(timestamp=json_pipe['timestamp'])

                # cpu
                cpu = json_pipe['cpu']
                msg['cpu'] = dict(kernel=cpu['kernel'],
                                  user=cpu['user'],
                                  irq=cpu['irq'],
                                  nrCore=cpu['nrCore'],
                                  total=cpu['total'])

                # memory
                memory = json_pipe['mem']
                msg['memory'] = dict(kernel=memory['kernel'],
                                     cache=memory['cache'],
                                     free=memory['free'],
                                     anon=memory['anon'],
                                     total=memory['total'])

                # storage
                storage = json_pipe['storage']['total']
                msg['storage'] = dict(free=storage['free'],
                                      usage=storage['usage'],
                                      total=storage['total'])

                # network
                network = json_pipe['net']
                msg['network'] = dict(
                    inbound=network['inbound'], outbound=network['outbound'])

                # save msg to db
                save_database(msg)

                #print msg!
                print(msg)

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
