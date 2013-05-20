#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from unittest import TestCase, main
from random import randint

Resource = namedtuple('Resource', ['name', 'url', 'polling_interval','check'])

hs = Resource('HS', 'http://www.hs.fi', lambda: randint(0,0), lambda x: x.status_code==200)

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

