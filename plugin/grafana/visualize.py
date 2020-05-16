import json
import pprint
import sys

from common.guider import GuiderInstance, RequestManager
from influxdb import InfluxDBClient


def get_data_by_command(target_addr, request_id, cmd):
    result = dict(result=0, data=dict(), errMsg='')
    pipe = None
    if cmd is None or cmd is '' or target_addr is None or target_addr is '':
        result['result'] = -1
        result['errorMsg'] = 'Required data missing'
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
            insert_db(result)
            pprint.pprint(result)
        pipe.close()
        stop_command_run(request_id)
    except Exception as e:
        print(e)
        if pipe:
            pipe.close()
        stop_command_run(request_id)


def stop_command_run(request_id):
    result = dict(result=0, data='stop success', errMsg='')
    if RequestManager.get_request_status(request_id):
        RequestManager.stop_request(request_id)
    else:
        result['result'] = -1
        result['errMsg'] = 'stop failed'


def setup_db(host, port):
    user = config['influxDBClientConfig']['user']
    password = config['influxDBClientConfig']['password']
    db_name = config['influxDBClientConfig']['database']
    db_user = config['influxDBClientConfig']['db_user']
    db_user_password = config['influxDBClientConfig']['db_password']

    client = InfluxDBClient(host, port, user, password, db_name)

    if not {'name': db_name} in client.get_list_database():
        client.create_database(db_name)
        client.create_retention_policy('awesome_policy', '3d', 3, default=True)
    client.switch_user(db_user, db_user_password)

    return client


def insert_db(guider_data):
    pass


if __name__ == '__main__':
    global config
    with open('./visualization.conf', 'r') as config_file:
        config = json.load(config_file)
    try:
        setup_db(config['influxDBClientConfig']['host'], config['influxDBClientConfig']['port'])
    except Exception as e:
        print(e)
    get_data_by_command(sys.argv[1], 1, 'GUIDER top -J')
