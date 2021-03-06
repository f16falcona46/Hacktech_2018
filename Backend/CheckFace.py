#!/usr/bin/env python3

import cognitive_face as cf
import sys

KEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'  # Replace with a valid subscription key (keeping the quotes in place).
cf.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
cf.BaseUrl.set(BASE_URL)

faces = cf.face.detect(sys.argv[1])
result = cf.face.identify([faces[0]["faceId"]], "authorized_entry")

if result[0]["candidates"]:
	person_info = cf.person.get("authorized_entry", result[0]["candidates"][0]["personId"])
	print("Hello, " + person_info["name"] + ".")
else:
	print("Face not recognized.")
