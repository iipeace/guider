from flask import make_response, render_template, request
from flask_restful import Resource


class Main(Resource):
    def __init__(self):
        pass

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html', server_addr=request.host_url), 200, headers)
