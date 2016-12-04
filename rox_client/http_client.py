from http.client import HTTPConnection
import simplejson


JSON_HEADERS = {'Content-type': 'application/json'}


class RoxHttpClient(object):

    conn = None
    cache_size_limit = None
    _cache = None

    def __init__(self, host='0.0.0.0', port=5000, cache_size_limit=8):
        self.conn = HTTPConnection('{}:{}'.format(host, port))
        self.cache_size_limit = cache_size_limit
        self._cache = {}

    def set(self, key, value):
        self.conn.request(
            'POST',
            '/set',
            simplejson.dumps({key: value}),
            JSON_HEADERS
        )
        self.conn.getresponse()

    def set_bulk(self, data):
        self.conn.request(
            'POST',
            '/set',
            simplejson.dumps(data),
            JSON_HEADERS
        )
        self.conn.getresponse()

    def set_cached(self, key, value):
        self._cache[key] = value
        if len(self._cache) >= self.cache_size_limit:
            self.conn.request(
                'POST',
                '/set_bulk',
                simplejson.dumps(self._cache),
                JSON_HEADERS
            )
            self.conn.getresponse()
            self._cache = {}

    def get(self, key):
        self.conn.request(
            'GET',
            '/get',
            simplejson.dumps(key),
            JSON_HEADERS
        )
        resp = self.conn.getresponse()
        return resp.read().decode()
