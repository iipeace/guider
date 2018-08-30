import json
from pprint import pprint

with open('../sample_output/guider.report.sample') as data_file:
    data = json.load(data_file)

pprint(data)
print('-----------------------------------')

print(data['mem']['kernel'])

json_body = [
    {
        "measurement": "cpu_load_short",
        "tags": {
            "host": "server01",
            "region": "us-west"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "value": 0.64
        }
    }
]
print('-----------------------------------')
pprint(json_body)
print('-----------------------------------')

json_body_2 = list()

json_dic = {
    "measurement": "cpu_load_short",
    "tags": {
        "host": "server01",
        "region": "us-west"
    },
    "time": "2009-11-10T23:00:00Z",
    "fields": {
        "value": 0.64
    }
}
json_body_2.append(json_dic)
json_body_2.append(json_dic)
pprint(json_body_2)