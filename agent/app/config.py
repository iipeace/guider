import os

basedir = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = '../static'


class Config:
    Debug = False
    Testing = False
    # MONGO_SERVER = 'localhost'


class DevelopmentConfig(Config):
    Debug = True
    # define default address #
    IP = 'localhost'
    PORT = 8080


class TestingConfig(Config):
    Testing = True


class ProductConfig(Config):
    Debug = False


config_dict = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductConfig
)