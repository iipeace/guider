#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from pprint import pprint
from influxdb import InfluxDBClient
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def InsertDB(file_path) :
    json_dic_tags = {
        "host": "db_host_server",
        "region": "aws_korea"
    }

    json_body_list = list()

    with open(file_path) as data_file:
        guider_data = json.load(data_file)

    for super_k in guider_data.keys() :
        json_dic = dict()
        json_dic["tags"] = json_dic_tags
        json_dic["measurement"] = super_k
        json_dic["fields"] = dict()
        for sub_k in guider_data[super_k] :
            #TODO : Add execption precessing
            json_dic["fields"][sub_k] = guider_data[super_k][sub_k]
        if len(json_dic["fields"]) > 0 :
            json_body_list.append(json_dic)

    try :
        client = InfluxDBClient('13.124.47.121', 8086, 'root', 'root', 'guider_data')
        client.write_points(json_body_list)
        result = client.query('select value from mem;')
    except :
        print('Error is occurred. Check [file_name].[time].error !!!')
        #TODO : Copy [file_name] file to [file_name].[time].error when exception is occurred.

class GuiderOutputEventHandler(PatternMatchingEventHandler) :

    def setPath(self, path) :
        self.path = path

    def on_modified(self, event):
        print('event type: ' + event.event_type + '  path : ' +  event.src_path)
        InsertDB(self.path)


def fileObservingNInsertDB(path) :


    x = path.split('/')
    x.reverse()
    file_name = x[0]

    patterns = ['*' + file_name]
    print('file_name : ' + file_name)
    event_handler = GuiderOutputEventHandler(patterns = patterns)
    event_handler.setPath(path)
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

path = sys.argv[1] if len(sys.argv) > 1 else './guider.report'

fileObservingNInsertDB(path)
