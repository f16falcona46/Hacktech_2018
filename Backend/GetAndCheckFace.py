#!/usr/bin/env python3

import urllib.request
import time
import cognitive_face as cf
import sys
import wsgiref.simple_server
import cgi
import base64
import subprocess
from threading import Timer

RASPI_IP = "http://192.168.137.92:8051"
FILENAME = "picture.jpg"
GROUP = "authorized_entry"

KEY = '64ebe5b92a9a4d7e8e841a7f8a5e04ef'  # Replace with a valid subscription key (keeping the quotes in place).
cf.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
cf.BaseUrl.set(BASE_URL)

urllib.request.urlretrieve(RASPI_IP + "/" + "lock")

def app(env, start_response):
	if env["PATH_INFO"] == "/check":
		start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
		urllib.request.urlretrieve(RASPI_IP + "/" + FILENAME, FILENAME)
		faces = cf.face.detect(FILENAME)
		if faces:
			result = cf.face.identify([faces[0]["faceId"]], GROUP)
			if result[0]["candidates"]:
				person_info = cf.person.get(GROUP, result[0]["candidates"][0]["personId"])
				print("Hello, " + person_info["name"] + ".")
				urllib.request.urlretrieve(RASPI_IP + "/" + "unlock")
				cf.person.add_face(FILENAME, GROUP, result[0]["candidates"][0]["personId"])
				response = [('1 "%s"' % person_info["name"]).encode("utf-8")]
				print(response)
				lock_after_entry = Timer(5, lambda : urllib.request.urlretrieve(RASPI_IP + "/" + "lock"))
				lock_after_entry.start()
			else:
				print("Face not recognized.")
				urllib.request.urlretrieve(RASPI_IP + "/" + "lock")
				response = [b"""-1"""]
		else:
			print("No face detected...")
			urllib.request.urlretrieve(RASPI_IP + "/" + "lock")
			response = [b"""0"""]
		return response
	else:
		start_response("200 OK", [("Content-type", "text/html; charset=utf-8")])
		return [b"""Unsupported."""]

httpd = wsgiref.simple_server.make_server("localhost", 8062, app)
httpd.serve_forever()