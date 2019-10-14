from flask import make_response, render_template, request, jsonify
from flask_restful import Resource
from datetime import datetime
from monitoring.models import Data, spread_data, deserialize_data


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


class Dataset(Resource):
    def __init__(self):
        pass

    def get(self):
        args = request.args
        start = args.get('start', None)
        end = args.get('end', None)
        num = args.get('num', 20)
        from_utc = 9 * 60 * 60
        try:
            if start is None:
                start = (Data.objects.order_by('+timestamp').limit(1))
                start = int(datetime.timestamp(start[0]['timestamp'])) + \
                    from_utc
            else:
                start = int(start)
            if end is None:
                end = (Data.objects.order_by('-timestamp').limit(1))
                end = int(datetime.timestamp(end[0]['timestamp'])) + from_utc
            else:
                end = int(end)
            num = int(num)
        except Exception as e:
            print('Failed to parse start, end ', e)
            return jsonify(dict(status="failed", data=[]))
        datas = list(Data.objects().order_by('+timestamp').all())
        print(len(datas), start, end)
        # TODO: Quering Database in range, Not processing everything.
        # TODO: only fetch data in a certain mac_address.
        result = []
        idx = 0
        for c in range(num):
            period = int((end-start)/num)
            timestamp_bound = start+period*(c+1)
            sum = {}
            cnt = 0
            while idx < len(datas):
                timestamp = int(datetime.timestamp(datas[idx].timestamp)) + \
                            from_utc
                if timestamp > timestamp_bound:
                    break
                if (timestamp < start) or (timestamp > end):
                    idx += 1
                    continue
                spread = spread_data(datas[idx])
                for k in spread.keys():
                    if k in sum:
                        sum[k] += spread[k]
                    else:
                        sum[k] = 0
                idx += 1
                cnt += 1

            result.append(dict(
                timestamp=timestamp_bound,
                data=deserialize_data(sum, cnt)
            ))

        return jsonify(dict(status="ok", data=result))


class Slack(Resource):

    def get(self):
        # msg = request.args.get('msg')
        # token = get_secret('SLACK_OAUTH_TOKEN')
        # slack = Slacker(token)
        # slack.chat.post_message(channel='#guideropensource', text=msg)
        pass

    def post(self):
        # if request.form.get('token') != get_secret('SLACK_VERIFY_TOKEN'):
        #     return Response(
        #         '안녕', content_type='application/json;charset=utf-8')
        pass
