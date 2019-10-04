import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    Debug = False
    Testing = False
    # MONGO_SERVER = 'localhost'
    STATIC_FOLDER = '../static'
    THREADS_PER_PAGE = 2


class DevelopmentConfig(Config):
    Debug = True
    DEVELOPMENT = True


class TestingConfig(Config):
    Testing = True


class ProductConfig(Config):
    Debug = False


config_dict = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductConfig
)