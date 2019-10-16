from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

from app.config import config_dict, config_database
from monitoring.models import db
from monitoring.controllers import Main, Slack, Dataset
from monitoring.services import get_dashboard_data, disconnect_with_guider, get_data_by_command


def create_app(config_name):
    f_config = config_dict[config_name]
    app = Flask(__name__,
                template_folder=f_config.STATIC_FOLDER,
                static_url_path='',
                static_folder=f_config.STATIC_FOLDER)
    CORS(app, resources={
        r"/dataset/*": {"origin": "*"},
        r"/slack/*": {"origin": "*"},
    })
    app.config.from_object(f_config)
    app.config['MONGODB_SETTINGS'] = config_database

    socket = SocketIO(app)
    socket.init_app(app, cors_allowed_origins="*")

    try:
        db.init_app(app)
    except Exception as e:
        print('Failed to connect MongoDB', e)

    api = Api(app)

    api.add_resource(Main, '/', '/<path:path>')
    api.add_resource(Dataset, '/dataset')
    api.add_resource(Slack, '/slack/')

    socket.on_event('get_dashboard_data', get_dashboard_data)
    socket.on_event('get_data_by_command', get_data_by_command)
    socket.on_event('request_stop', disconnect_with_guider)
    return app, socket
