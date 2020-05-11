# Guider Grafana

### Requirement
```
- Grafana
- InfluxDB
```

### Run
Run guider server. Only ports between 50 and 999 are available.
```sh
$ cd ../../guider && python3 guider.py server -x {PORT} && cd ../plugin/grafana
```
Run visualization client. Only ports between 50 and 999 are available.
```sh
$ python3 visualize.py {guider server IP:PORT}
```