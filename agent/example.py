#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from guider import NetworkManager

# add guider path #
curDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '%s/../guider' % curDir)

if __name__ == '__main__':

    # run server before launch below client code #
    '''
    $ guider/guider.py server
    '''

    # set network info #
    '''
    Choose one of below calls. (None: default address)
    1. NetworkManager.prepareServerConn(CLIENT_IP:PORT, SERVER_IP:PORT)
    2. NetworkManager.prepareServerConn(None, SERVER_IP:PORT)
    3. NetworkManager.prepareServerConn(None, None)
    '''
    NetworkManager.prepareServerConn(None, None)

    # get connection with server #
    conn = NetworkManager.getServerConn()
    if not conn:
        print('\nFail to get connection with server')
        sys.exit(0)

    # request command #
    pipe = NetworkManager.getCmdPipe(conn, 'GUIDER top -a -J')
    if not pipe:
        print('\nFail to get command pipe')
        sys.exit(0)

    # get data from server #
    while 1:
        data = pipe.getData()
        if not data:
            break

        print(data.rstrip())

    # close command pipe to terminate process on server #
    pipe.close()
