from http.client import HTTPConnection
import simplejson


JSON_HEADERS = {'Content-type': 'application/json'}


class RoxHttpClient(object):

    conn = HTTPConnection('0.0.0.0:5000')

    def set(self, key, value):
        self.conn.request(
            'POST',
            '/set',
            simplejson.dumps({key: value}),
            JSON_HEADERS
        )
        self.conn.getresponse()

    def get(self, key):
        self.conn.request(
            'GET',
            '/get',
            simplejson.dumps(key),
            JSON_HEADERS
        )
        resp = self.conn.getresponse()
        return resp.read().decode()
