#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep, time
from unittest import TestCase, main

from requests import ConnectionError, get

from config import to_monitor

car = lambda x: x[0]

## Credit where is due:
## http://www.andreas-jung.com/contents/a-python-decorator-for-measuring-the-execution-time-of-methods
def timed(method):
    def g(*args, **kw):
        ts = time()
        result = method(*args, **kw)
        te = time()
        #print '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts)
        return result, te-ts 
    return g

@timed
def timed_get(url):
    return get(url)

def harnessed(method):
    def f(*args, **kw):
        try:
            result, timing = method(*args, **kw)
            return  {'status':'OK', 'stuff':None}, result, timing
        except Exception as e:
            return {'status':'Error', 'stuff':e}, None, None ## Ugly. Not a lot, but ugly nevertheless
        #print '%r (%r, %r) %2.2f sec' % (method.__name__, args, kw, te-ts)
    return f

@harnessed
def harnessed_get(url):
    return timed_get(url)

class TestDrive(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_hs(self):
        self.assertEqual(len([ i for i in to_monitor if i.name=='HS']), 1)

    def test_hs_check(self):
        resource = car(filter(lambda i: i.name=='HS', to_monitor))
        self.assertTrue(resource.check(get(resource.url)))

    def test_hs_timed(self):
        resource = car([ i for i in to_monitor if i.name=='HS'])
        a,b = timed_get(resource.url)
        self.assertTrue(resource.check(a) and b>0) 

    def test_hs_check(self):
        resource = car([ i for i in to_monitor if i.name=='HS'])
        self.assertTrue(resource.check(get(resource.url)))

    def test_missing_resource(self):
        resource = car(filter(lambda i: i.name=='Missing Resource', to_monitor))
        self.assertRaises(ConnectionError, get, resource.url)

    def test_harnessed_smooth(self):
        resource = car(filter(lambda i: i.name=='HS', to_monitor))
        harness, op_return, timing_info = harnessed_get(resource.url)
        self.assertTrue(harness['status']=='OK' and resource.check(op_return))

    def test_harnessed_bumpy(self):
        resource = car(filter(lambda i: i.name=='Missing Resource', to_monitor))
        harness, op_return, timing_info = harnessed_get(resource.url)
        self.assertTrue(harness['status']=='Error' and issubclass(harness['stuff'].__class__, Exception))

    def test_facebook(self):
        resource = car(filter(lambda i: i.name=='Facebook', to_monitor))
        harness, op_return, timing_info = harnessed_get(resource.url)
        self.assertTrue(harness['status']=='OK' and resource.check(op_return))

 
if __name__ == '__main__':
    main()

