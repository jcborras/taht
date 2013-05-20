#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep, time
from unittest import TestCase, main

from requests import ConnectionError, get

from config import ToMonitor

car = lambda x: x[0]

def harnessed(method):
    def f(*args, **kw):
        try:
            result = method(*args, **kw)
            return  {'status':'OK', 'stuff':None}, result
        except Exception as e:
            return {'status':'Error', 'stuff':e}, None
        #print '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts)
    return f

@harnessed
def harnessed_get(url):
    return get(url)

## Credit where is due:
## http://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
def timed(method):
    def timing_func(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        #print '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts)
        return result, te-ts 
    return timing_func

@timed
def timed_get(url):
    return get(url)

    
class TestDrive(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_hs(self):
        self.assertEqual(len([ i for i in ToMonitor if i.name=='HS']), 1)

    def test_hs_check(self):
        resource = car(filter(lambda i: i.name=='HS', ToMonitor))
        sleep(resource.polling_interval())
        self.assertTrue(resource.check(get(resource.url)))

    def test_hs_timed(self):
        resource = car([ i for i in ToMonitor if i.name=='HS'])
        sleep(resource.polling_interval())
        a,b = timed_get(resource.url)
        self.assertTrue(resource.check(a) and b>0) 

    def test_hs_check(self):
        resource = car([ i for i in ToMonitor if i.name=='HS'])
        sleep(resource.polling_interval())
        self.assertTrue(resource.check(get(resource.url)))

    def test_missing_resource(self):
        resource = car(filter(lambda i: i.name=='Missing Resource', ToMonitor))
        self.assertRaises(ConnectionError, get, resource.url)

    def test_harnessed_smooth(self):
        resource = car(filter(lambda i: i.name=='HS', ToMonitor))
        a,b = harnessed_get(resource.url)
        self.assertTrue(a['status']=='OK' and resource.check(b))

    def test_harnessed_bumpy(self):
        resource = car(filter(lambda i: i.name=='Missing Resource', ToMonitor))
        a,b = harnessed_get(resource.url)
        self.assertTrue(a['status']=='Error' and issubclass(a['stuff'].__class__, Exception))


 
if __name__ == '__main__':
    main()

