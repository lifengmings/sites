import json
import requests
import time
from django.conf import settings


def post_cmd(cmd):
    url = 'http://api.heclouds.com/devices/34318983/datapoints'
    headers = {
        'api-key': settings.API_KEY,
    }
    values = {'datastreams': [{"id": "status", "datapoints": [{"time": time.time(), "value": cmd}]}]}
    jdata = json.dumps(values)
    res = requests.request("POST", url, data=jdata, headers=headers)
    return json.loads(res.content).get('error')


def get_status():
    url = 'http://api.heclouds.com/devices/34318983/datapoints?datastream_id=status&limit=1'
    headers = {
        'api-key': settings.API_KEY,
    }
    r = requests.get(url, headers=headers)
    data = json.loads(r.text).get('data').get('datastreams')
    status = data[0].get('datapoints')[0].get('value')
    return 'on' if status == 1 else 'off'


def judg_s_time():
    t = time.localtime()
    if (t[5] not in (0, 6)) and (9 <= t[3] <= 11 or 14 <= t[3] <= 17):
        return True
    else:
        return False


def judg_c_time():
    t = time.localtime()
    if (t[5] not in (0, 6)) and (7 <= t[3] <= 8 or 12 <= t[3] <= 13):
        return True
    else:
        return False
