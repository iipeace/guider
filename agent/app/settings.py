import os, json

basedir = os.path.abspath(os.path.dirname(__file__))
secret_file = os.path.join(basedir, 'secrets.json')

# TODO add except logic
try:
    with open(secret_file) as f:
        secrets = json.loads(f.read())
except:
    pass


def get_secret(key):
    try:
        return secrets[key]
    except KeyError:
        print('KEY IS NOT EXIST')