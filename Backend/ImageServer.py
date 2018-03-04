#!/usr/bin/env python3

import wsgiref.simple_server
import cgi
import base64
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, 1)

def app(env, start_response):
	if env["PATH_INFO"] == "/lock":
		start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
		with open('/sys/class/pwm/pwmchip0/pwm0/duty_cycle', 'w') as pwm:
			pwm.write("800000\n")	
		GPIO.output(4, 1)
		response = [b"""Locked."""]
		return response
	elif env["PATH_INFO"] == "/unlock":
		start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
		with open('/sys/class/pwm/pwmchip0/pwm0/duty_cycle', 'w') as pwm:
			pwm.write("2400000\n")
		GPIO.output(4, 0)
		response = [b"""Unlocked."""]
		return response
	elif env["PATH_INFO"] == "/picture.jpg":
		start_response("200 OK", [("Content-type", "image/jpeg; charset=utf-8")])
		subprocess.call(["raspistill", "--timeout", "3000", "-o", "picture.jpg"])
		with open("picture.jpg", mode='rb') as image:
			fileContent = image.read()
		return [fileContent]
	elif env["PATH_INFO"] == "/full_list.cgi":
		response = [b"""<html><head><title>Gimme the params</title></head><body><table>"""]
		for k, v in env.items():
			response.append(("<tr><td>%s</td><td>%s</td></tr>\n" % (k, v)).encode("utf-8"))
		response.append(b"""</table><hr /><a href="/">Home</a></html>""")
		return response
	else:
		start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
		return [b"""Unsupported<hr /><a href="/">Home</a>"""]

httpd = wsgiref.simple_server.make_server("raspberrypi.local", 8051, app)
httpd.serve_forever()