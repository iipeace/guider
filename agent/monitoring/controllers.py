#-*- coding:utf-8 -*-

from flask import make_response, render_template, request, Response
from flask_restful import Resource

from slacker import Slacker

from app.settings import get_secret


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


class Slack(Resource):

    def get(self):
        msg = request.args.get('msg')
        token = get_secret('SLACK_OAUTH_TOKEN')
        slack = Slacker(token)
        slack.chat.post_message(channel='#guideropensource', text=msg)

    def post(self):
        if request.form.get('token') != get_secret('SLACK_VERIFY_TOKEN'):
            return
            return Response('안녕', content_type='application/json;charset=utf-8')
