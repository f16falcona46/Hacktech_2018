#!/usr/bin/env python3

import cognitive_face as cf
import sys
import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.OUT)
servo = gpio.PWM(18, 50)
servo.start(0.01)

KEY = '64ebe5b92a9a4d7e8e841a7f8a5e04ef'  # Replace with a valid subscription key (keeping the quotes in place).
cf.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
cf.BaseUrl.set(BASE_URL)

faces = cf.face.detect(sys.argv[1])
result = cf.face.identify([faces[0]["faceId"]], "authorized_entry")

if result[0]["candidates"]:
	person_info = cf.person.get("authorized_entry", result[0]["candidates"][0]["personId"])
	print("Hello, " + person_info["name"] + ".")
	servo.ChangeDutyCycle(0.001)
else:
	print("Face not recognized.")

gpio.cleanup()