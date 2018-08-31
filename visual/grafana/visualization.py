import json
from pprint import pprint
from influxdb import InfluxDBClient

json_dic_tags = {
        "host": "db_host_server",
        "region": "aws_korea"
    }

json_body_list = list()


with open('../sample_output/guider.report.sample') as data_file:
    guider_data = json.load(data_file)

for super_k in guider_data.keys() :
    json_dic = dict()
    json_dic["tags"] = json_dic_tags
    print(super_k)
    json_dic["measurement"] = super_k
    json_dic["fields"] = dict()
    for sub_k in guider_data[super_k] :
        print(super_k + '_' + sub_k)
        json_dic["fields"][sub_k] = guider_data[super_k][sub_k]
    if len(json_dic["fields"]) > 0 :
        json_body_list.append(json_dic)

print("-----------------------------------------")
pprint(json_body_list)
print("-----------------------------------------")


client = InfluxDBClient('13.124.47.121', 8086, 'root', 'root', 'guider_data')
client.write_points(json_body_list)
result = client.query('select value from mem;')
print("Result: {0}".format(result))