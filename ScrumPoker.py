#! /usr/bin/env python

import os

from flask import Flask
from flask import request, Response, jsonify
from flask import render_template, send_from_directory


import requests

mydict={}
mydict2={}
reveal=False

app = Flask(__name__, static_url_path='')


@app.route('/')
def start():
    return render_template('index.html', name='Scrum poker')


@app.route('/reset')
def reset():
    global mydict, mydict2, reveal
    mydict={}
    mydict2={}
    reveal=False
    return 200


@app.route('/reveal')
def reveal():
    global reveal
    reveal=True
    return 200


@app.route('/vote')
def vote():
    global mydict, mydict2
    name = request.args.get('name')
    score = int(request.args.get('score'))
    mydict.update({name: score})
    mydict2.update({name: 0})
    return jsonify(mydict)


@app.route('/getvotes')
def getvotes():
    global mydict, mydict2, reveal
    if reveal:
        return jsonify(mydict)
    return jsonify(mydict2)

if __name__ == '__main__':
    app.run()

