#!/usr/bin/env python3
# external imports
from flask import Flask,redirect,request,jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import jsonpickle
from subprocess import call
from radio import Radio
#from gpio import setup as gpio_setup

app = Flask(__name__)
CORS(app)
radio = Radio()

@app.route("/api/vol/up")
def volume_up():
    return radio.volume_change(5)

@app.route("/api/vol/down")
def volume_down():
    return radio.volume_change(-5)

@app.route("/api/next")
def next():
    return radio.next()

@app.route("/api/prev")
def prev():
    return radio.prev()

@app.route("/api/pause")
def pause():
    return radio.pause()

@app.route("/api/play")
def play():
    nr = int(request.args.get('nr'))
    return radio.play(nr+1)

@app.route("/api/status")
def status():
    return radio.status()

@app.route("/api/add",methods=["POST"])
def add():
    data = jsonpickle.decode(request.data.decode('utf-8'))
    return radio.add(data['name'],data['url'])

if __name__ == '__main__':
    #gpio_setup()
    app.run()
