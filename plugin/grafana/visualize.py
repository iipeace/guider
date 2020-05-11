import json
import sys

from common.guider import GuiderInstance, RequestManager


def get_data_by_command(target_addr, request_id, cmd):
    result = dict(result=0, data=dict(), errMsg='')
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
            print(result)
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


if __name__ == '__main__':
    get_data_by_command(sys.argv[1], 1, "GUIDER top -J")
