#!/usr/bin/env python3

import cognitive_face as cf
import sys

KEY = 'AAAAAAAAAAAAAAAAAAAAAAAAAAA'  # Replace with a valid subscription key (keeping the quotes in place).
cf.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
cf.BaseUrl.set(BASE_URL)

group = "authorized_entry"

emma = {u'personId': u'2444ef9e-e053-4156-81f1-b3bc8b483568'}
mahima = {'personId': '4c1312ef-f807-4dd1-a950-63fab8150c04'}

cf.person.add_face(sys.argv[1], group, mahima["personId"])
