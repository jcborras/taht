#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import namedtuple
from random import randint

Resource = namedtuple('Resource', ['name', 'url', 'polling_interval','check'])

hs = Resource('HS', 'http://www.hs.fi', lambda: randint(1,3), lambda x: x.status_code==200)
missing_resource = Resource('Missing Resource', 'http://fsdfsdfds.f-secure.com/', lambda: randint(2,4), lambda x: True)
fb = Resource('Facebook', 'http://www.facebook.com', lambda: randint(2,4), lambda x: 'form id="login_form"' in x.text)
rogueserver = Resource('RogueServer', 'http://localhost:5000', lambda: randint(0,1), lambda x: 'Expected' in x.text)

to_monitor = [rogueserver, hs, missing_resource, fb]
