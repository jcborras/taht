#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from string import ascii_letters, digits
from random import sample, randint

def random_hostname():
    return reduce(lambda x,y:x+y, sample(ascii_letters+digits, 16))

def missing_resource():
    return Resource(name='Missing Resource',
                    url='http://%s.f-secure.com/' % random_hostname(),
                    polling_interval=lambda: randint(10,20),
                    check=lambda x: True)

Resource = namedtuple('Resource', ['name', 'url', 'polling_interval','check'])

hs = Resource('HS', 'http://www.hs.fi', polling_interval=lambda:
              randint(10,30), check=lambda x: x.status_code==200)

fb = Resource('Facebook', 'http://www.facebook.com',
              polling_interval=lambda: randint(20,40),
              check=lambda x:'form id="login_form"' in x.text)

rogueserver = Resource('RogueServer', 'http://localhost:5000',
                       polling_interval=lambda: randint(1,2),
                       check=lambda x: 'Expected' in x.text)

to_monitor = [rogueserver, hs,  missing_resource(), fb,  missing_resource(),
              missing_resource(), rogueserver, rogueserver]

