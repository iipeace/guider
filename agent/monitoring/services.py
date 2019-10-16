import sys
import json

from flask_socketio import emit
from monitoring.models import CPU, Memory, Network, Storage, Data
from common.guider import GuiderInstance, RequestManager


def save_database(msg):
    try:
        cpu = CPU(kernel=msg['cpu']['kernel'], user=msg['cpu']['user'],
                  irq=msg['cpu']['irq'], nrCore=msg['cpu']['nrCore'],
                  total=msg['cpu']['total'])

        memory = Memory(kernel=msg['memory']['kernel'],
                        cache=msg['memory']['cache'],
                        free=msg['memory']['free'],
                        anon=msg['memory']['anon'],
                        total=msg['memory']['total'])

        network = Network(inbound=msg['network']['inbound'],
                          outbound=msg['network']['outbound'])

        storage = Storage(free=msg['storage']['free'],
                          usage=msg['storage']['usage'],
                          total=msg['storage']['total'])

        data = Data(cpu=cpu, memory=memory, network=network,
                    storage=storage, mac_addr=msg['mac_addr'])
        data.save()

        print('database saved in mongodb!')
    except Exception as e:
        print('failed to save instance in MongoDB', e)


def get_data_by_command(timestamp, target_addr, cmd):

    result = dict(result=0, data=dict(), errMsg='')
    if cmd is None or cmd is '':
        result['result'] = -1
        result['errorMsg'] = 'Required data missing'
        emit('set_command_data', result)
        sys.exit(0)

    pipe = GuiderInstance.get_instance(target_addr).run_cmd(cmd)
    RequestManager.add_request(timestamp)

    while RequestManager.get_requestStatus(timestamp):
        str_pipe = pipe.getData()
        if not str_pipe:
            result['result'] = -1
            emit('set_command_data', result)
            pipe.close()
            RequestManager.clear_request()
            break
        result['data'] = str_pipe
        emit('set_command_data', result)


def get_dashboard_data(timestamp, target_addr):

    result = dict(result=0, data=dict(), errMsg='')
    # execute remote command for real-time visualization #
    cmd = 'GUIDER top -J -a -e dn'
    pipe = GuiderInstance.get_instance(target_addr).run_cmd(cmd)
    if not pipe:
        print('\nFail to execute remote command')
        result['result'] = -1
        emit('set_dashboard_data', result)
        RequestManager.clear_request()
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

                msg = dict(timestamp=json_pipe['timestamp'],
                           mac_addr=json_pipe['net']['repmac'])

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
                # # storage
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

                result = dict(result=0, data=msg)
                emit('set_dashboard_data', result)

            except (json.decoder.JSONDecodeError, KeyError) as e:
                print(str_pipe)
                print(e)
                line = '-' * 50
                print("%s\n%s\n%s" % (line, len(str_pipe), line))
                result['result']= -1
                result['errorMsg'] =e
                emit('set_dashboard_data', result)
                pipe.close()
            except Exception as e:
                print('Error occured', e)
                result['result']= -1
                result['errorMsg'] =e
                emit('set_dashboard_data', result)
                pipe.close()
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
