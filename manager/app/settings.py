import os
import json

basedir = os.path.abspath(os.path.dirname(__file__))
secret_file = os.path.join(basedir, 'secrets.json')

# TODO add except logic
try:
    with open(secret_file) as f:
        secrets = json.loads(f.read())
except FileNotFoundError:
    raise Exception('setting file is not exists, add for secret key')


def get_secret(key):
    try:
        return secrets[key]
    except KeyError:
        print('key is not exist')
