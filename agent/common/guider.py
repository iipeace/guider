class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class GuiderInstance(Singleton):
    def __init__(self):
        self.target_addr = ''
        self.is_connected = False
        