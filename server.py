#!/usr/bin/env python
# -*- coding: utf-8

__author__ = 'jcb'

from logging import basicConfig, DEBUG
from random import sample, randint
from time import sleep

from flask import abort, render_template, Flask

APP_PORT = 5000
APP_HOSTNAME = 'localhost'

ROOT_URL='/'
HTTP_STATUS_CODES = [200,400,200,404,200,500,200,501]

app = Flask(__name__)
formatstr = "%(asctime)s %(levelname)s %(message)s"
basicConfig(format=formatstr, level=DEBUG)
app.logger.setLevel(DEBUG)

def random_content():
    if sample([True,False],1)[0]:
        return 'Expected'
    return 'Unexpected'

@app.route(ROOT_URL, methods=['GET'])
def frontpage():
    sleep(randint(0,5))
    sc = sample(HTTP_STATUS_CODES,1)[0]
    if sc==200:
        return render_template("index.html", content=random_content())
    abort(sc)

if __name__ == '__main__':
    app.run(host=APP_HOSTNAME, port=APP_PORT, debug=True)
