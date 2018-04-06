#!/usr/bin/env python3

from twilio.rest import Client
import wsgiref.simple_server
import cgi
import base64
import subprocess

account_sid = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
auth_token = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"
client = Client(account_sid, auth_token)

def app(env, start_response):
	input = env["PATH_INFO"][1:].split(',')
	verification_code = input[0]
	targetnum = "+1" + input[1]
	start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
	content = "Your security code is: " + verification_code
	message = client.messages.create(
		to=targetnum, 
		from_="+12565764528",
		body=content)
	response = [b"""Sent."""]
	return response

httpd = wsgiref.simple_server.make_server("localhost", 8061, app)
httpd.serve_forever()
