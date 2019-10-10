from flask import Flask
from flask_restful import Api
from flask_socketio import SocketIO
from flask_cors import CORS

from app.config import config_dict, config_database
from monitoring.models import db
from monitoring.controllers import Main
from monitoring.services import communicate_with_guider, disconnect_with_guider


def create_app(config_name):
    f_config = config_dict[config_name]
    app = Flask(__name__,
                template_folder=f_config.STATIC_FOLDER,
                static_url_path='',
                static_folder=f_config.STATIC_FOLDER)
    app.config.from_object(f_config)
    app.config['MONGODB_SETTINGS'] = config_database
    CORS(app, resources={r"*": {"origins": "*"}})

    socket = SocketIO(app)
    socket.init_app(app, cors_allowed_origins="*")

    db.init_app(app)

    api = Api(app)
    api.add_resource(Main, '/', '/<path:path>')

    socket.on_event('request_start', communicate_with_guider)
    socket.on_event('request_stop', disconnect_with_guider)
    return app, socket
