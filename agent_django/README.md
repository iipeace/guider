# Guider Web

### Build Frontend Codes
It is recommended to build at static/ directory
```sh
$ cd ./django_vue/ && npm install && npm run build && cd ..
```

### Install Python Dependencies 
```shell script
$ pip3 install virtualenv
```
```shell script
$ virtualenv venv 
```
```shell script
$ source ./venv/bin/activate
```
```sh
$ pip3 install -r requirements.txt
```

### Set
Set a secret key in JSON format
```shell script
$ vi ./agent_django/secret.json
```
Add templates tags in ./static/index.html
```html
<!DOCTYPE html>
{% load render_bundle from webpack_loader %}
....
{% render_bundle 'index' %}
</body>
```


### Run
Run frontend
```
$ cd ./django_vue/ && npm run serve
```
Run backend
```sh
$ python3 manage.py runserver 0.0.0.0:8000
```