#!/usr/bin/env python3
from subprocess import call
from subprocess import check_output
import requests
import jsonpickle

INITIAL_STATIONS = {
    'BBC1' : 'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1xtra_mf_p?s=1494665120&e=1494679520&h=f169d1bb0d7a29dafbd65df4683dec43',
    'BBC1x' : 'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio1_mf_p?s=1494665172&e=1494679572&h=eb49096486cafc50ee51d19042206ca8',
    'BBC2' : 'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_6music_mf_p?s=1494664968&e=1494679368&h=1c2b42a5e8bf1b8baedea2473219035d',
    'BBC3' : 'http://bbcmedia.ic.llnwd.net/stream/bbcmedia_radio4extra_mf_q?s=1494665239&e=1494679639&h=e4e7ec6bb9eb4cf7415bee4cf4b49e8b',
}

STATION_NAMES = ['BBC1','BBC1x','BBC2','BBC3']

# http://stream3.polskieradio.pl:8900/

class RadioStation:

    def __init__(self,name,url):
        self.name = name
        self.url = url

class Radio:

    def __init__(self):
        self.is_playing = False
        self.volume = 100
        self.current_station = 0
        self.volume_change(+100)
        self.stop()
        self.clear()
        self.stations = []
        for name in STATION_NAMES:
            url = INITIAL_STATIONS[name]
            self.add(name,url)

    def play(self,number):
        self.current_station = number-1
        self.is_playing = True
        call(["mpc","play",'{}'.format(number)])
        return self.status()

    def add(self,name,url):
        station = RadioStation(name,url)

        status = call(["mpc","add",url])
        if status==0:
            self.stations.append(station)
        return self.status()

    def stop(self):
        call(["mpc","stop"])
        self.is_playing = False
        return self.status()

    def pause(self):
        call(["mpc", "pause"])
        self.is_playing = False
        return self.status()

    def clear(self):
        call(["mpc", "clear"])
        self.stations = []
        self.current_station = 0
        self.is_playing = False
        return self.status()

    def next(self):
        count = len(self.stations)
        self.current_station = (self.current_station+1)%count
        call(["mpc", "play", "{}".format(self.current_station+1)])
        return self.status()

    def prev(self):
        count = len(self.stations)
        self.current_station = (self.current_station-1)%count
        call(["mpc", "play", "{}".format(self.current_station+1)])
        return self.status()

    def volume_change(self,amount):
        self.volume += amount
        if self.volume < 0:
            self.volume = 0
        if self.volume > 100:
            self.volume = 100
        call(["mpc","volume","{}{}".format("+" if amount>0 else "",amount)])
        return self.status()

    def status(self):
        return jsonpickle.encode(self)
