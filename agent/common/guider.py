import sys
import os

curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../../guider' % curDir)
from guider import NetworkManager


class SingleTonInstance(object):
    instances= {}

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(RequestManager, self).__new__(self)
            return self.instance


class RequestManager(SingleTonInstance):
    @classmethod
    def add_request(cls, request_id):
        cls.instances[request_id] = True

    @classmethod
    def disable_request(cls, request_id):
        cls.instances[request_id] = False

    @classmethod
    def get_requestStatus(cls, request_id):
        return cls.instances.get(request_id)

    @classmethod
    def clear_request(cls):
        cls.instances.clear()


class GuiderInstance(SingleTonInstance):

    @classmethod
    def set_network_manager(cls, target_addr):
        network_mgr = NetworkManager(mode=None, ip=None, port=None)
        network_mgr.prepareServerConn(None, target_addr)
        if target_addr not in cls.instances:
            cls.instances[target_addr] = network_mgr

    @classmethod
    def run_cmd(cls, target_addr, cmd):
        network_mgr = cls.instances.get(target_addr)
        pipe = network_mgr.execRemoteCmd(cmd)
        if not pipe:
            raise Exception("Fail to execute remote command")
        return pipe

    @classmethod
    def stop_connection(cls, target_addr):
        del cls.instances[target_addr]

    @classmethod
    def get_network_manager(cls, target_addr):
        if target_addr not in cls.instances:
            raise Exception('object is not exist')
        return cls.instances.get(target_addr)
