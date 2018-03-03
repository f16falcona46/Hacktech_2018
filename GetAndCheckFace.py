#!/usr/bin/env python3

import urllib.request
import time
import cognitive_face as cf
import sys

RASPI_IP = "http://192.168.137.130:8051"
FILENAME = "picture.jpg"
GROUP = "authorized_entry"

KEY = '64ebe5b92a9a4d7e8e841a7f8a5e04ef'  # Replace with a valid subscription key (keeping the quotes in place).
cf.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
cf.BaseUrl.set(BASE_URL)

urllib.request.urlretrieve(RASPI_IP + "/" + FILENAME, FILENAME)
urllib.request.urlretrieve(RASPI_IP + "/" + "lock")

faces = cf.face.detect(FILENAME)
if faces:
	result = cf.face.identify([faces[0]["faceId"]], GROUP)
	if result[0]["candidates"]:
		person_info = cf.person.get(GROUP, result[0]["candidates"][0]["personId"])
		print("Hello, " + person_info["name"] + ".")
		urllib.request.urlretrieve(RASPI_IP + "/" + "unlock")
		cf.person.add_face(sys.argv[1], GROUP, result[0]["candidates"][0]["personId"])
	else:
		print("Face not recognized.")
		urllib.request.urlretrieve(RASPI_IP + "/" + "lock")
else:
	print("No face detected...")
	urllib.request.urlretrieve(RASPI_IP + "/" + "lock")