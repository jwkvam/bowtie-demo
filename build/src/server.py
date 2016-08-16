#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import click
from flask import Flask, render_template, copy_current_request_context
from flask_socketio import SocketIO, emit
import eventlet

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import iris

app = Flask(__name__)
app.debug = False
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('3#change')
def _(*args):
    
    foo = copy_current_request_context(iris.mainviewz)
    eventlet.spawn(foo, *args)
    

@socketio.on('1#change')
def _(*args):
    
    foo = copy_current_request_context(iris.mainviewx)
    eventlet.spawn(foo, *args)
    

@socketio.on('4#change')
def _(*args):
    
    foo = copy_current_request_context(iris.regress2)
    eventlet.spawn(foo, *args)
    

@socketio.on('5#select')
def _(*args):
    
    foo = copy_current_request_context(iris.regress)
    eventlet.spawn(foo, *args)
    

@socketio.on('2#change')
def _(*args):
    
    foo = copy_current_request_context(iris.mainviewy)
    eventlet.spawn(foo, *args)
    


@click.command()
@click.option('--host', '-h', default='0.0.0.0', help='Host IP')
@click.option('--port', '-p', default=9991, help='port number')
def main(host, port):
    socketio.run(app, host=host, port=port)

if __name__ == '__main__':
    main()