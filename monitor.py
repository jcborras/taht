#!/usr/bin/env
# -*- coding: utf-8 -*-

from unittest import TestCase, main
from requests import get
from config import ToMonitor


class TestDrive(TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_hs(self):
        self.assertEqual(len([ i for i in ToMonitor if i.name=='HS']), 1)


 
if __name__ == '__main__':
    main()

