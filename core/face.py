import requests
import json
from collections import Counter

from core import util

"""
    using Face++ API https://www.faceplusplus.com/face-searching/
"""

faceset_name = util.get_property("faceset")


def detect(img_name):
    """see https://console.faceplusplus.com/documents/5679127"""
    url = 'https://api-us.faceplusplus.com/facepp/v3/detect'
    files = {
        'api_key': (None, util.get_property("gest_api_key")),
        'api_secret': (None, util.get_property("gest_api_secret")),
        'image_file': (img_name, open(img_name, 'rb')),
        'return_attributes': (None, 'smiling,emotion'),
    }
    x = requests.post(url, files=files)
    res = json.loads(x.text)
    print(len(res['faces']))
    face_token = res['faces'][0]['face_token']
    smile = res['faces'][0]['attributes']['smile']
    emotions = res['faces'][0]['attributes']['emotion']
    emotion = Counter(emotions).most_common(1)[0][0]
    return face_token, smile, emotion


def faceset(face_tokens, set_name=faceset_name):
    """see https://console.faceplusplus.com/documents/6329329"""
    url = 'https://api-us.faceplusplus.com/facepp/v3/faceset/create'
    files = {
        'api_key': (None, util.get_property("gest_api_key")),
        'api_secret': (None, util.get_property("gest_api_secret")),
        'outer_id': (None, set_name),
        'force_merge': (None, '1'),
        'face_tokens': (None, ",".join(face_tokens))
    }
    x = requests.post(url, files=files)
    print(x)


def search(face_token, set_name=faceset_name):
    """see https://console.faceplusplus.com/documents/5681455"""
    url = 'https://api-us.faceplusplus.com/facepp/v3/search'
    files = {
        'api_key': (None, util.get_property("gest_api_key")),
        'api_secret': (None, util.get_property("gest_api_secret")),
        'outer_id': (None, set_name),
        'face_token': (None, face_token)
    }
    x = requests.post(url, files=files)
    res = json.loads(x.text)
    print(len(res['results']))
    match_face_token = res['results'][0]['face_token']
    return match_face_token

