#!/usr/bin/env python3

import cognitive_face as cf
import sys

KEY = 'AAAAAAAAAAAAAAAAAAAA'  # Replace with a valid subscription key (keeping the quotes in place).
cf.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
cf.BaseUrl.set(BASE_URL)

group = "authorized_entry"

person = cf.person.create(group, sys.argv[1])

cf.person.add_face(sys.argv[2], group, person["personId"])
