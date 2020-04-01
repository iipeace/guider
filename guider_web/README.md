# Guider Web

## Build Frontend Codes
Build to static/ directory
```sh
$ cd ./front-vue/ && npm install && npm run build && cd ..
```

### Requirement
```
- Python (>= 3.6)
```

## Install Python Dependencies
It is recommended to use virtualenv 
```sh
$ pip3 install -r requirements.txt
```

## Run
```sh
$ python manage.py runserver
```
IF you want to listen on all available public IPs
```sh
$ python3 manage.py runserver 0.0.0.0:8000
```


