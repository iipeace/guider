#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import time

from influxdb import InfluxDBClient
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def InsertDB(file_path):
    json_dic_tags = {
        "host": config['jsonDicTags']['host'],
        "region": config['jsonDicTags']['region']
    }

    json_body_list = list()

    with open(file_path) as data_file:
        guider_data = json.load(data_file)

    for super_k in guider_data.keys():
        json_dic = dict()
        json_dic["tags"] = json_dic_tags
        json_dic["measurement"] = super_k
        json_dic["fields"] = dict()
        for sub_k in guider_data[super_k]:
            # TODO : Add execption precessing
            json_dic["fields"][sub_k] = guider_data[super_k][sub_k]
        if len(json_dic["fields"]) > 0:
            json_body_list.append(json_dic)

    try:
        client = InfluxDBClient(config['influxDBClientConfig']['host'], config['influxDBClientConfig']['port'], config['influxDBClientConfig']['username'], config['influxDBClientConfig']['password'], config['influxDBClientConfig']['database'])
        client.write_points(json_body_list)
        # Unused variable
        # result = client.query('select value from mem;')
    except Exception:
        print('Error is occurred. Check [file_name].[time].error !!!')
        # TODO : Copy [file_name] file to [file_name].[time].error when exception is occurred.


class GuiderOutputEventHandler(PatternMatchingEventHandler):
    def setFilePath(self, filePath):
	print('filePath : %s' % filePath)
        self.filePath = filePath

    def on_modified(self, event):
        print('event type: ' + event.event_type + '  path : ' + event.src_path)
        InsertDB(self.filePath)


def fileObservingNInsertDB(path):
    x = path.split('/')

    fileDir = ''
    for i in range(len(x)-1):
	fileDir = fileDir + x[i] + '/'
    print('fileDir : %s' % fileDir)

    fileName = x[len(x)-1]
    print('fileName : %s' % fileName)

    patterns = ['*' + fileName]
    event_handler = GuiderOutputEventHandler(patterns=patterns)
    event_handler.setFilePath(fileDir + fileName)
    observer = Observer()
    observer.schedule(event_handler, fileDir, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(config['observer']['sleep'])
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def loadConfiguration(filePath='./visualization.conf'):
    global config
    with open(filePath, 'r') as configFile:
	config = json.load(configFile)

	
def printArgv():
    for i in range(len(sys.argv)):
        print("sys.argv[%d] = '%s'" % (i, sys.argv[i]))


printArgv()

path = sys.argv[1] if len(sys.argv) > 1 else './guider.report'
configPath = sys.argv[2] if len(sys.argv) > 2 else './visualization.conf'

loadConfiguration(configPath)
print('config : ', str(config))

fileObservingNInsertDB(path)
