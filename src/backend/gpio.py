#!/usr/bin/env python3
import RPi.GPIO as gpio
import requests
#https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
LED_BLUE=17
LED_WHITE=18
LED_GREEN=23
LED_RED=24
BTN_1=10 # toggle mode
BTN_2=22 # next/increase vol/play
BTN_3=27 # prev/decrease vol/pause

API_URL='http://localhost:5000/api'

MODE_VOLUME = 'volume'
MODE_TRACK_CONTROL = 'track-control'
MODE_PLAY_CONTROL = 'play-control'

MODES=[MODE_VOLUME,MODE_TRACK_CONTROL,MODE_PLAY_CONTROL]
mode = 0

MODE_LED_MAP = {
	MODE_VOLUME : LED_BLUE,
	MODE_TRACK_CONTROL : LED_WHITE,
	MODE_PLAY_CONTROL : LED_GREEN
}

def setup():
	inputs = [BTN_1,BTN_2,BTN_3]
	outputs = [LED_BLUE,LED_WHITE,LED_GREEN,LED_RED]
	gpio.setup(inputs,gpio.IN)
	gpio.setup(outpus,gpio.OUT)
	led_on(MODE_LED_MAP(MODES(mode)))
	setup_button_callbacks()

def led_on(led):
	gpio.output(gpio.HIGH)

def led_off(led):
	gpio.output(gpio.LOW)

def setup_button_callbacks():
	GPIO.add_event_detect(BTN_1, gpio.FALLING, callback=on_toggle_press, bouncetime=200)
	GPIO.add_event_detect(BTN_2, gpio.FALLING, callback=on_next_press, bouncetime=200)
	GPIO.add_event_detect(BTN_3, gpio.FALLING, callback=on_prev_press, bouncetime=200)

def on_toggle_press(btn):
	print('toggle detected')
	led_off(MODE_LED_MAP(MODES(mode)))
	mode = (mode+1)%3
	led_on(MODE_LED_MAP(MODES(mode)))

def on_next_press(btn):
	print('next detected')
	curr_mode = MODES[mode]
	if curr_mode == MODE_VOLUME:
		requests.get('{}/{}'.format(API_URL,"vol/up"))
		pass
	elif curr_mode == MODE_PLAY_CONTROL:
		requests.get('{}/{}'.format(API_URL,"play"))
		pass
	elif curr_mode == MODE_TRACK_CONTROL:
		requests.get('{}/{}'.format(API_URL,"next"))
		pass

def on_prev_press(btn):
	print('prev detected')
	if curr_mode == MODE_VOLUME:
		requests.get('{}/{}'.format(API_URL,"vol/down"))
		pass
	elif curr_mode == MODE_PLAY_CONTROL:
		requests.get('{}/{}'.format(API_URL,"pause"))
		pass
	elif curr_mode == MODE_TRACK_CONTROL:
		requests.get('{}/{}'.format(API_URL,"prev"))
		pass
