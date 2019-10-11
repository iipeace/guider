import sys
import os

curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../../guider' % curDir)
from guider import NetworkManager


class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class GuiderInstance(Singleton):
    def __init__(self):
        self.target_addr = ''
        self.conn = None

    @classmethod
    def connect(cls, target_addr):
        NetworkManager.prepareServerConn(None, target_addr)
        conn = NetworkManager.getServerConn()
        if not conn:
            raise Exception('Fail to get connection with server')
        cls.target_addr = target_addr
        cls.conn = conn