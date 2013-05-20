#!/usr/bin/env
# -*- coding: utf-8 -*-

from collections import namedtuple
from unittest import TestCase, main

Resource = namedtuple('Resource', ['name', 'url', 'poll','check'])

hs = Resource('HS', 'http://www.hs.fi', lambda: randint(10), lambda x: x.status==200)

ToMonitor = [hs]

class TestDrive(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test1(self):
        pass

 
if __name__ == '__main__':
    main()

