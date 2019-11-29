from flask import make_response, render_template, request, jsonify
from flask_restful import Resource
from datetime import datetime
from monitoring.models import Datas, spread_data, deserialize_data


class Main(Resource):
    def __init__(self):
        pass

    def get(self):
        headers = {'Content-Type': 'text/html'}
        response = make_response(render_template("index.html", server_addr=request.host_url))
        response.headers = headers
        return response


class Devices(Resource):
    def __init__(self):
        pass

    def get(self):
        from app import is_connected
        if not is_connected:
            return jsonify(dict(status="failed", msg="failed to connect mongoDB"))

        from monitoring.models import Devices
        if Devices.objects.count() == 0:
            find_devices_from_db()
        devices = list(Devices.objects)
        results = []
        from_utc = 9 * 60 * 60
        for device in devices:
            results.append(dict(
                start=int(datetime.timestamp(device['start'])+from_utc),
                end=int(datetime.timestamp(device['end'])+from_utc),
                count=device['count'],
                mac_addr=device['mac_addr']
            ))
        print(results)
        return jsonify(dict(status="ok", data=results))


class Dataset(Resource):
    def __init__(self):
        pass

    def get(self):
        from app import is_connected
        if not is_connected:
            return jsonify(dict(status="failed", msg="failed to connect mongoDB"))
        args = request.args
        start = args.get('start', None)
        end = args.get('end', None)
        num = args.get('num', 20)
        mac_addr = args.get('mac_addr', None)
        count = Datas.objects(mac_addr=mac_addr).count()
        from_utc = 9 * 60 * 60
        # check if database exists

        if mac_addr is None:
            jsonify(dict(status="failed", data=[], msg="We need mac_addr"))
        if count == 0:
            return jsonify(dict(status="ok", data=[]))
        else:
            db_start = (Datas.objects(mac_addr=mac_addr).order_by('+timestamp').limit(1))
            db_start = int(datetime.timestamp(db_start[0]['timestamp'])) + \
                from_utc
            db_end = (Datas.objects(mac_addr=mac_addr).order_by('-timestamp').limit(1))
            db_end = int(datetime.timestamp(db_end[0]['timestamp'])) + from_utc
        # validate query string
        try:
            if start is None:
                start = db_start
            else:
                start = int(start)

            if end is None:
                end = db_end
            else:
                end = int(end)
            num = int(num)
        except Exception as e:
            print('Failed to parse start, end ', e)
            return jsonify(dict(status="failed", msg="Failed to parse start, end"))
        datas = list(Datas.objects().order_by('+timestamp').all())
        print(len(datas), start, end)
        # TODO: Quering Database in range, Not processing everything.
        # TODO: only fetch data in a certain mac_address.

        # Summarized results in database.
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

        return jsonify(dict(
            status="ok", data=result,
            meta=dict(start=db_start, end=db_end, count=count)))


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
        #         'Hello', content_type='application/json;charset=utf-8')
        pass


def find_devices_from_db():
    # fetch new data from dbs
    datas = list(Datas.objects)

    print('%d datas are found at mongoDB' % (len(datas)))
    devices = dict()
    for data in datas:
        timestamp = data.timestamp
        if data.mac_addr in devices:
            if timestamp < devices[data.mac_addr]['start']:
                devices[data.mac_addr]['start'] = timestamp
            if timestamp > devices[data.mac_addr]['end']:
                devices[data.mac_addr]['end'] = timestamp
            devices[data.mac_addr]['count'] += 1
        else:
            devices[data.mac_addr] = dict(
                start=timestamp,
                end=timestamp,
                count=1,
                mac_addr=data.mac_addr
            )
    from monitoring.models import Devices
    results = list(devices.values())
    for result in results:
        Devices(**result).save()
    print('saved %d new devices info' % (len(results)))
