#!/usr/bin/env python3

import cognitive_face as cf

GROUP = "authorized_entry"

KEY = '64ebe5b92a9a4d7e8e841a7f8a5e04ef'  # Replace with a valid subscription key (keeping the quotes in place).
cf.Key.set(KEY)

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
cf.BaseUrl.set(BASE_URL)

cf.person_group.train(GROUP)
cf.util.wait_for_person_group_training(GROUP)