#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, emit
import eventlet
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import example

app = Flask(__name__)
app.debug = False
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('5#click')
def _(*args):

    foo = copy_current_request_context(example.foo2)
    eventlet.spawn(foo, *args)


@socketio.on('1#change')
def _(*args):

    foo = copy_current_request_context(example.foo)
    eventlet.spawn(foo, *args)


@socketio.on('4#change')
def _(*args):

    foo = copy_current_request_context(example.foo3)
    eventlet.spawn(foo, *args)


@socketio.on('3#click')
def _(*args):

    foo = copy_current_request_context(example.newtable)
    eventlet.spawn(foo, *args)



if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    print(port)
    socketio.run(app, host='0.0.0.0', port=int(port))
