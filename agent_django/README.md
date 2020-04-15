# Guider Web

### Build Frontend Codes
It is recommended to build at static/ directory
```sh
$ cd ./django_vue/ && npm install && npm run build && cd ..
```

### Requirement
```
- Python (>= 3.6)
```

### Install Python Dependencies
It is recommended to use virtualenv 
```sh
$ pip3 install -r requirements.txt
```

### Set
Set a secret key in JSON format
```shell script
$ vi ./agent_django/secret.json
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