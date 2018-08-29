import json
from pprint import pprint

with open('../sample_output/guider.report.sample') as data_file:
    data = json.load(data_file)

pprint(data)
print('-----------------------------------')

print(data['mem']['kernel'])