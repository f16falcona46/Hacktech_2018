#!/usr/bin/env python3

from twilio.rest import Client
import wsgiref.simple_server
import cgi
import base64
import subprocess

account_sid = "ACa8aef683b117c2fccbb70fe045807aac"
auth_token = "3ee396149de44599c9709a029f27abb0"
client = Client(account_sid, auth_token)

def app(env, start_response):
	verification_code = env["PATH_INFO"][1:]
	start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
	content = "Your security code is: " + verification_code
	message = client.messages.create(
		to="+14104290174", 
		from_="+12565764528",
		body=content)
	response = [b"""Sent."""]
	return response

httpd = wsgiref.simple_server.make_server("localhost", 8061, app)
httpd.serve_forever()