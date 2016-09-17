#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import traceback
from functools import wraps

import click
from flask import Flask, render_template, copy_current_request_context
from flask import request, Response
from flask_socketio import SocketIO, emit
import eventlet


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == 'username' and password == 'password'

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# import the user created module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import example

app = Flask(__name__)
app.debug = False
socketio = SocketIO(app)

def context(func):
    def foo():
        with app.app_context():
            func()
    return foo


class Scheduler(object):

    def __init__(self, seconds, func):
        self.seconds = seconds
        self.func = func
        self.thread = None

    def start(self):
        self.thread = eventlet.spawn(self.run)

    def run(self):
        ret = eventlet.spawn(context(self.func))
        eventlet.sleep(self.seconds)
        try:
            ret.wait()
        except:
            traceback.print_exc()
        self.thread = eventlet.spawn(self.run)

    def stop(self):
        if self.thread:
            self.thread.cancel()


@app.route('/')

def index():
    return render_template('index.html')


@socketio.on('4#change')
def _(*args):
    
    foo = copy_current_request_context(example.regress2)
    eventlet.spawn(foo, *args)
    

@socketio.on('1#change')
def _(*args):
    
    foo = copy_current_request_context(example.mainviewx)
    eventlet.spawn(foo, *args)
    

@socketio.on('2#change')
def _(*args):
    
    foo = copy_current_request_context(example.mainviewy)
    eventlet.spawn(foo, *args)
    

@socketio.on('3#change')
def _(*args):
    
    foo = copy_current_request_context(example.mainviewz)
    eventlet.spawn(foo, *args)
    

@socketio.on('5#select')
def _(*args):
    
    foo = copy_current_request_context(example.regress)
    eventlet.spawn(foo, *args)
    


@click.command()
@click.option('--host', '-h', default='0.0.0.0', help='Host IP')
@click.option('--port', '-p', default=9991, help='port number')
def main(host, port):
    scheds = []
    

    for sched in scheds:
        sched.start()
    socketio.run(app, host=host, port=port)
    for sched in scheds:
        sched.stop()

if __name__ == '__main__':
    main()