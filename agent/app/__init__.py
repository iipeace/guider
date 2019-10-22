from app.config import config_dict, config_database
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_socketio import SocketIO
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from monitoring.controllers import Main, Slack, Devices, Dataset
from monitoring.services import get_dashboard_data, stop_command_run, get_data_by_command, health_check
is_connected = False


def create_app(config_name):
    f_config = config_dict[config_name]
    app = Flask(__name__,
                template_folder=f_config.STATIC_FOLDER,
                static_url_path='',
                static_folder=f_config.STATIC_FOLDER)
    CORS(app, resources={
        r"/dataset/*": {"origin": "*"},
        r"/devices/*": {"origin": "*"},
        r"/slack/*": {"origin": "*"},
    })
    app.config.from_object(f_config)
    app.config['MONGODB_SETTINGS'] = config_database

    socket = SocketIO(app)
    socket.init_app(app, cors_allowed_origins="*")
    print('Attempt to connect to MongoDB...')
    global is_connected
    client = MongoClient()
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        is_connected = True
        print('Connected to MongoDB!')
    except ConnectionFailure:
        print('Failed to connect to MongoDB. You should restart server to reconnect!')
        is_connected = False

    api = Api(app)

    api.add_resource(Main, '/', '/<path:path>')
    api.add_resource(Dataset, '/dataset')
    api.add_resource(Devices, '/devices')
    api.add_resource(Slack, '/slack/')

    socket.on_event('get_dashboard_data', get_dashboard_data)
    socket.on_event('get_data_by_command', get_data_by_command)
    socket.on_event('stop_command_run', stop_command_run)
    socket.on_event('health_check', health_check)
    return app, socket

