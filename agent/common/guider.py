import sys
import os

curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../../guider' % curDir)
from guider import NetworkManager


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


class GuiderInstance(object):
    _target_addr = None
    _network_manager = None
    __instance = None

    @staticmethod
    def get_instance(target_addr):
        if GuiderInstance.__instance is None or \
                GuiderInstance.__instance and \
                GuiderInstance.__instance.get_target_addr() != target_addr:
            GuiderInstance(target_addr)
        return GuiderInstance.__instance

    def __init__(self, target_addr):
        self.target_addr = target_addr
        self._network_manager = NetworkManager(mode=None, ip=None, port=None)
        self._network_manager.prepareServerConn(None, target_addr)
        GuiderInstance.__instance = self

    def get_target_addr(self):
        return self.target_addr

    def run_cmd(self, cmd):
        pipe = self._network_manager.execRemoteCmd(cmd)
        if not pipe:
            raise Exception("FAIL Connect with guider")
        return pipe

    def stop_cmd(self, pipe):
        pipe.close()
