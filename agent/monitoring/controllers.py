<<<<<<< HEAD
from flask import make_response, render_template, request, jsonify
from flask_restful import Resource
from time import time
from monitoring.models import Data
=======
# -*- coding:utf-8 -*-

from flask import make_response, render_template, request, Response
from flask_restful import Resource

from slacker import Slacker

# from app.settings import get_secret

>>>>>>> upstream/master

class Main(Resource):
    def __init__(self):
        pass

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('index.html', server_addr=request.host_url),
            200,
            headers
        )


<<<<<<< HEAD
class Dataset(Resource):
    def __init__(self):
        pass
    def get(self):

        args = request.args
        # start = args.get('start', 0)
        # end = args.get('end', int(time()))
        # TODO: validate timestamp
        # num = args.get('num', 20)
    
        last = Data.objects().order_by('-timestamp').limit(1)
        first = Data.objects().order_by('+timestamp').limit(1)

        print(first['timestamp'], last['timestamp'])
        #print('start:timestamp = ', data[0]['timestamp'])
        #print('end:timestamp = ', data[-1]['timestamp'])
        #return jsonify(data)
        return jsonify(first)
=======
class Slack(Resource):

    def get(self):
        msg = request.args.get('msg')
        # token = get_secret('SLACK_OAUTH_TOKEN')
        # slack = Slacker(token)
        # slack.chat.post_message(channel='#guideropensource', text=msg)
        pass

    def post(self):
        # if request.form.get('token') != get_secret('SLACK_VERIFY_TOKEN'):
        #     return Response(
        #         '안녕', content_type='application/json;charset=utf-8')
        pass
>>>>>>> upstream/master
