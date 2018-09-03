#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler



class MyHandler(PatternMatchingEventHandler):
    def on_modified(self, event):
        print('event type: ' + event.event_type + '  path : ' +  event.src_path)


if __name__ == "__main__":
    file_name = sys.argv[1] if len(sys.argv) > 1 else '.'
    file_name = '*' + file_name
    patterns = [file_name]
    print('file_name : ' + file_name)
    event_handler = MyHandler(patterns = patterns)
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
