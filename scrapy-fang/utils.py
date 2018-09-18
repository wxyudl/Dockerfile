# _*_encoding:utf-8_*_

import json
import urllib
import urllib.request
import urllib.parse


class Utils:
    def __init__(self):
        self.version = 1.0

    def getLocat(self, name):
        req = urllib.request.Request(
            "http://api.map.baidu.com/geocoder/v2/?address="
            + name
            + "&output=json&ak=E7psKcLqG8CoZg74ed1qgrYy",
            None,
            {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36"
            },
        )
        response = urllib.request.urlopen(req)
        location = {
            'lng': '-',
            'lat': '-'
        }
        res = json.loads(response.read())
        if res["status"] == 0:
            location = res["result"]["location"]

        return location