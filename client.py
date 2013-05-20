#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
# Importing multiprocessing is an overkill maybe but I don't like the GIL anyway
from multiprocessing import Lock, Process, Pool
from unittest import TestCase, main
from time import sleep

from requests import codes
from config import to_monitor
from monitor import harnessed_get

# the single logger approach is ugly b/c adds contention (competition for single resource)
# TODO: encapsulate a logger from the python stdlib
class Logger:
    def __init__(self):
        self.lock = Lock()
        
    def __call__(self, string=''):
        self.lock.acquire()
        print string
        self.lock.release()

logger = Logger()

def f(x):
    while True:
        sleep(x.polling_interval())
        harness, req, timing_info = harnessed_get(x.url)
        if harness['status']=='Error':
            logger('%s -1 Error retrieving: %s' % (datetime.now(), x.url))
            continue
        if req.status_code!=codes.ok: # TODO: Treats all errors alike (3xx and not 4xx are not 5xx)
            logger('%s %s %s' % (datetime.now(), req.status_code, x.url))
            continue
        if not x.check(req):
            logger('%s %s %s BadContent' % (datetime.now(), req.status_code, x.url))
            continue
        logger('%s %s %s' % (datetime.now(), req.status_code, x.url))


l = [ Process(target=f, args=(to_monitor[i],)) for i in range(len(to_monitor)) ]
tmp = [ i.start() for i in l]
tmp = [ i.join() for i in l]

