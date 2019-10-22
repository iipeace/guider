import json
import sys
from datetime import datetime

from common.guider import GuiderInstance, RequestManager
from flask_socketio import emit
from monitoring.models import CPU, Memory, Network, Storage, Datas, Devices


def save_database(msg):
    from app import is_connected
    if not is_connected:
        print('Failed to connect mongodb. so messages would not be saved on database.')
        return
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

        data = Datas(cpu=cpu, memory=memory, network=network,
                     storage=storage, mac_addr=msg['mac_addr'])
        data.save()
        # refreshing Devices
        devices = Devices.objects(mac_addr=msg['mac_addr'])
        if len(devices) >= 1:
            for device in devices:
                device.update(
                    set__end=datetime.utcnow(),
                    set__count=device['count']+1
                )
        else:
            Devices(
                start=datetime.utcnow(),
                end=datetime.utcnow(),
                mac_addr=msg['mac_addr'],
                count=1
            ).save()
        print('database saved in mongodb!')
    except Exception as e:
        print('failed to save instance in MongoDB', e)


def get_data_by_command(target_addr, request_id, cmd):
    result = dict(result=0, data=dict(), errMsg='')
    if cmd is None or cmd is '' or target_addr is None or target_addr is '':
        result['result'] = -1
        result['errorMsg'] = 'Required data missing'
        emit(request_id, result)
        sys.exit(0)

    try:
        RequestManager.add_request(request_id)
        GuiderInstance.set_network_manager(target_addr)
        pipe = GuiderInstance.get_command_pipe(target_addr, cmd)
        while RequestManager.get_request_status(request_id):
            str_pipe = pipe.getData()
            if not str_pipe:
                break
            result['data'] = str_pipe.replace('\n', '</br>')
            emit(request_id, result)
        pipe.close()
        stop_command_run(request_id)
    except Exception as e:
        print(e)
        if pipe:
            pipe.close()
        stop_command_run(request_id)
        emit(request_id, result)


def parse_to_dashboard_data(data):
    json_pipe = json.loads(data)

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

    return msg


def get_dashboard_data(request_id, target_addr):
    result = dict(result=-1, data=dict(), errorMsg='')
    if target_addr is None or target_addr is '':
        result['errorMsg'] = 'Guider Address data missing'
        emit('set_dashboard_data', result)
        return None

    cmd = 'GUIDER top -J -a -e dn'
    try:
        GuiderInstance.set_network_manager(target_addr)
        pipe = GuiderInstance.get_command_pipe(target_addr, cmd)
    except Exception as e:
        print(e)
        result['errorMsg'] = 'Fail to connect with guider'
        emit('set_dashboard_data', result)
        return None

    RequestManager.add_request(request_id)

    while RequestManager.get_request_status(request_id):
        # read data from Guider #
        try:
            str_pipe = pipe.getData()
            if not str_pipe:
                result['errorMsg'] = 'Fail to connect with guider'
                emit('set_dashboard_data', result)
                break
            data_type = pipe.getDataType(str_pipe)
        except Exception as e:
            print(e)
            break

        if data_type == 'JSON':
            try:
                # convert, parse string to JSON #
                msg = parse_to_dashboard_data(pipe.getData())
                # save msg to db
                save_database(msg)
                # call web method
                result = dict(result=0, data=msg)
                emit('set_dashboard_data', result)
            except (json.decoder.JSONDecodeError, KeyError) as e:
                print(e)
                line = '-' * 50
                print("%s\n%s\n%s" % (line, len(str_pipe), line))
                result['errorMsg'] = e
                emit('set_dashboard_data', result)
                pipe.close()
            except Exception as e:
                print('Error occured', e)
                result['errorMsg'] = e
                emit('set_dashboard_data', result)
                pipe.close()
        else:
            print('not json')
            # print('[%s] %s' % (data_type, str_pipe))
            pass

    if pipe:
        pipe.close()
    RequestManager.stop_request(request_id)

    print('request_finished')


def stop_command_run(request_id):
    result = dict(result=0, data='stop success', errMsg='')
    stop_event = request_id + '_stop'
    if RequestManager.get_request_status(request_id):
        RequestManager.stop_request(request_id)
        emit(stop_event, result)
    else:
        result['result'] = -1
        result['errMsg'] = 'stop failed'
        emit(stop_event, result)


def health_check(target_addr, request_id):
    get_data_by_command(target_addr, request_id, 'GUIDER list')
