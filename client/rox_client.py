import http.client
import simplejson
import urllib.parse


class RoxClient(object):

    rox_client = None

    def __init__(self):
        self.rox_client = http.client.HTTPConnection('0.0.0.0:5000')

    def put(self, key, value):
        self.rox_client.request(
            "GET", "/set?key={key}&value={value}".format(
                key=urllib.parse.quote(simplejson.dumps(key)),
                value=urllib.parse.quote(simplejson.dumps(value))
            )
        )
        self.rox_client.getresponse()

    def get(self, key):
        self.rox_client.request(
            "GET", "/get?key={key}".format(
                key=urllib.parse.quote(simplejson.dumps(key))
            )
        )
        resp = self.rox_client.getresponse()
        return simplejson.loads(resp.read())
