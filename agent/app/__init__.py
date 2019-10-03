from flask import Flask, render_template, request

from app.config import config_dict


def create_app(config_name):
    app = Flask(__name__,
                template_folder='../static',
                static_url_path='',
                static_folder='../static')
    app.config.from_object(config_dict[config_name])

    @app.route('/')
    def index():
        print("route /")
        return render_template('index.html', server_addr=request.host_url)

    return app