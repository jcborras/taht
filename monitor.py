#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep, time
from unittest import TestCase, main

from requests import get

from config import ToMonitor

car = lambda x: x[0]

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
        resource = car([ i for i in ToMonitor if i.name=='HS'])
        sleep(resource.polling_interval())
        self.assertTrue(resource.check(get(resource.url)))

    def test_timed_get(self):
        resource = car([ i for i in ToMonitor if i.name=='HS'])
        sleep(resource.polling_interval())
        a,b = timed_get(resource.url)
        self.assertTrue(resource.check(a))
        self.assertTrue(b>0)

    def _test_hs_timed(self):
        resource = car([ i for i in ToMonitor if i.name=='HS'])
        sleep(resource.polling_interval())
        t0 = time()
        r = get(resource.url)
        d = None
        self.assertTrue(resource.check(get(resource.url)))


 
if __name__ == '__main__':
    main()

