from http.client import HTTPConnection
import simplejson
import urllib.parse


class KeyIsNotHashableException(Exception):
    pass


def assert_key_is_hashable(func):

    def wrapped_func(key, *args):
        try:
            {key: None}
        except:
            raise KeyIsNotHashableException()
        return func(key, *args)

    return wrapped_func


class RoxClient(object):

    conn = HTTPConnection('0.0.0.0:5000')

    @assert_key_is_hashable
    def set(self, key, value):
        self.conn.request(
            "POST", "/set?key={key}&value={value}".format(
                key=urllib.parse.quote(simplejson.dumps(key)),
                value=urllib.parse.quote(simplejson.dumps(value))
            )
        )
        self.conn.getresponse()

    @assert_key_is_hashable
    def get(self, key):
        self.conn.request(
            "GET", "/get?key={key}".format(
                key=urllib.parse.quote(simplejson.dumps(key))
            )
        )
        resp = self.conn.getresponse()
        return simplejson.loads(resp.read())
